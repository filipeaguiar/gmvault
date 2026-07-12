import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


class CampaignIntroductionRenderingTests(unittest.TestCase):
    def build_site(self, content: dict[str, str]) -> str:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "site"
            dest = Path(temp_dir) / "public"
            root.mkdir()
            shutil.copytree("layouts", root / "layouts")
            shutil.copytree("assets", root / "assets")
            (root / "hugo.yaml").write_text(
                "baseURL: https://example.com/gmvault/\ntitle: Test Vault\n",
                encoding="utf-8",
            )
            for relative, text in content.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")
            subprocess.run(
                ["hugo", "--source", str(root), "--destination", str(dest), "--quiet"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return (dest / "campaigns/demo/index.html").read_text(encoding="utf-8")

    def test_campaign_renders_intro_child_before_adventure_grid_and_filters_card(self):
        html = self.build_site(
            {
                "content/campaigns/demo/_index.md": """
                ---
                title: Demo Campaign
                params:
                  kind: campaign
                draft: false
                ---
                Campaign body.
                """,
                "content/campaigns/demo/adventures/_index.md": """
                ---
                title: Adventures
                draft: false
                ---
                """,
                "content/campaigns/demo/adventures/intro/_index.md": """
                ---
                title: Intro Fragment
                weight: 10
                params:
                  kind: adventure
                  content_role: introduction
                draft: false
                ---
                Intro body appears here.
                """,
                "content/campaigns/demo/adventures/play/_index.md": """
                ---
                title: Play Adventure
                weight: 20
                params:
                  kind: adventure
                draft: false
                ---
                Play body.
                """,
            }
        )

        self.assertIn("Intro body appears here", html)
        self.assertLess(html.index("Intro body appears here"), html.index("Aventuras / Arcos de Jogo"))
        self.assertIn("Play Adventure", html)
        self.assertNotIn("Intro Fragment</a>", html)

    def test_campaign_intro_fragments_are_sorted_by_weight_then_title(self):
        html = self.build_site(
            {
                "content/campaigns/demo/_index.md": """
                ---
                title: Demo Campaign
                params:
                  kind: campaign
                draft: false
                ---
                """,
                "content/campaigns/demo/adventures/_index.md": "---\ntitle: Adventures\ndraft: false\n---\n",
                "content/campaigns/demo/adventures/b/_index.md": """
                ---
                title: Beta Intro
                weight: 10
                params:
                  kind: adventure
                  content_role: introduction
                draft: false
                ---
                Beta body.
                """,
                "content/campaigns/demo/adventures/a/_index.md": """
                ---
                title: Alpha Intro
                weight: 10
                params:
                  kind: adventure
                  content_role: introduction
                draft: false
                ---
                Alpha body.
                """,
            }
        )

        self.assertLess(html.index("Alpha body."), html.index("Beta body."))


if __name__ == "__main__":
    unittest.main()
