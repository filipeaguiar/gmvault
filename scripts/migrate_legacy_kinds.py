#!/usr/bin/env python3
"""Move legacy ``params.kind`` front matter to Hugo's top-level ``type`` field."""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = PROJECT_ROOT / "content"


def params_block_end(lines: list[str], start: int) -> int:
    end = start + 1
    while end < len(lines):
        if lines[end].strip() and not lines[end].startswith((" ", "\t")):
            break
        end += 1
    return end


def migrate_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return "skipped"
    end = text.find("\n---", 4)
    if end == -1:
        return "skipped"

    lines = text[4:end].splitlines(keepends=True)
    changed = False

    # Repair files changed by an earlier top-level-kind migration. Hugo 0.164
    # reserves ``kind``, so page semantics must use the supported ``type`` key.
    for index, line in enumerate(lines):
        if line.startswith("kind:"):
            lines[index] = "type:" + line.split(":", 1)[1]
            changed = True
            if index + 1 < len(lines) and lines[index + 1].startswith((" ", "\t")):
                lines.insert(index + 1, "params:\n")
            break

    index = 0
    while index < len(lines):
        if lines[index].strip() != "params:" or lines[index].startswith((" ", "\t")):
            index += 1
            continue
        block_end = params_block_end(lines, index)
        kind_index = next(
            (child for child in range(index + 1, block_end) if lines[child].lstrip().startswith("kind:")),
            None,
        )
        if kind_index is None:
            index = block_end
            continue

        kind_value = lines[kind_index].split(":", 1)[1].strip()
        other_children = [
            child for child in range(index + 1, block_end)
            if child != kind_index and lines[child].strip() and not lines[child].lstrip().startswith("#")
        ]
        has_type = any(line.startswith("type:") for line in lines)
        if other_children:
            lines.pop(kind_index)
            if not has_type:
                lines.insert(index, f"type: {kind_value}\n")
                index += 1
        else:
            lines[index] = f"type: {kind_value}\n" if not has_type else ""
            lines.pop(kind_index)
        changed = True
        index += 1

    if not changed:
        return "unchanged"
    path.write_text("---\n" + "".join(lines) + text[end:], encoding="utf-8")
    return "migrated"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_ROOT, help="Arquivo ou diretório a corrigir.")
    args = parser.parse_args()
    target = args.path.resolve()
    files = [target] if target.is_file() else sorted(target.rglob("*.md"))
    counts: dict[str, int] = {}
    for path in files:
        result = migrate_file(path)
        counts[result] = counts.get(result, 0) + 1
    print(f"Migrados: {counts.get('migrated', 0)}; sem alteração: {counts.get('unchanged', 0)}; ignorados: {counts.get('skipped', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
