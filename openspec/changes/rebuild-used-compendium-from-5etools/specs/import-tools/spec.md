## ADDED Requirements

### Requirement: Compendium descriptions use 5e.tools exclusively
Importers and generators SHALL obtain automatically generated descriptive and mechanical compendium content exclusively from 5e.tools data.

#### Scenario: Character source contains a reusable rule description
- **WHEN** a D&D Beyond or manually created character requires a reusable compendium entity
- **THEN** the generator SHALL resolve the entity text in 5e.tools instead of copying the external character-source description

#### Scenario: Entity is unavailable in 5e.tools
- **WHEN** no safe 5e.tools entity can be resolved
- **THEN** the generator SHALL report the unresolved entity and SHALL NOT silently populate its compendium description from another source

### Requirement: Importers apply deterministic 5e.tools source priority
Entity resolution SHALL honor an explicitly declared source first, otherwise prioritize XPHB over PHB for applicable player-rule entities, and then use a documented type-specific fallback.

#### Scenario: XPHB and PHB versions exist
- **WHEN** a player-rule entity is requested without a pinned source and both XPHB and PHB records exist
- **THEN** the importer SHALL select XPHB and persist that source choice

#### Scenario: Goblin has no XPHB or PHB record
- **WHEN** Goblin is requested without a pinned source
- **THEN** the importer SHALL select the configured 5e.tools species fallback, such as MPMM, and record it explicitly

#### Scenario: Campaign reference pins MM
- **WHEN** JttRC references a monster from MM and an XMM record with the same name exists
- **THEN** the campaign importer SHALL retain the MM record declared by the campaign source

### Requirement: Importers share current compendium serializers
Campaign, character, and rebuild workflows SHALL use shared type-specific normalizers and serializers for generated compendium entities.

#### Scenario: Spell is generated through different workflows
- **WHEN** the same 5e.tools spell and source are requested by character import and compendium rebuild
- **THEN** both workflows SHALL produce the same structured spell schema and provenance fields
