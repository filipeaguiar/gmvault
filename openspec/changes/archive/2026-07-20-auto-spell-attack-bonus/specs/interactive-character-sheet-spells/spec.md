## MODIFIED Requirements

### Requirement: Spell attack controls use the character spell attack bonus
The character sheet SHALL derive spell attack notation from the resolved character spell attack bonus when a referenced spell has `spell_info.attack_type`, rather than storing a character-specific formula in the compendium. The resolved bonus SHALL use an explicit non-placeholder `char_info.spell_attack_bonus` when present; otherwise, for a supported single-class profile, it SHALL use proficiency plus the modifier identified by `char_info.spellcasting.ability`. If neither source can resolve a valid bonus, the sheet SHALL omit only the attack control and SHALL continue rendering the spell and its other structured roll controls.

#### Scenario: Ranged spell attack is displayed
- **WHEN** Eldritch Blast has `attack_type: ranged` and the character has an explicit `spell_attack_bonus: 6`
- **THEN** the spell title line SHALL render an attack control with `data-roll-notation="1d20+6"`

#### Scenario: Ranged spell attack is derived
- **WHEN** Eldritch Blast has `attack_type: ranged` and a single-class character has `proficiency_bonus: 2`, `mods.cha: 4`, and `spellcasting.ability: cha` without an explicit spell attack override
- **THEN** the spell title line SHALL render an attack control with `data-roll-notation="1d20+6"`

#### Scenario: Spell attack data is incomplete
- **WHEN** a spell has `attack_type` but the character has neither an explicit usable attack bonus nor complete supported derivation inputs
- **THEN** the spell title line SHALL omit the attack control
- **THEN** any structured damage, healing, or generic dice controls SHALL remain renderable

#### Scenario: Multi-class attack source is ambiguous
- **WHEN** a character has multiple spellcasting classes and the spell entry does not identify a casting ability or resolvable class source
- **THEN** the sheet SHALL NOT derive a spell attack control from the global profile
