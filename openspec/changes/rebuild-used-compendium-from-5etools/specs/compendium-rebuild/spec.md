## ADDED Requirements

### Requirement: Rebuild inventory follows transitive compendium references
The rebuild workflow SHALL discover compendium references in campaign and character YAML and Markdown and SHALL recursively follow references from selected compendium pages until reaching a fixed point.

#### Scenario: Direct and indirect references exist
- **WHEN** a character references a class page and that class page references feature rules
- **THEN** the inventory SHALL include the class and all reachable feature-rule pages

#### Scenario: Page is unreachable
- **WHEN** a compendium entity is not reachable from any campaign or character reference
- **THEN** the inventory SHALL classify it as unused

### Requirement: Rebuild produces a reviewable manifest
The workflow SHALL create a manifest containing each selected internal URL, entity kind, canonical name, selected 5e.tools source, remote identity, resolution status, and selection reason.

#### Scenario: Multiple sources contain the same name
- **WHEN** an entity name resolves to more than one 5e.tools source
- **THEN** the manifest SHALL record the source selected by policy and the reason for that selection

#### Scenario: Entity cannot be resolved safely
- **WHEN** a required entity is missing or remains ambiguous
- **THEN** validation SHALL fail and promotion SHALL be blocked

### Requirement: Rebuild uses staging before promotion
Downloads and generated Markdown SHALL be written to a staging area and SHALL NOT overwrite the active compendium during scan, resolution, generation, or validation.

#### Scenario: Remote download fails
- **WHEN** a 5e.tools request fails during reconstruction
- **THEN** the active compendium SHALL remain unchanged

#### Scenario: Staging passes validation
- **WHEN** every required entity resolves and all validations pass
- **THEN** the operator MAY explicitly promote the staged compendium

### Requirement: Promotion removes unused entities
Promotion SHALL remove entity pages outside the current transitive closure while preserving compendium indexes and reserved non-entity files.

#### Scenario: Unused entity is present
- **WHEN** a successful promotion finds an entity classified as unused by the current manifest
- **THEN** that entity file SHALL be removed from the active compendium

#### Scenario: Files changed after inventory
- **WHEN** compendium or campaign inputs change after the manifest scan
- **THEN** promotion SHALL require a new scan rather than applying a stale deletion list

### Requirement: Rebuild preserves required URLs
Generated pages SHALL preserve the existing internal slugs and URLs used by campaigns, characters, and reachable compendium dependencies.

#### Scenario: Existing required spell is rebuilt
- **WHEN** `/compendium/spells/guidance/` is selected and regenerated
- **THEN** the generated page SHALL remain resolvable at `/compendium/spells/guidance/`

### Requirement: Rebuild validates generated content
The workflow SHALL validate YAML, required schema fields, references, unresolved source tags, duplicate slugs, and Hugo builds before promotion.

#### Scenario: Generated page contains invalid YAML
- **WHEN** staging validation encounters invalid front matter
- **THEN** validation SHALL fail and promotion SHALL be blocked

#### Scenario: All checks pass
- **WHEN** schema, references, source tags, slugs, tests, and Hugo builds are valid
- **THEN** the workflow SHALL report staging as eligible for explicit promotion
