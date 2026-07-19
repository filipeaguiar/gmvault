## ADDED Requirements

### Requirement: Compendium entities record 5e.tools provenance
Every automatically generated compendium entity SHALL record structured provenance identifying 5e.tools as provider, the canonical entity name and type, and the selected publication source.

#### Scenario: Imported entity has a specific source
- **WHEN** an entity is generated from an XPHB spell record
- **THEN** its front matter SHALL identify `5e.tools`, `spell`, the canonical spell name, and `XPHB`

#### Scenario: Compendium page is translated
- **WHEN** a generated page receives Portuguese textual fields
- **THEN** its canonical source identity and provenance SHALL remain unchanged

### Requirement: Rebuilt compendium entities use the current structured schema
Each rebuilt entity SHALL populate the current type-specific structured block when the corresponding data exists in 5e.tools.

#### Scenario: Spell is rebuilt
- **WHEN** a selected spell is generated
- **THEN** `spell_info` SHALL include its level, numeric level, school, casting metadata, attack type, damage types, saving throws, and structured rolls when available

#### Scenario: Monster is rebuilt
- **WHEN** a selected monster is generated
- **THEN** its page SHALL include the supported structured stat block fields and cleaned Markdown content available from the selected record
