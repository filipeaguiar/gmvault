## MODIFIED Requirements

### Requirement: Spells UI Layout
The character sheet template SHALL display a top operational list containing only spells ready for use and a lower management list containing the other accessible referenced spells. Both lists SHALL resolve spell identity, level, content, and shared mechanics from canonical compendium pages, group entries by accessible spell level, and remain usable without JavaScript.

#### Scenario: Viewing the spells section for a prepared caster
- **WHEN** a prepared caster has prepared spells and other accessible referenced class spells
- **THEN** the top list SHALL contain the prepared spells and cantrips ready for use
- **THEN** the lower management list SHALL contain each other accessible referenced spell exactly once

#### Scenario: Viewing the spells section for a known or pact caster
- **WHEN** a known or pact caster has referenced known spells
- **THEN** all known spells SHALL appear in the top ready-for-use list
- **THEN** the interface SHALL NOT imply that those spells require preparation

#### Scenario: Spell reference resolves
- **WHEN** a spell entry has a valid internal compendium reference
- **THEN** the card SHALL obtain its visible title, level, details, and shared mechanics from the resolved compendium page

#### Scenario: Legacy spell reference is unresolved
- **WHEN** a legacy spell entry cannot resolve its internal reference but contains inline fallback fields
- **THEN** the sheet SHALL remain renderable and SHALL show an identifiable inline fallback without failing the Hugo build

### Requirement: Prepared Spells vs Class Spells
The system SHALL maintain separate ready-for-use and management lists and SHALL provide preparation checkboxes only for management entries that the character's spellcasting profile or entry-specific metadata marks as preparable. Changing a checkbox SHALL update the two lists as temporary browser state without making the browser state canonical character data. Ready-list cards SHALL NOT repeat a per-card “Preparada” badge.

#### Scenario: Preparing an eligible spell
- **WHEN** the user checks a preparation checkbox for an eligible spell in the management list
- **THEN** the same spell SHALL move to the ready-for-use list without creating a duplicate
- **THEN** its compendium content and structured roll metadata SHALL remain intact

#### Scenario: Unpreparing an eligible spell
- **WHEN** the user clears a preparation checkbox for an eligible prepared spell through the management control
- **THEN** the spell SHALL leave the ready-for-use list and return to the management list exactly once

#### Scenario: Spell does not support preparation
- **WHEN** a spell belongs to a known, pact, spontaneous, always-available, or feature-granted source that is not preparable
- **THEN** the management entry SHALL be read-only and SHALL NOT display a preparation checkbox

#### Scenario: Ready spell card is rendered
- **WHEN** a spell appears in the top ready-for-use list
- **THEN** its card SHALL NOT display a repeated “Preparada” badge

#### Scenario: JavaScript or local storage is unavailable
- **WHEN** the page cannot execute the spell manager script or persist local state
- **THEN** the server-rendered ready and management lists SHALL remain readable
- **THEN** the character front matter SHALL remain the canonical preparation state

### Requirement: Spell List Search Filter
The system SHALL provide search and level filters that operate across the ready-for-use and management lists. It SHALL render level controls only for spell circles the character can access or for explicitly granted ready spells.

#### Scenario: Filtering spells by name
- **WHEN** the user types “Cure” into the spell search field
- **THEN** the interface SHALL hide cards in both spell lists whose names do not contain “Cure”, case-insensitively

#### Scenario: Character has access only to cantrips and first-level spells
- **WHEN** the normalized character data exposes cantrips and positive first-level slots but no access to higher spell levels
- **THEN** the level filter SHALL show only the all-level, cantrip, and first-level controls

#### Scenario: Inaccessible class spell is referenced
- **WHEN** a class catalog contains a spell above every spell circle accessible to the character and the spell is not explicitly granted
- **THEN** that spell SHALL NOT appear in the management list or create a level filter

#### Scenario: Granted spell exceeds normal slot level
- **WHEN** an always-available or feature-granted ready spell has a level above the character's normal slots
- **THEN** the ready spell SHALL remain visible and its own level SHALL be available as a filter

### Requirement: Dynamic Spell Slots Trackers
The system SHALL render interactive spell-slot trackers from the character's positive slot resources and SHALL omit spell levels for which the character has no usable slots. Pact slots SHALL retain their profile-specific label and level instead of being presented as unrelated normal slots.

#### Scenario: Character has first-level slots only
- **WHEN** the character data contains `spell_slots: {1: 4}`
- **THEN** the template SHALL render exactly four first-level slot checkboxes
- **THEN** it SHALL NOT render slot groups for levels 2 through 9

#### Scenario: Slot dictionary contains zero values
- **WHEN** a spell-slot level has a value of zero
- **THEN** the template SHALL omit that slot group

#### Scenario: Pact caster has pact slots
- **WHEN** the spellcasting profile identifies pact magic and provides a positive pact slot level and count
- **THEN** the tracker SHALL identify the resource as pact slots and SHALL render only the accessible pact slot group

### Requirement: Dice Roller Integration
The system SHALL render structured spell roll controls from each resolved compendium page and SHALL preserve their Dice+ metadata when a spell is filtered or moved between ready and management lists.

#### Scenario: Clicking a damage spell
- **WHEN** the resolved compendium page for Fireball exposes the structured notation `8d6`
- **THEN** an element with `data-roll-notation="8d6"` SHALL be present on the character spell card
- **THEN** clicking the enhanced value after Dice+ readiness SHALL trigger the existing Owlbear integration

#### Scenario: Preparing a spell with roll metadata
- **WHEN** a management card containing structured roll metadata is moved into the ready list
- **THEN** its roll notation, roll type, accessible label, and other Dice+ `data-*` attributes SHALL remain unchanged

#### Scenario: Spell has no structured roll
- **WHEN** the resolved compendium page exposes no valid structured roll metadata
- **THEN** the spell card SHALL remain readable and SHALL NOT infer a roll from its description
