## 1. Implement Forge Roll Parser

- [x] 1.1 Create the helper template `layouts/partials/helpers/forge_roll_parser.html`.
- [x] 1.2 Implement regex replacement in the parser to convert attack modifiers (e.g., `+5 to hit` -> `[1d20+5] to hit` and `+6 para acertar` -> `[1d20+6] para acertar`).
- [x] 1.3 Implement regex replacement in the parser to convert dice equations (e.g., `2d6 + 3` -> `[2d6+3]`, `1d8` -> `[1d8]`), removing unnecessary spacing.
- [x] 1.4 Clean up double brackets `[[2d6+3]]` -> `[2d6+3]` to support imported 5e.tools formatting.

## 2. Update Forge Statblock Helper

- [x] 2.1 Parse monster traits, actions, bonus actions, reactions, and legendary actions directly from their Markdown body sections in `forge_statblock.html`, splitting by headings.
- [x] 2.2 Calculate character attribute modifiers (Str, Dex) and Proficiency bonus based on total class levels.
- [x] 2.3 Resolve inventory weapon properties (Finesse, Ranged) and dynamically calculate total attack and damage bonuses.
- [x] 2.4 Resolve spell metadata and descriptions from `/compendium/spells/` for characters, prepending metadata and parsing descriptions.
- [x] 2.5 Apply `forge_roll_parser.html` to all action, ability, legendary action, reaction, bonus action, and spell description fields.

## 3. Validation and Testing

- [x] 3.1 Run a local build to generate the static files.
- [x] 3.2 Validate the generated `/exports/forge/statblocks.json` using `jq` to ensure it is valid JSON and contains the formatted roll chips.
- [x] 3.3 Run the automated python/pytest test suite to verify there are no layout or export regressions.
