#!/usr/bin/env python3
"""Marca como publicados os documentos Markdown do compêndio.

Por padrão apenas informa os arquivos que seriam alterados. Use --apply para
alterar ``draft: true`` para ``draft: false`` no front matter.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMPENDIUM_ROOT = PROJECT_ROOT / "content" / "compendium"
DRAFT_TRUE = re.compile(r"^(draft:\s*)true(\s*(?:#.*)?)$", re.MULTILINE)


def publish(path: Path, apply: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    if not original.startswith("---\n"):
        return False
    front_matter_end = original.find("\n---", 4)
    if front_matter_end == -1:
        return False

    front_matter = original[:front_matter_end]
    updated_front_matter, substitutions = DRAFT_TRUE.subn(r"\1false\2", front_matter, count=1)
    if not substitutions:
        return False

    if apply:
        path.write_text(updated_front_matter + original[front_matter_end:], encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Grava as alterações. Sem esta opção, apenas lista os arquivos.")
    args = parser.parse_args()

    changed = [path for path in sorted(COMPENDIUM_ROOT.rglob("*.md")) if publish(path, args.apply)]
    action = "Publicados" if args.apply else "Seriam publicados"
    for path in changed:
        print(f"{action}: {path.relative_to(PROJECT_ROOT)}")
    print(f"Total: {len(changed)} documento(s) do compêndio.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
