import argparse
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from translate_drafts import (
    MarkdownDocument,
    TranslationError,
    add_translation_metadata,
    build_translation_prompt,
    filter_image_only_handouts,
    get_lmstudio_translation,
    get_openai_compatible_translation,
    has_translatable_body,
    load_glossary_config,
    parse_args,
    process_document,
    translation_route,
    publish_completed_adventures,
    run_document_batch,
    select_glossary_config,
    translate_text,
)


class _Response:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return io.BytesIO(self.payload)

    def __exit__(self, *_args):
        return False


class LmStudioTranslationTests(unittest.TestCase):
    def glossary_file(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(
            {
                "required_translations": {"rules": {"Saving Throw": "Teste de Resistência"}},
                "protected_terms": ["Kasem"],
                "contextual_terms": {"save": {"note": "Termo contextual"}},
                "forbidden_outputs": ["Salvaguarda"],
            },
            handle,
        )
        handle.close()
        return Path(handle.name)

    def test_image_only_handouts_are_excluded_by_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            handouts = root / "handouts"
            adventures = root / "adventures"
            handouts.mkdir()
            adventures.mkdir()
            image_only = handouts / "map.md"
            index = handouts / "_index.md"
            narrative = adventures / "chapter.md"
            image_only.write_text(
                "---\ntitle: Map\nparams:\n  kind: handout\n---\n\n![Map](/images/map.webp)\n",
                encoding="utf-8",
            )
            index.write_text("---\ntitle: Handouts\n---\n", encoding="utf-8")
            narrative.write_text("---\ntitle: Chapter\n---\n\nNarrative text.\n", encoding="utf-8")

            selected, skipped = filter_image_only_handouts([image_only, index, narrative])

            self.assertEqual(selected, [index, narrative])
            self.assertEqual(skipped, [image_only])

    def test_structural_or_media_only_bodies_do_not_require_translation(self):
        self.assertFalse(has_translatable_body(""))
        self.assertFalse(has_translatable_body("![Map](/images/map.webp)"))
        self.assertFalse(has_translatable_body("<!-- navigation note -->\n\n---\n\nhttps://example.test/path"))
        self.assertFalse(has_translatable_body("```json\n{\"key\": \"value\"}\n```"))
        self.assertTrue(has_translatable_body("## Introduction\n\nCampaign overview."))
        self.assertEqual(translation_route(MarkdownDocument(Path("item.md"), "", {"title": "Dagger"}, "")), "title_only")
        self.assertEqual(translation_route(MarkdownDocument(Path("rule.md"), "", {"summary": "A useful rule."}, "")), "front_matter")

        document = MarkdownDocument(Path("_index.md"), "draft: false\nstatus: draft", {"draft": False, "status": "draft"}, "")
        result = process_document(
            document,
            lambda text: self.fail(f"Unexpected translation request: {text}"),
            {},
            apply=True,
            include_non_draft=False,
            translate_frontmatter=False,
            source="en",
            target="pt",
        )
        self.assertEqual(result.skipped_reason, "sem conteúdo textual para tradução")

    def test_image_only_handouts_can_be_explicitly_included(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "handouts" / "art.md"
            path.parent.mkdir()
            path.write_text("---\ntitle: Art\n---\n\n![Art](/images/art.webp)\n", encoding="utf-8")

            selected, skipped = filter_image_only_handouts([path], include=True)

            self.assertEqual(selected, [path])
            self.assertEqual(skipped, [])

    def test_completed_adventure_and_ancestor_indexes_are_published(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            campaign = Path(temp_dir) / "campaign"
            adventure = campaign / "adventures" / "salted-legacy" / "session-01"
            other = campaign / "adventures" / "written-in-blood"
            adventure.mkdir(parents=True)
            other.mkdir(parents=True)

            translated = "translation:\n  target_language: pt-BR\n  status: machine_translated"
            for path in (
                campaign / "_index.md",
                campaign / "adventures" / "_index.md",
                campaign / "adventures" / "salted-legacy" / "_index.md",
                adventure / "_index.md",
            ):
                path.write_text("---\ndraft: true\nstatus: draft\n---\n", encoding="utf-8")
            chapter = adventure / "chapter.md"
            chapter.write_text(
                f"---\ndraft: true\nstatus: draft\n{translated}\n---\n\nTexto traduzido.\n",
                encoding="utf-8",
            )
            unfinished = other / "chapter.md"
            unfinished.write_text(
                "---\ndraft: true\nstatus: draft\n---\n\nEnglish text.\n",
                encoding="utf-8",
            )

            published = publish_completed_adventures(campaign, apply=True)

            self.assertIn(chapter, published)
            for path in (
                campaign / "_index.md",
                campaign / "adventures" / "_index.md",
                campaign / "adventures" / "salted-legacy" / "_index.md",
                adventure / "_index.md",
                chapter,
            ):
                document = path.read_text(encoding="utf-8")
                self.assertIn("draft: false", document)
                self.assertIn("status: published", document)
            self.assertIn("draft: true", unfinished.read_text(encoding="utf-8"))

    def test_prompt_contains_every_glossary_section_and_ptbr_rules(self):
        config = load_glossary_config(self.glossary_file())
        prompt = build_translation_prompt(config)
        self.assertIn("português do Brasil", prompt)
        self.assertIn("Saving Throw => Teste de Resistência", prompt)
        self.assertIn("Kasem", prompt)
        self.assertIn("Termo contextual", prompt)
        self.assertIn("Salvaguarda", prompt)
        self.assertIn("Markdown", prompt)

    def test_selects_only_terms_used_in_complete_document(self):
        config = {
            "version": 1,
            "required_translations": {
                "rules": {
                    "Saving Throw": "Teste de Resistência",
                    "Armor Class": "Classe de Armadura",
                }
            },
            "protected_terms": ["Kasem", "Sholeh"],
            "contextual_terms": {
                "save": {"note": "Use salvar fora de regras"},
                "check": {"note": "Use teste em regras"},
            },
            "forbidden_outputs": ["Salvaguarda"],
        }

        selected = select_glossary_config(
            config,
            "# KASEM\nMake a saving throw now. Do not check this yet.",
        )

        self.assertEqual(
            selected["required_translations"],
            {"rules": {"Saving Throw": "Teste de Resistência"}},
        )
        self.assertEqual(selected["protected_terms"], ["Kasem"])
        self.assertEqual(selected["contextual_terms"], {"check": {"note": "Use teste em regras"}})
        self.assertEqual(selected["forbidden_outputs"], ["Salvaguarda"])
        prompt = build_translation_prompt(selected)
        self.assertNotIn("Armor Class", prompt)
        self.assertNotIn("Sholeh", prompt)
        self.assertNotIn("Use salvar fora de regras", prompt)

    def test_selection_matches_front_matter_and_body_as_one_document(self):
        config = {
            "required_translations": {"rules": {"Armor Class": "Classe de Armadura"}},
            "protected_terms": ["Kasem"],
            "contextual_terms": {},
            "forbidden_outputs": [],
        }
        document_text = "title: Armor Class\n---\nKasem enters the room."

        selected = select_glossary_config(config, document_text)

        self.assertIn("Armor Class", selected["required_translations"]["rules"])
        self.assertEqual(selected["protected_terms"], ["Kasem"])

    def test_required_common_noun_remains_visible_for_grammatical_translation(self):
        source = "Travelers return with stories of vanishing equipment."
        received = []

        def translate(text):
            received.append(text)
            return "Viajantes retornam com histórias de equipamentos desaparecidos."

        result = translate_text(source, translate, {"Equipment": "Equipamento"})

        self.assertEqual(received, [source])
        self.assertEqual(result, "Viajantes retornam com histórias de equipamentos desaparecidos.")
        self.assertNotIn("desaparecimento Equipamento", result)

    def test_translate_text_reports_completed_blocks_with_partial_text(self):
        events = []
        result = translate_text(
            "First paragraph.\n\nSecond paragraph.",
            lambda text: f"PT:{text}",
            {},
            on_block=lambda current, total, partial, elapsed: events.append(
                (current, total, partial, elapsed)
            ),
        )
        self.assertEqual(result, "PT:First paragraph.\n\nPT:Second paragraph.")
        self.assertEqual([(event[0], event[1]) for event in events], [(1, 2), (2, 2)])
        self.assertEqual(events[0][2], "PT:First paragraph.\n\n")
        self.assertEqual(events[1][2], result)
        self.assertTrue(all(event[3] >= 0 for event in events))

    def test_process_document_writes_checkpoint_per_block_and_removes_it_on_success(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "chapter.md"
            path.write_text("---\ndraft: true\n---\n\nFirst.\n\nSecond.\n", encoding="utf-8")
            document = MarkdownDocument(path, "draft: true", {"draft": True}, "\nFirst.\n\nSecond.\n")
            checkpoint = path.with_suffix(path.suffix + ".translation.partial")
            snapshots = []
            process_document(
                document,
                lambda text: f"PT:{text}",
                {},
                apply=True,
                include_non_draft=False,
                translate_frontmatter=False,
                source="en",
                target="pb",
                progress=lambda current, total, elapsed: snapshots.append(
                    (current, total, elapsed, checkpoint.read_text(encoding="utf-8"))
                ),
            )
            self.assertEqual([(item[0], item[1]) for item in snapshots], [(1, 2), (2, 2)])
            self.assertIn("PT:First.", snapshots[0][3])
            self.assertNotIn("PT:Second.", snapshots[0][3])
            self.assertFalse(checkpoint.exists())

    def test_cli_accepts_openai_compatible_engine_and_connection_options(self):
        with patch(
            "sys.argv",
            [
                "translate_drafts.py",
                "--scope",
                "compendium",
                "--engine",
                "openai-compatible",
                "--base-url",
                "http://localhost:8000/v1",
                "--model",
                "custom-model",
            ],
        ):
            args = parse_args()

        self.assertEqual(args.engine, "openai-compatible")
        self.assertEqual(args.base_url, "http://localhost:8000/v1")
        self.assertEqual(args.model, "custom-model")

    def test_cli_treats_lmstudio_as_openai_compatible_alias(self):
        with patch("sys.argv", ["translate_drafts.py", "--scope", "compendium", "--engine", "lmstudio"]):
            args = parse_args()

        self.assertEqual(args.engine, "openai-compatible")

    def test_cli_help_uses_openai_compatible_neutral_text(self):
        stdout = io.StringIO()
        with patch("sys.argv", ["translate_drafts.py", "--help"]), patch("sys.stdout", stdout):
            with self.assertRaises(SystemExit) as raised:
                parse_args()

        self.assertEqual(raised.exception.code, 0)
        help_text = stdout.getvalue()
        self.assertIn("openai-compatible", help_text)
        self.assertNotIn("LM Studio", help_text)

    @patch("translate_drafts.urlopen")
    def test_client_posts_openai_request_and_returns_content(self, urlopen):
        urlopen.return_value = _Response(
            {"choices": [{"message": {"content": "Teste de Resistência"}, "finish_reason": "stop"}]}
        )
        translate = get_openai_compatible_translation(
            "http://127.0.0.1:1234/v1", "google/gemma-4-e4b", "SYSTEM", timeout=12, retries=1
        )
        self.assertEqual(translate("Saving Throw"), "Teste de Resistência")
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data)
        self.assertEqual(request.full_url, "http://127.0.0.1:1234/v1/chat/completions")
        self.assertEqual(payload["model"], "google/gemma-4-e4b")
        self.assertEqual(payload["temperature"], 0.1)
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 12)

    @patch("translate_drafts.urlopen")
    def test_client_retries_empty_and_truncated_responses(self, urlopen):
        urlopen.side_effect = [
            _Response({"choices": [{"message": {"content": ""}, "finish_reason": "stop"}]}),
            _Response({"choices": [{"message": {"content": "parcial"}, "finish_reason": "length"}]}),
            _Response({"choices": [{"message": {"content": "completo"}, "finish_reason": "stop"}]}),
        ]
        translate = get_lmstudio_translation("http://localhost:1234/v1", "model", "SYSTEM", retries=3)
        self.assertEqual(translate("source"), "completo")
        self.assertEqual(urlopen.call_count, 3)

    @patch("translate_drafts.urlopen")
    def test_client_fails_after_retry_budget(self, urlopen):
        urlopen.return_value = _Response({"choices": []})
        translate = get_lmstudio_translation("http://localhost:1234/v1", "model", "SYSTEM", retries=2)
        with self.assertRaises(TranslationError):
            translate("source")
        self.assertEqual(urlopen.call_count, 2)

    def test_metadata_records_engine_and_model(self):
        meta = add_translation_metadata({}, "en", "pb", engine="lmstudio", model="google/gemma-4-e4b")
        self.assertEqual(meta["translation"]["engine"], "lmstudio")
        self.assertEqual(meta["translation"]["model"], "google/gemma-4-e4b")

    def test_character_reference_is_structural_and_not_translated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "character.md"
            path.write_text(
                "---\nref: /compendium/rules/sneak-attack/\ncompendium_refs:\n  - /compendium/rules/sneak-attack/\n---\n\nDescrição da ficha.\n",
                encoding="utf-8",
            )
            document = MarkdownDocument(
                path,
                "ref: /compendium/rules/sneak-attack/\ncompendium_refs:\n  - /compendium/rules/sneak-attack/",
                {
                    "ref": "/compendium/rules/sneak-attack/",
                    "compendium_refs": ["/compendium/rules/sneak-attack/"],
                    "char_info": {"actions": [{"name": "Sneak Attack", "ref": "/compendium/rules/sneak-attack/"}]},
                },
                "\nDescrição da ficha.\n",
            )
            translated = process_document(
                document,
                lambda text: f"PT:{text}",
                {},
                apply=False,
                include_non_draft=True,
                translate_frontmatter=True,
                source="en",
                target="pb",
            )
            self.assertTrue(translated.changed)
            self.assertEqual(document.front_matter["ref"], "/compendium/rules/sneak-attack/")
            self.assertEqual(document.front_matter["compendium_refs"], ["/compendium/rules/sneak-attack/"])
            self.assertIn("ref: /compendium/rules/sneak-attack/", path.read_text(encoding="utf-8"))

    def test_status_draft_is_translation_pending_without_changing_hugo_draft(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "public-compendium.md"
            path.write_text("---\ndraft: false\nstatus: draft\n---\n\nEnglish text\n", encoding="utf-8")
            document = MarkdownDocument(
                path=path,
                front_matter_raw="draft: false\nstatus: draft",
                front_matter={"draft": False, "status": "draft"},
                body="\nEnglish text\n",
            )
            result = process_document(
            document,
            lambda text: f"PT:{text}",
            {},
            apply=False,
            include_non_draft=False,
            translate_frontmatter=False,
            source="en",
            target="pb",
        )
            self.assertTrue(result.changed)
            self.assertFalse(document.front_matter["draft"])
            self.assertEqual(document.front_matter["status"], "draft")

    def test_already_translated_document_is_skipped_without_force(self):
        document = MarkdownDocument(
            path=Path("unused.md"),
            front_matter_raw="",
            front_matter={"draft": True, "translation": {"target_language": "pt-BR"}},
            body="Already translated",
        )
        result = process_document(
            document,
            lambda text: text,
            {},
            apply=False,
            include_non_draft=False,
            translate_frontmatter=False,
            source="en",
            target="pb",
            engine="lmstudio",
            model="model",
            force_retranslate=False,
        )
        self.assertEqual(result.skipped_reason, "already translated to pt-BR")

    def test_structural_markdown_targets_and_shortcodes_are_preserved(self):
        source = (
            "[Secret Door](/campaigns/demo/adventures/quest/)\n"
            "![Map](/images/campaigns/demo/map.webp)\n"
            "{{< relref \"adventures/quest\" >}}\n"
            "<a href=\"adventures/quest/\">Secret HTML</a>\n"
            "<img src=\"../maps/market.webp\" alt=\"Market Map\">\n"
            "https://example.com/Keep/This\n"
        )

        def aggressive(text):
            return (
                text.replace("Secret Door", "Porta Secreta")
                .replace("Map", "Mapa")
                .replace("campaigns", "campanhas")
                .replace("adventures", "aventuras")
                .replace("images", "imagens")
                .replace("example", "exemplo")
                .replace("maps", "mapas")
                .replace("market", "mercado")
            )

        result = translate_text(source, aggressive, {})

        self.assertIn("[Porta Secreta](/campaigns/demo/adventures/quest/)", result)
        self.assertIn("![Mapa](/images/campaigns/demo/map.webp)", result)
        self.assertIn('{{< relref "adventures/quest" >}}', result)
        self.assertIn('href="adventures/quest/"', result)
        self.assertIn('src="../maps/market.webp"', result)
        self.assertIn("https://example.com/Keep/This", result)
        self.assertNotIn("/campanhas/", result)
        self.assertNotIn("/imagens/", result)
        self.assertNotIn("../mapas/", result)

    def test_front_matter_structural_fields_are_not_translated(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "scene.md"
            path.write_text(
                "---\ndraft: true\ntitle: Secret Door\nsummary: Open the hidden door.\n"
                "slug: secret-door\nurl: /campaigns/demo/secret-door/\n"
                "aliases:\n- /campaigns/demo/old-secret-door/\n"
                "locations:\n- /campaigns/demo/locations/market/\n"
                "params:\n  kind: scene\n  content_role: introduction\n---\n\nBody.\n",
                encoding="utf-8",
            )
            document = MarkdownDocument(
                path=path,
                front_matter_raw="",
                front_matter={
                    "draft": True,
                    "title": "Secret Door",
                    "summary": "Open the hidden door.",
                    "slug": "secret-door",
                    "url": "/campaigns/demo/secret-door/",
                    "aliases": ["/campaigns/demo/old-secret-door/"],
                    "locations": ["/campaigns/demo/locations/market/"],
                    "params": {"kind": "scene", "content_role": "introduction"},
                },
                body="Body.",
            )

            def aggressive(text):
                return text.replace("Secret", "Secreta").replace("Open", "Abra").replace("campaigns", "campanhas")

            result = process_document(
                document,
                aggressive,
                {},
                apply=False,
                include_non_draft=False,
                translate_frontmatter=True,
                source="en",
                target="pb",
            )

            self.assertTrue(result.changed)
            self.assertEqual(document.front_matter["slug"], "secret-door")
            self.assertEqual(document.front_matter["url"], "/campaigns/demo/secret-door/")
            self.assertEqual(document.front_matter["aliases"], ["/campaigns/demo/old-secret-door/"])
            self.assertEqual(document.front_matter["locations"], ["/campaigns/demo/locations/market/"])
            self.assertEqual(document.front_matter["params"], {"kind": "scene", "content_role": "introduction"})
            self.assertNotIn("/campanhas/", path.read_text(encoding="utf-8"))

    def test_checkpoint_snapshots_preserve_structural_destinations(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "chapter.md"
            path.write_text(
                "---\ndraft: true\nlocations:\n- /campaigns/demo/locations/market/\n---\n\n"
                "[Door](/campaigns/demo/door/)\n\nSecond block.\n",
                encoding="utf-8",
            )
            document = MarkdownDocument(
                path,
                "draft: true\nlocations:\n- /campaigns/demo/locations/market/",
                {"draft": True, "locations": ["/campaigns/demo/locations/market/"]},
                "[Door](/campaigns/demo/door/)\n\nSecond block.\n",
            )
            checkpoint = path.with_suffix(path.suffix + ".translation.partial")
            snapshots = []

            process_document(
                document,
                lambda text: text.replace("Door", "Porta").replace("campaigns", "campanhas"),
                {},
                apply=True,
                include_non_draft=False,
                translate_frontmatter=False,
                source="en",
                target="pb",
                progress=lambda *_args: snapshots.append(checkpoint.read_text(encoding="utf-8")),
            )

            self.assertTrue(snapshots)
            self.assertTrue(all("/campaigns/demo/door/" in snapshot for snapshot in snapshots))
            self.assertTrue(all("/campaigns/demo/locations/market/" in snapshot for snapshot in snapshots))
            self.assertTrue(all("/campanhas/" not in snapshot for snapshot in snapshots))

    def test_builtin_deepseek_v4_pro_profile_is_available_without_local_config(self):
        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "sys.argv",
            [
                "translate_drafts.py",
                "--scope",
                "compendium",
                "--profile",
                "deepseek-v4-pro",
                "--config",
                str(Path(temp_dir) / "missing.json"),
            ],
        ):
            args = parse_args()

        self.assertEqual(args.engine, "openai-compatible")
        self.assertEqual(args.model, "deepseek-v4-pro")
        self.assertEqual(args.base_url, "https://api.deepseek.com/v1")

    def test_translation_rejects_forbidden_output_and_preserves_provenance(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "rule.md"
            source = {"provider": "5e.tools", "book": "XPHB", "remote_id": "abc"}
            path.write_text("---\ndraft: true\n---\n\nSaving Throw.\n", encoding="utf-8")
            document = MarkdownDocument(path, "", {"draft": True, "source": source}, "Saving Throw.\n")

            with self.assertRaises(TranslationError):
                process_document(
                    document,
                    lambda _text: "Salvaguarda",
                    {},
                    apply=False,
                    include_non_draft=False,
                    translate_frontmatter=False,
                    source="en",
                    target="pb",
                    engine="openai-compatible",
                    model="deepseek-v4-pro",
                    forbidden_outputs=["Salvaguarda"],
                )
            self.assertEqual(document.front_matter["source"], source)

    def test_batch_continues_after_file_error_and_reports_path(self):
        paths = [Path("one.md"), Path("broken.md"), Path("three.md")]
        completed = []
        failures = []

        def process(path):
            if path.name == "broken.md":
                raise TranslationError("timed out after 180s")
            return path.name

        results, errors = run_document_batch(
            paths,
            process,
            jobs=2,
            on_result=lambda path, result, elapsed: completed.append((path, result, elapsed)),
            on_error=lambda failure: failures.append(failure),
        )

        self.assertCountEqual(results, ["one.md", "three.md"])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].path, Path("broken.md"))
        self.assertEqual(errors[0].error_type, "TranslationError")
        self.assertIn("timed out after 180s", errors[0].message)
        self.assertGreaterEqual(errors[0].elapsed_seconds, 0)
        self.assertEqual(len(completed), 2)
        self.assertEqual(failures, errors)


if __name__ == "__main__":
    unittest.main()
