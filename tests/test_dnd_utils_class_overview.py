import os
import tempfile
from pathlib import Path

from dnd_utils import ensure_compendium_class_overview


def test_class_overview_creates_feature_rule_page_from_entries():
    class_data = {
        "class": [{"name": "Test Class"}],
        "classFeature": [
            {
                "className": "Test Class",
                "name": "Rage",
                "level": 1,
                "entries": ["The feature text comes from the class feature entry."],
            }
        ],
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        previous = os.getcwd()
        try:
            os.chdir(temp_dir)
            ref = ensure_compendium_class_overview("Test Class", class_data)
        finally:
            os.chdir(previous)

        assert ref == "/compendium/classes/test-class/"
        class_page = Path(temp_dir) / "content/compendium/classes/test-class.md"
        rule_page = Path(temp_dir) / "content/compendium/rules/rage.md"
        assert "### Nível 1" in class_page.read_text(encoding="utf-8")
        assert "[/compendium/rules/rage/]" not in class_page.read_text(encoding="utf-8")
        assert "/compendium/rules/rage/" in class_page.read_text(encoding="utf-8")
        rule_text = rule_page.read_text(encoding="utf-8")
        assert "draft: false" in rule_text
        assert 'visibility: "public"' in rule_text
        assert "The feature text comes from the class feature entry." in rule_text
