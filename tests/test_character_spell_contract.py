from pathlib import Path
import shutil
import subprocess
from unittest.mock import patch

import frontmatter

import create_character
import dnd_utils


def test_spell_profile_marks_prepared_and_known_entries():
    profile = dnd_utils.infer_spellcasting_profile(
        "Cleric",
        level=3,
        spell_slots={1: 4, 2: 2},
        spells=[
            {"name": "Healing Word", "ref": "/compendium/spells/healing-word/", "level": 1, "prepared": True},
            {"name": "Guidance", "ref": "/compendium/spells/guidance/", "level": 0, "known": True},
        ],
        class_spells=["/compendium/spells/healing-word/"],
    )
    assert profile["kind"] == "prepared"
    assert profile["uses_pact_slots"] is False


def test_spell_profile_marks_pact_magic():
    profile = dnd_utils.infer_spellcasting_profile(
        "Warlock",
        level=5,
        spell_slots={2: 2},
        spells=[
            {"name": "Eldritch Blast", "ref": "/compendium/spells/eldritch-blast/", "level": 0, "known": True},
        ],
        class_spells=["/compendium/spells/eldritch-blast/"],
    )
    assert profile["kind"] == "pact"
    assert profile["uses_pact_slots"] is True


def test_create_character_persists_spell_entries_with_refs(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "content/campaigns/demo/characters").mkdir(parents=True)
    (tmp_path / "content/compendium/spells").mkdir(parents=True)
    (tmp_path / "content/compendium/rules").mkdir(parents=True)

    race_data = {"race": [{"name": "Human", "source": "PHB", "size": ["M"], "speed": 30}], "subrace": []}
    class_data = {
        "class": [{"name": "Cleric", "source": "PHB", "hd": {"faces": 8}, "startingProficiencies": {"skills": [{"choose": {"count": 2, "from": ["insight", "religion"]}}]}}],
        "classFeature": [],
    }

    inputs = iter([
        "demo",
        "Character Name",
        "Neutral Good",
        "Human",
        "Espécie Base",
        "Cleric",
        "3",
        "Nenhuma",
        "10", "10", "10", "10", "10", "10",
        "Usar padrão da espécie (se houver)",
        "1,2",
        "0",
        "",
        "Healing Word",
        "",
    ])

    def fake_input(prompt=""):
        return next(inputs)

    with patch("builtins.input", side_effect=fake_input), \
         patch("sys.argv", ["create_character.py", "--campaign", "demo"]), \
         patch("create_character.load_species_data", return_value=race_data), \
         patch("create_character.load_class_index", return_value={"cleric": "cleric.json"}), \
         patch("create_character.load_class_data", return_value=class_data), \
         patch("create_character.dnd_utils.load_background_data", return_value={"background": []}), \
         patch("create_character.dnd_utils.load_item_data", return_value={"item": []}), \
         patch("create_character.fetch_from_5etools", return_value="/compendium/spells/healing-word/"), \
         patch("create_character.dnd_utils.fetch_from_5etools", return_value="/compendium/spells/healing-word/"), \
         patch("create_character.publish_compendium_page"), \
         patch("create_character.ensure_compendium_class_overview"), \
         patch("create_character.prompt_choices_for_feature", return_value=[]), \
         patch("create_character.select_feats_for_level", return_value=[]), \
         patch("create_character.ask_choice", side_effect=lambda prompt, options: options[0] if options else ""):
        create_character.main()

    post = frontmatter.load(tmp_path / "content/campaigns/demo/characters/demo.md")
    assert isinstance(post["char_info"]["spells"], list)
    assert post["char_info"]["spells"]
    assert post["char_info"]["spells"][0]["ref"].startswith("/compendium/spells/")
    assert "spellcasting" in post["char_info"]


def test_non_spellcaster_hides_grimoire_tab(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()
    for name in ("content", "layouts", "assets", "static"):
        source = Path(__file__).resolve().parents[1] / name
        if source.exists():
            shutil.copytree(source, project / name)
    shutil.copy2(Path(__file__).resolve().parents[1] / "hugo.yaml", project / "hugo.yaml")

    character_path = project / "content/campaigns/journeys-through-the-radiant-citadel/characters/pinky.md"
    character = frontmatter.load(character_path)
    character["char_info"]["spells"] = []
    character["char_info"]["class_spells"] = []
    frontmatter.dump(character, character_path)

    destination = tmp_path / "public"
    subprocess.run(
        ["hugo", "--source", str(project), "--destination", str(destination), "-D", "--gc", "--minify", "--quiet"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    html = (destination / "campaigns/journeys-through-the-radiant-citadel/characters/pinky/index.html").read_text(encoding="utf-8")
    assert 'id=tab-grimoire' not in html
