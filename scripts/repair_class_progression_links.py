#!/usr/bin/env python3
"""Restore feature links in existing class and subclass progression pages."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from compendium_rebuild import FiveEToolsCatalog, slugify


CLASSES = ROOT / "content" / "compendium" / "classes"
RULES = ROOT / "content" / "compendium" / "rules"


def page_title(ref: str, fallback: str) -> str:
    path = ROOT / "content" / ref.strip("/")
    path = path.with_suffix(".md")
    if not path.exists():
        return fallback
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return fallback
    end = text.find("\n---", 4)
    data = yaml.safe_load(text[4:end]) or {}
    return data.get("titulo_pt_br") or data.get("title") or fallback


def main() -> int:
    catalog = FiveEToolsCatalog()
    updated = 0
    for path in sorted(CLASSES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---", 4)
        metadata = yaml.safe_load(text[4:end]) or {}
        source = metadata.get("source") or {}
        remote_file = source.get("remote_file")
        entity_name = source.get("entity_name")
        source_book = source.get("book")
        entity_key = source.get("remote_key")
        if not all((remote_file, entity_name, source_book, entity_key)):
            continue
        data = catalog.get_json(remote_file)
        if entity_key == "class":
            features = [item for item in data.get("classFeature", []) if item.get("className") == entity_name and item.get("source") == source_book]
        elif entity_key == "subclass":
            subclass = next((item for item in data.get("subclass", []) if item.get("name") == entity_name and item.get("source") == source_book), {})
            short_name = subclass.get("shortName") or entity_name
            features = [item for item in data.get("subclassFeature", []) if item.get("subclassShortName") == short_name and item.get("source") == source_book]
        else:
            continue
        if not features:
            continue
        levels: dict[int, list[str]] = defaultdict(list)
        for feature in features:
            name = feature.get("name")
            if not name:
                continue
            ref = f"/compendium/rules/{slugify(name)}/"
            title = page_title(ref, name)
            levels[int(feature.get("level", 0))].append(f"- [{title}]({ref})")
        body = "\n".join(
            line for level in sorted(levels)
            for line in (f"## Nível {level}", "", *levels[level], "")
        ).strip()
        rendered = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=120)
        path.write_text(f"---\n{rendered}---\n\n{body}\n", encoding="utf-8")
        updated += 1
    print(f"Progressões corrigidas: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
