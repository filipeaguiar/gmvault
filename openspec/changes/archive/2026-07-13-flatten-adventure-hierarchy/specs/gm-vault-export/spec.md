## MODIFIED Requirements

### Requirement: Campaign export mirrors campaign play hierarchy
Campaign GMVault JSON SHALL serialize campaign material into categories suitable for external GM tools and SHALL detect adventures and scenes by `kind` metadata, nesting scenes directly under adventures across both simplified and legacy campaign hierarchies.

#### Scenario: Campaign has adventures
- **WHEN** a campaign page is rendered as GMVault JSON
- **THEN** the export SHALL include an `Aventuras` category containing adventure categories

#### Scenario: Adventure has simplified sessions and scenes
- **WHEN** an adventure contains direct child session pages and those sessions contain direct child scene pages
- **THEN** the export SHALL flatten the hierarchy and list all those scenes directly in the adventure's scenes category

#### Scenario: Adventure has legacy sessions and scenes
- **WHEN** an adventure contains session sections under `sessions/` and scene pages under `scenes/`
- **THEN** the export SHALL flatten the hierarchy and list all those scenes directly in the adventure's scenes category

#### Scenario: Mixed hierarchy exists during transition
- **WHEN** an adventure contains a mix of simplified and legacy session or scene locations
- **THEN** the export SHALL flatten the hierarchy and list all valid scene pages directly without duplicating any page
