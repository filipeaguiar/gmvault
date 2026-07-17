import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

import pytest
import yaml

import compendium_rebuild as rebuild


def markdown(title, body="", **metadata):
    values = {"title": title, **metadata}
    return f"---\n{yaml.safe_dump(values, sort_keys=False)}---\n\n{body}\n"


def test_baseline_fixture_is_consistent_and_covers_source_cases():
    fixtures = Path(__file__).parent / "fixtures" / "compendium_rebuild"
    inventory = json.loads((fixtures / "current_inventory.json").read_text())
    cases = json.loads((fixtures / "source_cases.json").read_text())["cases"]

    assert inventory["direct_references"] + inventory["transitive_dependencies"] == inventory["selected_entities"]
    assert inventory["selected_entities"] + inventory["unused_entities"] == inventory["total_entity_pages"]
    assert {case["kind"] for case in cases} >= {"monster", "magic_item", "class", "species", "rule", "spell", "item"}


def test_scan_extracts_yaml_body_and_transitive_references():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        campaigns = root / "content/campaigns/demo"
        compendium = root / "content/compendium"
        campaigns.mkdir(parents=True)
        (compendium / "classes").mkdir(parents=True)
        (compendium / "rules").mkdir(parents=True)
        (compendium / "spells").mkdir(parents=True)
        (campaigns / "character.md").write_text(
            markdown("Hero", "[Spell](/compendium/spells/guidance/)", compendium_refs=["/compendium/classes/rogue/"]),
            encoding="utf-8",
        )
        (compendium / "classes/rogue.md").write_text(markdown("Rogue", "[Feature](/compendium/rules/cunning-action/)"), encoding="utf-8")
        (compendium / "rules/cunning-action.md").write_text(markdown("Cunning Action"), encoding="utf-8")
        (compendium / "spells/guidance.md").write_text(markdown("Guidance"), encoding="utf-8")
        (compendium / "spells/unused.md").write_text(markdown("Unused"), encoding="utf-8")

        with patch.multiple(
            rebuild,
            PROJECT_ROOT=root,
            CONTENT_ROOT=root / "content",
            CAMPAIGN_ROOT=root / "content/campaigns",
            COMPENDIUM_ROOT=compendium,
        ):
            manifest = rebuild.scan_inventory()

    assert manifest["counts"] == {"direct": 2, "transitive_dependencies": 1, "selected": 3, "unused": 1, "total_entities": 4}
    assert manifest["unused"] == ["/compendium/spells/unused/"]
    assert {item["url"] for item in manifest["selected"]} == {
        "/compendium/classes/rogue/", "/compendium/rules/cunning-action/", "/compendium/spells/guidance/"
    }


def record(kind, name, source):
    return rebuild.CatalogRecord(kind, name, source, f"{kind}.json", kind, {"name": name, "source": source})


def test_source_priority_explicit_xphb_and_goblin_fallback():
    base = {"direct_origins": ["character"]}
    selected, reason, error = rebuild.choose_record(
        {**base, "kind": "spell", "canonical_name": "Guidance", "slug": "guidance"},
        [record("spell", "Guidance", "PHB"), record("spell", "Guidance", "XPHB")], {},
    )
    assert not error and selected.source == "XPHB" and "XPHB" in reason

    selected, _, error = rebuild.choose_record(
        {**base, "kind": "species", "canonical_name": "Goblin", "slug": "goblin"},
        [record("species", "Goblin", "VGM"), record("species", "Goblin", "MPMM")], {},
    )
    assert not error and selected.source == "MPMM"

    selected, reason, error = rebuild.choose_record(
        {"direct_origins": ["campaign"], "kind": "monster", "canonical_name": "Aboleth", "slug": "aboleth"},
        [record("monster", "Aboleth", "MM"), record("monster", "Aboleth", "XMM")],
        {("monster", "aboleth"): "MM"},
    )
    assert not error and selected.source == "MM" and "JttRC" in reason


def test_unhandled_ambiguity_fails_with_sources():
    selected, reason, error = rebuild.choose_record(
        {"direct_origins": [], "kind": "monster", "canonical_name": "Thing", "slug": "thing"},
        [record("monster", "Thing", "AAA"), record("monster", "Thing", "BBB")], {},
    )
    assert selected is None and reason is None
    assert "AAA" in error and "BBB" in error


