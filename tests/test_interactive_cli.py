import unittest
from unittest.mock import patch

from interactive_cli import (
    campaign_menu,
    dndbeyond_menu,
    main,
    translation_menu,
)


class InteractiveMenuTests(unittest.TestCase):
    @patch("interactive_cli.subprocess.run")
    @patch("interactive_cli.Prompt.ask", return_value="2")
    def test_launcher_delegates_to_selected_script(self, _prompt, run):
        run.return_value.returncode = 0
        self.assertEqual(main(), 0)
        command = run.call_args.args[0]
        self.assertTrue(command[1].endswith("import_dndbeyond.py"))
        self.assertEqual(command[2], "--menu")

    @patch("interactive_cli.Prompt.ask", return_value="0")
    def test_launcher_can_exit(self, _prompt):
        self.assertEqual(main(), 0)

    @patch("interactive_cli._summary", return_value=True)
    @patch("interactive_cli.Prompt.ask", side_effect=["jttrc"])
    def test_campaign_menu_maps_slug(self, _prompt, _summary):
        self.assertEqual(campaign_menu(), {"slug": "jttrc"})

    @patch("interactive_cli._summary", return_value=True)
    @patch("interactive_cli._numbered_choice", return_value="cidadela-radiante")
    @patch("interactive_cli.Prompt.ask", return_value="168106464")
    def test_dndbeyond_menu_maps_character_and_campaign(self, _prompt, _choice, _summary):
        self.assertEqual(
            dndbeyond_menu(),
            {"char_id": "168106464", "campaign": "cidadela-radiante"},
        )

    @patch("interactive_cli._summary", return_value=True)
    @patch(
        "interactive_cli._numbered_choice",
        side_effect=[
            {"scope": "campaign", "campaign": "jttrc"},
            4,
            False,
            False,
            True,
        ],
    )
    def test_translation_menu_maps_options(self, _choice, _summary):
        result = translation_menu()
        self.assertEqual(result["scope"], "campaign")
        self.assertEqual(result["campaign"], "jttrc")
        self.assertEqual(result["jobs"], 4)
        self.assertFalse(result["apply"])

    @patch("interactive_cli._summary", return_value=False)
    @patch("interactive_cli.Prompt.ask", side_effect=["jttrc"])
    def test_cancel_returns_none(self, _prompt, _summary):
        self.assertIsNone(campaign_menu())


if __name__ == "__main__":
    unittest.main()
