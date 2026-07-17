#!/usr/bin/env python3
"""Report controlled RPG terms found in a Markdown corpus but absent from the glossary."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import yaml

from translate_drafts import load_glossary_config

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_GLOSSARY = PROJECT_ROOT / "translation_glossary.json"
DEFAULT_CORPUS = PROJECT_ROOT / ".compendium-staging" / "compendium"
DEFAULT_REPORT = PROJECT_ROOT / "glossary_audit_report.json"

# Terms are candidates, not automatic translations. The list focuses on 2024
# rules vocabulary and recurring stat-block/equipment concepts.
MECHANICAL_CANDIDATES = (
    "D20 Test", "Heroic Inspiration", "Influence Action", "Magic Action",
    "Study Action", "Utilize Action", "Emanation", "Weapon Mastery",
    "Mastery Property", "Armor Training", "Weapon Proficiency",
    "Tool Proficiency", "Creature Type", "Initiative Bonus", "Passive Insight",
    "Passive Investigation", "Temporary Hit Point", "Concentration Check",
    "Exhaustion Level", "Bloodied Value", "Attunement Slot", "Short Rest",
    "Long Rest", "Reaction Trigger", "Bonus Action", "Free Object Interaction",
    "Unarmed Strike", "Grapple Escape", "Spellcasting Focus", "Area of Effect",
    "Cone", "Cube", "Cylinder", "Line", "Sphere", "Teleportation",
    "Difficult Terrain", "Damage Threshold", "Object Interaction",
)


def iter_text(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from iter_text(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_text(child)


def markdown_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return raw
    parts = raw.split("---", 2)
    try:
        metadata = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        metadata = {}
    return "\n".join([*iter_text(metadata), parts[2] if len(parts) > 2 else ""])


def flatten_required(config: dict[str, Any]) -> dict[str, str]:
    return {
        source: target
        for terms in config.get("required_translations", {}).values()
        if isinstance(terms, dict)
        for source, target in terms.items()
    }


def audit_corpus(corpus: Path, glossary_path: Path = DEFAULT_GLOSSARY) -> dict[str, Any]:
    config = load_glossary_config(glossary_path)
    controlled = {term.casefold() for term in flatten_required(config)}
    counts: Counter[str] = Counter()
    files = sorted(corpus.rglob("*.md"))
    texts = [markdown_text(path) for path in files]
    for candidate in MECHANICAL_CANDIDATES:
        pattern = re.compile(rf"(?<![\w]){re.escape(candidate)}(?![\w])", re.IGNORECASE)
        counts[candidate] = sum(len(pattern.findall(text)) for text in texts)
    uncovered = [
        {"term": term, "occurrences": count}
        for term, count in counts.most_common()
        if count and term.casefold() not in controlled
    ]
    unresolved_tags = sum(len(re.findall(r"\{@[a-zA-Z]+\s", text)) for text in texts)
    return {
        "schema_version": 1,
        "corpus": str(corpus),
        "files_scanned": len(files),
        "controlled_terms": len(controlled),
        "uncovered_candidates": uncovered,
        "unresolved_5etools_tags": unresolved_tags,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--glossary", type=Path, default=DEFAULT_GLOSSARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args(argv)
    report = audit_corpus(args.corpus, args.glossary)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
