## ADDED Requirements

### Requirement: Index pages provide ordered navigation
Index and section pages SHALL present child pages in a deterministic navigation order suitable for use during a live RPG session.

#### Scenario: Child pages have weights
- **WHEN** a section page renders child pages with `weight` metadata
- **THEN** the index SHALL order those children by ascending weight before less-specific ordering

#### Scenario: Child pages have equal or missing weights
- **WHEN** child pages have equal or missing `weight` values
- **THEN** the index SHALL use a stable title-based order as the effective tie breaker where practical

### Requirement: Index cards are informative without being noisy
Index pages SHALL show each visible child with title, summary when available, and compact metadata such as kind/status when available.

#### Scenario: Child has summary and kind
- **WHEN** a visible child page has summary and kind metadata
- **THEN** the index card SHALL display the resolved title, summary, and compact kind badge

#### Scenario: Child lacks summary
- **WHEN** a visible child page lacks summary metadata
- **THEN** the index SHALL still render a usable navigation item without requiring summary text

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
