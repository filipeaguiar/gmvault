#!/usr/bin/env python3
"""Localiza e baixa novamente páginas afetadas por rótulos de fonte do 5e.tools.

Versões antigas do resolvedor exibiam a fonte de tags, como ``|XPHB``, no corpo
Markdown. Este utilitário encontra páginas importadas cujo corpo contém o código
registrado em ``source.book`` e as recria com o resolvedor corrigido.

Por segurança, a execução padrão apenas lista candidatos. Use ``--apply`` para
substituir os arquivos. Páginas com metadados de tradução são ignoradas, pois
uma nova sincronização preservaria o texto editorial e não eliminaria o erro.
"""

from __future__ import annotations

import argparse
import re
import sys

import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from compendium_rebuild import FiveEToolsCatalog, parse_markdown, sync_compendium_entity

PROJECT_ROOT = Path(__file__).resolve().parent
COMPENDIUM_ROOT = PROJECT_ROOT / "content" / "compendium"
DEFAULT_CACHE = PROJECT_ROOT / ".cache" / "5etools"
SUPPORTED_KINDS = {"monster", "magic_item", "item", "class", "species", "race", "feat", "spell", "rule"}
EDITORIAL_FIELDS = ("draft", "visibility", "status", "summary", "tags", "titulo_pt_br")


@dataclass(frozen=True)
class CorruptedPage:
    path: Path
    kind: str
    name: str
    slug: str
    book: str
    editorial: dict[str, Any]
    translated: bool


def remove_translation_metadata(path: Path) -> None:
    """Prevent the shared synchronizer from preserving the old translated body."""
    metadata, body = parse_markdown(path)
    metadata.pop("translation", None)
    path.write_text(
        f"---\n{yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=120)}---{body}",
        encoding="utf-8",
    )


def restore_editorial_metadata(path: Path, editorial: dict[str, Any]) -> None:
    """Keep publication and review decisions while replacing generated prose."""
    metadata, body = parse_markdown(path)
    metadata.update(editorial)
    path.write_text(
        f"---\n{yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=120)}---{body}",
        encoding="utf-8",
    )


def source_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    source = metadata.get("source")
    return source if isinstance(source, dict) else {}


def find_corrupted_pages(
    root: Path = COMPENDIUM_ROOT, *, include_translated: bool = False
) -> tuple[list[CorruptedPage], list[Path], list[Path]]:
    """Return repairable candidates plus pages requiring manual provenance review."""
    candidates: list[CorruptedPage] = []
    skipped_translations: list[Path] = []
    missing_provenance: list[Path] = []
    if not root.exists():
        return candidates, skipped_translations, missing_provenance

    pages: list[tuple[Path, dict[str, Any], str]] = []
    source_codes: set[str] = set()
    for path in sorted(root.rglob("*.md")):
        if path.name == "_index.md":
            continue
        metadata, body = parse_markdown(path)
        pages.append((path, metadata, body))
        book = str(source_metadata(metadata).get("book") or "").strip()
        if book:
            source_codes.add(book)
    if not source_codes:
        return candidates, skipped_translations, missing_provenance
    code_pattern = re.compile(
        rf"(?<![A-Za-z0-9_-])(?:{'|'.join(re.escape(code) for code in sorted(source_codes))})(?![A-Za-z0-9_-])"
    )

    for path, metadata, body in pages:
        # The erroneous renderer inserts a source code as a standalone word in
        # prose; front matter is intentionally not inspected.
        if not code_pattern.search(body):
            continue
        source = source_metadata(metadata)
        book = str(source.get("book") or "").strip()
        if source.get("provider") != "5e.tools" or not book:
            missing_provenance.append(path)
            continue
        translated = bool(metadata.get("translation"))
        if translated and not include_translated:
            skipped_translations.append(path)
            continue
        params = metadata.get("params") if isinstance(metadata.get("params"), dict) else {}
        kind = str(source.get("entity_type") or metadata.get("kind") or params.get("kind") or "")
        if kind not in SUPPORTED_KINDS:
            print(f"AVISO: tipo não suportado em {path}: {kind or 'ausente'}", file=sys.stderr)
            continue
        candidates.append(
            CorruptedPage(
                path=path,
                kind=kind,
                name=str(source.get("entity_name") or metadata.get("title") or path.stem),
                slug=path.stem,
                book=book,
                editorial={
                    field: metadata[field]
                    for field in (EDITORIAL_FIELDS if not translated else ("draft", "visibility", "status", "tags"))
                    if field in metadata
                },
                translated=translated,
            )
        )
    return candidates, skipped_translations, missing_provenance


