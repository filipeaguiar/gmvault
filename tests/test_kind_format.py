import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _frontmatter(path):
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---"), path
    return yaml.safe_load(text.split("---", 2)[1]) or {}


def test_authored_content_uses_nested_kind_only():
    pages = list((ROOT / "content").rglob("*.md"))
    assert pages

    for path in pages:
        metadata = _frontmatter(path)
        assert "kind" not in metadata, f"legacy top-level kind in {path}"
        assert metadata.get("params", {}).get("kind"), f"missing params.kind in {path}"


def test_archetypes_generate_nested_kind():
    for path in (ROOT / "archetypes").glob("*.md"):
        text = path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        assert not re.search(r"^kind\s*:", frontmatter, re.MULTILINE), path
        if re.search(r"^\s+kind:\s*", frontmatter, re.MULTILINE):
            assert re.search(r"^params:\s*$", frontmatter, re.MULTILINE), path


def test_kind_helper_prioritizes_params_kind_and_keeps_legacy_fallback():
    helper = (ROOT / "layouts/partials/helpers/kind.html").read_text(encoding="utf-8")
    assert "or .Params.params.kind .Params.kind" in helper
