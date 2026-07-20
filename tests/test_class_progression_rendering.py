import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_class_progression_renders_structured_sections_and_subclass_links():
    with tempfile.TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "project"
        project.mkdir()
        for name in ("content", "layouts", "assets", "static"):
            source = ROOT / name
            if source.exists():
                shutil.copytree(source, project / name)
        shutil.copy2(ROOT / "hugo.yaml", project / "hugo.yaml")

        classes = project / "content/compendium/classes"
        classes.mkdir(parents=True, exist_ok=True)
        (classes / "test-class.md").write_text(
            "---\n"
            "title: Test Class\n"
            "params:\n  kind: class\n"
            "draft: false\nvisibility: public\nstatus: ready\n"
            "class_info:\n  hit_dice: d10\n  primary_ability: Strength\n"
            "---\n\n"
            "### Nível 1\n\n"
            "- [Rage](/compendium/rules/rage/)\n"
            "- [Weapon Mastery](/compendium/rules/weapon-mastery/)\n\n"
            "### Nível 2\n\n"
            "- [Reckless Attack](/compendium/rules/reckless-attack/)\n",
            encoding="utf-8",
        )
        (classes / "test-subclass.md").write_text(
            "---\n"
            "title: Test Subclass\n"
            "params:\n  kind: class\n"
            "draft: false\nvisibility: public\nstatus: ready\n"
            "parent_class: /compendium/classes/test-class/\n"
            "summary: A test subclass summary.\n"
            "---\n\nSubclass content.\n",
            encoding="utf-8",
        )

        destination = Path(temp_dir) / "public"
        subprocess.run(
            [
                "hugo",
                "--source",
                str(project),
                "--destination",
                str(destination),
                "--gc",
                "--minify",
                "--quiet",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        html = (destination / "compendium/classes/test-class/index.html").read_text(encoding="utf-8")
        assert "class-page-header" in html
        assert "class-progression-section" in html
        assert "class-progression-content" in html
        assert "Nível 1" in html
        assert "Nível 2" in html
        assert "/gmvault/compendium/rules/rage/" in html
        assert "Você pode imbuir-se" in html
        assert "Maestria em Armas" in html
        assert "subclasses-section" in html
        assert "Test Subclass" in html
        assert "A test subclass summary." in html


def test_character_class_tab_hides_future_level_progression():
    with tempfile.TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "project"
        project.mkdir()
        for name in ("content", "layouts", "assets", "static"):
            shutil.copytree(ROOT / name, project / name)
        shutil.copy2(ROOT / "hugo.yaml", project / "hugo.yaml")

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

        html = (destination / "campaigns/journeys-through-the-radiant-citadel/characters/nyx-clair/index.html").read_text(encoding="utf-8")
        class_tab = re.search(r"<div id=tab-class.*?(?=<div id=tab-features)", html, re.DOTALL).group(0)
        assert "Nível 1" in class_tab
        assert '<h2 id=nível-3>' not in class_tab
