from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_character_archetype_uses_referential_shape():
    archetype = (ROOT / "archetypes" / "character.md").read_text(encoding="utf-8")
    assert 'type: "character"' in archetype
    assert "actions: []" in archetype
    assert "equipment: []" in archetype
    assert "spells: []" in archetype
    assert "compendium_refs: []" in archetype
    assert "description:" not in archetype
