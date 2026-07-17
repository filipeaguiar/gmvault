## 1. Baseline and fixtures

- [x] 1.1 Capture the current direct-reference, transitive-reference, and unused-entity counts in deterministic test fixtures
- [x] 1.2 Add representative fixtures for JttRC source-pinned monsters/items, XPHB/PHB duplicates, Goblin fallback, class features, actions, spells, and structured items
- [x] 1.3 Run the existing Python and Hugo test/build baseline and record unrelated pre-existing failures before changing import code

## 2. Reference inventory and manifest

- [x] 2.1 Implement recursive extraction of `/compendium/.../` references from campaign and character YAML and Markdown bodies
- [x] 2.2 Implement transitive traversal of references contained in selected compendium pages, excluding indexes and reserved files from entity deletion
- [x] 2.3 Implement manifest serialization with URL, kind, canonical name, selected source, remote identity, resolution status, selection reason, dependency origin, and input fingerprint
- [x] 2.4 Add tests proving that the current 171 direct references retain the 20 reachable rule dependencies and classify the remaining entity pages as unused
- [x] 2.5 Reject promotion when campaign or compendium input fingerprints differ from the scan that produced the manifest

## 3. 5e.tools resolution and source policy

- [x] 3.1 Implement a shared cached 5e.tools catalog client for the entity files needed by the selected manifest
- [x] 3.2 Implement explicit-source resolution for JttRC references so MM and other declared records are not replaced by homonymous XMM records
- [x] 3.3 Implement XPHB-first and PHB-fallback resolution for applicable classes, feats, spells, items, species, actions, and class rules
- [x] 3.4 Implement and test the non-PHB species fallback that resolves Pinky's Goblin to an explicit available 5e.tools source such as MPMM
- [x] 3.5 Resolve class-feature and action-rule dependencies from 5e.tools class/action data instead of external character descriptions
- [x] 3.6 Fail resolution on missing or unhandled ambiguous entities and include actionable diagnostics in the manifest

## 4. Current-schema compendium generation

- [x] 4.1 Define and test shared provenance fields for provider, publication source, entity type, canonical name, and remote identity
- [x] 4.2 Refactor shared entity parsing/serialization for spells, including current `spell_info` mechanics and structured rolls without regressing the structured-spell-rolls change
- [x] 4.3 Implement current-schema serializers for monsters, mundane items, magic items, classes, species, feats, actions, and class-feature rules
- [x] 4.4 Update campaign, D&D Beyond, and interactive-character workflows to call shared 5e.tools compendium generators rather than copying descriptive text from other sources
- [x] 4.5 Preserve requested internal slugs while recording canonical 5e.tools names and sources
- [x] 4.6 Add tests that equivalent requests from rebuild and character/import workflows produce equivalent schemas and provenance

## 5. Staging, validation, and controlled promotion

- [x] 5.1 Implement generation into an isolated staging directory without modifying `content/compendium/`
- [x] 5.2 Validate staged YAML, required per-kind fields, duplicate slugs, internal references, unresolved 5e.tools tags, and manifest completeness
- [x] 5.3 Implement explicit promotion that replaces selected entities and removes only manifest-classified unused entities
- [x] 5.4 Preserve `_index.md`, reserved files, campaign content, and character files during promotion
- [x] 5.5 Add rollback guidance and tests for failed downloads, failed validation, stale manifests, and interrupted promotion

## 6. DeepSeek V4 Pro translation option

- [x] 6.1 Add a selectable `deepseek-v4-pro` profile using the official DeepSeek OpenAI-compatible endpoint and `DEEPSEEK_API_KEY`
- [x] 6.2 Update the interactive translation menu to display profile/model choices and include the selected engine, endpoint profile, and model in confirmation
- [x] 6.3 Stop recommending `deepseek-chat` while retaining only deliberate backward compatibility where required
- [x] 6.4 Add tests for V4 Pro payloads, secret resolution, metadata recording, interactive selection, and dry-run behavior

## 7. Glossary audit and update

- [x] 7.1 Implement a corpus audit that reports repeated mechanical terms absent from controlled glossary categories without modifying the glossary automatically
- [x] 7.2 Run the audit against the staged 5e.tools corpus and review candidates for 2024/XPHB terminology, creature statistics, equipment, class features, actions, and spells
- [x] 7.3 Update `translation_glossary.json` with reviewed terms, contextual notes, protected names, and newly observed forbidden-output corrections
- [x] 7.4 Add tests for new glossary entries, provenance protection, leaked tokens, forbidden outputs, and unresolved source markup

## 8. Rebuild, translate, and remove obsolete content

- [x] 8.1 Generate and inspect the final manifest, confirming all direct and transitive references, selected sources, and deletion candidates
- [x] 8.2 Rebuild all selected entities from 5e.tools into staging and verify that every required existing URL is preserved
- [x] 8.3 Confirm DeepSeek credentials and expected candidate/cost summary before issuing paid V4 Pro translation requests
- [x] 8.4 Translate staged drafts with `deepseek-v4-pro`, including safe textual front matter, while preserving provenance and structured mechanics
- [x] 8.5 Run post-translation validation and retain every rebuilt page as draft/status draft for editorial review
- [x] 8.6 Promote the validated staging set and delete every current entity outside the approved transitive closure

## 9. Final verification

- [ ] 9.1 Verify that every campaign, character, and selected compendium reference resolves after promotion
- [ ] 9.2 Run the full Python test suite, including importer, character, translation, manifest, schema, and structured-roll tests
- [ ] 9.3 Run `hugo -D --gc --minify` and `hugo --gc --minify` and inspect warnings and generated player-facing pages
- [ ] 9.4 Audit the final diff for accidental campaign/character changes, leaked secrets, non-5e.tools provenance, published machine translations, and undeleted unused entities
