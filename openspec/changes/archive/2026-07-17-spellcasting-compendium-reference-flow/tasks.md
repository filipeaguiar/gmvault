## 1. Canonical spell data helpers

- [x] 1.1 Add focused tests for canonical spell materialization, minimal reference-driven entries, duplicate merging, source/availability precedence, and unresolved-name failures in `dnd_utils.py`.
- [x] 1.2 Implement shared `dnd_utils.py` helpers that materialize 5e.tools spell pages, build operational entries keyed by `ref`, and deduplicate references without copying shared spell metadata.
- [x] 1.3 Extend spellcasting profile inference to expose generic preparation capability, accessible positive slot levels, pact slot level/count, and safe read-only fallback for ambiguous hybrid sources.
- [x] 1.4 Verify that spell synchronization keeps structured `spell_info` roll metadata while preserving translated/editorially reviewed front matter and Markdown bodies.

## 2. Character generation and editing flows

- [x] 2.1 Add or update fixture-based tests for D&D Beyond class, race, background, feat, and other granted spells, including duplicate source records and unresolved spells.
- [x] 2.2 Refactor `import_dndbeyond.py` to materialize every supported spell through the shared helper and emit deduplicated `ref`-driven entries with prepared/known/always/granted source state.
- [x] 2.3 Refactor `create_character.py` to use canonical spell refs, omit duplicated title/level/mechanics from new entries, and deduplicate class catalog and `compendium_refs` values.
- [x] 2.4 Refactor `edit_character.py` to use the same canonical helper, normalize resolvable legacy entries, preserve unresolved legacy fallbacks, and recompute the spellcasting profile after edits.
- [x] 2.5 Add regression tests proving all three character flows preserve operational state and do not fabricate refs when 5e.tools resolution fails.

## 3. Hugo spell collection and rendering

- [ ] 3.1 Add Hugo render fixtures/tests for prepared, known, pact, hybrid, granted-spell, duplicate-ref, and unresolved legacy character data.
- [ ] 3.2 Create a reusable Hugo partial/helper that normalizes `char_info.spells`, `char_info.class_spells`, and spell-kind `compendium_refs` by canonical ref, with operational entries taking precedence.
- [ ] 3.3 Classify normalized spells into ready and management collections using profile and entry-specific availability, excluding inaccessible catalog levels while retaining granted ready spells.
- [ ] 3.4 Refactor the Grimório layout to render the ready list at the top, remove repeated “Preparada” badges, and render only the remaining references in the lower management list.
- [ ] 3.5 Generate level filters, grouped headings, counters, normal slot trackers, and pact slot trackers only for levels/resources the character can access.
- [ ] 3.6 Render preparation checkboxes only for eligible entries and read-only management rows for known, pact, spontaneous, always, granted, or ambiguous entries.
- [ ] 3.7 Preserve safe inline fallback rendering for legacy unresolved entries and ensure the initial server-rendered interface remains useful without JavaScript.

## 4. Browser interaction and presentation

- [ ] 4.1 Add JavaScript DOM tests for cross-list search/filtering, prepare/unprepare transitions, deduplication, local-state validation, unavailable storage, and positive slot tracking.
- [ ] 4.2 Refactor `assets/js/spells.js` to move stable spell nodes between ready and management lists without cloning divergent cards or rewriting roll-control HTML.
- [ ] 4.3 Validate restored `localStorage` refs against rendered eligibility, keep state scoped by character pathname, and treat front matter as the canonical initial state.
- [ ] 4.4 Update `assets/css/character-sheet.css` for distinct ready/management sections, compact eligible controls, accessible focus states, and narrow viewport behavior without adding heavy dependencies.
- [ ] 4.5 Extend spell roll rendering/runtime tests to prove `data-roll-notation`, roll type, accessible labels, and Dice+ behavior survive filtering and preparation changes.

## 5. Documentation and validation

- [ ] 5.1 Update `archetypes/character.md` and `docs/character-compendium-data.md` with the reference-driven spell contract, operational availability fields, class catalog compatibility, and `localStorage` limitations.
- [ ] 5.2 Run targeted Python and JavaScript test suites for spellcasting profiles, character import/edit/create flows, spell rendering, structured rolls, and Dice+ runtime behavior.
- [ ] 5.3 Run `hugo -D --gc --minify` and `hugo --gc --minify`, reviewing draft and unresolved-reference behavior in both builds.
- [ ] 5.4 Run OpenSpec validation for `spellcasting-compendium-reference-flow` and review generated diffs for accidental spell-body, translation, visibility, or editorial metadata changes.
