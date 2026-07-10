#!/usr/bin/env python3
"""Translate draft Markdown content with Argos Translate and a controlled RPG glossary.

This script is intentionally independent from Hugo. Hugo builds must not require
Argos Translate; only this optional post-import workflow does.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    import yaml
except ImportError:  # pragma: no cover - exercised in environments without PyYAML
    yaml = None

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_GLOSSARY = PROJECT_ROOT / "translation_glossary.json"
PROTECTED_PREFIX = "ZXQPROTECTED"
GLOSSARY_PREFIX = "ZXQGLOSSARY"

STRUCTURAL_FRONT_MATTER_KEYS = {
    "kind",
    "params",
    "draft",
    "date",
    "lastmod",
    "weight",
    "visibility",
    "status",
    "tags",
    "related",
    "characters",
    "npcs",
    "locations",
    "factions",
    "handouts",
    "compendium_refs",
    "stats",
    "stats_meta",
    "char_info",
    "spell_info",
    "item_info",
    "feat_info",
    "race_info",
    "class_info",
    "spells_usage",
    "aliases",
    "url",
    "slug",
    "layout",
    "type",
    "outputs",
    "translation",
}

TEXTUAL_FRONT_MATTER_KEYS = {"title", "summary", "description", "titulo_pt_br"}


@dataclass
class MarkdownDocument:
    path: Path
    front_matter_raw: str
    front_matter: dict[str, Any]
    body: str


@dataclass
class ProcessResult:
    path: Path
    changed: bool
    skipped_reason: str | None = None


class TranslationError(RuntimeError):
    """Raised when translation cannot be performed safely."""


class Protector:
    def __init__(self) -> None:
        self._items: list[str] = []

    def protect(self, text: str) -> str:
        patterns = [
            r"```[\s\S]*?```",  # fenced code blocks
            r"~~~[\s\S]*?~~~",  # alternate fenced code blocks
            r"!\[[^\]]*\]\([^\)]*\)",  # markdown images
            r"\{\{[\s\S]*?\}\}",  # Hugo shortcodes/templates
            r"\[\[[^\]]+\]\]",  # dice notation
            r"`[^`\n]+`",  # inline code
        ]
        for pattern in patterns:
            text = re.sub(pattern, self._store_match, text)

        # Protect link destinations but leave labels translatable.
        text = re.sub(r"(\[[^\]]+\]\()([^\)]+)(\))", self._protect_link_destination, text)

        # Protect bare URLs and internal Hugo paths.
        text = re.sub(r"https?://[^\s\)\]\}\>]+", self._store_match, text)
        text = re.sub(r"(?<![\w])/(campaigns|compendium|images|static)/[^\s\)\]\}\<\"']*", self._store_match, text)
        return text

    def restore(self, text: str) -> str:
        for index, original in enumerate(self._items):
            text = text.replace(self._token(index), original)
        return text

    def _token(self, index: int) -> str:
        return f"{PROTECTED_PREFIX}{index:05d}ZXQ"

    def _store(self, value: str) -> str:
        self._items.append(value)
        return self._token(len(self._items) - 1)

    def _store_match(self, match: re.Match[str]) -> str:
        return self._store(match.group(0))

    def _protect_link_destination(self, match: re.Match[str]) -> str:
        return f"{match.group(1)}{self._store(match.group(2))}{match.group(3)}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Traduz arquivos Markdown em draft usando Argos Translate e glossário controlado."
    )
    parser.add_argument("--scope", choices=["compendium", "campaign"], required=True, help="Escopo de tradução.")
    parser.add_argument("--campaign", help="Slug da campanha. Obrigatório com --scope campaign.")
    parser.add_argument("--path", help="Subcaminho opcional dentro do escopo selecionado.")
    parser.add_argument("--apply", action="store_true", help="Grava alterações. Sem esta flag, executa dry-run.")
    parser.add_argument(
        "--include-non-draft",
        action="store_true",
        help="Inclui arquivos sem draft: true. Use apenas para manutenção controlada.",
    )
    parser.add_argument(
        "--translate-frontmatter",
        action="store_true",
        help="Também traduz campos textuais seguros do front matter, como title e summary.",
    )
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY), help="Caminho do glossário JSON.")
    parser.add_argument("--source", default="en", help="Código do idioma de origem Argos. Padrão: en.")
    parser.add_argument("--target", default="pt", help="Código do idioma de destino Argos. Padrão: pt.")
    return parser.parse_args()


def resolve_scope(args: argparse.Namespace) -> Path:
    if args.scope == "compendium":
        base = PROJECT_ROOT / "content" / "compendium"
    else:
        if not args.campaign:
            raise TranslationError("--campaign <slug> é obrigatório quando --scope campaign é usado.")
        base = PROJECT_ROOT / "content" / "campaigns" / args.campaign

    if not base.exists():
        raise TranslationError(f"Escopo não encontrado: {base}")

    if not args.path:
        return base

    requested = Path(args.path)
    if not requested.is_absolute():
        requested = PROJECT_ROOT / requested
    requested = requested.resolve()
    base_resolved = base.resolve()

    if requested != base_resolved and base_resolved not in requested.parents:
        raise TranslationError(f"O caminho informado escapa do escopo selecionado: {requested}")
    if not requested.exists():
        raise TranslationError(f"Caminho não encontrado: {requested}")
    return requested


def discover_markdown_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix == ".md" else []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def parse_markdown(path: Path) -> MarkdownDocument | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    try:
        _, front_matter_raw, body = text.split("---", 2)
    except ValueError:
        return None
    if yaml is None:
        raise TranslationError("PyYAML não está instalado. Ative .venv e instale as dependências do script.")
    data = yaml.safe_load(front_matter_raw) or {}
    if not isinstance(data, dict):
        return None
    return MarkdownDocument(path=path, front_matter_raw=front_matter_raw, front_matter=data, body=body.lstrip("\n"))


def load_glossary(path: Path) -> dict[str, str]:
    if not path.exists():
        raise TranslationError(f"Glossário não encontrado: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TranslationError("Glossário deve ser um objeto JSON de termo origem para tradução.")
    glossary: dict[str, str] = {}
    for source, target in data.items():
        if isinstance(source, str) and isinstance(target, str) and source.strip() and target.strip():
            glossary[source] = target
    return glossary


def tokenize_glossary(text: str, glossary: dict[str, str]) -> tuple[str, dict[str, str]]:
    token_targets: dict[str, str] = {}
    for index, source in enumerate(sorted(glossary, key=len, reverse=True)):
        token = f"{GLOSSARY_PREFIX}{index:05d}ZXQ"
        pattern = re.compile(rf"(?<![\w]){re.escape(source)}(?![\w])", re.IGNORECASE)
        if pattern.search(text):
            text = pattern.sub(token, text)
            token_targets[token] = glossary[source]
    return text, token_targets


def restore_glossary(text: str, token_targets: dict[str, str]) -> str:
    for token, target in token_targets.items():
        text = text.replace(token, target)
    return text


def get_argos_translation(source_code: str, target_code: str) -> Callable[[str], str]:
    try:
        import argostranslate.translate
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise TranslationError(
            "Argos Translate não está instalado. Ative o ambiente com `source .venv/bin/activate` "
            "ou instale `argostranslate`."
        ) from exc

    installed_languages = argostranslate.translate.get_installed_languages()
    source = next((lang for lang in installed_languages if lang.code == source_code), None)
    target = next((lang for lang in installed_languages if lang.code == target_code), None)
    if source is None or target is None:
        raise TranslationError(f"Modelo Argos {source_code} -> {target_code} não está instalado.")
    translation = source.get_translation(target)
    if translation is None:
        raise TranslationError(f"Modelo Argos {source_code} -> {target_code} não está instalado.")
    return translation.translate


def translate_text(text: str, translate: Callable[[str], str], glossary: dict[str, str]) -> str:
    if not text.strip():
        return text

    protector = Protector()
    protected = protector.protect(text)
    tokenized, token_targets = tokenize_glossary(protected, glossary)

    translated_blocks: list[str] = []
    blocks = re.split(r"(\n\s*\n)", tokenized)
    for block in blocks:
        if not block.strip() or re.fullmatch(r"\n\s*\n", block):
            translated_blocks.append(block)
        else:
            translated_blocks.append(translate(block))

    translated = "".join(translated_blocks)
    translated = restore_glossary(translated, token_targets)
    translated = protector.restore(translated)
    return translated


def translate_front_matter(
    front_matter: dict[str, Any], translate: Callable[[str], str], glossary: dict[str, str]
) -> dict[str, Any]:
    updated = dict(front_matter)
    for key in TEXTUAL_FRONT_MATTER_KEYS:
        value = updated.get(key)
        if isinstance(value, str) and value.strip():
            updated[key] = translate_text(value, translate, glossary)
    return updated


def add_translation_metadata(front_matter: dict[str, Any], source: str, target: str) -> dict[str, Any]:
    updated = dict(front_matter)
    updated["draft"] = True
    translation_meta = dict(updated.get("translation") or {})
    translation_meta.update(
        {
            "source_language": source,
            "target_language": "pt-BR" if target == "pt" else target,
            "engine": "argos",
            "status": "machine_translated",
        }
    )
    updated["translation"] = translation_meta
    return updated


def render_markdown(front_matter: dict[str, Any], body: str) -> str:
    if yaml is None:
        raise TranslationError("PyYAML não está instalado. Ative .venv e instale as dependências do script.")
    yaml_text = yaml.safe_dump(front_matter, allow_unicode=True, sort_keys=False, width=1000).strip()
    return f"---\n{yaml_text}\n---\n\n{body.rstrip()}\n"


def process_document(
    document: MarkdownDocument,
    translate: Callable[[str], str] | None,
    glossary: dict[str, str],
    *,
    apply: bool,
    include_non_draft: bool,
    translate_frontmatter: bool,
    source: str,
    target: str,
) -> ProcessResult:
    if document.front_matter.get("draft") is not True and not include_non_draft:
        return ProcessResult(document.path, changed=False, skipped_reason="not draft")

    if translate is None:
        return ProcessResult(document.path, changed=True)

    translated_body = translate_text(document.body, translate, glossary)
    front_matter = document.front_matter
    if translate_frontmatter:
        front_matter = translate_front_matter(front_matter, translate, glossary)
    front_matter = add_translation_metadata(front_matter, source, target)

    rendered = render_markdown(front_matter, translated_body)
    original = document.path.read_text(encoding="utf-8")
    changed = rendered != original
    if apply and changed:
        document.path.write_text(rendered, encoding="utf-8")
    return ProcessResult(document.path, changed=changed)


def main() -> int:
    args = parse_args()
    try:
        root = resolve_scope(args)
        glossary = load_glossary(Path(args.glossary))
        files = discover_markdown_files(root)

        print(f"Escopo: {args.scope}")
        if args.scope == "campaign":
            print(f"Campanha: {args.campaign}")
        print(f"Raiz analisada: {root}")
        print(f"Modo: {'apply' if args.apply else 'dry-run'}")
        print(f"Arquivos Markdown encontrados: {len(files)}")

        translate = None
        if args.apply:
            translate = get_argos_translation(args.source, args.target)

        processed = 0
        changed = 0
        skipped = 0
        for path in files:
            document = parse_markdown(path)
            if document is None:
                skipped += 1
                print(f"[skip] {path} — sem front matter YAML válido")
                continue

            result = process_document(
                document,
                translate,
                glossary,
                apply=args.apply,
                include_non_draft=args.include_non_draft,
                translate_frontmatter=args.translate_frontmatter,
                source=args.source,
                target=args.target,
            )
            if result.skipped_reason:
                skipped += 1
                print(f"[skip] {path} — {result.skipped_reason}")
            else:
                processed += 1
                if result.changed:
                    changed += 1
                    print(f"[change] {path}")
                else:
                    print(f"[ok] {path} — sem alterações")

        print("\nResumo:")
        print(f"  processados: {processed}")
        print(f"  alterariam/alterados: {changed}")
        print(f"  ignorados: {skipped}")
        if not args.apply:
            print("\nDry-run: nenhum arquivo foi modificado. Use --apply para gravar traduções.")
        return 0
    except TranslationError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
