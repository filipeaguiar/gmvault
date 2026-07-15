## MODIFIED Requirements

### Requirement: Global compendium is separate from campaigns
Reusable rules content SHALL live under `content/compendium/` and SHALL not belong to any single campaign. The global compendium index SHALL show canonical child sections as organized navigation groups with counts and safe fallback behavior.

#### Scenario: Compendium index is opened
- **WHEN** the compendium section page is rendered
- **THEN** it SHALL show the canonical child sections as organized navigation groups, with a title, icon, summary when available, and count of visible pages for each section; it SHALL not require users to scan one undifferentiated list of all content pages.

#### Scenario: Compendium index displays canonical sections
- **WHEN** the compendium root contains sections for monsters, items, magic items, classes, races/species, feats, spells, backgrounds, conditions, or rules
- **THEN** the index SHALL render each available section as a separate navigable group or card with its resolved title, icon, summary, and visible-page count.

#### Scenario: Empty or unknown compendium section
- **WHEN** a compendium section has no visible child pages or has an unrecognized directory/category
- **THEN** the index SHALL omit empty groups and SHALL render an unknown non-empty section through a generic fallback without failing the build.
