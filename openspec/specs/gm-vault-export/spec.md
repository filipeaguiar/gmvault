# gm-vault-export Specification

## Purpose
Define the Hugo-generated GMVault JSON export used by external campaign or GM tools.
## Requirements
### Requirement: Site exposes GMVault JSON output
The Hugo configuration SHALL define a `GMVault` JSON output format named `gm-vault.json` for the home page and section pages.

#### Scenario: Site builds
- **WHEN** Hugo renders the home page or a section configured for the GMVault output format
- **THEN** it SHALL emit a JSON document using the `application/json` media type and `gm-vault` base name

### Requirement: Campaign export mirrors campaign play hierarchy
Campaign GMVault JSON SHALL serialize campaign material into categories suitable for external GM tools and SHALL detect adventures, sessions, and scenes by `kind` metadata across both simplified and legacy campaign hierarchies.

#### Scenario: Campaign has adventures
- **WHEN** a campaign page is rendered as GMVault JSON
- **THEN** the export SHALL include an `Aventuras` category containing adventure categories

### Requirement: Campaign handouts are exported
Campaign GMVault JSON SHALL include campaign-scoped handouts as a dedicated category when a campaign has a `handouts/` section.

#### Scenario: Campaign has handouts
- **WHEN** a campaign page has a `handouts/` section
- **THEN** the export SHALL include a `Handouts` category containing the handout pages

#### Scenario: Adventure has simplified sessions and scenes
- **WHEN** an adventure contains direct child session pages and those sessions contain direct child scene pages
- **THEN** the export SHALL nest sessions and scenes under the relevant adventure category

#### Scenario: Adventure has legacy sessions and scenes
- **WHEN** an adventure contains session sections under `sessions/` and scene pages under `scenes/`
- **THEN** the export SHALL nest sessions and scenes under the relevant adventure category

#### Scenario: Mixed hierarchy exists during transition
- **WHEN** an adventure contains a mix of simplified and legacy session or scene locations
- **THEN** the export SHALL include all valid session and scene pages without duplicating the same page

### Requirement: Export items have stable generated identifiers
Exported pages and categories SHALL include deterministic generated IDs derived from their permalink or category context.

#### Scenario: Page item is exported
- **WHEN** a page is included in GMVault JSON
- **THEN** the item SHALL include type `page`, display name, URL, and an ID prefixed with `page_`

#### Scenario: Category item is exported
- **WHEN** a category is included in GMVault JSON
- **THEN** the item SHALL include type `category`, display name, child items, and an ID prefixed with `cat_`

### Requirement: Player-visible export flag is preserved
Exported page items SHALL indicate when source pages are intended for player visibility.

#### Scenario: Player-visible page is exported
- **WHEN** a page has `visibility: players` or `visibility: public`
- **THEN** the exported item SHALL include `visibleToPlayers: true`

#### Scenario: GM-only page is exported
- **WHEN** a page does not have player or public visibility
- **THEN** the exported item SHALL omit `visibleToPlayers`

