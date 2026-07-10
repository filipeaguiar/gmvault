# compendium Specification

## Purpose
Define the global reusable compendium and how campaign and character pages reference compendium entities.

## Requirements

### Requirement: Global compendium is separate from campaigns
Reusable rules content SHALL live under `content/compendium/` and SHALL not belong to any single campaign.

#### Scenario: Compendium index is opened
- **WHEN** the compendium section page is rendered
- **THEN** it SHALL show child sections or pages for reusable global content

### Requirement: Compendium supports core RPG entity kinds
The compendium SHALL support monsters, items, magic items, classes, races, feats, spells, backgrounds, conditions, and rules.

#### Scenario: Entity page exists
- **WHEN** a compendium entity page is rendered
- **THEN** the layout SHALL display its title, content, and metadata using either a kind-specific partial or the default page renderer

#### Scenario: Monster page exists
- **WHEN** a monster page has stat block metadata
- **THEN** the monster renderer SHALL display a stat block-oriented view before or alongside the Markdown content

### Requirement: Campaign pages can reference compendium pages
Campaign-scoped pages SHALL be able to reference compendium pages through URL lists in front matter.

#### Scenario: Compendium reference resolves
- **WHEN** a page contains a `compendium_refs` list with internal URLs
- **THEN** the relationships renderer SHALL resolve each URL with `site.GetPage` and display the referenced page title as a link

#### Scenario: Compendium reference is missing
- **WHEN** a URL in `compendium_refs` cannot be resolved
- **THEN** the relationships renderer SHALL display the raw path as a broken-link fallback instead of failing the build

### Requirement: Player character pages group compendium references
Character pages SHALL group referenced compendium pages into useful player-facing sections such as class and race, class features, spells, feats, and equipment.

#### Scenario: Character references spells
- **WHEN** a character page references spell pages
- **THEN** the character renderer SHALL group spells by level and show compact casting metadata when available

#### Scenario: Character references items or magic items
- **WHEN** a character page references item or magic item pages
- **THEN** the character renderer SHALL show those references in an equipment-oriented section
