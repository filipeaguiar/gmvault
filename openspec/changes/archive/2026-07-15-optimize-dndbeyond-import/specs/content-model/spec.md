## ADDED Requirements

### Requirement: Character pages define structured stats under char_info
Character pages SHALL define structured statistics under `char_info` including class, race, AC, HP, stats (Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma), feats, speed (including walk, swim, fly, climb, burrow), senses, languages, size, and alignment.

#### Scenario: Full character stats are available
- **WHEN** a character page is rendered by Hugo
- **THEN** the layout SHALL be able to access the pre-calculated speed, saves, senses, languages, size, and alignment from the front matter under `char_info` without requiring fallback template calculations
