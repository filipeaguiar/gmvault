import tempfile
import unittest
from pathlib import Path

from content_roles import CONTENT_ROLE_INTRODUCTION
from import_campaign import (
    assign_import_weights,
    existing_content_role,
    front_matter_content_role_lines,
    imported_scene_content_role,
)


class ImportCampaignContentRoleTests(unittest.TestCase):
    def test_assigns_explicit_weights_by_input_order(self):
        entries = [{"name": "Intro"}, {"name": "Salted Legacy"}, {"name": "Written in Blood"}]

        weighted = assign_import_weights(entries)

        self.assertEqual([item["weight"] for item in weighted], [10, 20, 30])

    def test_campaign_intro_chapter_and_adventure_intro_sections_are_classified(self):
        self.assertEqual(
            imported_scene_content_role("Welcome to the Radiant Citadel", level="campaign_chapter"),
            CONTENT_ROLE_INTRODUCTION,
        )
        self.assertEqual(
            imported_scene_content_role("Background", level="adventure_section"),
            CONTENT_ROLE_INTRODUCTION,
        )
        self.assertEqual(
            imported_scene_content_role("Adventure Hook", level="adventure_section"),
            CONTENT_ROLE_INTRODUCTION,
        )
        self.assertIsNone(imported_scene_content_role("Welcome to the Market", level="adventure_section"))

    def test_front_matter_lines_persist_role_under_params(self):
        lines = front_matter_content_role_lines(CONTENT_ROLE_INTRODUCTION)

        self.assertEqual(lines, ['  content_role: "introduction"'])

    def test_existing_manual_role_is_preserved_for_idempotent_reimport(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "scene.md"
            path.write_text(
                "---\ntitle: Manual\nparams:\n  kind: scene\n  content_role: introduction\n---\n\nBody\n",
                encoding="utf-8",
            )

            self.assertEqual(existing_content_role(path), CONTENT_ROLE_INTRODUCTION)


if __name__ == "__main__":
    unittest.main()
