## ADDED Requirements

### Requirement: Draft translator discovers draft Markdown pages by scope
The draft translation script SHALL discover Markdown files under an explicit scope and select only pages whose YAML front matter contains `draft: true` by default.

#### Scenario: Compendium scope is selected
- **WHEN** the user runs the script with `--scope compendium`
- **THEN** the script SHALL scan Markdown files under `content/compendium/`

#### Scenario: Campaign scope is selected
- **WHEN** the user runs the script with `--scope campaign --campaign <campaign-slug>`
- **THEN** the script SHALL scan Markdown files under `content/campaigns/<campaign-slug>/`

#### Scenario: Campaign scope is missing campaign slug
- **WHEN** the user runs the script with `--scope campaign` without `--campaign`
- **THEN** the script SHALL stop with a clear error explaining that a campaign slug is required

#### Scenario: Draft page is present in selected scope
- **WHEN** the script scans the selected scope and finds a Markdown page with `draft: true`
- **THEN** the page SHALL be included in the translation candidate list

#### Scenario: Non-draft page is present in selected scope
- **WHEN** the script scans the selected scope and finds a Markdown page without `draft: true`
- **THEN** the page SHALL be skipped unless the user explicitly enables non-draft processing

#### Scenario: Path is limited
- **WHEN** the user supplies a path option within the selected scope
- **THEN** the script SHALL only scan Markdown files under that path

#### Scenario: Path escapes selected scope
- **WHEN** the user supplies a path outside the selected scope
- **THEN** the script SHALL stop with a clear error instead of scanning unrelated content

### Requirement: Draft translator uses Argos Translate locally
The draft translation script SHALL translate selected English text to Portuguese using Argos Translate as a local translation engine.

#### Scenario: Argos model is available
- **WHEN** the script runs and an English to Portuguese Argos model is installed
- **THEN** the script SHALL use that model to translate eligible text segments

#### Scenario: Argos model is missing
- **WHEN** the script runs and no English to Portuguese Argos model is available
- **THEN** the script SHALL stop with a clear error explaining that Argos Translate or the required model must be installed

### Requirement: Draft translator preserves Markdown and Hugo structure
The draft translation script SHALL preserve front matter structure and Markdown constructs that could break the site if translated.

#### Scenario: Front matter contains structural fields
- **WHEN** the script processes YAML front matter fields such as `kind`, `visibility`, `status`, relationships, stats, URLs, or numeric metadata
- **THEN** those structural fields SHALL remain semantically unchanged

#### Scenario: Markdown contains protected constructs
- **WHEN** the body contains code blocks, inline code, URLs, internal paths, Markdown image syntax, Hugo shortcodes, or dice notation
- **THEN** those constructs SHALL be protected from machine translation and restored unchanged

### Requirement: Draft translator tokenizes glossary terms before translation
The draft translation script SHALL replace configured RPG/D&D glossary source terms with stable tokens before machine translation.

#### Scenario: Source text contains glossary term
- **WHEN** eligible text contains a glossary source term such as `Armor Class` or `Hit Points`
- **THEN** the script SHALL replace that term with a stable token before calling Argos Translate

#### Scenario: Translation completes
- **WHEN** Argos Translate returns translated text containing glossary tokens
- **THEN** the script SHALL replace each token with the configured Portuguese glossary translation

### Requirement: Glossary is versioned and editable
The project SHALL include a human-editable glossary file for controlled RPG/D&D term translations.

#### Scenario: Glossary file exists
- **WHEN** the script starts
- **THEN** it SHALL load glossary entries from the project glossary file

#### Scenario: Glossary entry is updated manually
- **WHEN** a maintainer changes a glossary translation
- **THEN** subsequent script runs SHALL use the updated translation without code changes

### Requirement: Draft translator is safe by default
The draft translation script SHALL default to a non-destructive dry-run mode and only write files when the user explicitly requests application.

#### Scenario: Dry-run execution
- **WHEN** the user runs the script without an apply flag
- **THEN** the script SHALL report candidate files and intended changes without modifying files

#### Scenario: Apply execution
- **WHEN** the user runs the script with the apply flag
- **THEN** the script MAY overwrite selected draft files with translated content after preserving protected structure

### Requirement: Draft translator marks machine-translated content
The draft translation script SHALL mark translated files with metadata indicating that translation was automatic and requires human review.

#### Scenario: File is translated
- **WHEN** the script writes a translated Markdown file
- **THEN** the file SHALL include translation metadata with source language, target language, engine, and machine translation status

#### Scenario: File remains draft
- **WHEN** the script writes a translated Markdown file
- **THEN** the file SHALL remain `draft: true` unless the user explicitly changes it outside the script
