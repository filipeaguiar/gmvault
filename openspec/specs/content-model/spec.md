# content-model Specification

## Purpose
Define the Markdown content structure for campaigns, adventures, sessions, scenes, support sections, metadata, and archetypes.
## Requirements
### Requirement: Markdown pages use YAML front matter
Every authored content page SHALL be represented as Markdown with YAML front matter containing editorial metadata that layouts can render or use for navigation. Layouts SHALL resolve `kind` from top-level front matter and SHALL also support legacy `params.kind` as a fallback.

#### Scenario: Page metadata is available
- **WHEN** a content page is rendered with top-level `kind`
- **THEN** the layouts SHALL be able to read title, summary, draft, weight, visibility, status, tags, and kind when those fields are provided

#### Scenario: Legacy nested kind is available
- **WHEN** a content page is rendered with `params.kind` and without top-level `kind`
- **THEN** the layouts SHALL treat `params.kind` as the page kind for kind-specific partials, icons, badges, breadcrumbs, and navigation decisions

#### Scenario: Both kind fields are available
- **WHEN** a content page has both top-level `kind` and `params.kind`
- **THEN** top-level `kind` SHALL take precedence

### Requirement: Campaign hierarchy is campaign adventure session scene
Campaign content SHALL be organized under `content/campaigns/<campaign-slug>/` with adventures, sessions, and scenes forming the operational play hierarchy. The canonical physical structure for new content SHALL place session branch bundles directly under their adventure and scene pages directly under their session, while legacy `sessions/` and `scenes/` collection directories remain supported for existing content. The campaign collection index at `content/campaigns/_index.md` SHALL be able to function as a GM navigation page that lists child campaign pages when visibility and draft build settings allow.

#### Scenario: Campaign collection index exists
- **WHEN** `content/campaigns/_index.md` exists as the campaign collection page
- **THEN** it SHALL be able to list child campaign pages through automatic child navigation when those pages are included in the current Hugo build and not hidden by visibility rules

#### Scenario: Campaign page exists
- **WHEN** a campaign `_index.md` exists
- **THEN** it SHALL act as the campaign landing page and expose campaign overview content plus links or cards for journal, characters, NPCs, locations, factions, handouts, and adventures when present

#### Scenario: Adventure pages exist
- **WHEN** an adventure exists under `adventures/<adventure-slug>/`
- **THEN** it SHALL be represented by an `_index.md` page and may contain direct child session branch bundles

#### Scenario: Simplified session pages exist
- **WHEN** a session exists under `adventures/<adventure-slug>/<session-slug>/_index.md`
- **THEN** it SHALL be treated as a session page and may contain direct child scene pages

#### Scenario: Simplified scene pages exist
- **WHEN** a scene exists under `adventures/<adventure-slug>/<session-slug>/<scene-slug>.md`
- **THEN** it SHALL be treated as a scene page with operational preparation content for play

#### Scenario: Legacy session pages exist
- **WHEN** a session exists under `adventures/<adventure-slug>/sessions/<session-slug>/_index.md`
- **THEN** it SHALL remain supported as a session page

#### Scenario: Legacy scene pages exist
- **WHEN** a scene exists under `adventures/<adventure-slug>/sessions/<session-slug>/scenes/<scene-slug>.md`
- **THEN** it SHALL remain supported as a scene page

### Requirement: Campaign support sections are first-class content
Campaigns SHALL support journal entries, characters, NPCs, locations, factions, and handouts as campaign-scoped content collections.

#### Scenario: Campaign support section exists
- **WHEN** a support section has child pages
- **THEN** list layouts SHALL display navigable cards or lists for those children

### Requirement: Archetypes exist for major page kinds
The repository SHALL include archetypes for creating the main campaign and compendium content kinds.

#### Scenario: New content is generated
- **WHEN** Hugo creates content using a project archetype
- **THEN** the generated Markdown SHALL include draft, weight, summary, visibility, status, tags, and kind-oriented metadata suitable for manual editing

