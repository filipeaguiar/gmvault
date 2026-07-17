# interactive-character-sheet-spells Specification

## Purpose
TBD - created by archiving change interactive-spells-search. Update Purpose after archive.
## Requirements
### Requirement: Spells UI Layout
The character sheet template SHALL display spells logically grouped by levels, using `<details>` and `<summary>` HTML tags as accordions.

#### Scenario: Viewing the spells section
- **WHEN** the character has spells in their frontmatter
- **THEN** the Hugo template iterates through the spells, creating an accordion for each where the summary is the spell name

### Requirement: Prepared Spells vs Class Spells
The system SHALL display two separate spell sections: "Magias Disponíveis/Preparadas" and "Lista Completa", with checkboxes to toggle spell presence in the prepared list using Vanilla JavaScript.

#### Scenario: Preparing a spell
- **WHEN** the user checks a box next to a spell in the "Lista Completa" section
- **THEN** the JavaScript logic moves or clones that spell's DOM element into the "Magias Disponíveis" section

### Requirement: Spell List Search Filter
The system SHALL provide a search input field above the "Lista Completa" section to filter the spells in real-time.

#### Scenario: Filtering the giant spell list
- **WHEN** the user types "Cure" into the search field
- **THEN** the JavaScript hides all spell accordions that do not contain the word "Cure" (case-insensitive)

### Requirement: Dynamic Spell Slots Trackers
The system SHALL render interactive checkboxes acting as spell slot trackers by reading the `spell_slots` dictionary injected in the YAML.

#### Scenario: Casting a spell
- **WHEN** the Markdown contains `spell_slots: {1: 4}`
- **THEN** the Hugo template renders exactly four checkboxes for level 1 slots
- **THEN** the user can click one of the checkboxes to mark it as used during the session

### Requirement: Dice Roller Integration
The system SHALL identify spell damage or healing formulas and output `data-roll-notation` elements.

#### Scenario: Clicking a damage spell
- **WHEN** the user opens the "Fireball" accordion
- **THEN** an element with `data-roll-notation="8d6"` is visible
- **THEN** clicking it triggers the Owlbear Rodeo integration

