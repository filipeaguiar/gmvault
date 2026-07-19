import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import dnd_utils


def test_rule_stub_uses_shared_serializer_with_feature_source():
    with TemporaryDirectory() as temporary_directory:
        previous_cwd = Path.cwd()
        os.chdir(temporary_directory)
        try:
            with patch(
                "compendium_rebuild.sync_compendium_entity",
                return_value="/compendium/rules/cunning-action/",
            ) as sync:
                ref = dnd_utils.create_rule_stub(
                    "Cunning Action", ["Feature text"], source="XPHB"
                )
        finally:
            os.chdir(previous_cwd)

    assert ref == "/compendium/rules/cunning-action/"
    sync.assert_called_once_with(
        "rule",
        "Cunning Action",
        slug="cunning-action",
        source="XPHB",
        origin="character",
    )


def test_rule_stub_keeps_existing_legacy_page_without_overwriting():
    with TemporaryDirectory() as temporary_directory:
        previous_cwd = Path.cwd()
        os.chdir(temporary_directory)
        try:
            path = Path("content/compendium/rules/cunning-action.md")
            path.parent.mkdir(parents=True)
            path.write_text("existing", encoding="utf-8")
            with patch("compendium_rebuild.sync_compendium_entity") as sync:
                ref = dnd_utils.create_rule_stub("Cunning Action", [], source="XPHB")
        finally:
            os.chdir(previous_cwd)

    assert ref == "/compendium/rules/cunning-action/"
    sync.assert_not_called()
