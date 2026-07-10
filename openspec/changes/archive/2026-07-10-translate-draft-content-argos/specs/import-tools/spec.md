## ADDED Requirements

### Requirement: Import workflow supports optional draft translation
The repository import workflow SHALL support an optional post-processing step that translates imported draft Markdown pages without changing the import scripts' primary responsibility of generating structured content.

#### Scenario: Import creates draft English content
- **WHEN** an import script creates Markdown pages with `draft: true`
- **THEN** those pages SHALL be eligible for later processing by the draft translation script

#### Scenario: Translation is not requested
- **WHEN** a maintainer runs an import script without running the translation script
- **THEN** the import script SHALL continue to generate Markdown content without requiring Argos Translate

#### Scenario: Translation script is run after import
- **WHEN** a maintainer runs the draft translation script after importing content
- **THEN** the workflow SHALL preserve the imported content structure while translating eligible draft text for editorial review
