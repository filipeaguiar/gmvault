## Context

The site currently lists campaigns on the home page by scanning pages whose effective `kind` is `campaign`. Imported campaigns create valid campaign `_index.md` files, but they are drafts by default and only appear when Hugo runs with `-D`. The `/campaigns/` collection page is marked `visibility: public`, so the automatic child navigation intentionally hides child pages with `visibility: gm`.

This is consistent with the visibility safety model, but it is confusing for the GM workflow because the campaign collection index is expected to function as a GM navigation page.

## Goals / Non-Goals

**Goals:**

- Make `/campaigns/` a GM-oriented index so it can list GM campaign pages.
- Preserve visibility-safe behavior for truly public/player pages.
- Keep imported draft campaigns draft-only unless Hugo is run with `-D` or the campaign is manually published with `draft: false`.
- Keep the change lightweight and static-Hugo-only.

**Non-Goals:**

- Do not add authentication or access control.
- Do not publish imported campaigns automatically by changing importer defaults from `draft: true` to `draft: false`.
- Do not expose GM campaign structure from public/player pages.
- Do not introduce JavaScript or a backend.

## Decisions

1. Change `content/campaigns/_index.md` to `visibility: "gm"`.
   - Rationale: the campaign collection index is a GM navigation surface because campaigns commonly contain spoilers.
   - Alternative considered: special-case `campaigns_index` in `child_pages.html` to show GM children even from public visibility. Rejected because it weakens the general visibility rule and makes the index metadata misleading.

2. Keep imported campaign `_index.md` pages as drafts.
   - Rationale: imports are raw material requiring review, translation, and editorial cleanup before publishing.
   - Alternative considered: make importer-created campaign pages `draft: false`. Rejected because it would publish large imported content unexpectedly in production builds.

3. Add/adjust documentation instead of adding new runtime concepts.
   - Rationale: the observed behavior is mostly configuration and workflow clarity. The layouts already support automatic child page navigation when visibility allows.

## Risks / Trade-offs

- GM campaign index remains accessible by URL in a static deployment → Mitigation: document that `visibility` is editorial/navigation metadata, not security.
- Draft imported campaigns still do not appear in production builds → Mitigation: document that `hugo server -D` is required for reviewing imported drafts and `draft: false` is required for publishing.
- Changing `/campaigns/` to GM may hide breadcrumbs/navigation behavior from public expectations → Mitigation: this matches the campaign-vault spoiler model and keeps player-safe pages isolated.
