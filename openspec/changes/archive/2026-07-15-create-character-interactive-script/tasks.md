## 1. Setup and CLI Boilerplate

- [x] 1.1 Create `create_character.py` and set up standard `argparse` options (e.g. `--campaign`).
- [x] 1.2 Implement the interactive prompting logic (using built-in `input` or a library like `Rich`/`questionary` if available) to handle step-by-step questions for basic data (Name, Campaign, Race, Class, Level, Alignment).

## 2. Shared Utilities Refactoring

- [x] 2.1 Refactor `import_dndbeyond.py` to extract common functions (`slugify`, `fetch_from_5etools`, `dump_yaml_indented`) into a new `dnd_utils.py` (or similar shared module), so both scripts can import them cleanly.
- [x] 2.2 Move `get_modifier` to the shared module.

## 3. Data Collection and Calculation

- [x] 3.1 Prompt the user for Ability Scores (STR, DEX, CON, INT, WIS, CHA) and automatically calculate their modifiers.
- [x] 3.2 Prompt the user for AC, Max HP, Speed, and senses.
- [x] 3.3 Prompt for equipment, spells, and proficiencies (can be simplified list inputs).

## 4. Compendium Syncing

- [x] 4.1 Execute `fetch_from_5etools` for the provided Race to ensure it exists in the compendium.
- [x] 4.2 Execute `fetch_from_5etools` for the provided Class/Subclass.
- [x] 4.3 Loop through provided spells and equipment to download them into the compendium via `fetch_from_5etools`.
- [x] 4.4 Aggregate all returned paths into the `compendium_refs` list.

## 5. File Generation

- [x] 5.1 Map all collected data and calculated modifiers into the final Python dictionaries (`char_info`, `skills`, `actions`, `equipment`, `spells`).
- [x] 5.2 Generate the final Markdown file in `content/campaigns/<campaign>/characters/<slug>.md` using the exact layout from `import_dndbeyond.py`.
- [x] 5.3 Use `dump_yaml_indented` to guarantee correct YAML formatting without inline JSON strings.
