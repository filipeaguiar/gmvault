## ADDED Requirements

### Requirement: Characters include level features in Forge metadata
The Forge exporter SHALL extract class and subclass level-specific features from the character's `compendium_refs` and include them in the traits/features section Z034.

#### Scenario: Character has class or subclass features
- **WHEN** a character page contains `compendium_refs` pointing to kind `rule` or `feat`
- **THEN** the exporter SHALL append these features to the Forge `abilities` array `Z034` with stable IDs, names, and descriptions
