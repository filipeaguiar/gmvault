## ADDED Requirements

### Requirement: Terminology update to Species
The system SHALL use the term "Espécie" (and "species" internally) in all templates, frontmatters, folders, and outputs, instead of the legacy "Raça" (and "race" or "races").

#### Scenario: Displaying species in Character Sheet
- **WHEN** viewing a character sheet
- **THEN** it renders "Espécie" in the metadata line and lists the character's species/variant.

### Requirement: Guided Species Selection
The CLI tool SHALL parse the `races.json` file from 5e.tools to present the list of available species and guide the user to choose one, including selecting any available subraces or variants.

#### Scenario: User selects an Elf with High Elf variant
- **WHEN** selecting Elf
- **THEN** the CLI presents available subraces/variants (e.g., Wood Elf, High Elf, Eladrin) and stores the selected subrace parameters.

### Requirement: Guided Class and Hit Dice Resolution
The CLI tool SHALL fetch class definition from class files (e.g. `classes.json`) to resolve the class hit dice (HD) and calculate base HP automatically based on level and Constitution modifier.

#### Scenario: Resolving HP for Level 3 Rogue
- **WHEN** user chooses Rogue Level 3 with CON score 14 (+2 mod)
- **THEN** the tool resolves Hit Dice as d8 and calculates max HP as: 8 (1st level) + 5 * 2 (subsequent levels) + 3 * 2 (CON mod) = 24 HP.

### Requirement: Attribute Entry with Species Bonuses
The CLI tool SHALL prompt for Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma, and automatically add any ability score increases from the chosen species/variant.

#### Scenario: Applying Elf ability scores
- **WHEN** user chooses Elf (+2 Dex, +1 Int) and enters base stats
- **THEN** the script automatically calculates final stats by adding the species bonuses.
