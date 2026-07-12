import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


RADIANT_CITADEL_ADVENTURE_WEIGHTS = [
    ("welcome-to-the-radiant-citadel", "Welcome to the Radiant Citadel", 10),
    ("salted-legacy", "Salted Legacy", 20),
    ("written-in-blood", "Written in Blood", 30),
    ("the-fiend-of-hollow-mine", "The Fiend of Hollow Mine", 40),
    ("wages-of-vice", "Wages of Vice", 50),
    ("sins-of-our-elders", "Sins of Our Elders", 60),
    ("gold-for-fools-and-princes", "Gold for Fools and Princes", 70),
    ("trail-of-destruction", "Trail of Destruction", 80),
    ("in-the-mists-of-manivarsha", "In the Mists of Manivarsha", 90),
    ("between-tangled-roots", "Between Tangled Roots", 100),
    ("shadow-of-the-sun", "Shadow of the Sun", 110),
    ("the-nightseas-succor", "The Nightsea's Succor", 120),
    ("buried-dynasty", "Buried Dynasty", 130),
    ("orchids-of-the-invisible-mountain", "Orchids of the Invisible Mountain", 140),
    ("beyond-the-radiant-citadel", "Beyond the Radiant Citadel", 150),
    ("the-radiant-citadel", "The Radiant Citadel", 160),
    ("credits", "Credits", 170),
]


class ChildPagesOrderTests(unittest.TestCase):
    def test_child_pages_partial_orders_by_weight_then_title(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "layouts" / "_default").mkdir(parents=True)
            (root / "layouts" / "partials" / "helpers").mkdir(parents=True)
            (root / "content" / "section").mkdir(parents=True)

            (root / "hugo.yaml").write_text(
                'baseURL: "http://example.org/"\nlanguageCode: "pt-br"\ntitle: "Order Test"\n',
                encoding="utf-8",
            )
            (root / "layouts" / "_default" / "list.html").write_text(
                '{{ partial "child_pages.html" . }}',
                encoding="utf-8",
            )
            for source, target in (
                (PROJECT_ROOT / "layouts" / "partials" / "child_pages.html", root / "layouts" / "partials" / "child_pages.html"),
                (PROJECT_ROOT / "layouts" / "partials" / "helpers" / "kind.html", root / "layouts" / "partials" / "helpers" / "kind.html"),
                (PROJECT_ROOT / "layouts" / "partials" / "helpers" / "visibility.html", root / "layouts" / "partials" / "helpers" / "visibility.html"),
            ):
                shutil.copyfile(source, target)

            (root / "content" / "section" / "_index.md").write_text(
                "---\ntitle: Section\nvisibility: gm\n---\n",
                encoding="utf-8",
            )
            for slug, title, weight in (
                ("zulu", "Zulu", 20),
                ("alpha", "Alpha", 20),
                ("middle", "Middle", 10),
            ):
                page = root / "content" / "section" / slug
                page.mkdir()
                (page / "_index.md").write_text(
                    f'---\ntitle: "{title}"\nparams:\n  kind: "adventure"\nweight: {weight}\nvisibility: "gm"\n---\n',
                    encoding="utf-8",
                )

            public = root / "public"
            subprocess.run(
                ["hugo", "--source", str(root), "--destination", str(public), "--quiet"],
                check=True,
            )
            html = (public / "section" / "index.html").read_text(encoding="utf-8")
            titles = [
                match.strip()
                for match in re.findall(r'<i class="ra [^"]+"[^>]*></i>\s*([^<]+?)\s*</a>', html, re.S)
            ]

        self.assertEqual(titles, ["Middle", "Alpha", "Zulu"])

    def test_radiant_citadel_adventure_indexes_have_editorial_weights(self):
        root = PROJECT_ROOT / "content" / "campaigns" / "journeys-through-the-radiant-citadel" / "adventures"

        for slug, title, weight in RADIANT_CITADEL_ADVENTURE_WEIGHTS:
            path = root / slug / "_index.md"
            self.assertTrue(path.is_file(), f"Índice ausente: {path}")
            front_matter = path.read_text(encoding="utf-8").split("---", 2)[1]
            data = yaml.safe_load(front_matter)
            self.assertEqual(data.get("title"), title)
            self.assertEqual(data.get("weight"), weight, f"weight incorreto em {path}")


if __name__ == "__main__":
    unittest.main()
