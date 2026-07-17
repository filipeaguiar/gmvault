## ADDED Requirements

### Requirement: Interactive Spell Lookup
The system SHALL prompt the user to search for a spell by name and display matching results from the 5e.tools dataset during character creation or edition.

#### Scenario: User searches for a spell
- **WHEN** the user is prompted to add a spell and types "Fireball"
- **THEN** the system queries the `spells-*.json` data and displays exact or partial matches

### Requirement: Disambiguation Menu
The system SHALL present a disambiguation menu if multiple spells match the search term.

#### Scenario: Multiple spells match
- **WHEN** the user types "Cure"
- **THEN** the system displays options like "Cure Wounds", "Mass Cure Wounds"

### Requirement: Spell Slots Calculation
The system SHALL automatically calculate the number of spell slots based on the character's class and level during creation, injecting a `spell_slots` dictionary into the YAML.

#### Scenario: Character is created
- **WHEN** a Level 5 Wizard is generated via `create_character.py`
- **THEN** the system calculates the slots and adds `spell_slots: {1: 4, 2: 3, 3: 2}` to the Markdown frontmatter

### Requirement: Front Matter Integration
The system SHALL automatically inject the resolved spell reference into the character's front matter.

#### Scenario: Spell is added to character
- **WHEN** the user confirms the addition of a spell
- **THEN** the system downloads the spell to the compendium and appends the URL to the character's references
