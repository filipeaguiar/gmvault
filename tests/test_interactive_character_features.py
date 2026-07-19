import unittest
from unittest.mock import patch
import os
import shutil
from pathlib import Path
import create_character

class TestCreateCharacterFeatures(unittest.TestCase):
    def setUp(self):
        self.char_slug = "test-class-features-character"
        self.output_path = f"content/campaigns/journeys-through-the-radiant-citadel/characters/{self.char_slug}.md"
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    @patch("create_character.ask")
    @patch("create_character.ask_int")
    @patch("create_character.ask_choice")
    @patch("create_character.ask_multiple_feat_choices")
    @patch("create_character.ask_manual_feats")
    def test_create_rogue_thief_level_3(self, mock_ask_manual_feats, mock_ask_multiple, mock_ask_choice, mock_ask_int, mock_ask):
        mock_ask_manual_feats.return_value = []
        mock_ask_multiple.return_value = []
        # Setup mocked inputs
        # 1. Campanha
        # 2. Nome do personagem
        # 3. Alinhamento
        # 4. Espécie Base
        # 5. Variante/Subespécie
        # 6. Classe
        # 7. Nível
        # 8. Subclasse
        # 9. Atributos base (str, dex, con, int, wis, cha)
        # 10. Bônus rule
        # 11. Perícias (skills)
        # 12. Perícias adicionais
        # 13. Especialização (expertise)
        # 14. Saves da classe (str, dex, con, int, wis, cha)
        
        # We need to map options to labels
        def mock_ask_choice_side_effect(prompt, options):
            prompt_lower = prompt.lower()
            if "campanha" in prompt_lower:
                return "journeys-through-the-radiant-citadel"
            elif "espécie base" in prompt_lower:
                return next(o for o in options if "human" in o.lower())
            elif "variante" in prompt_lower:
                return next(o for o in options if "espécie base" in str(o[0]).lower())
            elif "classe principal" in prompt_lower:
                return "Rogue"
            elif "subclasse" in prompt_lower:
                # options could be a list of strings or tuples, handle both
                for o in options:
                    o_str = str(o[0]).lower() if isinstance(o, tuple) else str(o).lower()
                    if "thief" in o_str:
                        return o
                return options[0]
            elif "aumentos de atributos" in prompt_lower:
                return "Não aplicar aumentos (manter atributos base secos)"
            else:
                return options[0]

        mock_ask_choice.side_effect = mock_ask_choice_side_effect

        def mock_ask_int_side_effect(prompt, default=0):
            prompt_lower = prompt.lower()
            if "nível" in prompt_lower:
                return 3
            elif "adicionais" in prompt_lower:
                return 0 # no extra skills
            else:
                return 10 # stats base

        mock_ask_int.side_effect = mock_ask_int_side_effect

        mock_ask_calls = []
        def mock_ask_side_effect(prompt, default=None):
            mock_ask_calls.append(prompt)
            prompt_lower = prompt.lower()
            if "nome do personagem" in prompt_lower:
                return "Test Class Features Character"
            elif "alinhamento" in prompt_lower:
                return "True Neutral"
            elif "perícias" in prompt_lower:
                return "1,2,3,4" # Rogue level 1 requires 4 skills
            elif "especialização" in prompt_lower:
                return "1,2" # Rogue level 1 requires 2 expertises
            elif "save" in prompt_lower:
                # rogue is dex and int
                if "dex" in prompt_lower or "int" in prompt_lower:
                    return "s"
                return "n"
            return default or ""

        mock_ask.side_effect = mock_ask_side_effect

        # Run creation main
        with patch("sys.argv", ["create_character.py"]):
            create_character.main()

        # Assertions
        self.assertTrue(os.path.exists(self.output_path), "Ficha do personagem deveria ter sido gerada.")
        
        with open(self.output_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check frontmatter contents
        self.assertIn("title: \"Test Class Features Character\"", content)
        self.assertIn("class: \"Rogue\"", content)
        self.assertIn("class_level: 3", content)
        self.assertIn("subclass: \"Thief\"", content)
        
        # Check that Thief/Rogue level 3 features are present in actions
        # Rogue level 1: Sneak Attack, Expertise
        # Rogue level 2: Cunning Action
        # Thief level 3: Fast Hands, Second-Story Work
        self.assertIn("name: Sneak Attack", content)
        self.assertIn("name: Cunning Action", content)
        self.assertIn("name: Fast Hands", content)
        self.assertIn("name: Second-Story Work", content)
        
        # Check Sneak Attack formula extraction (2d6 for level 3)
        self.assertIn("roll: 2d6", content)
        
        # Check compendium references
        self.assertIn("/compendium/rules/sneak-attack/", content)
        self.assertIn("/compendium/rules/cunning-action/", content)
        self.assertIn("/compendium/rules/fast-hands/", content)

if __name__ == "__main__":
    unittest.main()
