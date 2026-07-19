from unittest.mock import patch

from dnd_utils import build_level_up_plan
from edit_character import level_up_character


def test_level_up_plan_prefers_xphb_and_resolves_subclass_short_name():
    class_data = {
        "subclass": [{"name": "Blade Scholar", "shortName": "Scholar Blade"}],
        "classFeature": [
            {"name": "Extra Attack", "className": "Fighter", "level": 5, "source": "PHB"},
            {"name": "Extra Attack", "className": "Fighter", "level": 5, "source": "XPHB"},
        ],
        "subclassFeature": [
            {"name": "Arcane Edge", "subclassShortName": "Scholar Blade", "level": 5, "source": "XPHB"},
            {"name": "Other Feature", "subclassShortName": "Other", "level": 5, "source": "XPHB"},
        ],
    }
    plan = build_level_up_plan({"class": "Fighter", "subclass": "Blade Scholar", "level": 4}, class_data)
    assert plan["valid"]
    assert plan["target_level"] == 5
    assert plan["subclass_short"] == "Scholar Blade"
    assert [(feature["name"], feature["source"]) for feature in plan["features"]] == [
        ("Extra Attack", "XPHB"), ("Arcane Edge", "XPHB")
    ]


def test_level_up_plan_rejects_invalid_or_maximum_level_character():
    assert not build_level_up_plan({}, {}).get("valid")
    assert not build_level_up_plan({"class": "Wizard", "level": 20}, {}).get("valid")


def test_cancelled_level_up_does_not_mutate_character():
    post = {"title": "Test Hero", "char_info": {"class": "Fighter", "level": 1, "class_level": 1, "hp": "10", "hp_max": "10", "hp_current": "10", "stats": {"con": 10}, "actions": []}}
    original = repr(post)
    with patch("edit_character.dnd_utils.fetch_class_json", return_value={"classFeature": [], "subclassFeature": []}), patch("edit_character.ask_choice", side_effect=["Média: +6 HP", "Cancelar"]):
        assert not level_up_character(post, None)
    assert repr(post) == original


def _rogue_with_skills():
    return {
        "title": "Expert Hero",
        "char_info": {
            "class": "Rogue",
            "level": 1,
            "class_level": 1,
            "hp": "8",
            "hp_max": "8",
            "hp_current": "8",
            "stats": {"con": 10, "dex": 14},
            "skills": {
                "acrobatics": {"stat": "dex", "proficient": True, "expertise": False, "bonus": 4},
                "stealth": {"stat": "dex", "proficient": True, "expertise": False, "bonus": 4},
                "perception": {"stat": "wis", "proficient": True, "expertise": False, "bonus": 2},
                "history": {"stat": "int", "proficient": False, "expertise": False, "bonus": 0},
            },
            "actions": [],
        },
    }


def _expertise_class_data():
    return {
        "classFeature": [
            {"name": "Expertise", "className": "Rogue", "level": 2, "source": "XPHB"},
        ],
        "subclassFeature": [],
    }


def test_level_up_applies_expertise_and_doubles_skill_bonus():
    post = _rogue_with_skills()
    with patch("edit_character.dnd_utils.fetch_class_json", return_value=_expertise_class_data()), patch("edit_character.dnd_utils.create_rule_stub", return_value=None), patch("edit_character.ask_choice", side_effect=["Média: +5 HP", "acrobatics", "stealth", "Confirmar"]):
        assert level_up_character(post, None)

    skills = post["char_info"]["skills"]
    assert skills["acrobatics"]["expertise"]
    assert skills["stealth"]["expertise"]
    assert skills["acrobatics"]["bonus"] == 6
    assert skills["stealth"]["bonus"] == 6
    assert not skills["perception"]["expertise"]


def test_expertise_rejects_duplicate_or_cancelled_selection_without_mutating_character():
    post = _rogue_with_skills()
    original = repr(post)
    with patch("edit_character.dnd_utils.fetch_class_json", return_value=_expertise_class_data()), patch("edit_character.dnd_utils.create_rule_stub", return_value=None), patch("edit_character.ask_choice", side_effect=["Média: +5 HP", "acrobatics", "acrobatics"]):
        assert not level_up_character(post, None)
    assert repr(post) == original

    post = _rogue_with_skills()
    original = repr(post)
    with patch("edit_character.dnd_utils.fetch_class_json", return_value=_expertise_class_data()), patch("edit_character.dnd_utils.create_rule_stub", return_value=None), patch("edit_character.ask_choice", side_effect=["Média: +5 HP", "Cancelar"]):
        assert not level_up_character(post, None)
    assert repr(post) == original


def test_expertise_requires_two_eligible_proficient_skills():
    post = _rogue_with_skills()
    post["char_info"]["skills"]["stealth"]["expertise"] = True
    post["char_info"]["skills"]["perception"]["expertise"] = True
    original = repr(post)
    with patch("edit_character.dnd_utils.fetch_class_json", return_value=_expertise_class_data()), patch("edit_character.dnd_utils.create_rule_stub", return_value=None), patch("edit_character.ask_choice", return_value="Média: +5 HP"):
        assert not level_up_character(post, None)
    assert repr(post) == original
