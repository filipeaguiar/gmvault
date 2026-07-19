## MODIFIED Requirements

### Requirement: Glossary is versioned, editable, and auditable against the selected corpus
The project SHALL include a human-editable glossary file for controlled RPG/D&D term translations and SHALL provide a way to report relevant source terms from the selected English corpus that are absent from or potentially inconsistent with the glossary.

#### Scenario: Glossary file exists
- **WHEN** the script starts
- **THEN** it SHALL load glossary entries from the project glossary file

#### Scenario: Glossary entry is updated manually
- **WHEN** a maintainer changes a glossary translation
- **THEN** subsequent script runs SHALL use the updated translation without code changes

#### Scenario: Selected corpus contains uncovered terminology
- **WHEN** the glossary audit scans staged 5e.tools content and finds relevant repeated mechanical terms without controlled entries
- **THEN** it SHALL report candidates for editorial review without automatically accepting translations

## ADDED Requirements

### Requirement: Draft translation preserves source provenance
The translator SHALL treat compendium source-provider, source-book, remote identity, entity kind, and canonical entity name metadata as structural fields.

#### Scenario: Rebuilt compendium page is translated
- **WHEN** the translator processes a page generated from 5e.tools
- **THEN** provenance values SHALL remain semantically unchanged

### Requirement: Glossary audit validates controlled output rules
Glossary and post-translation validation SHALL detect unresolved protection tokens, forbidden outputs, and source-specific markup that escaped cleanup.

#### Scenario: Translation leaks an internal token
- **WHEN** translated output contains a protection or glossary token
- **THEN** validation SHALL fail for that document and SHALL preserve it for review
