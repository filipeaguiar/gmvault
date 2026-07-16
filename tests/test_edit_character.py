import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import frontmatter

import edit_character


class EditCharacterTests(unittest.TestCase):
    @patch("dnd_utils.load_item_data", return_value={"item": []})
    @patch("dnd_utils.urllib.request.urlopen")
    def test_item_search_includes_base_items(self, urlopen, _load_item_data):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {"baseitem": [{"name": "Dagger"}]}
        ).encode()
        urlopen.return_value = response

        self.assertEqual(edit_character.dnd_utils.search_item_by_name("dagger"), ["Dagger"])

    def test_find_characters_lists_character_pages_by_title(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            characters = Path(temp_dir) / "content/campaigns/example/characters"
            characters.mkdir(parents=True)
            (characters / "_index.md").write_text(
                "---\ntitle: Characters\nparams:\n  kind: section\n---\n",
                encoding="utf-8",
            )
            (characters / "pinky.md").write_text(
                "---\ntitle: Pinky\nparams:\n  kind: character\nchar_info:\n  equipment: []\n---\n\nBiography\n",
                encoding="utf-8",
            )

            found = edit_character.find_characters(
                str(Path(temp_dir) / "content/campaigns/*/characters/*.md")
            )

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0][0], "Pinky (example)")
        self.assertEqual(found[0][1].name, "pinky.md")

    @patch("edit_character.ask_int", return_value=2)
    @patch("edit_character.ask_choice", return_value="Dagger")
    @patch("edit_character.dnd_utils.search_item_by_name")
    @patch("edit_character.ask", side_effect=["dag", ""])
    def test_choose_equipment_searches_disambiguates_and_collects_quantity(
        self, _ask, search, _choice, _ask_int
    ):
        search.return_value = ["Dagger", "Dagger of Venom"]

        selected = edit_character.choose_equipment()

        self.assertEqual(selected, [{"name": "Dagger", "quantity": 2}])
        search.assert_called_once_with("dag")

    @patch(
        "edit_character.dnd_utils.fetch_from_5etools",
        return_value="/compendium/items/dagger/",
    )
    def test_add_equipment_changes_only_equipment_and_references(self, fetch):
        post = frontmatter.Post(
            "Biography\n",
            title="Pinky",
            char_info={"hp": 9, "equipment": []},
            compendium_refs=["/compendium/classes/rogue/"],
        )
        before = copy.deepcopy(post.metadata)

        added = edit_character.add_equipment(
            post, [{"name": "Dagger", "quantity": 2}]
        )

        self.assertEqual(added, 1)
        self.assertEqual(post["char_info"]["hp"], before["char_info"]["hp"])
        self.assertEqual(
            post["char_info"]["equipment"],
            [
                {
                    "name": "Dagger",
                    "ref": "/compendium/items/dagger/",
                    "quantity": 2,
                    "equipped": False,
                }
            ],
        )
        self.assertEqual(
            post["compendium_refs"],
            ["/compendium/classes/rogue/", "/compendium/items/dagger/"],
        )
        fetch.assert_called_once_with("item", "Dagger")

    @patch("edit_character.ask", return_value="1")
    @patch(
        "edit_character.is_equippable_item",
        side_effect=lambda item: item["name"] != "Potion",
    )
    def test_choose_equipped_items_applies_comma_separated_selection(
        self, _equippable, _ask
    ):
        post = frontmatter.Post(
            "Biography\n",
            char_info={
                "equipment": [
                    {"name": "Dagger", "quantity": 2, "equipped": False},
                    {"name": "Shield", "quantity": 1, "equipped": True},
                    {"name": "Potion", "quantity": 1, "equipped": False},
                ]
            },
        )

        changed = edit_character.choose_equipped_items(post)

        self.assertTrue(changed)
        equipment = post["char_info"]["equipment"]
        self.assertTrue(equipment[0]["equipped"])
        self.assertFalse(equipment[1]["equipped"])
        self.assertFalse(equipment[2]["equipped"])

    @patch("edit_character.ask", return_value="99")
    @patch("edit_character.is_equippable_item", return_value=True)
    def test_99_equips_all_items(self, _equippable, _ask):
        post = frontmatter.Post(
            "Biography\n",
            char_info={
                "equipment": [
                    {"name": "Dagger", "quantity": 1, "equipped": False},
                    {"name": "Shield", "quantity": 1, "equipped": False},
                ]
            },
        )

        self.assertTrue(edit_character.choose_equipped_items(post))
        self.assertTrue(
            all(item["equipped"] for item in post["char_info"]["equipment"])
        )

    @patch("edit_character.ask", return_value="")
    @patch("edit_character.is_equippable_item", return_value=True)
    def test_blank_equipped_selection_preserves_current_state(
        self, _equippable, _ask
    ):
        post = frontmatter.Post(
            "Biography\n",
            char_info={
                "equipment": [
                    {"name": "Dagger", "quantity": 1, "equipped": True}
                ]
            },
        )

        self.assertFalse(edit_character.choose_equipped_items(post))
        self.assertTrue(post["char_info"]["equipment"][0]["equipped"])

    def test_save_character_preserves_markdown_body_exactly(self):
        original = (
            b"---\n"
            b"title: Pinky\n"
            b"char_info:\n"
            b"  hp: 9\n"
            b"  equipment: []\n"
            b"compendium_refs: []\n"
            b"---\n\n"
            b"### Biography\n"
            b"Body with trailing spaces.  \n\n"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "pinky.md"
            path.write_bytes(original)
            body = edit_character.read_body_bytes(path)
            post = frontmatter.load(path)
            post["char_info"]["equipment"].append({"name": "Dagger"})

            edit_character.save_character(path, post, body)

            self.assertEqual(edit_character.read_body_bytes(path), body)
            saved = frontmatter.load(path)
            self.assertEqual(saved.content, post.content)
            self.assertEqual(saved["char_info"]["hp"], 9)
            self.assertEqual(saved["char_info"]["equipment"], [{"name": "Dagger"}])


if __name__ == "__main__":
    unittest.main()
