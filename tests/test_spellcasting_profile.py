from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import frontmatter

from dnd_utils import infer_spellcasting_profile


def test_infer_spellcasting_profile_distinguishes_prepared_known_and_pact():
    cleric = infer_spellcasting_profile("Cleric", level=5)
    bard = infer_spellcasting_profile("Bard", level=5)
    warlock = infer_spellcasting_profile("Warlock", level=5)

    assert cleric["kind"] == "prepared"
    assert cleric["can_prepare"] is True
    assert cleric["can_mark_known"] is False
    assert bard["kind"] == "known"
    assert bard["can_prepare"] is False
    assert bard["can_mark_known"] is True
    assert warlock["kind"] == "pact"
    assert warlock["uses_pact_slots"] is True
    assert warlock["can_prepare"] is False


def test_character_sheet_renders_spell_manager_chrome():
    with tempfile.TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "project"
        project.mkdir()
        for name in ("content", "layouts", "assets", "static"):
            source = ROOT / name
            if source.exists():
                shutil.copytree(source, project / name)
        shutil.copy2(ROOT / "hugo.yaml", project / "hugo.yaml")

        character_path = (
            project
            / "content/campaigns/journeys-through-the-radiant-citadel/characters/pinky.md"
        )
        character = frontmatter.load(character_path)
        character["char_info"]["spellcasting"] = infer_spellcasting_profile("Cleric", level=1)
        character["char_info"]["spellcasting"]["prepared_limit"] = 2
        character["char_info"]["spellcasting"]["prepared_count"] = 1
        character["char_info"]["spellcasting"]["known_count"] = 1
        character["char_info"]["spellcasting"]["cantrips_known"] = 2
        character["char_info"]["spellcasting"]["has_search"] = True
        character["char_info"]["spell_slots"] = {1: 2}
        character["char_info"]["spells"] = [
            {
                "name": "Cure Wounds",
                "ref": "/compendium/spells/cure-wounds/",
                "level": 1,
                "usage": "1 action",
                "prepared": True,
            }
        ]
        character["char_info"]["class_spells"] = ["/compendium/spells/cure-wounds/"]
        frontmatter.dump(character, character_path)

        destination = Path(temp_dir) / "public"
        subprocess.run(
            [
                "hugo",
                "--source",
                str(project),
                "--destination",
                str(destination),
                "-D",
                "--gc",
                "--minify",
                "--quiet",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        html = (
            destination
            / "campaigns/journeys-through-the-radiant-citadel/characters/pinky/index.html"
        ).read_text(encoding="utf-8")

    assert "spell-manager" in html
    assert "spell-manager-counters" in html
    assert "spell-manager-toolbar" in html
    assert "spell-level-filters" in html
    assert "spell-search" in html
