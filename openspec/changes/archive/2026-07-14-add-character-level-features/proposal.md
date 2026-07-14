## Why

Each class and subclass in 5e.tools contains a detailed list of features gained at each level. Currently, these level-specific features are not integrated, translated, or rendered in the imported character sheets or the exported Forge cards, limiting player and DM reference during sessions.

## What Changes

- **Class/Subclass Level Features Extraction**: Update the D&D Beyond import tool to extract and map level-specific features for both classes and subclasses from 5e.tools source files.
- **Translation Pipeline integration**: Feed these extracted level features through the translation strategy to populate Brazilian Portuguese versions in `/compendium/rules/`.
- **Character Sheet Display**: Display the list of level features (with descriptions) in the character's Markdown file.
- **Forge Export Integration**: Include level features in the Forge card metadata (e.g., in the traits/features section `Z034` or similar).

## Capabilities

### New Capabilities

*(None)*

### Modified Capabilities

- `import-tools`: Add requirement to parse, translate, and link class and subclass level-specific features from 5e.tools during character imports.
- `forge-statblock-export`: Include level-specific class and subclass features in the exported Forge metadata (Z034).

## Impact

- `import_dndbeyond.py`: Updates the parser to walk class/subclass features by level.
- `layouts/partials/helpers/forge_statblock.html`: Updates the exporter to parse and include class/subclass features in `Z034`.
- Character front matter and compendium rules.
