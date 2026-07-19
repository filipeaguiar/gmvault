## ADDED Requirements

### Requirement: Local character compendium synchronization
The system SHALL provide shared 5e.tools synchronization for local character data and SHALL resolve, when represented by the character, classes, species, subclasses, feats, standard actions, class features, subclass features, spells, items, and magic items into canonical local compendium pages before associating their URLs with the character.

#### Scenario: Local character requires missing shared content
- **WHEN** creation or editing introduces a supported referenced entity that has no local compendium page
- **THEN** the synchronization service SHALL resolve and materialize its canonical compendium page through the supported 5e.tools source
- **THEN** it SHALL return and associate the canonical internal URL

#### Scenario: Entity cannot be resolved
- **WHEN** an entity is absent or ambiguous in the supported 5e.tools source
- **THEN** the synchronization service SHALL report the unresolved entity
- **THEN** it SHALL NOT invent a canonical URL or remove existing character data

### Requirement: Existing local character synchronization
The editor SHALL offer an explicit operation to synchronize all supported compendium references represented in an existing local character note.

#### Scenario: Existing character has historical missing references
- **WHEN** the user selects compendium synchronization for an existing character
- **THEN** the editor SHALL materialize each resolvable supported entity represented by that character
- **THEN** it SHALL deduplicate and preserve the character's existing operational state and unresolved legacy entries

### Requirement: Synchronization preserves editorial content
The synchronization service SHALL preserve an existing compendium page's Markdown body and editorial metadata while updating only canonical structured data supported by the underlying compendium resolver.

#### Scenario: Existing translated page is synchronized
- **WHEN** synchronization resolves an entity whose compendium page already has translated or reviewed content
- **THEN** it SHALL retain that page's body and editorial metadata
- **THEN** it SHALL not create a duplicate page for the same canonical entity
