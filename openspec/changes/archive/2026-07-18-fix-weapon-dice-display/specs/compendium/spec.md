## MODIFIED Requirements

### Requirement: Compendium supports core RPG entity kinds
The compendium SHALL support monsters, items, magic items, classes, races, feats, spells, backgrounds, conditions, and rules. Item and magic item pages SHALL use mapped values in `item_info` fields, not raw 5e.tools abbreviations.

#### Scenario: Entity page exists
- **WHEN** a compendium entity page is rendered
- **THEN** the layout SHALL display its title, content, and metadata using either a kind-specific partial or the default page renderer

#### Scenario: Monster page exists
- **WHEN** a monster page has stat block metadata
- **THEN** the monster renderer SHALL display a stat block-oriented view before or alongside the Markdown content

#### Scenario: Weapon item has mapped item_info
- **WHEN** a weapon item page has `item_info.type` containing a 5e.tools type code like `M|XPHB`
- **THEN** the compendium rebuild process SHALL map it to `Weapon` (melee) or `Weapon` (ranged)
- **THEN** the `damage_type` SHALL be mapped from abbreviation to full name (e.g., `P` → `piercing`)
- **THEN** the `properties` SHALL be mapped from abbreviations to full names (e.g., `F|XPHB` → `finesse`)

#### Scenario: Armor item has mapped item_info
- **WHEN** an armor item page has `item_info.type` containing a 5e.tools type code like `LA|XPHB`
- **THEN** the compendium rebuild process SHALL map it to `Light Armor`, `Medium Armor`, `Heavy Armor`, or `Shield`
