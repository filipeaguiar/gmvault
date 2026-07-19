#!/usr/bin/env python3
"""Bulk-import 2024-priority character classes, subclasses, features, and feats.

Uses the same catalog and ``sync_compendium_entity`` serializer used by local
character creation/editing. XPHB wins whenever the same entity also exists in
older source books; TCE and XGE provide only entries without an XPHB version.
All generated pages remain drafts for editorial review.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from compendium_rebuild import FiveEToolsCatalog, slugify, sync_compendium_entity
from dnd_utils import source_priority


CLASS_SOURCE = "XPHB"
OPTIONAL_SOURCES = {"XPHB", "TCE", "XGE"}
OUTPUT_ROOT = Path("content/compendium")


def prefer_current(records, key):
    """Keep one record per entity identity, preferring its XPHB revision."""
    grouped = defaultdict(list)
    for record in records:
        grouped[key(record)].append(record)
    return [min(group, key=lambda record: source_priority(record.source)) for group in grouped.values()]


def write_subclass_progression(record, feature_refs: dict[tuple[str, str], list[tuple[int, str, str]]]) -> None:
    """Add subclass hierarchy and level progression after shared serialization."""
    data = record.data
    path = OUTPUT_ROOT / "classes" / f"{slugify(record.name)}.md"
    text = path.read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---", 2)[1]) or {}
    metadata["parent_class"] = f"/compendium/classes/{slugify(data['className'])}/"
    by_level = defaultdict(list)
    subclass_key = data.get("shortName") or record.name
    for level, name, ref in feature_refs.get((subclass_key, record.source), []):
        by_level[level].append(f"- [{name}]({ref})")
    progression = []
    for level in sorted(by_level):
        progression.extend([f"## Nível {level}", "", *by_level[level], ""])
    rendered = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=120)
    body = "\n".join(progression).strip()
    path.write_text(f"---\n{rendered}---\n\n{body}\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Grava as páginas no compêndio ativo.")
    args = parser.parse_args()

    catalog = FiveEToolsCatalog()
    class_records = catalog.records("class")
    classes = [record for record in class_records if record.remote_key == "class" and record.source == CLASS_SOURCE]
    class_names = {record.name for record in classes}
    raw_subclasses = [
        record for record in class_records
        if record.remote_key == "subclass"
        and record.source in OPTIONAL_SOURCES
        and record.data.get("className") in class_names
        and record.data.get("classSource") == CLASS_SOURCE
    ]
    subclasses = prefer_current(raw_subclasses, lambda record: (record.data["className"], record.name.casefold()))
    subclass_keys = {(record.data.get("shortName") or record.name, record.source) for record in subclasses}

    rule_records = catalog.records("rule")
    raw_class_features = [
        record for record in rule_records
        if record.remote_key == "classFeature"
        and record.source in OPTIONAL_SOURCES
        and record.data.get("className") in class_names
        and record.data.get("classSource") == CLASS_SOURCE
    ]
    raw_subclass_features = [
        record for record in rule_records
        if record.remote_key == "subclassFeature"
        and record.source in OPTIONAL_SOURCES
        and (record.data.get("subclassShortName"), record.source) in subclass_keys
    ]
    class_features = prefer_current(
        raw_class_features,
        lambda record: (record.data.get("className"), record.name.casefold(), record.data.get("level")),
    )
    subclass_features = prefer_current(
        raw_subclass_features,
        lambda record: (record.data.get("className"), record.data.get("subclassShortName"), record.name.casefold(), record.data.get("level")),
    )
    features = class_features + subclass_features

    raw_feats = [record for record in catalog.records("feat") if record.source in OPTIONAL_SOURCES]
    feats = prefer_current(raw_feats, lambda record: record.name.casefold())

    print(f"Classes: {len(classes)}; subclasses: {len(subclasses)}; features: {len(features)}; feats: {len(feats)}")
    if not args.apply:
        print("Dry run. Execute com --apply para gravar as páginas.")
        return 0

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    feature_refs = defaultdict(list)
    for record in classes + subclasses:
        sync_compendium_entity("class", record.name, slug=slugify(record.name), source=record.source, origin="bulk-class-import", catalog=catalog)
    for record in features:
        ref = sync_compendium_entity("rule", record.name, slug=slugify(record.name), source=record.source, origin="bulk-class-import", catalog=catalog)
        if record.remote_key == "subclassFeature" and ref:
            feature_refs[(record.data.get("subclassShortName"), record.source)].append((int(record.data.get("level", 0)), record.name, ref))
    for record in feats:
        sync_compendium_entity("feat", record.name, slug=slugify(record.name), source=record.source, origin="bulk-class-import", catalog=catalog)
    for record in subclasses:
        write_subclass_progression(record, feature_refs)

    print("Importação concluída. Revise os drafts antes de publicar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
