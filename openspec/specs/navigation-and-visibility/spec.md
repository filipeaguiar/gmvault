# navigation-and-visibility Specification

## Purpose
Define navigation, breadcrumb, relationship, and editorial visibility behavior for GM and player-facing pages.
## Requirements
### Requirement: Visibility is editorial metadata, not access control
The site SHALL treat `visibility` as presentation metadata and SHALL NOT represent it as authentication, authorization, or real security.

#### Scenario: Public deployment contains GM pages
- **WHEN** the site is published as static files
- **THEN** pages marked `gm` may still be accessible by URL and SHALL NOT be considered protected content

### Requirement: Breadcrumbs are limited to GM-oriented pages
Breadcrumb navigation SHALL be shown for GM-oriented pages and hidden for player/public-oriented pages to reduce accidental spoiler navigation.

#### Scenario: GM page renders
- **WHEN** a page has GM visibility or is treated as GM-only by kind
- **THEN** breadcrumbs SHALL render from the home page through ancestors to the current page

#### Scenario: Player-facing page renders
- **WHEN** a page has `visibility: players` or `visibility: public`
- **THEN** breadcrumbs SHALL be omitted

#### Scenario: Page lacks visibility
- **WHEN** a page does not define `visibility`
- **THEN** navigation logic SHALL treat it as GM-oriented by default

### Requirement: Player-facing relationships are restricted
Player-facing pages SHALL avoid exposing campaign relationship groups or relationship destinations that could reveal spoiler structure.

#### Scenario: Player page has relationships
- **WHEN** a page has `visibility: players` or `visibility: public`
- **THEN** the relationships renderer SHALL only expose links whose resolved destination is also `players` or `public`

#### Scenario: Player page references GM destination
- **WHEN** a page has `visibility: players` or `visibility: public` and a relationship URL resolves to a page with `visibility: gm` or missing visibility
- **THEN** the relationships renderer SHALL omit that relationship link

#### Scenario: Player page has unresolved relationship path
- **WHEN** a page has `visibility: players` or `visibility: public` and a relationship URL cannot be resolved
- **THEN** the relationships renderer SHALL omit the unresolved path instead of showing it as a fallback

#### Scenario: GM page has relationships
- **WHEN** a page has GM visibility
- **THEN** the relationships renderer MAY expose characters, NPCs, locations, factions, handouts, compendium references, and related pages

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

