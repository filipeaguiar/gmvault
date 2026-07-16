# character-background-equipment Specification

## Purpose
TBD - created by archiving change interactive-background-equipment. Update Purpose after archive.
## Requirements
### Requirement: Background Selection and Initial Equipment
The system SHALL prompt the user to select a Background from the 2024 core rules (XPHB) during character creation. Upon selection, the system SHALL automatically map the starting equipment items provided by the Background and populate them into the character's inventory (`char_info.equipment`), and ensure the corresponding items exist in the local compendium.

#### Scenario: User selects Criminal background
- **WHEN** the user selects the "Criminal" background during character creation
- **THEN** the system automatically adds 2 Daggers, Thieves' Tools, Crowbar, 2 Pouches, and Traveler's Clothes to the character's equipment list.

### Requirement: Class Pack Selection and Expansion
The system SHALL prompt the user to choose an equipment pack (e.g., Burglar's Pack, Explorer's Pack) when applicable, based on their chosen class. The system SHALL "explode" the chosen pack into its individual component items and add each item separately to the character's equipment list, ensuring they exist in the compendium.

#### Scenario: User selects Burglar's Pack
- **WHEN** the user selects a "Burglar's Pack"
- **THEN** the system adds Backpack, Ball Bearings, Bell, 10 Candles, Crowbar, Hooded Lantern, 7 Oil flasks, 5 Rations, Rope, Tinderbox, and Waterskin as individual items in the character's equipment list.

