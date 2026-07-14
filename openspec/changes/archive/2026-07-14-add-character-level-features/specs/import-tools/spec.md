## ADDED Requirements

### Requirement: Import script extracts and translates class and subclass level features
The import script `import_dndbeyond.py` SHALL extract level-specific features for classes and subclasses from 5e.tools JSON files during character import and translate them into Portuguese.

#### Scenario: Character has class and subclass level features
- **WHEN** `import_dndbeyond.py` is run for a character with a subclass or class features defined in 5e.tools
- **THEN** it SHALL extract those features, create translated compendium rules under `content/compendium/rules/`, and reference them in the character's `compendium_refs`
