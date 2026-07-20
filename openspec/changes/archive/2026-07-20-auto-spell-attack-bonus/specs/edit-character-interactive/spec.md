## ADDED Requirements

### Requirement: Character editor maintains resolved casting ability
The interactive character editor SHALL preserve a supported existing `char_info.spellcasting.ability` and SHALL refresh it from resolved single-class data when an edit or synchronization recalculates the spellcasting profile. It SHALL not assign an ambiguous ability to a multiclass character.

#### Scenario: Synchronizing a single-class spellcaster
- **WHEN** the user synchronizes a single-class spellcaster whose resolved class data identifies a spellcasting ability
- **THEN** the editor SHALL write the corresponding normalized ability key to `char_info.spellcasting.ability`

#### Scenario: Editing a multiclass character without per-spell metadata
- **WHEN** the selected character has multiple spellcasting classes and no unambiguous single profile ability
- **THEN** the editor SHALL preserve existing data without inventing a global casting ability

### Requirement: Character editor preserves explicit spell attack overrides
The interactive character editor SHALL preserve a configured `char_info.spell_attack_bonus` while updating spellcasting profile data, unless the user explicitly changes that override through a supported operation.

#### Scenario: Editing a character with an exceptional bonus
- **WHEN** the selected character has an explicit spell attack bonus that differs from proficiency plus casting modifier
- **THEN** an unrelated spellcasting edit or synchronization SHALL retain the explicit bonus
