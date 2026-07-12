import json
import tempfile
import unittest
from pathlib import Path

from translate_drafts import TranslationError, load_glossary


class TranslationGlossaryTests(unittest.TestCase):
    def write_glossary(self, payload: object) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "glossary.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_loads_versioned_categorized_glossary(self) -> None:
        path = self.write_glossary(
            {
                "schema_version": 2,
                "locale": "pt-BR",
                "required_translations": {
                    "mechanics": {
                        "saving throw": "teste de resistência",
                        "attack roll": "jogada de ataque",
                    },
                    "skills": {"Perception": "Percepção"},
                },
                "protected_terms": ["Kasem Aroon"],
                "contextual_terms": {
                    "check": {
                        "note": "Traduzir conforme a construção mecânica.",
                        "preferred": ["teste", "verificação"],
                    }
                },
                "forbidden_outputs": ["Salvaguarda"],
            }
        )

        glossary = load_glossary(path)

        self.assertEqual(glossary["saving throw"], "teste de resistência")
        self.assertEqual(glossary["attack roll"], "jogada de ataque")
        self.assertEqual(glossary["Perception"], "Percepção")
        self.assertNotIn("Kasem Aroon", glossary)

    def test_rejects_duplicate_source_terms_across_categories(self) -> None:
        path = self.write_glossary(
            {
                "schema_version": 2,
                "locale": "pt-BR",
                "required_translations": {
                    "mechanics": {"check": "teste"},
                    "editorial": {"check": "verificação"},
                },
                "protected_terms": [],
                "contextual_terms": {},
                "forbidden_outputs": [],
            }
        )

        with self.assertRaisesRegex(TranslationError, "duplicado.*check"):
            load_glossary(path)

    def test_project_glossary_is_extensive_and_uses_ptbr_mechanics(self) -> None:
        glossary_path = Path(__file__).resolve().parents[1] / "translation_glossary.json"
        payload = json.loads(glossary_path.read_text(encoding="utf-8"))
        glossary = load_glossary(glossary_path)

        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["locale"], "pt-BR")
        self.assertGreaterEqual(len(glossary), 250)
        self.assertEqual(glossary["Saving Throw"], "Teste de Resistência")
        self.assertEqual(glossary["Death Saving Throw"], "Teste de Resistência contra a Morte")
        self.assertIn("Dyn Singh Night Market", payload["protected_terms"])
        self.assertIn("Salvaguarda", payload["forbidden_outputs"])


if __name__ == "__main__":
    unittest.main()
