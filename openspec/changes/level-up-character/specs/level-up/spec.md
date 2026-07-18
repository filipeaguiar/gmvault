## ADDED Requirements

### Requirement: Character level up updates derived statistics
The system SHALL recalculate all derived statistics when a character levels up, including proficiency bonus, hit points, spell slots, and save bonuses.

#### Scenario: Level up increments level
- **WHEN** the user selects "Subir de nível" for a character at level N
- **THEN** the system SHALL set `level` and `class_level` to N+1

#### Scenario: Proficiency bonus is recalculated
- **WHEN** the character levels up
- **THEN** the system SHALL calculate proficiency bonus as `(level - 1) // 4 + 2`

#### Scenario: Hit points increase by hit die average
- **WHEN** the user chooses "Média" (automático)
- **THEN** the system SHALL add `int(hit_dice_faces / 2) + 1 + con_modifier` to `hp_max`
- **THEN** the system SHALL set `hp_current` equal to `hp_max`

#### Scenario: Hit points increase by typed roll
- **WHEN** the user chooses "Rolagem" e digita o resultado do dado
- **THEN** the system SHALL add the typed value + con_modifier to `hp_max`
- **THEN** the system SHALL set `hp_current` equal to `hp_max`

#### Scenario: Hit points increase by fixed value
- **WHEN** the user chooses "Fixo" e digita um valor
- **THEN** the system SHALL add that value to `hp_max`
- **THEN** the system SHALL set `hp_current` equal to `hp_max`

#### Scenario: Spell slots are recalculated
- **WHEN** the character is a spellcaster and levels up
- **THEN** the system SHALL recalculate spell slots using `calculate_spell_slots()` for the new level

### Requirement: Character level up adds new class features
The system SHALL identify and add new class and subclass features available at the new level.

#### Scenario: New class features are displayed
- **WHEN** the character levels up to a level with new class features
- **THEN** the system SHALL display each new feature name and description
- **THEN** the system SHALL add the feature to `feature_actions` with a compendium reference

#### Scenario: New subclass features are displayed
- **WHEN** the character has a subclass and levels up to a level with new subclass features
- **THEN** the system SHALL display each new subclass feature
- **THEN** the system SHALL add the feature to `feature_actions`

#### Scenario: Feature requires a choice
- **WHEN** a new feature requires a user choice (e.g., Fighting Style, Metamagic)
- **THEN** the system SHALL prompt the user to select from available options
- **THEN** the system SHALL create a rule stub for the chosen option

### Requirement: Character level up offers feats at appropriate levels
The system SHALL offer feat selection at levels 4, 8, 12, 16, and 19 (or when the class grants ASIs).

#### Scenario: Feat selection at ASI level
- **WHEN** the character reaches a level where the class grants an Ability Score Improvement
- **THEN** the system SHALL ask the user to choose between increasing ability scores or selecting a feat
- **THEN** the system SHALL use `select_feats_for_level()` if the user chooses a feat

#### Scenario: No feat at non-ASI level
- **WHEN** the character levels up to a level without ASI
- **THEN** the system SHALL skip feat selection

### Requirement: Character level up preserves existing data
The system SHALL preserve all existing character data that is not affected by leveling up.

#### Scenario: Equipment is preserved
- **WHEN** the character levels up
- **THEN** the system SHALL keep all equipment entries unchanged

#### Scenario: Spells are preserved
- **WHEN** the character levels up
- **THEN** the system SHALL keep all existing spell entries
- **THEN** the system SHALL only add new spells if the user explicitly chooses them

#### Scenario: Skills are preserved
- **WHEN** the character levels up
- **THEN** the system SHALL keep all skill proficiencies and expertise selections
- **THEN** the system SHALL recalculate skill bonuses using the new proficiency bonus
