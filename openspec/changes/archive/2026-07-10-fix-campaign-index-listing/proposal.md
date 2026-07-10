## Why

Imported campaign pages can be created correctly but remain absent from the visible campaign navigation when the campaign index is treated as a public page. This makes the importer appear to have failed even though the campaign `_index.md` exists and uses `kind: campaign`.

## What Changes

- Treat the campaign collection index as a GM-oriented navigation page by default so it can list GM campaign children.
- Ensure the campaign index page renders automatic child campaign cards consistently.
- Preserve the rule that public/player pages do not expose GM child navigation.
- Document the expected behavior for imported draft campaigns: they appear only when Hugo is run with drafts enabled, while published campaigns appear in normal builds.
- No breaking changes.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `navigation-and-visibility`: Clarify that the campaign collection index is GM-oriented when it is intended to list GM campaigns, while public/player pages still omit GM children.
- `content-model`: Clarify that campaign collection indexes should expose child campaign pages through automatic navigation when visibility allows.

## Impact

- Affected content: `content/campaigns/_index.md` front matter.
- Affected layouts: campaign/list rendering if needed to ensure child campaign cards appear.
- Affected documentation: project guidance for campaign index visibility and imported draft campaigns.
- No external dependencies, backend, database, or JavaScript changes.
