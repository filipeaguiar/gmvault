import shutil
import subprocess
import tempfile
from pathlib import Path

import frontmatter


ROOT = Path(__file__).resolve().parents[1]


def test_equipment_cards_distinguish_weapon_types_and_consumables():
    with tempfile.TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "project"
        project.mkdir()
        for name in ("content", "layouts", "assets", "static"):
            source = ROOT / name
            if source.exists():
                shutil.copytree(source, project / name)
        shutil.copy2(ROOT / "hugo.yaml", project / "hugo.yaml")

        potion = project / "content/compendium/items/test-healing-potion.md"
        potion.write_text(
            "---\n"
            "title: Test Healing Potion\n"
            "params:\n  kind: item\n"
            "draft: false\nvisibility: public\n"
            "item_info:\n"
            "  type: Potion\n"
            "  consumable: true\n"
            "  cost: 50 gp\n"
            "  weight: 0.5 lb\n"
            "---\n\nRecupera pontos de vida quando consumida.\n",
            encoding="utf-8",
        )
        character = (
            project
            / "content/campaigns/journeys-through-the-radiant-citadel/characters/pinky.md"
        )
        post = frontmatter.load(character)
        post["char_info"]["equipment"].append(
            {
                "name": "Test Healing Potion",
                "ref": "/compendium/items/test-healing-potion/",
                "quantity": 3,
                "equipped": False,
            }
        )
        frontmatter.dump(post, character)

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
        assert "weapon-card weapon-ranged" in html
        assert "ra-crossbow" in html
        assert "weapon-card weapon-melee" in html
        assert "ra-broadsword" in html
        assert 'data-roll-label="Ataque: Shortbow"' in html
        assert 'data-roll-label="Dano: Dagger"' in html
        assert "Acuidade" in html
        assert "consumables-section" in html
        assert "equipment-card consumable-card" in html
        assert "Quantidade: 3" in html
        assert "ra-potion" in html
        assert "equipment-card gear-card" in html
        assert "ra-round-bottom-flask" in html
