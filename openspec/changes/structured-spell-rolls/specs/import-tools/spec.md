## ADDED Requirements

### Requirement: Spell imports extract structured roll metadata from 5e.tools
Import tools that create or synchronize spell compendium pages SHALL inspect `entries`, `entriesHigherLevel`, `scalingLevelDice`, `spellAttack`, `damageInflict`, `savingThrow`, and `miscTags` and SHALL write normalized mechanical metadata under `spell_info`.

#### Scenario: Import reads nested roll tags
- **WHEN** a roll tag occurs in a nested entries block or higher-level block
- **THEN** the importer SHALL include it in structured extraction rather than requiring it to appear in a top-level string

#### Scenario: Import preserves inline roll markup
- **WHEN** the importer extracts a roll into `spell_info.rolls`
- **THEN** it SHALL continue converting the original body tag into readable dice-friendly markup

#### Scenario: Import reads cantrip scaling table
- **WHEN** a spell contains `scalingLevelDice` as an object or a list of labeled scaling objects
- **THEN** the importer SHALL preserve each character-level threshold and formula in structured metadata

#### Scenario: Import distinguishes continuous and discrete slot scaling
- **WHEN** scaled tags contain `1-9` or `3,5,7,9` progression syntax
- **THEN** the importer SHALL normalize the correct slot thresholds without inventing intermediate increments

#### Scenario: Higher-level effect is prose-only
- **WHEN** entriesHigherLevel describes additional projectiles but provides no scaled tag or structured count field
- **THEN** the importer SHALL preserve the prose and base roll but SHALL NOT infer an aggregate dice formula

### Requirement: Spell metadata synchronization is non-destructive
When a spell page already exists locally, synchronization SHALL update its structured `spell_info` while preserving editorial front matter, translation metadata, title overrides, and Markdown body.

#### Scenario: Translated spell is synchronized
- **WHEN** an existing translated Fireball page is synchronized with current 5e.tools data
- **THEN** its translation metadata and Markdown body SHALL remain unchanged while roll metadata is updated

#### Scenario: Source spell cannot be resolved
- **WHEN** a local spell has no matching source record
- **THEN** synchronization SHALL report the unresolved page and SHALL NOT remove or rewrite its existing metadata
