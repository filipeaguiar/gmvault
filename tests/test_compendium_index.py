import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_compendium_index_groups_pages_and_uses_unknown_fallback():
    with __import__("tempfile").TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "project"
        project.mkdir()
        for name in ("content", "layouts", "assets", "static"):
            source = ROOT / name
            if source.exists():
                shutil.copytree(source, project / name)
        shutil.copy2(ROOT / "hugo.yaml", project / "hugo.yaml")

        fixture = project / "content/compendium/legacy-entry.md"
        fixture.write_text(
            "---\n"
            "title: Legacy Entry\n"
            "draft: false\n"
            "visibility: public\n"
            "status: ready\n"
            "---\n\n"
            "Conteúdo legado.\n",
            encoding="utf-8",
        )
        (project / "content/compendium/gm-entry.md").write_text(
            "---\n"
            "title: GM Entry\n"
            "draft: false\n"
            "visibility: gm\n"
            "status: ready\n"
            "---\n\n"
            "Conteúdo do mestre.\n",
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

        html = (destination / "compendium/index.html").read_text(encoding="utf-8")
        assert "compendium-group-title-feats" in html
        assert "compendium-group-title-rules" in html
        assert "compendium-group-title-other" in html
        assert "Legacy Entry" in html
        assert "GM Entry" not in html
        assert "/gmvault/compendium/species/goblin/" in html