def test_shared_sync_and_rebuild_use_equivalent_spell_schema_and_provenance():
    entity = {
        "name": "Guidance", "source": "XPHB", "level": 0, "school": "D",
        "time": [{"number": 1, "unit": "action"}], "range": {"distance": {"type": "touch"}},
        "components": {"v": True, "s": True}, "duration": [{"type": "instant"}],
        "entries": ["Roll {@dice 1d4}."],
    }
    remote = rebuild.CatalogRecord(
        "spell", "Guidance", "XPHB", "spells/spells-xphb.json", "spell", entity,
        rebuild.record_remote_id("spell", entity),
    )

    class FakeCatalog:
        def records(self, kind):
            assert kind == "spell"
            return [remote]

        def jttrc_sources(self):
            return {}

    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / "compendium"
        ref = rebuild.sync_compendium_entity(
            "spell", "Guidance", slug="guidance", output_root=output, catalog=FakeCatalog()
        )
        metadata, _ = rebuild.parse_markdown(output / "spells/guidance.md")

    expected = yaml.safe_load(
        rebuild.build_document(
            {"kind": "spell", "slug": "guidance", "direct_origins": ["character"]},
            remote,
            object(),
            {"/compendium/spells/guidance/"},
        ).split("---", 2)[1]
    )
    assert ref == "/compendium/spells/guidance/"
    assert metadata["spell_info"] == expected["spell_info"]
    assert metadata["source"] == expected["source"]


def test_generated_spell_has_provenance_and_structured_schema():
    entity = {
        "name": "Guidance", "source": "XPHB", "level": 0, "school": "D",
        "time": [{"number": 1, "unit": "action"}], "range": {"distance": {"type": "touch"}},
        "components": {"v": True, "s": True}, "duration": [{"type": "timed", "duration": {"amount": 1, "type": "minute"}, "concentration": True}],
        "entries": ["Roll {@dice 1d4}."],
    }
    remote = rebuild.CatalogRecord("spell", "Guidance", "XPHB", "spells/spells-xphb.json", "spell", entity)
    entry = {"kind": "spell", "slug": "guidance", "direct_origins": ["character"]}

    rendered = rebuild.build_document(entry, remote, object(), {"/compendium/spells/guidance/"})
    metadata = yaml.safe_load(rendered.split("---", 2)[1])

    assert metadata["source"]["provider"] == "5e.tools"
    assert metadata["source"]["book"] == "XPHB"
    assert metadata["spell_info"]["level_number"] == 0
    assert metadata["spell_info"]["rolls"][0]["notation"] == "1d4"
    assert metadata["draft"] is True and metadata["status"] == "draft"


def test_catalog_download_failure_does_not_touch_active_content():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        active = root / "content/compendium/rules/action.md"
        active.parent.mkdir(parents=True)
        active.write_text("active", encoding="utf-8")
        catalog = rebuild.FiveEToolsCatalog(root / "cache")
        with patch("compendium_rebuild.urllib.request.urlopen", side_effect=URLError("offline")):
            with pytest.raises(rebuild.RebuildError, match="Falha ao baixar"):
                catalog.get_json("actions.json")
        assert active.read_text(encoding="utf-8") == "active"


def test_validation_rejects_invalid_staging_and_promotion_rolls_back():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        campaigns = root / "content/campaigns"
        active = root / "content/compendium"
        staging = root / "staging"
        campaigns.mkdir(parents=True)
        (active / "rules").mkdir(parents=True)
        (staging / "rules").mkdir(parents=True)
        (active / "_index.md").write_text(markdown("Index"), encoding="utf-8")
        old = active / "rules/action.md"
        old.write_text(markdown("Old", source={"provider": "5e.tools"}), encoding="utf-8")
        staged = staging / "rules/action.md"
        staged.write_text(markdown("New", source={"provider": "5e.tools"}), encoding="utf-8")
        manifest = {
            "input_fingerprint": "",
            "missing_local": [],
            "selected": [{"url": "/compendium/rules/action/", "kind": "rule", "status": "resolved"}],
        }
        with patch.multiple(rebuild, PROJECT_ROOT=root, CAMPAIGN_ROOT=campaigns, COMPENDIUM_ROOT=active):
            manifest["input_fingerprint"] = rebuild.hash_paths(rebuild.input_paths())
            with patch("compendium_rebuild.shutil.copy2", side_effect=OSError("interrupted")):
                with pytest.raises(OSError, match="interrupted"):
                    rebuild.promote(manifest, staging)
        assert "Old" in old.read_text(encoding="utf-8")
        assert (active / "_index.md").exists()


def test_stale_manifest_is_rejected():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        campaigns = root / "content/campaigns"
        compendium = root / "content/compendium"
        campaigns.mkdir(parents=True)
        compendium.mkdir(parents=True)
        page = campaigns / "a.md"
        page.write_text(markdown("A"), encoding="utf-8")
        with patch.multiple(rebuild, PROJECT_ROOT=root, CAMPAIGN_ROOT=campaigns, COMPENDIUM_ROOT=compendium):
            fingerprint = rebuild.hash_paths(rebuild.input_paths())
            page.write_text(markdown("Changed"), encoding="utf-8")
            with pytest.raises(rebuild.RebuildError, match="obsoleto"):
                rebuild.assert_fresh_manifest({"input_fingerprint": fingerprint})
