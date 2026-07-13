# forge-statblock-export Specification

## Purpose
Define the Hugo-generated Forge JSON export format and the requirements for mapping and ordering character and monster pages into the Forge statblock structure.

## Requirements

### Requirement: Site generates a Forge statblock export
The Hugo build SHALL generate a JSON file at `/exports/forge/statblocks.json` using a dedicated output format, without requiring a post-build script.

#### Scenario: Production build generates Forge JSON
- **WHEN** the maintainer runs `hugo --gc --minify`
- **THEN** the build SHALL create `public/exports/forge/statblocks.json` with a JSON array as its root value

#### Scenario: Forge export is independent from GM Vault export
- **WHEN** Hugo generates the Forge output
- **THEN** the existing `gm-vault.json` outputs SHALL remain available and unchanged in their structure

### Requirement: Characters and monsters are exported as Forge records
The Forge export SHALL include every effective `character` page and every effective `monster` page available in the Hugo site, including pages with incomplete structured statistics.

#### Scenario: Character is exported
- **WHEN** a page resolves to kind `character`
- **THEN** the Forge array SHALL contain one record for that page

#### Scenario: Monster is exported
- **WHEN** a page resolves to kind `monster`
- **THEN** the Forge array SHALL contain one record for that page

#### Scenario: Incomplete monster statistics exist
- **WHEN** a monster page has no complete `stats` map
- **THEN** the Forge export SHALL still contain the monster identity and available metadata instead of omitting the record

### Requirement: Forge records use the expected envelope and metadata
Each Forge record SHALL contain `id`, `name`, `author`, `metadata`, `favorite`, and `updatedAt`. The metadata SHALL include the Forge namespaced identity and party fields and SHALL map available character `char_info` or monster `stats` values to the documented compact Forge keys.

#### Scenario: Record envelope is generated
- **WHEN** a character or monster is exported
- **THEN** its record SHALL contain the required envelope fields and `metadata` SHALL be an object

#### Scenario: Character metadata is mapped
- **WHEN** a character has `char_info` with class, race, AC, HP, or ability scores
- **THEN** the record SHALL include its localized name, party marker, and the available values in the corresponding Forge metadata keys

#### Scenario: Monster metadata is mapped
- **WHEN** a monster has `stats` with AC, HP, speed, challenge rating, attributes, or skills
- **THEN** the record SHALL include its localized name, non-party marker, and the available values in the corresponding Forge metadata keys

#### Scenario: Missing source values are handled
- **WHEN** a source page lacks a value required by an optional Forge field
- **THEN** the exporter SHALL use the documented empty/default representation and SHALL continue generating the record

#### Scenario: Character references inventory items
- **WHEN** a character has `compendium_refs` pointing to item or magic item pages and no explicit inventory
- **THEN** the exporter SHALL create inventory entries in `Z040` with stable IDs, names, quantity, and available item description

#### Scenario: Inventory item has attack data
- **WHEN** an inventory item has structured damage data
- **THEN** the exporter SHALL expose a corresponding action in `Z035`; when attack data is absent, it SHALL not fabricate a roll

### Requirement: Forge records have stable ordering and identifiers
The Forge exporter SHALL emit characters before monsters, order each group deterministically by weight, localized name, and permalink, and derive a UUID-shaped stable identifier from the page permalink.

#### Scenario: Records are ordered
- **WHEN** the same content is built twice
- **THEN** the records SHALL appear in the same order, with characters before monsters

#### Scenario: Record identifier is stable
- **WHEN** a page permalink does not change between builds
- **THEN** its Forge `id` SHALL remain unchanged and SHALL be unique within the export
