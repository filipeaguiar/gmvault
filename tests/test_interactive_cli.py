import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from interactive_cli import campaign_menu, main, translation_menu


class InteractiveMenuTests(unittest.TestCase):
    def test_create_character_script_invokes_its_cli_entrypoint(self):
        script = Path(__file__).resolve().parents[1] / "create_character.py"
        completed = subprocess.run(
            [sys.executable, str(script), "--help"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Criação de personagem", completed.stdout)
        self.assertIn("--menu", completed.stdout)

    @patch("interactive_cli.subprocess.run")
    @patch("interactive_cli.Prompt.ask", side_effect=["2", "0"])
    def test_launcher_delegates_to_selected_script(self, _prompt, run):
        run.return_value.returncode = 0
        self.assertEqual(main(), 0)
        command = run.call_args.args[0]
        self.assertTrue(command[1].endswith("create_character.py"))
        self.assertEqual(command[2], "--menu")

    @patch("interactive_cli.subprocess.run")
    @patch("interactive_cli.Prompt.ask", side_effect=["3", "0"])
    def test_launcher_delegates_to_character_editor(self, _prompt, run):
        run.return_value.returncode = 0
        self.assertEqual(main(), 0)
        command = run.call_args.args[0]
        self.assertTrue(command[1].endswith("edit_character.py"))
        self.assertEqual(command[2], "--menu")

    @patch("interactive_cli.subprocess.run")
    @patch("interactive_cli.Prompt.ask", side_effect=["2", "", "0"])
    def test_launcher_waits_before_clearing_failed_operation(self, prompt, run):
        run.return_value.returncode = 1
        self.assertEqual(main(), 0)
        self.assertIn(
            "Pressione Enter para voltar ao menu principal",
            prompt.call_args_list[1].args[0],
        )

    @patch("interactive_cli.Prompt.ask", return_value="0")
    def test_launcher_can_exit(self, _prompt):
        self.assertEqual(main(), 0)

    @patch("interactive_cli._summary", return_value=True)
    @patch("interactive_cli.Prompt.ask", side_effect=["jttrc"])
    def test_campaign_menu_maps_slug(self, _prompt, _summary):
        self.assertEqual(campaign_menu(), {"slug": "jttrc"})

    @patch("interactive_cli._summary", return_value=True)
    @patch(
        "interactive_cli._numbered_choice",
        side_effect=[
            {"scope": "campaign", "campaign": "jttrc"},
            {
                "profile": "deepseek-v4-pro",
                "engine": "openai-compatible",
                "model": "deepseek-v4-pro",
                "base_url": "https://api.deepseek.com/v1",
                "timeout": 300.0,
            },
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
        self.assertEqual(result["model"], "deepseek-v4-pro")
        self.assertEqual(result["profile"], "deepseek-v4-pro")

    @patch("interactive_cli._summary", return_value=False)
    @patch("interactive_cli.Prompt.ask", side_effect=["jttrc"])
    def test_cancel_returns_none(self, _prompt, _summary):
        self.assertIsNone(campaign_menu())


if __name__ == "__main__":
    unittest.main()
