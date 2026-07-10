## 1. Metadata resolution

- [x] 1.1 Add or apply a consistent Hugo pattern for resolving effective `kind` from `.Params.kind` with fallback to `.Params.params.kind`.
- [x] 1.2 Update kind-dependent layouts and partials to use the effective kind for partial selection, icons, badges, breadcrumbs, and special cases.
- [x] 1.3 Verify existing pages using legacy `params.kind` render with their intended kind-specific layouts.

## 2. Visibility-safe navigation

- [x] 2.1 Add or apply a consistent Hugo pattern for resolving effective visibility, treating missing visibility as GM-only for player-facing navigation.
- [x] 2.2 Update breadcrumbs so they remain hidden for `players` and `public` pages and default missing visibility to GM-oriented behavior.
- [x] 2.3 Update relationship rendering so player/public pages only link to resolved destinations that are also `players` or `public`.
- [x] 2.4 Update relationship rendering so unresolved paths are omitted on player/public pages but remain visible as broken-link fallbacks on GM pages.
- [x] 2.5 Update child page navigation so player/public index pages omit GM or unknown-visibility child pages.

## 3. Index layout behavior

- [x] 3.1 Refactor `child_pages.html` to produce deterministic, ordered index navigation using weight and stable title behavior where practical.
- [x] 3.2 Ensure index cards show resolved title, summary when available, and compact kind/status metadata without requiring all fields.
- [x] 3.3 Add markup classes as needed for index-specific layout without disrupting specialized kind partials.

## 4. Responsive iframe styling

- [x] 4.1 Update `assets/css/main.css` so index grids adapt from multi-column cards to a single-column compact layout at narrow widths.
- [x] 4.2 Ensure cards, metadata blocks, headers, relation blocks, and quick links avoid horizontal overflow inside narrow iframes.
- [x] 4.3 Ensure links and cards remain readable and clickable/tappable at small widths.

## 5. Validation

- [x] 5.1 Run `hugo --gc --minify` and fix any template or rendering errors.
- [x] 5.2 Inspect representative pages: home, campaigns index, campaign page, compendium index, campaign support section, player/public page, and GM page.
- [x] 5.3 Confirm a player/public page does not expose breadcrumbs, GM child links, GM relationship links, or unresolved relationship fallback paths.
- [x] 5.4 Run `openspec validate improve-index-layout-responsive-iframe --strict`.
