import unittest

from import_dndbeyond import STANDARD_ACTION_REFS


class ImportDndBeyondTests(unittest.TestCase):
    def test_standard_actions_are_referential(self):
        self.assertEqual(len(STANDARD_ACTION_REFS), 7)
        for ref in STANDARD_ACTION_REFS.values():
            self.assertTrue(ref.startswith("/compendium/rules/"))
            self.assertNotIn("description", ref)


if __name__ == "__main__":
    unittest.main()
