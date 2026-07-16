# create-character-interactive Specification

## Purpose
TBD - created by archiving change create-character-interactive-script. Update Purpose after archive.
## Requirements
### Requirement: Interactive Character Creation
The script SHALL prompt the user to input character details such as name, race, class, level, stats, spells, background, starting packs, and equipment via terminal interface.

#### Scenario: User provides character details
- **WHEN** the script is executed
- **THEN** it asks for basic information (name, campaign) and step-by-step asks for race, class, level, background, starting packs, ability scores, proficiencies, etc.

### Requirement: Compendium Population
The script SHALL query the `5etools` mirrors for any classes, subclasses, races, feats, spells, and items that the character has and download them into the compendium if they don't exist.

#### Scenario: Character has a new race
- **WHEN** the user inputs a race that isn't in the compendium
- **THEN** the script downloads the race from 5e.tools and saves it to `content/compendium/races/`.

### Requirement: Stat Calculation
The script SHALL automatically calculate modifiers, AC, max HP, and proficiency bonus based on level, stats, and class/race info.

#### Scenario: Calculating modifiers
- **WHEN** the user inputs a Strength score of 16
- **THEN** the script calculates the STR modifier as +3.

### Requirement: Frontmatter Generation
The script SHALL generate the Markdown file for the character in the selected campaign using `PyYAML` to correctly format `char_info` with lists and dictionaries.

#### Scenario: File creation
- **WHEN** the interactive flow is completed
- **THEN** the script creates `content/campaigns/<campaign>/characters/<slug>.md` with properly formatted YAML frontmatter and no inline single-line JSON blocks.

