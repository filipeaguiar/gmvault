## MODIFIED Requirements

### Requirement: Child page navigation is automatic
Section pages SHALL automatically list child pages as cards using title, summary, icon, and kind metadata when available, while respecting the current page visibility context. Collection pages intended to navigate GM material SHALL use GM visibility so that GM child pages can be listed without weakening public/player navigation restrictions.

#### Scenario: Section has children
- **WHEN** a list page has child pages
- **THEN** it SHALL render a navigable card grid ordered by weight

#### Scenario: Player-facing section has GM child
- **WHEN** a list page has `visibility: players` or `visibility: public` and a child page has `visibility: gm` or missing visibility
- **THEN** automatic child navigation SHALL omit that child page

#### Scenario: GM campaign collection has GM campaign children
- **WHEN** the campaign collection index has GM visibility and child campaign pages have GM visibility
- **THEN** automatic child navigation SHALL include those campaign pages when they are part of the current Hugo build

#### Scenario: Draft campaign child is not built
- **WHEN** a campaign child page has `draft: true` and Hugo is run without drafts enabled
- **THEN** automatic child navigation SHALL NOT list that campaign because the page is not part of the build

#### Scenario: Child is a subordinate class or race item
- **WHEN** a child page marks itself as a subordinate item using parent metadata
- **THEN** automatic child navigation SHALL omit it from the main card grid
