## 1. Importer structure generation

- [x] 1.1 Update `import_campaign.py:create_adventure_structure` so new adventures no longer create mandatory `sessions/_index.md`.
- [x] 1.2 Update `import_campaign.py:create_session_structure` so sessions are created directly under `adventures/<adventure-slug>/<session-slug>/`.
- [x] 1.3 Update scene file creation so scenes are written directly under the session directory instead of under `scenes/`.
- [x] 1.4 Update all import modes in `import_campaign.py` option 1, option 2, and option 3 paths to use the simplified session/scene locations.
- [x] 1.5 Ensure imported session and scene front matter still uses `kind: session` / `kind: scene` or compatible `params.kind`.

## 2. Layout compatibility

- [x] 2.1 Update adventure/session page rendering so direct child sessions and direct child scenes are listed correctly.
- [x] 2.2 Preserve rendering compatibility for legacy `sessions/<session>/scenes/<scene>.md` content.
- [x] 2.3 Avoid duplicate navigation when an adventure contains both simplified and legacy structures during transition.
- [x] 2.4 Confirm player/public visibility filtering still applies in both simplified and legacy structures.

## 3. GMVault export compatibility

- [x] 3.1 Refactor GMVault export discovery to identify adventures, sessions, and scenes by effective `kind` instead of only fixed path names.
- [x] 3.2 Include simplified direct session children in adventure export categories.
- [x] 3.3 Include simplified direct scene children in session export categories.
- [x] 3.4 Preserve export support for legacy `sessions/` and `scenes/` structures.

## 4. Archetypes and documentation

- [x] 4.1 Update relevant archetypes or usage guidance so new manual sessions/scenes follow the simplified hierarchy.
- [x] 4.2 Update `AGENTS.md` with the canonical simplified campaign structure and note that importers generate it automatically.
- [x] 4.3 Document that legacy structures remain supported but should not be generated for new imports.

## 5. Validation with automatic imports

- [x] 5.1 Remove or isolate a test imported campaign before validation.
- [x] 5.2 Run `import_campaign.py` on a small campaign/adventure source and verify it generates `adventures/<adventure>/<session>/<scene>.md`.
- [x] 5.3 Verify the import does not generate mandatory `sessions/_index.md` or `scenes/_index.md` in newly imported adventures.
- [x] 5.4 Run `hugo -D --gc --minify`.
- [x] 5.5 Inspect representative URLs for imported adventure, session, and scene pages.
- [x] 5.6 Run `openspec validate simplify-campaign-page-hierarchy --strict`.
