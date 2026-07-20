## ADDED Requirements

### Requirement: Single-class spell attack bonus is derived from structured character data
The system SHALL derive the base spell attack bonus for a single-class character as `char_info.proficiency_bonus + char_info.mods[char_info.spellcasting.ability]` when the spellcasting ability is a supported normalized ability key and both numeric inputs are available.

#### Scenario: Warlock attack is derived from Charisma and proficiency
- **WHEN** a single-class Warlock has `proficiency_bonus: 2`, `mods.cha: 4`, and `spellcasting.ability: cha`
- **THEN** the derived spell attack bonus SHALL be `6`

#### Scenario: Character lacks a resolvable casting ability
- **WHEN** a character has no supported `spellcasting.ability` or no matching numeric modifier
- **THEN** the system SHALL report no derived spell attack bonus
- **THEN** the system SHALL NOT invent a `+0` spell attack bonus

### Requirement: Explicit spell attack bonuses override derived base bonuses
The system SHALL use an explicitly configured character spell attack bonus in preference to a derived base spell attack bonus, so exceptional bonuses remain representable.

#### Scenario: Character has an explicit bonus
- **WHEN** a character has valid derivation inputs totaling `+6` and an explicitly configured spell attack bonus of `+7`
- **THEN** the resolved spell attack bonus SHALL be `+7`

#### Scenario: Legacy placeholder can be derived
- **WHEN** a legacy character has `spell_attack_bonus: 0` together with complete supported derivation inputs
- **THEN** the resolved spell attack bonus SHALL use the derived value
