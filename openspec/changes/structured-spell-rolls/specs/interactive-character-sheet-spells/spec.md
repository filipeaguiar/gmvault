## ADDED Requirements

### Requirement: Spell names expose inline Dice+ controls
The character sheet SHALL render available spell attack, damage, healing, and generic dice controls on the same visual line as the spell name in both prepared-spell cards and the complete class spell list.

#### Scenario: Prepared damage spell has an inline roll
- **WHEN** a prepared Fireball references a compendium page with a structured `8d6` damage roll
- **THEN** the prepared spell header SHALL display an `8d6` control with `data-roll-notation="8d6"` beside the spell name

#### Scenario: Class spell has an inline roll
- **WHEN** a class spell references a compendium page with structured rolls
- **THEN** the complete class list SHALL display those controls without requiring the details accordion to be opened

#### Scenario: Spell has no roll metadata
- **WHEN** a spell has no attack type and no structured rolls
- **THEN** its title line SHALL render without an empty roll container or an inferred formula

### Requirement: Spell attack controls use the character spell attack bonus
The character sheet SHALL derive spell attack notation from `char_info.spell_attack_bonus` when a referenced spell has `spell_info.attack_type`, rather than storing a character-specific formula in the compendium.

#### Scenario: Ranged spell attack is displayed
- **WHEN** Eldritch Blast has `attack_type: ranged` and the character has `spell_attack_bonus: 6`
- **THEN** the spell title line SHALL render an attack control with `data-roll-notation="1d20+6"`

### Requirement: Inline spell rolls respect the character's usable scaling tiers
The character sheet SHALL resolve structured scaling against the current character level and available `spell_slots`, and SHALL NOT render formulas for future character levels or unavailable slot levels.

#### Scenario: Cantrip scales with current character level
- **WHEN** a level 7 character displays Fire Bolt with character-level thresholds 1, 5, 11, and 17
- **THEN** the title line SHALL display `2d10` and SHALL NOT display `3d10` or `4d10`

#### Scenario: Character cannot upcast a spell yet
- **WHEN** a character has only level 3 spell slots and displays Fireball
- **THEN** the title line SHALL display the level 3 formula `8d6` and SHALL NOT display formulas for slot levels 4 through 9

#### Scenario: Character has multiple usable slot levels
- **WHEN** a character has level 3 and level 4 spell slots and displays Fireball
- **THEN** the title line SHALL expose only the usable level 3 and level 4 formulas with their slot levels identifiable

#### Scenario: Discrete slot threshold has not been reached
- **WHEN** Spirit Shroud has thresholds at slots 3, 5, 7, and 9 and the character has a level 4 slot
- **THEN** the resolved formula for that slot SHALL remain the level 3 threshold formula

#### Scenario: Multi-projectile spell lacks structured count scaling
- **WHEN** Magic Missile has a per-dart `1d4+1` roll and only prose describing additional darts
- **THEN** the title line SHALL show `1d4+1` as a per-dart roll and SHALL NOT display an inferred aggregate such as `3d4+3`

### Requirement: Inline spell rolls preserve progressive Dice+ behavior
Inline spell roll values SHALL remain readable text in a normal browser and SHALL use the existing `roll-ready` and `data-roll-notation` contract so the validated Dice+ bridge can enhance them.

#### Scenario: Character sheet opens without Dice+
- **WHEN** no compatible bridge is available
- **THEN** the inline formula SHALL remain readable and SHALL NOT require a separate roll button

#### Scenario: Prepared spell card is cloned
- **WHEN** `spells.js` clones a class spell into the prepared list
- **THEN** the cloned card SHALL preserve its inline roll metadata and controls
