## MODIFIED Requirements

### Requirement: Markdown pages use YAML front matter
Every authored content page SHALL be represented as Markdown with YAML front matter containing editorial metadata that layouts can render or use for navigation. The canonical location for the page kind SHALL be `params.kind`. The `draft` field SHALL control only whether Hugo includes the page in a build; translation/review pending state SHALL be represented by `status: draft` and/or `translation.status`. Layouts SHALL resolve `params.kind` as the primary value and SHALL retain temporary read compatibility with legacy top-level `kind` pages.

#### Scenario: Page metadata uses canonical nested kind
- **WHEN** a content page is created or maintained by an archetype, importer, script, or editor
- **THEN** its YAML front matter SHALL store the page kind as `params.kind` together with the available title, summary, draft, weight, visibility, status, and tags metadata.

#### Scenario: Legacy top-level kind is available
- **WHEN** a legacy content page is rendered with top-level `kind` and without `params.kind`
- **THEN** layouts SHALL treat top-level `kind` as a temporary compatibility fallback for kind-specific partials, icons, badges, breadcrumbs, and navigation decisions.

#### Scenario: Both kind fields are available
- **WHEN** a page has both `params.kind` and legacy top-level `kind`
- **THEN** `params.kind` SHALL take precedence and new generated content SHALL not create the duplicate top-level field.

#### Scenario: Maintained content is checked for canonical format
- **WHEN** the project validates authored content and generated fixtures
- **THEN** top-level `kind` entries SHALL be reported as legacy-format findings and all newly generated pages SHALL use `params.kind`.

#### Scenario: Public compendium content awaits translation
- **WHEN** a public compendium page still needs translation or editorial review
- **THEN** it SHALL be allowed to use `draft: false` with `status: draft` and/or `translation.status`, so Hugo can render the original text while the translation workflow continues to identify it as pending.

#### Scenario: Campaign or GM content awaits review
- **WHEN** campaign content or GM-only content is not ready for publication
- **THEN** it SHALL retain `draft: true` so it remains excluded from production builds, independently of its translation status.