### Requirement: Campaign pages expose their GM Vault export link
Campaign landing pages SHALL display a clickable and copyable URL for the campaign-specific `gm-vault.json` output.

#### Scenario: Campaign GM Vault link is rendered
- **WHEN** a campaign page has a `GMVault` output format
- **THEN** the page SHALL display a button configured to copy that campaign's generated `gm-vault.json` URL

#### Scenario: Campaign uses a base path
- **WHEN** the site `baseURL` contains a subpath such as `/gmvault/`
- **THEN** the displayed campaign export URL SHALL include the configured base path and campaign slug

#### Scenario: Campaign export URL can be copied
- **WHEN** the user clicks the campaign export button in a browser with Clipboard API support
- **THEN** the page SHALL call `navigator.clipboard.writeText` with the campaign JSON URL

### Requirement: Compendium pages expose the Forge export link
The Compendium landing page SHALL display a clickable and copyable URL for the global Forge statblock export.

#### Scenario: Compendium Forge link is rendered
- **WHEN** the Compendium landing page is rendered
- **THEN** it SHALL display a button configured to copy `/exports/forge/statblocks.json`

#### Scenario: Compendium Forge link is usable for import
- **WHEN** a user copies the displayed Forge URL
- **THEN** the URL SHALL resolve to the JSON array generated by the Hugo build

#### Scenario: Compendium Forge URL can be copied
- **WHEN** the user clicks the Forge export button in a browser with Clipboard API support
- **THEN** the page SHALL call `navigator.clipboard.writeText` with the Forge JSON URL

#### Scenario: Clipboard API is unavailable
- **WHEN** the browser does not provide Clipboard API support
- **THEN** the button SHALL display a copy failure status without exposing the URL as visible page text

### Requirement: Forge export formats descriptions into interactive roll chips
The Forge JSON statblock export layout SHALL parse and convert text roll notations in descriptions into Forge interactive roll chips.

#### Scenario: Attack modifier is parsed
- **WHEN** an action, ability, or item description contains a standard attack bonus notation like `+5 to hit` or `+6 para acertar`
- **THEN** the exporter SHALL convert it to a Forge roll chip `[1d20+5] to hit` or `[1d20+6] para acertar`

#### Scenario: Dice formula is parsed
- **WHEN** an action, ability, or item description contains a dice formula like `2d6 + 3` or `1d8`
- **THEN** the exporter SHALL convert it to a Forge roll chip `[2d6+3]` or `[1d8]`

#### Scenario: Multiple rolls are formatted
- **WHEN** a description containing multiple roll notations is exported
- **THEN** all instances of those notations SHALL be formatted as Forge roll chips

### Requirement: Character weapon attacks dynamically calculate bonuses
The Forge character exporter SHALL dynamically compute attack bonuses and damage modifiers for weapon actions based on character statistics and weapon properties.

#### Scenario: Finesse weapon uses dexterity
- **WHEN** a character has a higher Dexterity modifier than Strength modifier and uses a weapon with the Finesse property
- **THEN** the exporter SHALL calculate the attack bonus using the Dexterity modifier and proficiency bonus

#### Scenario: Heavy weapon uses strength
- **WHEN** a character uses a weapon without Finesse or Ranged properties (such as a Greataxe)
- **THEN** the exporter SHALL calculate the attack bonus using the Strength modifier and proficiency bonus

#### Scenario: Magic weapon bonus is added
- **WHEN** a weapon in the character's inventory has a positive magic bonus (e.g. `+1`)
- **THEN** the exporter SHALL add this bonus to both the calculated attack bonus and damage modifier chips

### Requirement: Spell list entries are enriched with compendium data
The Forge character exporter SHALL resolve spell definitions from the compendium to populate full descriptions and metadata for character spells.

#### Scenario: Spell details and description are resolved
- **WHEN** a character's spell is exported
- **THEN** the exporter SHALL fetch the corresponding spell page, prefix the cast time, range, components, and duration, append the spell's description, and convert all rolls to chips

