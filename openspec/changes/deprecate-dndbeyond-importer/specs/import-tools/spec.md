## MODIFIED Requirements

### Requirement: Import scripts generate Markdown content
Repository import scripts SHALL transform supported external campaign and compendium data into Hugo Markdown files with YAML front matter and body content. Character creation and maintenance SHALL be performed by local character tools rather than by an importer for the D&D Beyond API.

#### Scenario: Script imports campaign material
- **WHEN** `import_campaign.py` is run with supported source data and target options
- **THEN** it SHALL create campaign-scoped Markdown files under `content/campaigns/<campaign-slug>/`

#### Scenario: Local tool materializes compendium material
- **WHEN** a local character tool resolves supported compendium references
- **THEN** it SHALL create Markdown files under the appropriate `content/compendium/` subsection

## REMOVED Requirements

### Requirement: Import script extracts and translates class and subclass level features
**Reason**: Class and subclass feature resolution is moved to the local character compendium synchronization flow.
**Migration**: Use `create_character.py` for new characters or the full synchronization operation in `edit_character.py` for existing notes.

### Requirement: D&D Beyond character importer exports full stats, speeds, saves, senses, languages, size, and alignment
**Reason**: The D&D Beyond API importer is no longer supported.
**Migration**: Maintain these character-specific fields through local creation and editing; existing imported notes remain supported.

### Requirement: Character importer generates compendium-driven frontmatter
**Reason**: Canonical compendium references are now created by local character tools.
**Migration**: Synchronize an existing note with `edit_character.py` to materialize missing references.

### Requirement: Character importer preserves character-specific operational data
**Reason**: The importer is removed; preservation is governed by local editor behavior and existing character-sheet requirements.
**Migration**: Existing operational front matter remains valid and is preserved during local synchronization.

### Requirement: Character importer structures advanced metadata in compendium item pages
**Reason**: Item metadata synchronization is owned by the shared local compendium resolver.
**Migration**: Use local creation or editing to resolve item and magic-item references.

### Requirement: Character importer references compendium items in character frontmatter
**Reason**: Local creation and editing own character equipment references.
**Migration**: Existing `char_info.equipment` entries remain supported; the editor can synchronize their missing pages.
