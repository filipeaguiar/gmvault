import unittest
import os
import tempfile
import sys

# Adicionar a raiz e a pasta scripts ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from sync_character import parse_markdown_file, save_markdown_file

class TestSyncCharacter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file_path = os.path.join(self.temp_dir.name, "test_character.md")
        
        self.initial_content = """---
title: "Test Hero"
char_info:
  ac: 15
  hp: 20
  spells:
    - name: "Fireball"
compendium_refs: []
---
Este é o corpo inicial do personagem.
Contém notas do mestre e biografia.
"""
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write(self.initial_content)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_markdown_file(self):
        frontmatter, body = parse_markdown_file(self.test_file_path)
        
        self.assertEqual(frontmatter["title"], "Test Hero")
        self.assertEqual(frontmatter["char_info"]["ac"], 15)
        self.assertEqual(frontmatter["char_info"]["spells"][0]["name"], "Fireball")
        self.assertIn("Este é o corpo inicial do personagem.", body)
        self.assertIn("Contém notas do mestre e biografia.", body)

    def test_save_markdown_file_preserves_body(self):
        frontmatter, body = parse_markdown_file(self.test_file_path)
        
        # Modificar frontmatter
        frontmatter["char_info"]["ac"] = 18
        frontmatter["compendium_refs"] = ["/compendium/spells/fireball/"]
        
        save_markdown_file(self.test_file_path, frontmatter, body)
        
        # Recarregar e verificar
        new_frontmatter, new_body = parse_markdown_file(self.test_file_path)
        self.assertEqual(new_frontmatter["char_info"]["ac"], 18)
        self.assertEqual(new_frontmatter["compendium_refs"][0], "/compendium/spells/fireball/")
        self.assertEqual(new_body, body)

if __name__ == "__main__":
    unittest.main()
