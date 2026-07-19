## ADDED Requirements

### Requirement: Complete local character compendium synchronization
The editor SHALL synchronize all supported shared entities represented by the selected local character, including classes, species, subclasses, feats, standard actions, class and subclass features, spells, items, and magic items, after an operation introduces them and through an explicit full synchronization operation.

#### Scenario: Editor adds supported content
- **WHEN** an editing operation adds a supported item, magic item, feat, spell, action, or feature
- **THEN** the editor SHALL materialize its canonical local compendium page before associating its URL with the character

#### Scenario: User synchronizes an existing character
- **WHEN** the user selects the full compendium synchronization operation
- **THEN** the editor SHALL resolve all supported entities represented in the selected character
- **THEN** it SHALL retain unresolved legacy data and report entities it could not resolve

#### Scenario: Existing reference is already local
- **WHEN** a selected character already references an existing canonical compendium page
- **THEN** the editor SHALL reuse that page and SHALL NOT create a duplicate reference
