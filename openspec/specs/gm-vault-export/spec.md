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
Campaign GMVault JSON SHALL serialize campaign material into categories suitable for external GM tools and SHALL detect adventures, sessions, and scenes by `kind` metadata across both simplified and legacy campaign hierarchies. Within each adventure category, valid scene pages SHALL be listed directly as items rather than under an intermediate scenes category.

#### Scenario: Campaign has adventures
- **WHEN** a campaign page is rendered as GMVault JSON
- **THEN** the export SHALL include an `Aventuras` category containing adventure categories

#### Scenario: Adventure has simplified sessions and scenes
- **WHEN** an adventure contains direct child session pages and those sessions contain direct child scene pages
- **THEN** the export SHALL list all those scene pages directly in the relevant adventure category

#### Scenario: Adventure has legacy sessions and scenes
- **WHEN** an adventure contains session sections under `sessions/` and scene pages under `scenes/`
- **THEN** the export SHALL list all those scene pages directly in the relevant adventure category

#### Scenario: Mixed hierarchy exists during transition
- **WHEN** an adventure contains a mix of simplified and legacy session or scene locations
- **THEN** the export SHALL include all valid scene pages directly in the relevant adventure category without duplicating the same page

### Requirement: Campaign handouts are exported
Campaign GMVault JSON SHALL include campaign-scoped handouts in a dedicated root category when a campaign has handouts not associated with an adventure. Each adventure SHALL include a dedicated `Handouts` category when its adventure or scene pages reference campaign handouts.

#### Scenario: Campaign has general handouts
- **WHEN** a campaign page has a `handouts/` section containing handouts that are not referenced by an adventure or its scenes
- **THEN** the export SHALL include those pages in a root `Handouts` category

#### Scenario: Adventure has referenced handouts
- **WHEN** an adventure or one of its scene pages contains `handouts` references
- **THEN** the export SHALL include the resolved handout pages in a `Handouts` category inside that adventure

#### Scenario: Handout is referenced more than once within an adventure
- **WHEN** the same handout is referenced by an adventure and multiple scene pages
- **THEN** the export SHALL include that handout only once in that adventure's `Handouts` category

#### Scenario: No general handouts exist
- **WHEN** every campaign handout is associated with at least one adventure or no handouts exist
- **THEN** the export SHALL omit the root `Handouts` category when it has no items

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

