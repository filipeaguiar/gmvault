## Context

Currently, character class level features are populated directly from D&D Beyond's API `classFeatures` snippet. While this works, it can include homebrew details or poorly formatted snippets, does not cover subclass features from 5e.tools variants systematically, and lacks unified translation capabilities. In 5e.tools, each class and subclass has a complete list of level-specific features in `classFeature` and `subclassFeature` structures. We want to extract these features directly from the 5e.tools local or remote JSON files, translate them, write them as `/compendium/rules/<slug>.md` rules, and reference them in character sheets and the Forge card export.

## Goals / Non-Goals

**Goals:**
- Update `import_dndbeyond.py` to extract class and subclass level features from 5e.tools class JSON data based on character level.
- Save each level feature as a compendium rule (`/compendium/rules/<feature-slug>.md`) in `draft` status so it can be translated.
- Reference these rules in the character's `compendium_refs` in their markdown file.
- Update `layouts/partials/helpers/forge_statblock.html` to automatically extract and include all rule and feat references from `compendium_refs` in the Forge `abilities` array (`Z034`) for characters.

**Non-Goals:**
- Manually translate all D&D level features now (translation is handled by the `translate_drafts.py` pipeline).
- Change the core structure of the compendium layout.

## Decisions

- **Decision 1: Extract features from 5e.tools rather than D&D Beyond API**
  - *Rationale*: 5e.tools features are cleanly formatted and official. D&D Beyond API features often include formatting noise or custom/homebrew modifications.
- **Decision 2: Map subclass features to `compendium/rules/`**
  - *Rationale*: Level features are individual features (e.g., "Rage", "Evasion") rather than standalone classes/subclasses. Storing them as rules aligns with how other class/subclass features are handled.
- **Decision 3: Include all referenced rules/feats in Forge Z034 for characters**
  - *Rationale*: Currently, character cards in Forge export have empty `Z034` (abilities/features) lists. Populating Z034 using `compendium_refs` pointing to kind `rule` or `feat` provides the features/traits space with complete character features without bloating the main character markdown structure.

## Risks / Trade-offs

- [Risk] Large amount of rule files created in `/compendium/rules/`.
  - *Mitigation*: These files are lightweight Markdown drafts. They will be translated and ignored/built by Hugo without performance impact.
