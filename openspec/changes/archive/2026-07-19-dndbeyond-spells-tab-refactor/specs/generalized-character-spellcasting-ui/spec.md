## ADDED Requirements

### Requirement: Character spell lists are persisted in the ficha
The system SHALL persist the character's spell list as part of the character data so that the list survives reloads and can be generated automatically or manually by scripts.

#### Scenario: Character has spells from import or creation
- **WHEN** a character is created or imported with spells
- **THEN** the system SHALL store those spells in the character data
- **THEN** the spells SHALL remain available when the ficha is reopened

#### Scenario: Character adds a spell manually
- **WHEN** the user adds a spell manually during character creation or editing
- **THEN** the system SHALL append the spell to the persisted character spell list

### Requirement: Spell state is stored in localStorage
The system SHALL store the operational state of the spells tab in `localStorage` and SHALL NOT require Markdown rewrites to track session usage state.

#### Scenario: User marks a spell prepared
- **WHEN** the user changes the prepared state in the spells tab
- **THEN** the system SHALL persist that state in `localStorage`
- **THEN** the persisted character data SHALL remain unchanged

#### Scenario: User reloads the ficha
- **WHEN** the user reloads the page
- **THEN** the system SHALL restore the spells tab state from `localStorage`

### Requirement: Spell UI separates ready-to-use and learned-but-unprepared spells
The spells tab SHALL display spells in a way that separates spells ready for use from learned spells that are not currently prepared, using the character's spellcasting profile to decide which states exist.

#### Scenario: Prepared caster opens spells tab
- **WHEN** a prepared caster opens the spells tab
- **THEN** the system SHALL visually distinguish prepared spells from unprepared spells

#### Scenario: Known caster opens spells tab
- **WHEN** a known caster opens the spells tab
- **THEN** the system SHALL visually distinguish known spells from other learned spells if applicable

#### Scenario: Character has no spellcasting
- **WHEN** a character without spellcasting opens the spells tab
- **THEN** the system SHALL show a useful empty state or hide the tab

### Requirement: Scripts MAY add spells automatically or manually
The creation, edit, and import scripts SHALL be able to add spells automatically when granted by class, subclass, feat, race, or item, and SHALL allow manual entry when the class requires user choice.

#### Scenario: Class grants a spell automatically
- **WHEN** the class or another source grants a spell without user choice
- **THEN** the script SHALL add the spell to the character spell list automatically

#### Scenario: Class requires user choice
- **WHEN** the class requires the user to choose spells during creation or editing
- **THEN** the script SHALL prompt for manual selection and SHALL add the chosen spells to the character spell list

### Requirement: Spellcasting profile is resolved from 5e.tools
The system SHALL consult 5e.tools to determine how each class handles spells and which spell states apply to the character.

#### Scenario: Class is a prepared caster
- **WHEN** 5e.tools identifies the class as prepared
- **THEN** the system SHALL treat the character as a prepared caster for the purposes of the spells tab

#### Scenario: Class is a pact caster
- **WHEN** 5e.tools identifies the class as pact magic
- **THEN** the system SHALL apply pact-specific spell state handling in the spells tab

### Requirement: Legacy character spell fields remain compatible
The system SHALL continue to read `char_info.spells`, `char_info.class_spells`, and `spell_slots` as fallback inputs while the new spell data contract is being adopted.

#### Scenario: Legacy character opens spells tab
- **WHEN** a character only has legacy spell fields
- **THEN** the system SHALL render the spells tab using the legacy data as fallback

#### Scenario: New and legacy spell fields coexist
- **WHEN** a character contains both the new persisted spell list and legacy fields
- **THEN** the system SHALL use the new persisted spell list as the primary source and preserve compatibility with the legacy fields
