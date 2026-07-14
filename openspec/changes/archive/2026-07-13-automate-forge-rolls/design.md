## Context

Owlbear Rodeo's Forge extension uses a specific JSON metadata schema to define interactive unit sheets. Within list-based attributes (such as `Z034` Abilities, `Z035` Actions, etc.), any text formatted in square brackets (e.g. `[1d20+5]` or `[2d6+3]`) is rendered as a clickable dice roll chip.

Currently, the GM Vault's Hugo build generates the Forge export `/exports/forge/statblocks.json` with plain text descriptions. This design details how we will modify the Hugo layout templates to parse description text at build time, automatically wrap roll expressions in Forge chip notation, dynamically calculate weapon attack/damage modifiers for characters, and enrich spell details from the compendium.

## Goals / Non-Goals

**Goals:**
- Implement regex-based roll parsing at build time using Hugo template functions.
- Support conversion of attack rolls (e.g., `+5 to hit` -> `[1d20+5] to hit`).
- Support conversion of standard dice equations (e.g., `2d8 + 4` -> `[2d8+4]`).
- Dynamically calculate character attack bonuses and damage modifiers for weapons in their inventory, resolving the correct attribute (Strength vs Dexterity) based on Finesse/Range properties and adding the calculated proficiency bonus.
- Enrich spell entries (`Z039`) with descriptions and metadata (cast time, range, components, duration) resolved from compendium pages.
- Parse monster abilities and actions from their Markdown body sections.

**Non-Goals:**
- Changing the structure or content of the GM Vault JSON export.
- Implementing complex formula calculations (e.g., dynamic level-scaling) in Hugo templates.

## Decisions

### Decision 1: Create a central `forge_roll_parser.html` Hugo partial
- **Approach**: Define a helper partial `/layouts/partials/helpers/forge_roll_parser.html` that accepts a description string and returns the string with roll chips injected.
- **Rationale**: Reusable across multiple different sections (actions, abilities, items) in `forge_statblock.html`.
- **Alternatives Considered**: Inline regex replacement in `forge_statblock.html`. Rejected to prevent code duplication and keep the main statblock builder maintainable.

### Decision 2: Regex replacement patterns
- **Patterns**:
  - *Attack Rolls*: Match `([+-]\d+)\s*(?:to\s+hit|para\s+acertar)` and replace with `[1d20$1] to hit` or `[1d20$1] para acertar`. Since `$1` contains the sign (e.g. `+5` or `-2`), this translates to `[1d20+5]` or `[1d20-2]`.
  - *Dice Formulas*: Match `\b(\d+d\d+(?:\s*[+-]\s*\d+)?)\b` and wrap it as `[$1]`, removing any internal spaces (e.g., `2d6 + 3` becomes `[2d6+3]`).
  - *Double Bracket Cleanup*: Convert `\[\[([^\]]+)\]\]` to `[$1]` to easily support existing 5e.tools-imported markdown dice notation.

### Decision 3: Character Weapon Calculations
- **Logic**:
  - Calculate `Strength Modifier` and `Dexterity Modifier` using `floor((Attr - 10) / 2)`.
  - Calculate `Proficiency Bonus` based on total level: `floor((level - 1) / 4) + 2`.
  - Read weapon properties from the item page's `properties` field or description. If it contains `finesse`, `ranged`, `distância`, or `alcance`, use the maximum of Dex or Str. Otherwise, use Str.
  - Compute total attack bonus: `Attr Modifier + Proficiency Bonus + Weapon Magic Bonus`.
  - Compute total damage modifier: `Attr Modifier + Weapon Magic Bonus`.
  - Format the attack description string and pass it through the roll parser.

### Decision 4: Spell Details Resolution
- **Logic**:
  - For each spell in the character's list, locate the compendium page at `/compendium/spells/<spell-name>/`.
  - Extract spell details (`cast_time`, `range`, `components`, `duration`) and prepend them as a formatted header.
  - Append the spell's body content (`.RawContent`).
  - Run the entire string through the `forge_roll_parser.html` to generate roll chips.

## Risks / Trade-offs

- **Risk**: Fragile regex matches on custom/non-standard descriptions.
- **Mitigation**: Use conservative regex boundaries (`\b` and explicit keywords like `to hit`/`para acertar`) to avoid modifying plain text numbers or unrelated formats.
