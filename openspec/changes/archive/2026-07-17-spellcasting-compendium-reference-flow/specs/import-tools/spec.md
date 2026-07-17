## ADDED Requirements

### Requirement: Character spell flows materialize 5e.tools compendium pages
`create_character.py`, `edit_character.py`, and `import_dndbeyond.py` SHALL use shared 5e.tools spell resolution to create or synchronize a canonical local compendium page before writing a new character spell association. A new canonical association SHALL NOT be emitted when the source spell cannot be resolved unambiguously.

#### Scenario: Character creation selects a supported spell
- **WHEN** the interactive creation flow selects a spell present in the supported 5e.tools data
- **THEN** it SHALL create or synchronize the spell page under `content/compendium/spells/`
- **THEN** it SHALL write the returned internal URL into the character note

#### Scenario: Character editing adds a supported spell
- **WHEN** the interactive editing flow adds a spell present in the supported 5e.tools data
- **THEN** it SHALL use the same canonical materialization helper as character creation
- **THEN** it SHALL avoid adding a duplicate reference already associated with the character

#### Scenario: D&D Beyond import contains a supported spell
- **WHEN** the D&D Beyond payload contains a class, race, background, feat, item, or other granted spell supported by 5e.tools
- **THEN** the importer SHALL materialize the canonical compendium page
- **THEN** it SHALL associate the operational source and availability state with that canonical reference

#### Scenario: Spell cannot be resolved
- **WHEN** a new spell name cannot be resolved unambiguously in the supported 5e.tools source data
- **THEN** the flow SHALL report the unresolved spell
- **THEN** it SHALL NOT silently write a fabricated canonical reference for the new association

### Requirement: Character spell flows emit reference-driven operational entries
New character spell entries SHALL use the canonical `ref` as identity and SHALL include only character-specific state needed to determine readiness, preparation eligibility, source, and usage. Shared spell title, level, description, and roll mechanics SHALL remain in the compendium page. Inline shared fields SHALL remain supported only for legacy fallback.

#### Scenario: Prepared spell is emitted
- **WHEN** an imported or selected spell is prepared for the character
- **THEN** its character entry SHALL contain its canonical `ref` and prepared/availability state
- **THEN** it SHALL NOT duplicate the compendium description or structured roll metadata

#### Scenario: Known spell is emitted
- **WHEN** a known or pact caster has a known spell
- **THEN** the character entry SHALL identify the spell as ready through reference-driven operational state without marking it as requiring preparation

#### Scenario: Spell is always available from another source
- **WHEN** a race, background, feat, class feature, or item grants a spell that is always available
- **THEN** the character entry SHALL preserve its source and always-available or granted state
- **THEN** generic rendering SHALL be able to keep it in the ready list without a preparation checkbox

#### Scenario: Existing legacy character is edited
- **WHEN** the editor encounters spell entries with inline `name` or `level` fields
- **THEN** it SHALL preserve renderability while normalizing successfully resolved entries to canonical refs
- **THEN** it SHALL NOT delete unresolved legacy fallback data

### Requirement: Character spell flows deduplicate references and preserve state
Character spell generation SHALL deduplicate associations by canonical reference across D&D Beyond spell groups, selected spells, class catalogs, and `compendium_refs`. When duplicate source records are merged, the result SHALL preserve the most permissive ready state and all relevant character-specific source/usage information without duplicating shared mechanics.

#### Scenario: D&D Beyond returns the same spell in multiple groups
- **WHEN** one spell appears in class spells and in another spell source group
- **THEN** the generated character spell collection SHALL contain one canonical association
- **THEN** its merged state SHALL preserve preparation or always-available status and source information

#### Scenario: Spell is already in compendium references
- **WHEN** a selected spell's canonical URL already exists in `compendium_refs`
- **THEN** the flow SHALL reuse the URL and SHALL NOT append a duplicate

#### Scenario: Spell synchronization refreshes roll metadata
- **WHEN** canonical 5e.tools spell data includes structured attack, damage, healing, saving throw, or scaling metadata
- **THEN** the compendium synchronization SHALL retain that metadata in `spell_info`
- **THEN** the character entry SHALL continue to reference it without copying it

### Requirement: Spellcasting profiles expose accessible levels and preparation capability
Shared spellcasting inference SHALL expose enough generic profile and per-entry state for the renderer to determine ready spells, management spells, preparation eligibility, positive normal slots, and pact slots without hard-coding a character identity.

#### Scenario: Prepared caster profile is generated
- **WHEN** a supported prepared caster has positive slots and referenced class spells
- **THEN** the generated profile SHALL identify preparation as available
- **THEN** the renderer SHALL be able to derive accessible circles from the positive slot resources

#### Scenario: Known caster profile is generated
- **WHEN** a supported known caster is generated or imported
- **THEN** the profile SHALL identify its associated spells as known and ready
- **THEN** it SHALL NOT grant preparation controls solely because a class catalog exists

#### Scenario: Pact caster profile is generated
- **WHEN** a supported pact caster is generated or imported
- **THEN** the profile SHALL identify pact slot usage, count, and accessible pact slot level

#### Scenario: Hybrid source has explicit preparation behavior
- **WHEN** a character has spells from sources with different preparation rules
- **THEN** entry-specific availability or preparation capability SHALL override the global profile for those entries

#### Scenario: Profile cannot infer a preparation rule
- **WHEN** source metadata is insufficient to establish that a spell is preparable
- **THEN** the generated/rendered entry SHALL degrade to read-only instead of exposing an unsupported preparation action
