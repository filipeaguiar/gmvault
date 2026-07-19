import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _frontmatter(path):
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---"), path
    return yaml.safe_load(text.split("---", 2)[1]) or {}


def test_authored_content_uses_hugo_type(): 
    pages = list((ROOT / "content").rglob("*.md"))
    assert pages

    for path in pages:
        metadata = _frontmatter(path)
        assert "kind" not in metadata, f"deprecated top-level kind in {path}"
        assert metadata.get("type"), f"missing type in {path}"


def test_archetypes_generate_type(): 
    for path in (ROOT / "archetypes").glob("*.md"):
        if path.name == "default.md":
            continue
        text = path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        assert re.search(r"^type\s*:", frontmatter, re.MULTILINE), path
        assert not re.search(r"^\s+kind:\s*", frontmatter, re.MULTILINE), path


def test_kind_helper_uses_type_with_legacy_fallback():
    helper = (ROOT / "layouts/partials/helpers/kind.html").read_text(encoding="utf-8")
    assert ".Type" in helper
