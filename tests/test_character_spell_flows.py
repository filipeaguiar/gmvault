from pathlib import Path
import sys
from unittest.mock import Mock, patch

import frontmatter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import create_character
import edit_character


def raw_spell(name, *, level=1, prepared=False, uses_slot=True):
    return {
        "definition": {"name": name, "level": level},
        "prepared": prepared,
        "usesSpellSlot": uses_slot,
    }


def test_create_flow_emits_minimal_refs_and_skips_unresolved_names():
    fetcher = Mock(side_effect=lambda _kind, name: (
        "/compendium/spells/cure-wounds/" if name == "Cure Wounds" else None
    ))

    entries, unresolved = create_character.build_selected_spell_entries(
        [{"name": "Cure Wounds", "level": 1}, {"name": "Unknown", "level": 2}],
        "Cleric",
        fetcher=fetcher,
    )

    assert entries == [{
        "ref": "/compendium/spells/cure-wounds/",
        "prepared": True,
        "availability": "prepared",
        "source": "class",
        "usage": "1 action",
        "can_prepare": True,
    }]
    assert unresolved == ["Unknown"]


def test_edit_flow_normalizes_legacy_preserves_unresolved_and_recomputes_profile():
    post = frontmatter.Post(
        "Biography\n",
        char_info={
            "class": "Wizard",
            "level": 3,
            "spell_slots": {1: 4, 2: 2},
            "spells": [
                {"name": "Magic Missile", "level": 1, "prepared": True},
                {"name": "Homebrew Bolt", "level": 1, "description": "Legacy"},
            ],
            "class_spells": [
                "/compendium/spells/magic-missile/",
                "/compendium/spells/magic-missile/",
            ],
        },
        compendium_refs=[],
    )

    def resolve(_kind, name):
        return {
            "Magic Missile": "/compendium/spells/magic-missile/",
            "Shield": "/compendium/spells/shield/",
        }.get(name)

    with patch("edit_character.dnd_utils.fetch_from_5etools", side_effect=resolve):
        added = edit_character.add_spells(post, [{"name": "Shield", "level": 1}])

    assert added == 1
    spells = post["char_info"]["spells"]
    assert any(entry.get("ref") == "/compendium/spells/magic-missile/" for entry in spells)
    assert any(entry.get("name") == "Homebrew Bolt" for entry in spells)
    assert any(entry.get("ref") == "/compendium/spells/shield/" for entry in spells)
    assert post["char_info"]["class_spells"] == ["/compendium/spells/magic-missile/"]
    assert post["char_info"]["spellcasting"]["kind"] == "prepared"
    assert post["char_info"]["spellcasting"]["slot_levels"] == [1, 2]


def test_edit_flow_does_not_add_or_reference_unresolved_new_spell():
    post = frontmatter.Post(
        "Biography\n",
        char_info={"class": "Bard", "level": 1, "spells": []},
        compendium_refs=[],
    )
    with patch("edit_character.dnd_utils.fetch_from_5etools", return_value=None):
        added = edit_character.add_spells(post, [{"name": "Missing", "level": 1}])

    assert added == 0
    assert post["char_info"]["spells"] == []
    assert post["compendium_refs"] == []
