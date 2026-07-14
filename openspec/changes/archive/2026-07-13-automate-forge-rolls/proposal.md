## Why

The current Forge export for player characters and monsters does not format action, ability, or spell descriptions with dice roll chips. This prevents users from utilizing click-to-roll features inside Owlbear Rodeo's Forge extension.

## What Changes

- **Automatic Roll Detection**: The Hugo build will parse descriptions for standard D&D 5e roll patterns (e.g., "+X to hit", "XdY + Z" damage) in monster and character statistics.
- **Chip Notation Conversion**: Detected rolls will be formatted as Forge-compatible chips (e.g., `[1d20+X]` for attack rolls, `[XdY+Z]` for damage/healing rolls).
- **Dynamic Character Weapon Calculations**: For characters, weapon actions will dynamically calculate the attack bonus (`Proficiency Bonus + Attribute Modifier + Weapon Magic Bonus`) and damage modifier based on the weapon's properties (Finesse, Thrown, or Ranged) and the character's Strength/Dexterity attributes, converting the rolls into interactive chips (e.g., `[1d20+7]` and `[1d6+5]`).
- **Spell Details Enrichment**: Character spell lists will resolve spell metadata (cast time, range, components, duration) and descriptions from the compendium, formatting all inline dice rolls as clickable chips.
- **Improved Action Mapping**: Parse monster and character actions, traits, reactions, bonus actions, and legendary actions from their descriptions or Markdown body, applying the roll-to-chip parser.

## Capabilities

### New Capabilities

<!-- None -->

### Modified Capabilities

- `content-model`: Extend the Forge export requirements to cover automatic roll-to-chip transformation and dynamic character modifier calculations for actions, spells, and items.

## Impact

- **Affected Layouts**: `layouts/partials/helpers/forge_statblock.html` and `layouts/index.forge.json`.
- **Backward Compatibility**: Fully backward-compatible. Markdown file structures, metadata schemas, and existing GM Vault JSON exports remain completely unaffected.
