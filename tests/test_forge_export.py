import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


FORGE_EXPORT = "exports/forge/statblocks.json"
CAMPAIGN = "campaigns/journeys-through-the-radiant-citadel"


class ForgeExportTests(unittest.TestCase):
    def _build(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        subprocess.run(
            ["hugo", "--destination", temp_dir.name, "--quiet"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        destination = Path(temp_dir.name)
        records = json.loads(
            (destination / FORGE_EXPORT).read_text(encoding="utf-8")
        )
        return destination, records

    def test_export_contains_characters_monsters_and_pinky_metadata(self):
        _, records = self._build()
        party_records = [
            record
            for record in records
            if record["metadata"]["com.battle-system.forge/in-party"]
        ]
        monster_records = [
            record
            for record in records
            if not record["metadata"]["com.battle-system.forge/in-party"]
        ]
        pinky = next(record for record in records if record["name"] == "Pinky")

        self.assertEqual(len(party_records), 6)
        self.assertEqual(len(monster_records), 131)
        self.assertEqual(records[:6], party_records)
        self.assertTrue(any(record["name"] in {"gato", "cat"} for record in monster_records))
        self.assertEqual(pinky["metadata"]["com.battle-system.forge/Z001"], 2)
        self.assertEqual(pinky["metadata"]["com.battle-system.forge/Z004"], "Goblinoide")
        self.assertEqual(pinky["metadata"]["com.battle-system.forge/Z005"], 14)
        self.assertEqual(pinky["metadata"]["com.battle-system.forge/Z007"], 16)
        self.assertEqual(pinky["metadata"]["com.battle-system.forge/Z017"], 10)
        self.assertEqual(pinky["metadata"]["com.battle-system.forge/Z018"], 20)
        inventory_names = {
            item["name"]
            for item in pinky["metadata"]["com.battle-system.forge/Z040"]
        }
        self.assertIn("Arco Curto", inventory_names)
        self.assertIn("Espada Curta", inventory_names)

    def test_export_has_valid_unique_ids_and_stable_order(self):
        _, first = self._build()
        _, second = self._build()
        ids = [record["id"] for record in first]

        self.assertEqual(first, second)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(re.fullmatch(r"[0-9a-f-]{36}", value) for value in ids))
        self.assertTrue(
            all(
                record["metadata"]["com.battle-system.forge/in-party"]
                for record in first[:6]
            )
        )
        self.assertFalse(
            any(
                record["metadata"]["com.battle-system.forge/in-party"]
                for record in first[6:]
            )
        )

    def test_export_links_are_rendered(self):
        destination, _ = self._build()
        compendium_html = (destination / "compendium/index.html").read_text(
            encoding="utf-8"
        )
        campaign_html = (
            destination / f"{CAMPAIGN}/index.html"
        ).read_text(encoding="utf-8")

        forge_url = (
            "https://filipeaguiar.github.io/gmvault/exports/forge/statblocks.json"
        )
        campaign_url = (
            "https://filipeaguiar.github.io/gmvault/"
            "campaigns/journeys-through-the-radiant-citadel/gm-vault.json"
        )
        self.assertIn(f'data-copy-url="{forge_url}"', compendium_html)
        self.assertIn("Copiar URL do Forge!", compendium_html)
        self.assertIn("navigator.clipboard.writeText", compendium_html)
        self.assertNotIn(">" + forge_url + "</code>", compendium_html)
        self.assertIn(f'data-copy-url="{campaign_url}"', campaign_html)
        self.assertIn("Copiar URL do GM Vault", campaign_html)
        self.assertIn("navigator.clipboard.writeText", campaign_html)
        self.assertNotIn(">" + campaign_url + "</code>", campaign_html)


if __name__ == "__main__":
    unittest.main()