def add_assumed_xphb_rule_provenance(paths: list[Path]) -> int:
    """Backfill the approved canonical source for legacy class-rule pages."""
    updated = 0
    for path in paths:
        if path.parent.name != "rules":
            continue
        metadata, body = parse_markdown(path)
        if source_metadata(metadata):
            continue
        metadata["source"] = {
            "provider": "5e.tools",
            "book": "XPHB",
            "entity_type": "rule",
            "entity_name": str(metadata.get("title") or path.stem),
        }
        path.write_text(
            f"---\n{yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=120)}---{body}",
            encoding="utf-8",
        )
        print(f"PROVENIÊNCIA XPHB ADICIONADA: {path.relative_to(PROJECT_ROOT)}")
        updated += 1
    return updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Baixa e substitui os arquivos identificados.")
    parser.add_argument(
        "--include-translated",
        action="store_true",
        help="Também substitui páginas traduzidas, removendo a tradução editorial.",
    )
    parser.add_argument(
        "--assume-xphb-rules",
        action="store_true",
        help="Adiciona proveniência XPHB às regras legadas detectadas antes de sincronizá-las.",
    )
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="Diretório de cache do 5e.tools.")
    args = parser.parse_args(argv)

    candidates, skipped_translations, missing_provenance = find_corrupted_pages(
        include_translated=args.include_translated
    )
    if args.assume_xphb_rules:
        if not args.apply:
            parser.error("--assume-xphb-rules exige --apply")
        add_assumed_xphb_rule_provenance(missing_provenance)
        candidates, skipped_translations, missing_provenance = find_corrupted_pages(
            include_translated=args.include_translated
        )
    for page in candidates:
        action = "REPARAR" if args.apply else "CANDIDATO"
        print(f"{action}: {page.path.relative_to(PROJECT_ROOT)} ({page.kind}: {page.name}; fonte {page.book})")
    for path in skipped_translations:
        print(f"IGNORADO (tradução editorial): {path.relative_to(PROJECT_ROOT)}")
    for path in missing_provenance:
        print(f"REVISAR (sem proveniência para baixar novamente): {path.relative_to(PROJECT_ROOT)}")

    if not candidates:
        print("Nenhuma página sem tradução editorial necessita de reparo.")
        return 0
    if not args.apply:
        print(f"{len(candidates)} candidato(s). Execute com --apply para baixar e substituir.")
        return 0

    catalog = FiveEToolsCatalog(args.cache)
    failures = 0
    for page in candidates:
        try:
            if page.translated:
                remove_translation_metadata(page.path)
            result = sync_compendium_entity(
                page.kind,
                page.name,
                slug=page.slug,
                source=page.book,
                output_root=COMPENDIUM_ROOT,
                origin="repair-source-labels",
                catalog=catalog,
            )
        except Exception as exc:  # Preserve remaining candidates if one remote record fails.
            failures += 1
            print(f"ERRO: {page.path}: {exc}", file=sys.stderr)
            continue
        if result:
            restore_editorial_metadata(page.path, page.editorial)
            print(f"REPARADO: {page.path.relative_to(PROJECT_ROOT)}")
        else:
            failures += 1
            print(f"ERRO: não foi possível resolver {page.path}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
