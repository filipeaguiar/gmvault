# index-layout Specification

## Purpose
TBD - created by archiving change improve-index-layout-responsive-iframe. Update Purpose after archive.
## Requirements
### Requirement: Index pages provide ordered navigation
Index and section pages SHALL present child pages in deterministic navigation groups suitable for use during a live RPG session. Groups SHALL be derived from the canonical section/directory and, for pages within a section, from `kind`, legacy `params.kind`, or a generic fallback. Pages within each group SHALL be ordered by ascending `weight` and then by title where practical.

#### Scenario: Child pages are grouped by available metadata
- **WHEN** an index contains visible child pages with `kind`, legacy `params.kind`, or only a directory/category context
- **THEN** the index SHALL place each page in the corresponding group and SHALL provide a generic fallback group when no more specific classification is available.

#### Scenario: Child pages have weights
- **WHEN** a group renders child pages with `weight` metadata
- **THEN** the group SHALL order those children by ascending weight before less-specific ordering.

#### Scenario: Child pages have equal or missing weights
- **WHEN** child pages in a group have equal or missing `weight` values
- **THEN** the index SHALL use a stable title-based order as the effective tie breaker where practical.

#### Scenario: Public index filters groups and counts
- **WHEN** an index page has `visibility: players` or `visibility: public`
- **THEN** it SHALL exclude GM-only or unknown-visibility children from groups and counts, preserving the existing spoiler-navigation rule.

### Requirement: Index cards are informative without being noisy
Index pages SHALL show each visible child inside its category group with title, summary when available, and compact metadata such as kind/status when available. Each non-empty group SHALL expose a readable heading and visible-page count without rendering full child-page content.

#### Scenario: Child has summary and kind
- **WHEN** a visible child page has summary and kind metadata
- **THEN** the index card SHALL display the resolved title, summary, compact kind badge, and status when available inside its category group.

#### Scenario: Child lacks summary
- **WHEN** a visible child page lacks summary metadata
- **THEN** the index SHALL still render a usable navigation card using the title and available metadata without requiring summary text.

#### Scenario: Group has many child pages
- **WHEN** a category group contains many visible child pages
- **THEN** the index SHALL preserve compact cards and responsive grid behavior rather than embedding full Markdown descriptions for every child.

### Requirement: Index layout adapts to iframe width
Index pages SHALL remain usable inside narrow iframes without horizontal overflow or hidden navigation controls.

#### Scenario: Width is narrow
- **WHEN** the available viewport or iframe width is small
- **THEN** index navigation SHALL collapse to a single-column or compact layout that preserves readable titles and tappable links

#### Scenario: Width is wider
- **WHEN** the available viewport or iframe width supports multiple columns
- **THEN** index navigation MAY use a card grid to improve scanning efficiency

### Requirement: Index pages avoid player spoiler navigation
Index pages rendered from player/public contexts SHALL omit generated links to pages that are GM-only or have unknown visibility.

#### Scenario: Player-facing index has GM child
- **WHEN** an index page has `visibility: players` or `visibility: public` and one child has `visibility: gm`
- **THEN** the GM child SHALL be omitted from the generated index navigation

#### Scenario: Player-facing index has child without visibility
- **WHEN** an index page has `visibility: players` or `visibility: public` and one child lacks `visibility`
- **THEN** the child SHALL be treated as GM-only for generated player-facing navigation and omitted

#### Scenario: GM index has GM child
- **WHEN** an index page has GM visibility
- **THEN** generated index navigation MAY include GM child pages

### Requirement: Class and subclass layouts resolve related feature pages
Class and subclass layouts SHALL resolve feature URLs from their rendered progression content through `site.GetPage` and use a shared inline-description presentation.

#### Scenario: Layout renders a class progression
- **WHEN** the class layout encounters an internal compendium feature URL in the progression
- **THEN** it SHALL delegate presentation to the shared inline-description partial

### Requirement: Adventure indexes list simplified sessions
Adventure pages SHALL list direct child and nested session child scene pages.

#### Scenario: Adventure has direct session children
- **WHEN** an adventure page has direct child branch bundles with `kind: session`
- **THEN** the adventure index navigation SHALL collect scenes and display them directly in the scene timeline

#### Scenario: Adventure has legacy sessions section
- **WHEN** an adventure page has legacy sessions under `sessions/<session-slug>/`
- **THEN** the adventure index navigation SHALL collect and display all their scenes directly in the scene timeline

### Requirement: Session indexes list simplified scenes
Session pages SHALL list direct child scene pages when using the simplified hierarchy.

#### Scenario: Session has direct scene children
- **WHEN** a session page has direct child pages with `kind: scene`
- **THEN** the session index navigation SHALL display those scenes as navigable children

#### Scenario: Session has legacy scenes section
- **WHEN** a session page has legacy scenes under `scenes/<scene-slug>.md`
- **THEN** the session index navigation SHALL continue to display those scenes

