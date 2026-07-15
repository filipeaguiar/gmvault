## MODIFIED Requirements

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
