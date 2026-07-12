import unittest

from content_roles import (
    CONTENT_ROLE_INTRODUCTION,
    classify_imported_content_role,
    content_role_from_front_matter,
    is_introduction_role,
)


class ContentRoleTests(unittest.TestCase):
    def test_reads_introduction_from_top_level_or_params_front_matter(self):
        self.assertEqual(
            content_role_from_front_matter({"content_role": "introduction"}),
            CONTENT_ROLE_INTRODUCTION,
        )
        self.assertEqual(
            content_role_from_front_matter({"params": {"content_role": "introduction"}}),
            CONTENT_ROLE_INTRODUCTION,
        )

    def test_missing_or_unknown_role_is_normal_content(self):
        self.assertIsNone(content_role_from_front_matter({}))
        self.assertIsNone(content_role_from_front_matter({"params": {"content_role": "sidebar"}}))
        self.assertFalse(is_introduction_role(None))
        self.assertFalse(is_introduction_role("sidebar"))

    def test_import_heuristics_mark_only_editorial_introductions(self):
        self.assertEqual(
            classify_imported_content_role("Welcome to the Radiant Citadel", level="campaign_chapter"),
            CONTENT_ROLE_INTRODUCTION,
        )
        self.assertEqual(
            classify_imported_content_role("Adventure Background", level="adventure_section"),
            CONTENT_ROLE_INTRODUCTION,
        )
        self.assertEqual(
            classify_imported_content_role("Running the Adventure", level="adventure_section"),
            CONTENT_ROLE_INTRODUCTION,
        )
        self.assertIsNone(classify_imported_content_role("Market Games", level="adventure_section"))
        self.assertIsNone(classify_imported_content_role("A1. Guard Room", level="adventure_section"))


if __name__ == "__main__":
    unittest.main()
