## ADDED Requirements

### Requirement: New spellcaster profiles persist a normalized casting ability
The interactive character creation flow SHALL determine and persist `char_info.spellcasting.ability` as a normalized ability key for a selected single-class spellcaster when the class data resolves that ability. It SHALL leave the field empty rather than guessing when the ability cannot be resolved.

#### Scenario: Creating a Warlock
- **WHEN** the user creates a single-class Warlock and the resolved class data identifies Charisma as its spellcasting ability
- **THEN** the generated character front matter SHALL contain `char_info.spellcasting.ability: cha`

#### Scenario: Class ability cannot be resolved
- **WHEN** the selected class data does not provide an unambiguous spellcasting ability
- **THEN** the generated profile SHALL leave `spellcasting.ability` empty
- **THEN** the creation flow SHALL NOT assign an ability based only on class-name heuristics

### Requirement: New character creation distinguishes absent spell attack overrides
The interactive character creation flow SHALL not write `spell_attack_bonus: 0` merely as a placeholder for a character whose spell attack bonus is intended to be derived.

#### Scenario: Creating a spellcaster with a resolved ability
- **WHEN** the user creates a single-class spellcaster with a resolvable casting ability and no exceptional attack bonus
- **THEN** the generated front matter SHALL leave the explicit spell attack override absent or mark it as absent distinctly from zero
