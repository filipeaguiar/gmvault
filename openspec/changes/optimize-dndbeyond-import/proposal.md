## Why

Currently, `import_dndbeyond.py` only extracts a minimal subset of character statistics (AC, HP, base stats, feats), forcing the Hugo static build templates (`forge_statblock.html`) to perform complex dynamic calculations for saving throw proficiencies, movement speeds, senses, and languages. Storing these pre-calculated values directly in the character's front matter YAML during import simplifies the static template rendering, makes the markdown files self-contained, and improves the reliability of the Forge JSON export.

## What Changes

- **Update Importer Script**: Modify `import_dndbeyond.py` to extract and calculate size, alignment, speeds (walk, fly, swim, climb, burrow), senses (darkvision, passive perception), languages, and saving throw modifiers directly from the D&D Beyond API JSON.
- **Enrich Character Front Matter**: Write these newly computed fields under `char_info` in the generated character markdown files.
- **Simplify Hugo Export Logic**: Refactor `layouts/partials/helpers/forge_statblock.html` to read speed, saving throws, senses, and languages directly from `char_info` instead of calculating them dynamically.

## Capabilities

### New Capabilities
*None*

### Modified Capabilities
- `content-model`: Update character metadata requirements to include speed, saves, senses, languages, size, and alignment.
- `import-tools`: Update `import_dndbeyond.py` specification to include extraction and computation of these additional character fields.

## Impact

- **Affected Files**:
  - `import_dndbeyond.py`
  - `layouts/partials/helpers/forge_statblock.html`
  - Existing character markdown files in `content/campaigns/*/characters/` (will be updated on next import).
- **Dependencies**: No new external dependencies.
