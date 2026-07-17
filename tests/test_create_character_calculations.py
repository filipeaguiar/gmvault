import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import frontmatter

import create_character
from create_character import calculate_saves_data, calculate_skills_data


def test_skills_use_canonical_stat_field_and_bonus():
    mods = {"str": 1, "dex": 3, "con": 2, "int": 0, "wis": 2, "cha": 4}

    skills = calculate_skills_data({"deception", "arcana"}, mods, 2)

    assert skills["deception"] == {
        "bonus": 6,
        "proficient": True,
        "expertise": False,
        "stat": "cha",
    }
    assert skills["athletics"] == {
        "bonus": 1,
        "proficient": False,
        "expertise": False,
        "stat": "str",
    }


def test_warlock_saving_throw_list_is_normalized():
    mods = {"str": -1, "dex": 2, "con": 1, "int": 0, "wis": 2, "cha": 4}
    class_entry = {"name": "Warlock", "proficiency": ["wis", "cha"]}

    saves, proficient, summary = calculate_saves_data(class_entry, mods, 2)

    assert proficient == {
        "str": False,
        "dex": False,
        "con": False,
        "int": False,
        "wis": True,
        "cha": True,
    }
    assert saves["wis"] == 4
    assert saves["cha"] == 6
    assert summary == "Wis +4, Cha +6"


def test_warlock_character_is_written_after_final_calculations():
    race_data = {
        "race": [
            {
                "name": "Human",
                "source": "PHB",
                "size": ["M"],
                "speed": 30,
            }
        ],
        "subrace": [],
    }
    class_data = {
        "class": [
            {
                "name": "Warlock",
                "source": "PHB",
                "hd": {"number": 1, "faces": 8},
                "proficiency": ["wis", "cha"],
                "startingProficiencies": {
                    "skills": [
                        {
                            "choose": {
                                "count": 2,
                                "from": ["arcana", "deception"],
                            }
                        }
                    ]
                },
            }
        ],
        "classFeature": [],
    }

    def choose(prompt, options):
        lower = prompt.lower()
        if "espécie base" in lower:
            return "Human"
        if "variante" in lower:
            return options[0]
        if "classe principal" in lower:
            return "Warlock"
        if "pacote inicial" in lower:
            return "Nenhum"
        if "aumentos de atributos" in lower:
            return "Não aplicar aumentos (manter atributos base secos)"
        return options[0]

    def ask_value(prompt, default=None):
        lower = prompt.lower()
        if "nome do personagem" in lower:
            return "Test Warlock"
        if "alinhamento" in lower:
            return "True Neutral"
        if "escolha até" in lower:
            return "1,2"
        return ""

    def ask_number(prompt, default=0):
        lower = prompt.lower()
        if "nível" in lower:
            return 1
        if "perícias adicionais" in lower:
            return 0
        return 10

    previous_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            with (
                patch("sys.argv", ["create_character.py", "--campaign", "test"]),
                patch("create_character.ask_choice", side_effect=choose),
                patch("create_character.ask", side_effect=ask_value),
                patch("create_character.ask_int", side_effect=ask_number),
                patch("create_character.select_feats_for_level", return_value=[]),
                patch("create_character.load_species_data", return_value=race_data),
                patch(
                    "create_character.load_class_index",
                    return_value={"warlock": "class-warlock.json"},
                ),
                patch("create_character.load_class_data", return_value=class_data),
                patch(
                    "create_character.dnd_utils.load_background_data",
                    return_value={"background": []},
                ),
                patch(
                    "create_character.dnd_utils.load_item_data",
                    return_value={"item": []},
                ),
                patch(
                    "create_character.fetch_from_5etools",
                    side_effect=lambda kind, name: f"/compendium/{kind}s/{name.lower()}/",
                ),
                patch(
                    "create_character.dnd_utils.fetch_from_5etools",
                    side_effect=lambda kind, name: f"/compendium/{kind}s/{name.lower()}/",
                ),
                patch("create_character.ensure_compendium_class_overview"),
                patch("create_character.publish_compendium_page"),
            ):
                create_character.main()

            character_path = Path(
                "content/campaigns/test/characters/test-warlock.md"
            )
            assert character_path.is_file()
            post = frontmatter.load(character_path)
        finally:
            os.chdir(previous_cwd)

    assert post["char_info"]["class"] == "Warlock"
    assert post["char_info"]["saves_proficient"]["wis"] is True
    assert post["char_info"]["saves_proficient"]["cha"] is True
    assert post["char_info"]["skills"]["arcana"]["stat"] == "int"
