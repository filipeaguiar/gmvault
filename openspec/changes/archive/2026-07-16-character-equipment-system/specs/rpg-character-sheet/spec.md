## ADDED Requirements

### Requirement: Character sheet dynamically calculates attributes and AC from resolved compendium items
The character sheet template SHALL calculate attributes (Strength, Dexterity, etc.) and Armor Class (AC) by dynamically resolving each equipment item in `char_info.equipment` to its compendium page via `ref`, and applying its modifiers and properties.

#### Scenario: Equipped magic item in compendium overrides an attribute score
- **WHEN** the character has an equipped item in `char_info.equipment` referencing a compendium page with `item_info.modifiers.stat_override` (e.g. strength: 21)
- **THEN** the character's calculated Strength score SHALL be set to the overridden value (e.g. 21) if it is higher than their base score, and all derived modifiers, saving throws, and skill checks SHALL update dynamically.

#### Scenario: Equipped shield/armor in compendium modifies Armor Class
- **WHEN** the character has an equipped item referencing a compendium page with armor properties (e.g. `item_info.type: "Shield"` and `item_info.armor_class: 2`, or `item_info.type: "Light Armor"` and `item_info.armor_class: 11`)
- **THEN** the calculated Armor Class (AC) SHALL dynamically sum these values, applying Dexterity limits correctly (medium armor capped at +2, heavy armor ignoring Dex mod, shield added as bonus).

#### Scenario: Equipped magic item in compendium adds save/AC bonuses
- **WHEN** the character has an equipped item referencing a compendium page with `item_info.modifiers.ac_bonus` or `item_info.modifiers.save_bonus`
- **THEN** these active bonuses SHALL be dynamically added to the calculated AC and saving throws.

### Requirement: Equipment tab resolves detailed properties and active status from compendium
The Equipment tab UI SHALL resolve the detailed properties of each item (weapon properties, range, damage type, armor category) from its compendium page via `ref` and render them, showing active visual cues for equipped items.

#### Scenario: Weapon details are resolved from the compendium
- **WHEN** a weapon with a valid `ref` is displayed in the Equipment tab
- **THEN** the template SHALL fetch and render its properties (e.g. finesse, light), range, and damage type from the compendium page.

#### Scenario: Item has no compendium ref
- **WHEN** an item in `char_info.equipment` lacks a `ref` or is unresolved
- **THEN** the layout SHALL render its inline name and base fields as fallback without causing build-time errors.
