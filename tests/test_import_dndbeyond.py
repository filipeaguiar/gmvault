import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import yaml

from dnd_utils import dump_yaml_indented, fetch_from_5etools
from import_dndbeyond import STANDARD_ACTION_REFS


class ImportDndBeyondTests(unittest.TestCase):
    def test_standard_actions_are_referential(self):
        self.assertEqual(len(STANDARD_ACTION_REFS), 7)
        for ref in STANDARD_ACTION_REFS.values():
            self.assertTrue(ref.startswith("/compendium/rules/"))
            self.assertNotIn("description", ref)

    def test_empty_yaml_collections_remain_valid_after_a_key(self):
        self.assertEqual(f"spells:{dump_yaml_indented([], 4)}", "spells: []")
        self.assertEqual(f"metadata:{dump_yaml_indented({}, 2)}", "metadata: {}")

    def test_fetched_items_include_normalized_details_and_modifiers(self):
        item_payload = {
            "item": [
                {
                    "name": "Dagger",
                    "type": "M|XPHB",
                    "value": 200,
                    "weight": 1,
                    "property": ["F|XPHB", "L|XPHB", "T|XPHB"],
                    "range": "20/60",
                    "dmg1": "1d4",
                    "dmgType": "P",
                },
                {
                    "name": "Shortbow",
                    "type": "R",
                    "property": ["A", "2H"],
                    "range": "80/320",
                    "dmg1": "1d6",
                    "dmgType": "P",
                },
                {
                    "name": "Potion of Healing",
                    "type": "P",
                    "rarity": "common",
                    "consumable": True,
                },
                {
                    "name": "Gauntlets of Ogre Power",
                    "wondrous": True,
                    "rarity": "uncommon",
                    "reqAttune": True,
                    "ability": {"static": {"str": 19}},
                },
                {
                    "name": "Ring of Protection",
                    "type": "RG|DMG",
                    "rarity": "rare",
                    "bonusAc": "+1",
                    "bonusSavingThrow": "+1",
                },
            ]
        }
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(item_payload).encode()

        previous_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "dnd_utils.urllib.request.urlopen", return_value=response
        ):
            os.chdir(temp_dir)
            try:
                self.assertEqual(
                    fetch_from_5etools("item", "Dagger"),
                    "/compendium/items/dagger/",
                )
                self.assertEqual(
                    fetch_from_5etools("item", "Shortbow"),
                    "/compendium/items/shortbow/",
                )
                self.assertEqual(
                    fetch_from_5etools("magic_item", "Potion of Healing"),
                    "/compendium/magic-items/potion-of-healing/",
                )
                self.assertEqual(
                    fetch_from_5etools("magic_item", "Gauntlets of Ogre Power"),
                    "/compendium/magic-items/gauntlets-of-ogre-power/",
                )
                self.assertEqual(
                    fetch_from_5etools("magic_item", "Ring of Protection"),
                    "/compendium/magic-items/ring-of-protection/",
                )

                def item_info(relative_path):
                    text = Path(relative_path).read_text(encoding="utf-8")
                    return yaml.safe_load(text.split("---", 2)[1])["item_info"]

                dagger = item_info("content/compendium/items/dagger.md")
                shortbow = item_info("content/compendium/items/shortbow.md")
                potion = item_info(
                    "content/compendium/magic-items/potion-of-healing.md"
                )
                gauntlets = item_info(
                    "content/compendium/magic-items/gauntlets-of-ogre-power.md"
                )
                ring = item_info(
                    "content/compendium/magic-items/ring-of-protection.md"
                )
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(dagger["type"], "Weapon")
        self.assertEqual(dagger["weapon_type"], "melee")
        self.assertEqual(dagger["properties"], ["finesse", "light", "thrown"])
        self.assertEqual(dagger["range"], "20/60")
        self.assertEqual(dagger["damage"], "1d4")
        self.assertEqual(dagger["damage_type"], "piercing")
        self.assertEqual(shortbow["weapon_type"], "ranged")
        self.assertTrue(potion["consumable"])
        self.assertEqual(potion["type"], "Potion")
        self.assertEqual(gauntlets["type"], "Wondrous item")
        self.assertEqual(gauntlets["modifiers"]["stat_override"]["str"], 19)
        self.assertEqual(ring["type"], "Ring")
        self.assertEqual(ring["modifiers"]["ac_bonus"], 1)
        self.assertEqual(ring["modifiers"]["save_bonus"], 1)

    def test_item_sync_preserves_translation_metadata_and_markdown_body(self):
        payload = {
            "baseitem": [
                {
                    "name": "Dagger",
                    "type": "M",
                    "value": 200,
                    "weight": 1,
                    "property": ["F", "L", "T"],
                    "range": "20/60",
                    "dmg1": "1d4",
                    "dmgType": "P",
                }
            ]
        }
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(payload).encode()
        previous_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir, patch(
            "dnd_utils.urllib.request.urlopen", return_value=response
        ):
            os.chdir(temp_dir)
            try:
                path = Path("content/compendium/items/dagger.md")
                path.parent.mkdir(parents=True)
                body = "\n\nDescrição editorial preservada.\n"
                path.write_text(
                    "---\n"
                    "title: Dagger\n"
                    "titulo_pt_br: Adaga\n"
                    "translation:\n"
                    "  status: reviewed\n"
                    "item_info:\n"
                    "  type: Adventuring Gear\n"
                    "---"
                    + body,
                    encoding="utf-8",
                )

                self.assertEqual(
                    fetch_from_5etools("item", "Dagger"),
                    "/compendium/items/dagger/",
                )
                rendered = path.read_text(encoding="utf-8")
                metadata = yaml.safe_load(rendered.split("---", 2)[1])
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(rendered.split("---", 2)[2], body)
        self.assertEqual(metadata["titulo_pt_br"], "Adaga")
        self.assertEqual(metadata["translation"]["status"], "reviewed")
        self.assertEqual(metadata["item_info"]["type"], "Weapon")
        self.assertEqual(metadata["item_info"]["damage"], "1d4")


if __name__ == "__main__":
    unittest.main()
