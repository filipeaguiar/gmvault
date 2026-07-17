## MODIFIED Requirements

### Requirement: Compendium Population
The script SHALL query 5e.tools for classes, subclasses, species, feats, spells, items, and reusable rules required by the character, SHALL prioritize XPHB over PHB when no source is pinned and both apply, and SHALL persist the selected 5e.tools source with the generated compendium entity.

#### Scenario: Character has a new species
- **WHEN** the user selects a species that is not in the compendium
- **THEN** the script SHALL download it from 5e.tools, save it under `content/compendium/species/`, and record its selected source

#### Scenario: Character selects entity available in XPHB and PHB
- **WHEN** an applicable class, feat, spell, item, or rule exists in both XPHB and PHB and the user has not pinned a source
- **THEN** the script SHALL select XPHB

#### Scenario: Species requires another source
- **WHEN** a selected species such as Goblin exists in neither XPHB nor PHB
- **THEN** the script SHALL use the configured 5e.tools fallback source and SHALL preserve that source in generated metadata
