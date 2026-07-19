import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import yaml

from dnd_utils import (
    clean_5etools_tags,
    extract_spell_mechanics,
    fetch_from_5etools,
)


def spell(**values):
    base = {
        "name": "Test Spell",
        "level": 1,
        "entries": [],
        "entriesHigherLevel": [],
    }
    base.update(values)
    return base


def test_fireball_extracts_damage_save_and_continuous_slot_scaling():
    data = spell(
        name="Fireball",
        level=3,
        damageInflict=["fire"],
        savingThrow=["dexterity"],
        entries=[{"type": "entries", "entries": ["Take {@damage 8d6} damage."]}],
        entriesHigherLevel=["Increase {@scaledamage 8d6|3-9|1d6}."],
    )

    mechanics = extract_spell_mechanics(data)

    assert mechanics["level_number"] == 3
    assert mechanics["saving_throws"] == ["dexterity"]
    assert mechanics["damage_types"] == ["fire"]
    assert mechanics["rolls"] == [
        {
            "kind": "damage",
            "notation": "8d6",
            "label": "Dano",
            "damage_type": "fire",
            "scaling": {
                "mode": "spell_slot",
                "thresholds": {
                    "3": "8d6",
                    "4": "9d6",
                    "5": "10d6",
                    "6": "11d6",
                    "7": "12d6",
                    "8": "13d6",
                    "9": "14d6",
                },
            },
        }
    ]


def test_cure_wounds_is_healing_and_sleep_is_generic_dice():
    cure = spell(
        name="Cure Wounds",
        miscTags=["HL"],
        entries=["Regain {@dice 1d8} hit points."],
        entriesHigherLevel=["Increase {@scaledice 1d8|1-9|1d8}."],
    )
    sleep = spell(name="Sleep", entries=["Roll {@dice 5d8}."])

    assert extract_spell_mechanics(cure)["rolls"][0]["kind"] == "healing"
    assert extract_spell_mechanics(sleep)["rolls"] == [
        {"kind": "dice", "notation": "5d8", "label": "Dados"}
    ]


def test_magic_missile_keeps_per_dart_roll_without_prose_inference():
    data = spell(
        name="Magic Missile",
        damageInflict=["force"],
        entries=["Each dart deals {@damage 1d4 + 1} force damage."],
        entriesHigherLevel=["The spell creates one more dart for each slot above 1st."],
    )

    roll = extract_spell_mechanics(data)["rolls"][0]

    assert roll["notation"] == "1d4+1"
    assert "scaling" not in roll
    assert "3d4+3" not in json.dumps(roll)


def test_spell_attack_and_character_level_scaling_are_structured():
    eldritch_blast = spell(
        name="Eldritch Blast",
        level=0,
        spellAttack=["R"],
        damageInflict=["force"],
        entries=["Take {@damage 1d10} force damage."],
    )
    fire_bolt = spell(
        name="Fire Bolt",
        level=0,
        spellAttack=["R"],
        damageInflict=["fire"],
        entries=["Take {@damage 1d10} fire damage."],
        scalingLevelDice={
            "label": "fire damage",
            "scaling": {"1": "1d10", "5": "2d10", "11": "3d10", "17": "4d10"},
        },
    )

    assert extract_spell_mechanics(eldritch_blast)["attack_type"] == "ranged"
    scaling = extract_spell_mechanics(fire_bolt)["rolls"][0]["scaling"]
    assert scaling == {
        "mode": "character_level",
        "thresholds": {"1": "1d10", "5": "2d10", "11": "3d10", "17": "4d10"},
    }


def test_discrete_slot_scaling_and_spell_without_rolls():
    spirit_shroud = spell(
        name="Spirit Shroud",
        level=3,
        damageInflict=["radiant"],
        entries=["Deal {@damage 1d8}."],
        entriesHigherLevel=["Increase {@scaledamage 1d8|3,5,7,9|1d8}."],
    )
    mage_armor = spell(name="Mage Armor", entries=["The target's base AC becomes 13."])

    thresholds = extract_spell_mechanics(spirit_shroud)["rolls"][0]["scaling"]["thresholds"]
    assert thresholds == {"3": "1d8", "5": "2d8", "7": "3d8", "9": "4d8"}
    assert extract_spell_mechanics(mage_armor)["rolls"] == []


def test_scaled_inline_markup_remains_dice_friendly():
    rendered = clean_5etools_tags("Increase by {@scaledamage 8d6|3-9|1d6}.")
    assert 'data-roll-notation="8d6"' in rendered
    assert ">8d6</span>" in rendered


def test_reference_tags_ignore_source_and_keep_explicit_display_label():
    rendered = clean_5etools_tags(
        "Roll {@variantrule Initiative|XPHB}; gain {@variantrule "
        "Proficiency|XPHB|Proficiency Bonus}; avoid {@condition Incapacitated|XPHB}."
    )

    assert rendered == "Roll Initiative; gain Proficiency Bonus; avoid Incapacitated."


def test_filter_tags_do_not_expose_source_query_parameters():
    rendered = clean_5etools_tags(
        "See {@filter Eldritch Invocation Options|optionalfeatures|feature type=EI|source=XPHB}."
    )

    assert rendered == "See Eldritch Invocation Options."


def test_spell_sync_preserves_translation_and_markdown_body():
    fireball = spell(
        name="Fireball",
        level=3,
        school="V",
        damageInflict=["fire"],
        savingThrow=["dexterity"],
        entries=["Take {@damage 8d6} fire damage."],
        entriesHigherLevel=["Increase {@scaledamage 8d6|3-9|1d6}."],
    )
    response = MagicMock()
    response.__enter__.return_value.read.return_value = json.dumps(
        {"spell": [fireball]}
    ).encode()
    previous_cwd = Path.cwd()

    with tempfile.TemporaryDirectory() as temp_dir, patch(
        "dnd_utils.urllib.request.urlopen", return_value=response
    ):
        os.chdir(temp_dir)
        try:
            path = Path("content/compendium/spells/fireball.md")
            path.parent.mkdir(parents=True)
            body = "\n\nDescrição traduzida e revisada.\n"
            path.write_text(
                "---\n"
                "title: Fireball\n"
                "titulo_pt_br: Bola de Fogo\n"
                "translation:\n"
                "  status: reviewed\n"
                "spell_info:\n"
                "  level: 3rd level\n"
                "---"
                + body,
                encoding="utf-8",
            )

            assert fetch_from_5etools("spell", "Fireball") == "/compendium/spells/fireball/"
            rendered = path.read_text(encoding="utf-8")
            metadata = yaml.safe_load(rendered.split("---", 2)[1])
        finally:
            os.chdir(previous_cwd)

    assert rendered.split("---", 2)[2] == body
    assert metadata["titulo_pt_br"] == "Bola de Fogo"
    assert metadata["translation"]["status"] == "reviewed"
    assert metadata["spell_info"]["rolls"][0]["notation"] == "8d6"
