## ADDED Requirements

### Requirement: Character spell references resolve canonical compendium spells
Every spell association produced for a character SHALL resolve to a canonical page under `content/compendium/spells/`. The compendium page SHALL own shared spell identity, level, descriptive content, casting metadata, and structured roll metadata, while the character note SHALL retain only the internal reference and character-specific operational state.

#### Scenario: New character spell is associated
- **WHEN** a character creation, editing, or import flow adds a spell supported by the 5e.tools source data
- **THEN** the system SHALL create or synchronize its canonical compendium page
- **THEN** the character entry SHALL reference that page by internal URL

#### Scenario: Character uses canonical spell metadata
- **WHEN** the character renderer resolves a spell reference
- **THEN** it SHALL use `spell_info` and content from the compendium page instead of requiring duplicated title, level, description, or roll mechanics in the character note

#### Scenario: Character retains operational spell state
- **WHEN** a spell has preparation, availability, source, or character-specific usage state
- **THEN** the character note SHALL preserve that operational state alongside the spell reference
- **THEN** the compendium page SHALL remain reusable by other characters

#### Scenario: Existing reviewed spell page is synchronized
- **WHEN** the 5e.tools flow refreshes shared metadata for an existing translated or editorially reviewed spell page
- **THEN** the synchronization SHALL preserve local editorial front matter and reviewed Markdown body according to the repository's non-destructive compendium update rules

### Requirement: Character spell references are normalized and deduplicated
The character spell rendering flow SHALL normalize spell references from operational entries, class catalogs, and general compendium references into one collection keyed by canonical internal URL. Operational state SHALL take precedence over catalog-only data, and a spell SHALL appear no more than once in either rendered list.

#### Scenario: Spell exists in multiple character fields
- **WHEN** the same spell URL occurs in `char_info.spells`, `char_info.class_spells`, and `compendium_refs`
- **THEN** the normalized collection SHALL contain one spell association
- **THEN** state from `char_info.spells` SHALL take precedence

#### Scenario: General reference is not a spell
- **WHEN** `compendium_refs` contains class, feat, item, rule, and spell pages
- **THEN** only resolved pages whose kind is `spell` SHALL enter the spell collection

#### Scenario: Duplicate names have distinct canonical references
- **WHEN** two source entities share a display name but resolve to distinct canonical URLs
- **THEN** deduplication SHALL use the canonical URL rather than display text
