## MODIFIED Requirements

### Requirement: Class progression pages have structured visual presentation
Class pages in the compendium SHALL render their title, metadata, progression content grouped by level, level entries, and subclass links with a coherent visual hierarchy. Internal compendium links SHALL use project styling instead of relying on default browser link presentation.

#### Scenario: Class feature card displays with equipment-like layout
- **WHEN** a character sheet renders class features
- **THEN** each feature SHALL use the `equipment-card` visual pattern with icon container, heading, and badges
- **THEN** the card SHALL have a colored left border distinguishing it from equipment cards

#### Scenario: Class feature card shows level badge
- **WHEN** a class feature has level metadata available
- **THEN** the card SHALL display a badge with the level number

#### Scenario: Class feature card shows source badge
- **WHEN** a class feature is rendered
- **THEN** the card SHALL display a badge indicating the source ("Classe" or "Subclasse")

#### Scenario: Class feature card preserves content
- **WHEN** a class feature card is rendered
- **THEN** the compendium content SHALL remain visible below the header
