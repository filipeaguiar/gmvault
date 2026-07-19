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
