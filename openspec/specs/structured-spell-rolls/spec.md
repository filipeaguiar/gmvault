# structured-spell-rolls Specification

## Purpose
TBD - created by archiving change structured-spell-rolls. Update Purpose after archive.
## Requirements
### Requirement: Spell compendium pages store canonical roll metadata
The system SHALL store spell roll metadata under `spell_info.rolls` as a list of structured entries containing at least `kind`, `notation`, and `label`, using canonical identifiers independent of translated prose.

#### Scenario: Damage spell has a structured roll
- **WHEN** Fireball is imported with `{@damage 8d6}` and `damageInflict: [fire]`
- **THEN** its compendium front matter SHALL contain a `damage` roll with notation `8d6` and damage type `fire`

#### Scenario: Healing spell has a structured roll
- **WHEN** Cure Wounds is imported with a `dice` tag and `miscTags` containing `HL`
- **THEN** its compendium front matter SHALL classify the formula as `kind: healing`

#### Scenario: Generic dice spell is not misclassified
- **WHEN** Sleep contains `{@dice 5d8}` without the healing marker
- **THEN** its compendium front matter SHALL classify the formula as `kind: dice`

### Requirement: Structured spell metadata describes attack and defense semantics
The system SHALL store `spellAttack`, `damageInflict`, and `savingThrow` semantics in canonical `spell_info` fields without embedding a character-specific attack bonus.

#### Scenario: Ranged spell attack is imported
- **WHEN** Eldritch Blast contains `spellAttack: [R]`
- **THEN** its compendium front matter SHALL contain `attack_type: ranged`

#### Scenario: Saving throw metadata is imported
- **WHEN** Fireball contains `savingThrow: [dexterity]`
- **THEN** its compendium front matter SHALL list `dexterity` under `saving_throws`

### Requirement: Spell rolls are normalized and deduplicated
The system SHALL normalize whitespace in dice notation and SHALL avoid duplicate roll entries when base and scaled tags describe the same base formula.

#### Scenario: Formula whitespace is normalized
- **WHEN** Magic Missile contains `{@damage 1d4 + 1}`
- **THEN** the stored notation SHALL be `1d4+1`

#### Scenario: Scaled damage repeats the base formula
- **WHEN** Fireball contains both `{@damage 8d6}` and `{@scaledamage 8d6|3-9|1d6}`
- **THEN** `spell_info.rolls` SHALL contain one base `8d6` damage roll enriched with scaling metadata

### Requirement: Spell metadata preserves character-level and slot-level scaling
The system SHALL normalize `scalingLevelDice` as character-level thresholds and SHALL normalize `scaledamage` or `scaledice` tags as spell-slot thresholds, preserving continuous ranges and discrete progression steps.

#### Scenario: Cantrip has explicit character-level scaling
- **WHEN** Fire Bolt contains `scalingLevelDice` values for levels 1, 5, 11, and 17
- **THEN** its structured roll SHALL contain `character_level` thresholds mapping those levels to `1d10`, `2d10`, `3d10`, and `4d10`

#### Scenario: Leveled spell scales continuously by slot
- **WHEN** Fireball contains `{@scaledamage 8d6|3-9|1d6}`
- **THEN** its structured roll SHALL contain `spell_slot` thresholds from slot level 3 through 9 with the corresponding formulas

#### Scenario: Leveled spell scales at discrete slot steps
- **WHEN** Spirit Shroud contains `{@scaledamage 1d8|3,5,7,9|1d8}`
- **THEN** its structured roll SHALL preserve thresholds 3, 5, 7, and 9 without treating slot level 4 as a new increment

#### Scenario: Projectile count exists only in prose
- **WHEN** Magic Missile stores `1d4+1` per dart but describes additional darts only in higher-level prose
- **THEN** structured metadata SHALL preserve the per-dart `1d4+1` roll and SHALL NOT invent an aggregate formula or projectile-count scaling

### Requirement: Manual spell pages expose the structured schema
The spell archetype SHALL include the canonical roll, attack, damage, saving throw, and level-number fields so manually authored spells use the same format as imported spells.

#### Scenario: Maintainer creates a spell from the archetype
- **WHEN** Hugo creates a new spell page from `archetypes/spell.md`
- **THEN** the generated front matter SHALL include `level_number`, `attack_type`, `damage_types`, `saving_throws`, and `rolls` under `spell_info`, with the documented scaling structure available for manual entries

