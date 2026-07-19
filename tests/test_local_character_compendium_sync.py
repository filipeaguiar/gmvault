from unittest.mock import patch

import dnd_utils


def test_sync_materializes_local_character_references_and_deduplicates():
    calls = []

    def fetch(kind, name):
        calls.append((kind, name))
        return f"/compendium/{'magic-items' if kind == 'magic_item' else kind + 's'}/{dnd_utils.slugify(name)}/"

    info = {
        "class": "Wizard",
        "level": 3,
        "species": "Elf",
        "feats": ["Alert", "Alert"],
        "actions": [{"name": "Arcane Recovery"}],
        "equipment": [{"name": "Dagger"}],
        "spells": [{"name": "Magic Missile"}],
    }
    with patch("dnd_utils.fetch_from_5etools", side_effect=fetch), patch(
        "dnd_utils.fetch_class_json", return_value=None
    ), patch("dnd_utils._local_compendium_page", return_value=False):
        refs, unresolved = dnd_utils.sync_character_compendium(info, [])

    assert not unresolved
    assert len(refs) == len(set(refs))
    assert info["equipment"][0]["ref"].endswith("/dagger/")
    assert info["spells"][0]["ref"].endswith("/magic-missile/")
    assert info["actions"][0]["ref"].endswith("/arcane-recovery/")
    assert ("class", "Wizard") in calls
    assert ("species", "Elf") in calls


def test_sync_keeps_unresolved_legacy_data():
    info = {"class": "Unknown", "equipment": [{"name": "Lost Item"}]}
    with patch("dnd_utils.fetch_from_5etools", return_value=None), patch(
        "dnd_utils._local_compendium_page", return_value=False
    ):
        refs, unresolved = dnd_utils.sync_character_compendium(
            info, ["/compendium/items/legacy/"]
        )

    assert refs == ["/compendium/items/legacy/"]
    assert "Unknown" in unresolved
    assert "Lost Item" in unresolved
    assert "ref" not in info["equipment"][0]
