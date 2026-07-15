## ADDED Requirements

### Requirement: D&D Beyond character importer exports full stats, speeds, saves, senses, languages, size, and alignment
The character import script `import_dndbeyond.py` SHALL parse and calculate size, alignment, speeds, senses, languages, and saving throw modifiers from the D&D Beyond JSON and save them in the character's Markdown under `char_info`.

#### Scenario: Character speed is calculated
- **WHEN** `import_dndbeyond.py` parses a character with multiple movement speeds
- **THEN** it SHALL output walk, fly, swim, climb, and burrow speeds under `char_info.speed` in the front matter

#### Scenario: Character saving throws are calculated
- **WHEN** `import_dndbeyond.py` parses a character
- **THEN** it SHALL calculate modifiers for Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma saving throws (including starting class proficiencies and stat modifiers) and output them under `char_info.saves` in the front matter

#### Scenario: Character size and alignment are resolved
- **WHEN** `import_dndbeyond.py` parses a character
- **THEN** it SHALL map the D&D Beyond sizeId and alignmentId to human-readable strings (e.g. Medium, Lawful Good) and output them under `char_info.size` and `char_info.alignment` in the front matter

#### Scenario: Character senses and languages are resolved
- **WHEN** `import_dndbeyond.py` parses a character
- **THEN** it SHALL extract passive perception, darkvision, and other senses, along with all known languages, and output them under `char_info.senses` and `char_info.languages` in the front matter
