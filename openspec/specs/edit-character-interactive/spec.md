# edit-character-interactive Specification

## Purpose
TBD - created by archiving change edit-character-interactive. Update Purpose after archive.
## Requirements
### Requirement: Character Selection Menu
The system SHALL list all characters found across all campaigns in `content/campaigns/*/characters/*.md` and allow the user to select one to edit.

#### Scenario: User selects a character
- **WHEN** the user runs `edit_character.py`
- **THEN** the system lists existing characters by name (e.g. "Pinky (Radiant Citadel)")
- **THEN** the user selects a character via `ask_choice`

### Requirement: Interactive Equipment Addition
The system SHALL prompt the user to add new equipment using the interactive search flow from `dnd_utils.search_item_by_name`.

#### Scenario: User adds new weapon
- **WHEN** the user selects "Add Equipment" for Pinky
- **THEN** the system uses the exact search flow (asking item name, disambiguating, and asking quantity)
- **THEN** the item is fetched, downloaded if needed, and added to the YAML front matter

### Requirement: Preserve Unchanged Front Matter and Body
The system SHALL parse the Markdown file, modify ONLY the `equipment` and `compendium_refs` lists, and overwrite the file maintaining the Markdown body intact.

#### Scenario: File is updated
- **WHEN** the user finalizes adding equipment
- **THEN** the system updates the character's `.md` file
- **THEN** previously defined skills, hp, abilities and the Markdown body are preserved exactly as before

