# compendium Specification

## Purpose
Define the global reusable compendium and how campaign and character pages reference compendium entities.
## Requirements
### Requirement: Global compendium is separate from campaigns
Reusable rules content SHALL live under `content/compendium/` and SHALL not belong to any single campaign. The global compendium index SHALL show canonical child sections as organized navigation groups with counts and safe fallback behavior.

#### Scenario: Compendium index is opened
- **WHEN** the compendium section page is rendered
- **THEN** it SHALL show the canonical child sections as organized navigation groups, with a title, icon, summary when available, and count of visible pages for each section; it SHALL not require users to scan one undifferentiated list of all content pages.

#### Scenario: Compendium index displays canonical sections
- **WHEN** the compendium root contains sections for monsters, items, magic items, classes, races/species, feats, spells, backgrounds, conditions, or rules
- **THEN** the index SHALL render each available section as a separate navigable group or card with its resolved title, icon, summary, and visible-page count.

#### Scenario: Empty or unknown compendium section
- **WHEN** a compendium section has no visible child pages or has an unrecognized directory/category
- **THEN** the index SHALL omit empty groups and SHALL render an unknown non-empty section through a generic fallback without failing the build.

### Requirement: Compendium supports core RPG entity kinds
The compendium SHALL support monsters, items, magic items, classes, races, feats, spells, backgrounds, conditions, and rules. Item and magic item pages SHALL use mapped values in `item_info` fields, not raw 5e.tools abbreviations.

#### Scenario: Entity page exists
- **WHEN** a compendium entity page is rendered
- **THEN** the layout SHALL display its title, content, and metadata using either a kind-specific partial or the default page renderer

#### Scenario: Monster page exists
- **WHEN** a monster page has stat block metadata
- **THEN** the monster renderer SHALL display a stat block-oriented view before or alongside the Markdown content

#### Scenario: Weapon item has mapped item_info
- **WHEN** a weapon item page has `item_info.type` containing a 5e.tools type code like `M|XPHB`
- **THEN** the compendium rebuild process SHALL map it to `Weapon` (melee) or `Weapon` (ranged)
- **THEN** the `damage_type` SHALL be mapped from abbreviation to full name (e.g., `P` → `piercing`)
- **THEN** the `properties` SHALL be mapped from abbreviations to full names (e.g., `F|XPHB` → `finesse`)

#### Scenario: Armor item has mapped item_info
- **WHEN** an armor item page has `item_info.type` containing a 5e.tools type code like `LA|XPHB`
- **THEN** the compendium rebuild process SHALL map it to `Light Armor`, `Medium Armor`, `Heavy Armor`, or `Shield`

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

### Requirement: Class progression pages have structured visual presentation
Class pages in the compendium SHALL render their title, metadata, progression content grouped by level, level entries, and subclass links with a coherent visual hierarchy. Internal compendium links SHALL use project styling instead of relying on default browser link presentation. The grouped progression HTML SHALL remain reusable when the class page is embedded in a character sheet.

#### Scenario: Class feature card displays with equipment-like layout
- **WHEN** a character sheet renders class features
- **THEN** each feature SHALL use the `equipment-card` visual pattern with icon container, heading, and badges
- **THEN** the card SHALL have a colored left border distinguishing it from equipment cards

#### Scenario: Class feature card shows level badge
- **WHEN** a class feature has level metadata available
- **THEN** the card SHALL display a badge with the level number

#### Scenario: Class feature card shows source badge
- **WHEN** a class feature is rendered
- **THEN** the card SHALL display a badge indicating the source ("Classe" or "Subclasse")

#### Scenario: Class feature card preserves content
- **WHEN** a class feature card is rendered
- **THEN** the compendium content SHALL remain visible below the header

#### Scenario: Class page displays progression hierarchy
- **WHEN** a class page contains Markdown headings and level-based progression entries
- **THEN** the page SHALL present the resolved class name, metadata, level headings, and entries with distinguishable spacing, colors, borders, and typography suitable for quick consultation, without repeating generic progression titles.

#### Scenario: Localized class title is available
- **WHEN** a class page has `titulo_pt_br` in its front matter
- **THEN** the page SHALL use `titulo_pt_br` as the visible class name and SHALL use `title` only as fallback.

#### Scenario: Progression entries are grouped by level
- **WHEN** consecutive progression entries belong to the same character level
- **THEN** the page SHALL place them under one visible level heading, and SHALL start a new group when the level changes.

#### Scenario: Grouped progression is reused in a character sheet
- **WHEN** a character sheet renders the referenced class progression page
- **THEN** the same level headings and grouped entries SHALL remain visible without requiring duplicated class-rule content in the character front matter.

#### Scenario: Progression entry links to compendium content
- **WHEN** a progression entry contains an internal link to a rule or feature page
- **THEN** the link SHALL retain its destination, SHALL respect the configured site base path, and SHALL use the compendium link style with visible hover and keyboard focus states.

#### Scenario: Missing feature page is generated
- **WHEN** a class progression references a feature whose compendium page does not exist
- **THEN** the import/generation flow SHALL create a rule page with the available feature text and SHALL link the progression entry to that page instead of rendering an unresolved URL.

#### Scenario: Feature content is available in character context
- **WHEN** a character sheet renders a referenced class progression
- **THEN** each linked feature SHALL expose its corresponding compendium text through the existing character-content resolution without duplicating the rule text in the character front matter.

#### Scenario: Class page displays subclasses
- **WHEN** a class has child pages with `parent_class`
- **THEN** the subclass section SHALL render each child with a styled title, project icon, summary when available, and accessible internal link.

#### Scenario: Class page is rendered in a narrow viewport
- **WHEN** the class page is displayed in a notebook, mobile viewport, or narrow iframe
- **THEN** progression entries and links SHALL wrap or collapse to a single-column layout without horizontal overflow.

#### Scenario: Visual decoration is rendered
- **WHEN** icons and decorative elements are added to the class progression
- **THEN** the implementation SHALL use existing CSS icon classes and SHALL NOT add Unicode symbols or emoji characters as decoration.

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

