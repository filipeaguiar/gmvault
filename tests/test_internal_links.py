import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.check_internal_links import audit_public_dir


class InternalLinkAuditTests(unittest.TestCase):
    def test_fixture_classifies_internal_link_errors(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            public = Path(temp_dir)
            (public / "campaigns/demo").mkdir(parents=True)
            (public / "campaigns/demo/index.html").write_text(
                textwrap.dedent(
                    """
                    <html><body>
                      <h2 id="ok">Ok</h2>
                      <a href="/gmvault/campaigns/demo/#ok">valid</a>
                      <a href="/campaigns/demo/">outside base</a>
                      <a href="/gmvault/campaigns/missing/">missing page</a>
                      <a href="/gmvault/campaigns/demo/#missing">missing anchor</a>
                      <a href="">empty link</a>
                      <img src="/gmvault/images/missing.webp">
                      <a href="https://example.com/outside">external</a>
                    </body></html>
                    """
                ),
                encoding="utf-8",
            )

            findings = audit_public_dir(
                public,
                "https://filipeaguiar.github.io/gmvault/",
                scope="campaigns/demo/",
                include_external=True,
            )

            by_kind = {}
            for finding in findings:
                by_kind.setdefault(finding.kind, []).append(finding)
            self.assertNotIn("missing-file", [f.kind for f in findings if f.target.endswith("#ok")])
            self.assertEqual(len(by_kind["outside-base-path"]), 1)
            self.assertEqual(len([f for f in by_kind["missing-file"] if f.attribute == "href"]), 1)
            self.assertEqual(len([f for f in by_kind["missing-file"] if f.attribute == "src"]), 1)
            self.assertEqual(len(by_kind["missing-anchor"]), 1)
            self.assertEqual(len(by_kind["empty-target"]), 1)
            self.assertEqual(len(by_kind["external"]), 1)


    def test_radiant_campaign_quick_links_include_base_path_in_hugo_build(self):
        with tempfile.TemporaryDirectory() as dest:
            subprocess.run(
                ["hugo", "--destination", dest, "--quiet"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            html = (
                Path(dest)
                / "campaigns/journeys-through-the-radiant-citadel/index.html"
            ).read_text(encoding="utf-8")

        self.assertIn('/gmvault/campaigns/journeys-through-the-radiant-citadel/journal/', html)
        self.assertIn('/gmvault/campaigns/journeys-through-the-radiant-citadel/adventures/', html)
        self.assertNotIn('href="/campaigns/journeys-through-the-radiant-citadel/journal/"', html)
        self.assertNotIn('href="/campaigns/journeys-through-the-radiant-citadel/adventures/"', html)


if __name__ == "__main__":
    unittest.main()
