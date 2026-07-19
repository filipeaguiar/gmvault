import json
import subprocess
import tempfile
import unittest
from pathlib import Path


CAMPAIGN_EXPORT = (
    "campaigns/journeys-through-the-radiant-citadel/gm-vault.json"
)


class GMVaultExportTests(unittest.TestCase):
    def _build_campaign_export(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        subprocess.run(
            ["hugo", "--destination", temp_dir.name, "--quiet"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        path = Path(temp_dir.name) / CAMPAIGN_EXPORT
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _category(parent, name):
        return next(item for item in parent["categories"] if item["name"] == name)

    @staticmethod
    def _child_category(parent, name):
        return next(item for item in parent["items"] if item["name"] == name)

    def test_adventure_lists_scenes_directly_without_scene_category(self):
        export = self._build_campaign_export()
        adventures = self._category(export, "Aventuras")
        adventure = self._child_category(adventures, "Bem-vindo à Cidadela Radiante")

        self.assertTrue(adventure["items"])
        self.assertTrue(all(item["type"] == "page" for item in adventure["items"]))
        self.assertFalse(
            any(
                item["name"].startswith("Cenas de ")
                for item in adventure["items"]
                if item["type"] == "category"
            )
        )

    def test_adventure_handouts_are_nested_and_root_keeps_player_portraits(self):
        export = self._build_campaign_export()
        adventures = self._category(export, "Aventuras")
        adventure = self._child_category(adventures, "Legado Salgado")
        handouts = self._child_category(adventure, "Handouts")
        handout_urls = [item["url"] for item in handouts["items"]]

        self.assertEqual(len(handout_urls), len(set(handout_urls)))
        self.assertGreater(len(handout_urls), 0)

        root_handouts = next((item for item in export["categories"] if item["name"] == "Handouts"), None)
        if root_handouts:
            root_urls = [item["url"] for item in root_handouts["items"]]
            self.assertTrue(set(handout_urls).isdisjoint(root_urls))


if __name__ == "__main__":
    unittest.main()
