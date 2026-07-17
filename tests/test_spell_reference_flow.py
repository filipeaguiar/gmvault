from pathlib import Path
import sys
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dnd_utils import (
    build_spell_entry,
    deduplicate_spell_entries,
    infer_spellcasting_profile,
    materialize_spell,
    materialize_spell_entry,
    normalize_character_spell_entries,
)


def test_materialization_builds_minimal_reference_driven_entry():
    fetcher = Mock(return_value="/compendium/spells/bless/")

    entry = materialize_spell_entry(
        "Bless",
        fetcher=fetcher,
        prepared=True,
        availability="prepared",
        source="cleric",
        usage="1 action",
    )

    assert entry == {
        "ref": "/compendium/spells/bless/",
        "prepared": True,
        "availability": "prepared",
        "source": "cleric",
        "usage": "1 action",
    }
    assert "name" not in entry
    assert "level" not in entry
    assert "spell_info" not in entry
    fetcher.assert_called_once_with("spell", "Bless")


def test_unresolved_or_noncanonical_spell_does_not_fabricate_ref():
    assert materialize_spell("Missing", fetcher=Mock(return_value=None)) is None
    assert materialize_spell("Wrong", fetcher=Mock(return_value="/compendium/rules/wrong/")) is None
    assert build_spell_entry(None) is None


def test_duplicate_merge_preserves_most_ready_state_sources_and_usage():
    entries = deduplicate_spell_entries(
        [
            {
                "ref": "/compendium/spells/misty-step/",
                "prepared": False,
                "availability": "known",
                "source": "class",
                "usage": "slot",
            },
            {
                "ref": "/compendium/spells/misty-step",
                "prepared": True,
                "availability": "always",
                "source": "feat",
                "usage": "1/long rest",
            },
        ]
    )

    assert len(entries) == 1
    assert entries[0]["prepared"] is True
    assert entries[0]["availability"] == "always"
    assert entries[0]["source"] == "class"
    assert entries[0]["sources"] == ["class", "feat"]
    assert entries[0]["usages"] == ["slot", "1/long rest"]


def test_legacy_normalization_preserves_only_unresolved_inline_fallback():
    fetcher = Mock(side_effect=lambda _kind, name: (
        "/compendium/spells/guidance/" if name == "Guidance" else None
    ))

    result = normalize_character_spell_entries(
        [
            {"name": "Guidance", "level": 0, "prepared": True},
            {"name": "Homebrew Spark", "level": 1, "description": "Legacy"},
        ],
        fetcher=fetcher,
    )

    assert result[0] == {"ref": "/compendium/spells/guidance/", "prepared": True}
    assert result[1]["name"] == "Homebrew Spark"
    assert result[1]["level"] == 1


def test_profile_exposes_positive_and_pact_resources_with_safe_hybrid_fallback():
    pact = infer_spellcasting_profile(
        "Warlock", level=5, spell_slots={0: 1, 2: 0, 3: 2, "bad": 4}
    )
    hybrid = infer_spellcasting_profile(
        "Unknown",
        spells=[{"prepared": True}, {"prepared": False}],
        explicit_kind="hybrid",
    )

    assert pact["slot_levels"] == [3]
    assert pact["pact_slot_level"] == 3
    assert pact["pact_slot_count"] == 2
    assert pact["can_prepare"] is False
    assert hybrid["kind"] == "hybrid"
    assert hybrid["can_prepare"] is False
