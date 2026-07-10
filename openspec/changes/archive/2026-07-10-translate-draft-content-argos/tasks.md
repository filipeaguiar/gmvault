## 1. Setup and dependencies

- [x] 1.1 Decide and document the dependency installation path for `argostranslate` without making Hugo depend on it at build time.
- [x] 1.2 Create the new script file `translate_drafts.py` with CLI argument parsing for `--scope compendium` and `--scope campaign --campaign <slug>`.
- [x] 1.3 Add a versioned glossary file for controlled RPG/D&D term translations.

## 2. Markdown discovery and parsing

- [x] 2.1 Implement recursive Markdown discovery for `--scope compendium` under `content/compendium/`.
- [x] 2.2 Implement recursive Markdown discovery for `--scope campaign --campaign <slug>` under `content/campaigns/<slug>/`.
- [x] 2.3 Validate that campaign scope requires a campaign slug and fails clearly when missing.
- [x] 2.4 Parse YAML front matter and select only files with `draft: true` by default.
- [x] 2.5 Add CLI options for path limiting within the selected scope, dry-run default, explicit apply mode, and optional non-draft processing.
- [x] 2.6 Reject path limits that escape the selected scope.

## 3. Structure preservation

- [x] 3.1 Preserve structural YAML fields such as kind, visibility, status, relationships, stats, URLs, numbers, and nested metadata.
- [x] 3.2 Translate only eligible textual front matter fields when explicitly supported, with body Markdown as the main target.
- [x] 3.3 Protect fenced code blocks, inline code, URLs, internal paths, image syntax, shortcodes, and dice notation before translation.
- [x] 3.4 Restore protected Markdown constructs after translation without changing their original content.

## 4. Glossary tokenization

- [x] 4.1 Load glossary entries from the versioned glossary file.
- [x] 4.2 Tokenize glossary source terms before calling Argos Translate.
- [x] 4.3 Replace glossary tokens with configured Portuguese translations after machine translation.
- [x] 4.4 Include an initial glossary covering common D&D/RPG terms, attributes, checks, saves, actions, conditions, spell schools, and stat block labels.

## 5. Argos translation engine

- [x] 5.1 Detect whether Argos Translate is installed and fail with a clear message if unavailable.
- [x] 5.2 Detect whether an English to Portuguese model is installed and fail with a clear message if unavailable.
- [x] 5.3 Translate eligible text segments with Argos while preserving paragraph boundaries where practical.
- [x] 5.4 Provide progress output listing files processed, skipped, and changed.

## 6. Safe writing and metadata

- [x] 6.1 Keep dry-run as the default and avoid writing files unless `--apply` is provided.
- [x] 6.2 When applying, write translated Markdown back to the original file while preserving protected structure.
- [x] 6.3 Add or update translation metadata indicating source language, target language, engine, and machine translation status.
- [x] 6.4 Ensure translated files remain `draft: true`.

## 7. Documentation and validation

- [x] 7.1 Document usage, installation requirements, glossary behavior, and review expectations in project documentation or `AGENTS.md`.
- [x] 7.2 Run the script in dry-run mode with `--scope compendium` against a limited compendium path.
- [x] 7.3 Run the script in dry-run mode with `--scope campaign --campaign <slug>` against a limited campaign path.
- [x] 7.4 Run `python3 -m py_compile translate_drafts.py`.
- [x] 7.5 Run `hugo -D --gc --minify` after a controlled translation test.
- [x] 7.6 Run `openspec validate translate-draft-content-argos --strict`.
