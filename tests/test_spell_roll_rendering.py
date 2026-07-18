import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import frontmatter


ROOT = Path(__file__).resolve().parents[1]


def write_spell(path, title, spell_info):
    post = frontmatter.Post("Descrição da magia.\n", title=title, params={"kind": "spell"})
    post["draft"] = False
    post["visibility"] = "public"
    post["spell_info"] = spell_info
    frontmatter.dump(post, path)


def test_character_spell_headers_render_only_usable_rolls():
    with tempfile.TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "project"
        project.mkdir()
        for name in ("content", "layouts", "assets", "static"):
            source = ROOT / name
            if source.exists():
                shutil.copytree(source, project / name)
        shutil.copy2(ROOT / "hugo.yaml", project / "hugo.yaml")

        spells_dir = project / "content/compendium/spells"
        write_spell(
            spells_dir / "fire-bolt.md",
            "Fire Bolt",
            {
                "level": "Cantrip",
                "level_number": 0,
                "attack_type": "ranged",
                "rolls": [
                    {
                        "kind": "damage",
                        "notation": "1d10",
                        "label": "Dano",
                        "scaling": {
                            "mode": "character_level",
                            "thresholds": {
                                "1": "1d10",
                                "5": "2d10",
                                "11": "3d10",
                                "17": "4d10",
                            },
                        },
                    }
                ],
            },
        )
        write_spell(
            spells_dir / "fireball.md",
            "Fireball",
            {
                "level": "3rd level",
                "level_number": 3,
                "rolls": [
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
                            },
                        },
                    }
                ],
            },
        )
        write_spell(
            spells_dir / "eldritch-blast.md",
            "Eldritch Blast",
            {
                "level": "Cantrip",
                "level_number": 0,
                "attack_type": "ranged",
                "rolls": [{"kind": "damage", "notation": "1d10", "label": "Dano"}],
            },
        )
        write_spell(
            spells_dir / "magic-missile.md",
            "Magic Missile",
            {
                "level": "1st level",
                "level_number": 1,
                "rolls": [
                    {"kind": "damage", "notation": "1d4+1", "label": "Dano por dardo"}
                ],
            },
        )
        write_spell(
            spells_dir / "mage-armor.md",
            "Mage Armor",
            {"level": "1st level", "level_number": 1, "rolls": []},
        )

        character_path = (
            project
            / "content/campaigns/journeys-through-the-radiant-citadel/characters/pinky.md"
        )
        character = frontmatter.load(character_path)
        character["char_info"]["level"] = 7
        character["char_info"]["spell_attack_bonus"] = 6
        character["char_info"]["spell_slots"] = {1: 4, 3: 2, 4: 1}
        refs = [
            ("Fire Bolt", "/compendium/spells/fire-bolt/", 0),
            ("Fireball", "/compendium/spells/fireball/", 3),
            ("Eldritch Blast", "/compendium/spells/eldritch-blast/", 0),
            ("Magic Missile", "/compendium/spells/magic-missile/", 1),
            ("Mage Armor", "/compendium/spells/mage-armor/", 1),
        ]
        character["char_info"]["spells"] = [
            {"name": name, "ref": ref, "level": level, "usage": "1 action"}
            for name, ref, level in refs
        ]
        character["char_info"]["class_spells"] = [ref for _, ref, _ in refs]
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

    assert html.count("Fire Bolt — Dano") == 1
    assert re.search(r'data-roll-notation="?2d10"?', html)
    assert "3d10" not in html
    assert "4d10" not in html
    assert "Fireball — Dano — slot 3" in html
    assert "Fireball — Dano — slot 4" in html
    assert re.search(r'data-roll-notation="?8d6"?', html)
    assert re.search(r'data-roll-notation="?9d6"?', html)
    assert re.search(r'data-roll-kind="?damage"?', html)
    assert re.search(r'data-roll-damage-type="?fire"?', html)
    assert "10d6" not in html
    assert "Eldritch Blast — Ataque mágico" in html
    assert re.search(r'data-roll-notation="?1d20\+6"?', html)
    assert re.search(r'data-roll-kind="?attack"?', html)
    assert re.search(r'data-roll-attack-type="?ranged"?', html)
    assert "Magic Missile — Dano por dardo" in html
    assert re.search(r'data-roll-notation="?1d4\+1"?', html)
    assert "3d4+3" not in html
    assert "Mage Armor —" not in html


def test_spell_manager_moves_existing_cards_without_rebuilding_roll_controls():
    source = (ROOT / "assets/js/spells.js").read_text(encoding="utf-8")

    assert 'getElementById("ready-spells-list")' in source
    assert 'getElementById("management-spells-list")' in source
    assert "destination.appendChild(card)" in source
    assert 'card.style.display = matchesSearch && matchesLevel ? "" : "none"' in source
    assert "document.importNode" not in source
    assert "cloneNode" not in source
    assert ".innerHTML" not in source
    assert ".outerHTML" not in source
