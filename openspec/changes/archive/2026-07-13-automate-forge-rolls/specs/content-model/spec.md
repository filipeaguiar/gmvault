## ADDED Requirements

### Requirement: Forge export formats descriptions into interactive roll chips
The Forge JSON statblock export layout SHALL parse and convert text roll notations in descriptions into Forge interactive roll chips.

#### Scenario: Attack modifier is parsed
- **WHEN** an action, ability, or item description contains a standard attack bonus notation like `+5 to hit` or `+6 para acertar`
- **THEN** the exporter SHALL convert it to a Forge roll chip `[1d20+5] to hit` or `[1d20+6] para acertar`

#### Scenario: Dice formula is parsed
- **WHEN** an action, ability, or item description contains a dice formula like `2d6 + 3` or `1d8`
- **THEN** the exporter SHALL convert it to a Forge roll chip `[2d6+3]` or `[1d8]`

#### Scenario: Multiple rolls are formatted
- **WHEN** a description containing multiple roll notations is exported
- **THEN** all instances of those notations SHALL be formatted as Forge roll chips

### Requirement: Character weapon attacks dynamically calculate bonuses
The Forge character exporter SHALL dynamically compute attack bonuses and damage modifiers for weapon actions based on character statistics and weapon properties.

#### Scenario: Finesse weapon uses dexterity
- **WHEN** a character has a higher Dexterity modifier than Strength modifier and uses a weapon with the Finesse property
- **THEN** the exporter SHALL calculate the attack bonus using the Dexterity modifier and proficiency bonus

#### Scenario: Heavy weapon uses strength
- **WHEN** a character uses a weapon without Finesse or Ranged properties (such as a Greataxe)
- **THEN** the exporter SHALL calculate the attack bonus using the Strength modifier and proficiency bonus

#### Scenario: Magic weapon bonus is added
- **WHEN** a weapon in the character's inventory has a positive magic bonus (e.g. `+1`)
- **THEN** the exporter SHALL add this bonus to both the calculated attack bonus and damage modifier chips

### Requirement: Spell list entries are enriched with compendium data
The Forge character exporter SHALL resolve spell definitions from the compendium to populate full descriptions and metadata for character spells.

#### Scenario: Spell details and description are resolved
- **WHEN** a character's spell is exported
- **THEN** the exporter SHALL fetch the corresponding spell page, prefix the cast time, range, components, and duration, append the spell's description, and convert all rolls to chips
