import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import frontmatter
import pytest

import create_character
from dnd_utils import GoBackException


def answer(navigator, prompt, value, validator=None):
    return navigator.answer("test", prompt, lambda: value, validator)


def test_navigator_returns_to_only_the_previous_question():
    navigator = create_character.QuestionNavigator()
    navigator.begin_pass()
    assert answer(navigator, "name", "Old Name") == "Old Name"

    with pytest.raises(GoBackException):
        navigator.request_back()

    navigator.begin_pass()
    assert answer(navigator, "name", "New Name") == "New Name"
    assert navigator.answers == [{"key": "test:name#0", "value": "New Name"}]


def test_navigator_supports_successive_back_requests():
    navigator = create_character.QuestionNavigator()
    navigator.begin_pass()
    answer(navigator, "campaign", "demo")
    answer(navigator, "name", "Name")

    with pytest.raises(GoBackException):
        navigator.request_back()
    navigator.begin_pass()
    assert answer(navigator, "campaign", "ignored") == "demo"
    with pytest.raises(GoBackException):
        navigator.request_back()

    navigator.begin_pass()
    assert answer(navigator, "campaign", "other") == "other"


def test_navigator_cancels_when_there_is_no_previous_question():
    navigator = create_character.QuestionNavigator()
    navigator.begin_pass()

    with pytest.raises(create_character.NavigationCancelled):
        navigator.request_back()


def test_navigator_preserves_valid_later_answers_and_invalidates_incompatible_ones():
    navigator = create_character.QuestionNavigator()
    navigator.begin_pass()
    answer(navigator, "class", "Wizard")
    answer(navigator, "spell", "Fireball")
    answer(navigator, "level", 5)

    # Volta de uma pergunta por vez até classe.
    with pytest.raises(GoBackException):
        navigator.request_back()
    navigator.begin_pass()
    assert answer(navigator, "class", "ignored") == "Wizard"
    assert answer(navigator, "spell", "ignored") == "Fireball"
    with pytest.raises(GoBackException):
        navigator.request_back()
    navigator.begin_pass()
    assert answer(navigator, "class", "ignored") == "Wizard"
    with pytest.raises(GoBackException):
        navigator.request_back()

    navigator.begin_pass()
    assert answer(navigator, "class", "Cleric") == "Cleric"
    assert answer(
        navigator,
        "spell",
        "Cure Wounds",
        validator=lambda value: value in {"Cure Wounds"},
    ) == "Cure Wounds"


def test_invalid_integer_repeats_current_question_without_history_entry():
    navigator = create_character.QuestionNavigator()
    create_character._active_navigator = navigator
    navigator.begin_pass()
    try:
        with patch("builtins.input", side_effect=["invalid", "7"]):
            assert create_character.ask_int("Level", 1) == 7
    finally:
        create_character._active_navigator = None

    assert len(navigator.answers) == 1
    assert navigator.answers[0]["value"] == 7


def test_main_reopens_only_previous_questions_and_keeps_earlier_answers():
    race_data = {
        "race": [{"name": "Human", "source": "PHB", "size": ["M"], "speed": 30}],
        "subrace": [],
    }
    class_data = {
        "class": [
            {
                "name": "Fighter",
                "source": "PHB",
                "hd": {"number": 1, "faces": 10},
                "proficiency": ["str", "con"],
                "startingProficiencies": {
                    "skills": [{"choose": {"count": 0, "from": []}}]
                },
            }
        ],
        "classFeature": [],
    }
    responses = iter(
        [
            "Old Name",
            "True Neutral",
            "00",  # espécie -> alinhamento
            "00",  # alinhamento -> nome
            "Correct Name",
            "1",  # espécie; alinhamento anterior continua válido
            "1",  # espécie base/variante
            "1",  # classe
            "1",  # nível
            "1",  # pacote
            "", "", "", "", "", "",  # atributos padrão
            "4",  # não aplicar bônus
            "0",  # perícias adicionais
            "",  # equipamentos extras
            "",  # magias extras
        ]
    )
    prompts = []

    def fake_input(prompt):
        prompts.append(prompt)
        return next(responses)

    previous_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        try:
            with (
                patch("sys.argv", ["create_character.py", "--campaign", "demo"]),
                patch("builtins.input", side_effect=fake_input),
                patch("create_character.select_feats_for_level", return_value=[]),
                patch("create_character.load_species_data", return_value=race_data),
                patch("create_character.load_class_index", return_value={"fighter": "fighter.json"}),
                patch("create_character.load_class_data", return_value=class_data),
                patch("create_character.dnd_utils.load_background_data", return_value={"background": []}),
                patch("create_character.dnd_utils.load_item_data", return_value={"item": []}),
                patch("create_character.fetch_from_5etools", return_value=None),
                patch("create_character.dnd_utils.fetch_from_5etools", return_value=None),
                patch("create_character.publish_compendium_page"),
            ):
                create_character.main()

            post = frontmatter.load(
                "content/campaigns/demo/characters/correct-name.md"
            )
        finally:
            os.chdir(previous_cwd)

    assert post["title"] == "Correct Name"
    assert post["char_info"]["alignment"] == "True Neutral"
    assert sum("Nome do personagem" in prompt for prompt in prompts) == 2
    assert sum("Alinhamento" in prompt for prompt in prompts) == 2
