import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


class AdventureIntroductionRenderingTests(unittest.TestCase):
    def build_adventure(self, content: dict[str, str]) -> str:
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
            base = {
                "content/campaigns/demo/_index.md": """
                ---
                title: Demo Campaign
                params:
                  kind: campaign
                draft: false
                ---
                """,
                "content/campaigns/demo/adventures/_index.md": "---\ntitle: Adventures\ndraft: false\n---\n",
                "content/campaigns/demo/adventures/quest/_index.md": """
                ---
                title: Quest
                params:
                  kind: adventure
                draft: false
                ---
                Adventure body.
                """,
                "content/campaigns/demo/adventures/quest/001-start/_index.md": """
                ---
                title: Session 01
                weight: 10
                params:
                  kind: session
                draft: false
                ---
                Session body.
                """,
            }
            base.update(content)
            for relative, text in base.items():
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
            return (dest / "campaigns/demo/adventures/quest/index.html").read_text(encoding="utf-8")

    def test_adventure_renders_nested_intro_scenes_before_sessions_and_filters_cards(self):
        html = self.build_adventure(
            {
                "content/campaigns/demo/adventures/quest/001-start/01-background.md": """
                ---
                title: Background
                weight: 10
                params:
                  kind: scene
                  content_role: introduction
                draft: false
                ---
                Background intro text.
                """,
                "content/campaigns/demo/adventures/quest/001-start/02-play.md": """
                ---
                title: Play Scene
                weight: 20
                params:
                  kind: scene
                draft: false
                ---
                Play scene text.
                """,
            }
        )

        self.assertIn("Background intro text.", html)
        self.assertLess(html.index("Background intro text."), html.index("Cronograma de Sessões"))
        self.assertIn("Session 01", html)
        self.assertNotIn("Background</a>", html)

    def test_adventure_intro_fragments_are_sorted_by_weight_then_title(self):
        html = self.build_adventure(
            {
                "content/campaigns/demo/adventures/quest/001-start/02-beta.md": """
                ---
                title: Beta
                weight: 10
                params:
                  kind: scene
                  content_role: introduction
                draft: false
                ---
                Beta intro.
                """,
                "content/campaigns/demo/adventures/quest/001-start/01-alpha.md": """
                ---
                title: Alpha
                weight: 10
                params:
                  kind: scene
                  content_role: introduction
                draft: false
                ---
                Alpha intro.
                """,
            }
        )

        self.assertLess(html.index("Alpha intro."), html.index("Beta intro."))


if __name__ == "__main__":
    unittest.main()
