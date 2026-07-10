## 1. Campaign Index Visibility

- [x] 1.1 Update `content/campaigns/_index.md` so the campaign collection index is GM-oriented.
- [x] 1.2 Verify `/campaigns/` lists non-draft GM campaign children when running a normal Hugo build.
- [x] 1.3 Verify `/campaigns/` lists draft imported GM campaign children when running Hugo with drafts enabled.

## 2. Navigation Behavior

- [x] 2.1 Confirm public/player list pages still omit GM child pages.
- [x] 2.2 Confirm the home page campaign list behavior remains consistent with Hugo draft settings.
- [x] 2.3 Adjust list rendering only if the existing automatic child navigation does not render campaign cards after the visibility change.

## 3. Documentation and Validation

- [x] 3.1 Document that `/campaigns/` is a GM navigation page and that imported campaigns remain drafts until published.
- [x] 3.2 Run `hugo -D --gc --minify` and confirm imported draft campaigns can be rendered.
- [x] 3.3 Run `hugo --gc --minify` and confirm production builds still exclude draft campaigns.
- [x] 3.4 Run `openspec validate fix-campaign-index-listing --strict`.
