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



### Requirement: Complete local character compendium synchronization
The editor SHALL synchronize all supported shared entities represented by the selected local character, including classes, species, subclasses, feats, standard actions, class and subclass features, spells, items, and magic items, after an operation introduces them and through an explicit full synchronization operation.

#### Scenario: Editor adds supported content
- **WHEN** an editing operation adds a supported item, magic item, feat, spell, action, or feature
- **THEN** the editor SHALL materialize its canonical local compendium page before associating its URL with the character

#### Scenario: User synchronizes an existing character
- **WHEN** the user selects the full compendium synchronization operation
- **THEN** the editor SHALL resolve all supported entities represented in the selected character
- **THEN** it SHALL retain unresolved legacy data and report entities it could not resolve

#### Scenario: Existing reference is already local
- **WHEN** a selected character already references an existing canonical compendium page
- **THEN** the editor SHALL reuse that page and SHALL NOT create a duplicate reference


### Requirement: Editor exposes local level-up operation
The interactive character editor SHALL offer a level-up operation for a selected local character whose class progression can be resolved.

#### Scenario: Eligible character is selected
- **WHEN** the editor loads a character with a valid class and current level
- **THEN** the editor SHALL offer the level-up operation alongside existing editing operations

#### Scenario: Editor presents plan before writing
- **WHEN** the user selects level-up
- **THEN** the editor SHALL display the target level, automatic changes, new features, and required choices before modifying the file
