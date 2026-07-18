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
        assert "Legacy Entry" in html
        assert "GM Entry" not in html


def test_compendium_legacy_descriptions_render_markdown_links():
    with __import__("tempfile").TemporaryDirectory() as temp_dir:
        project = Path(temp_dir) / "project"
        project.mkdir()
        for name in ("content", "layouts", "assets", "static"):
            source = ROOT / name
            if source.exists():
                shutil.copytree(source, project / name)
        shutil.copy2(ROOT / "hugo.yaml", project / "hugo.yaml")

        (project / "layouts/_default").mkdir(parents=True, exist_ok=True)
        (project / "layouts/_default/single.html").write_text(
            "<!doctype html><html><body>"
            '{{ partial "helpers/compendium-content.html" (dict "name" .Title "legacy" .Params.legacy_description) }}'
            "</body></html>",
            encoding="utf-8",
        )

        fixture = project / "content/legacy-link.md"
        fixture.write_text(
            "---\n"
            "title: Legacy Link\n"
            "draft: false\n"
            "legacy_description: '[Guia](https://example.com)'\n"
            "---\n\n"
            "\n",
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

        html = (destination / "legacy-link/index.html").read_text(encoding="utf-8")
        assert '<a href=https://example.com>Guia</a>' in html
        assert "[Guia](https://example.com)" not in html
