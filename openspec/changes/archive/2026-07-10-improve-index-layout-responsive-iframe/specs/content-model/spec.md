## MODIFIED Requirements

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
