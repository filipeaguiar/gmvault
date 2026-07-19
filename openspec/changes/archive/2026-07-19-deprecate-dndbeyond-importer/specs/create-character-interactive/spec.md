## MODIFIED Requirements

### Requirement: Compendium Population
The script SHALL query the `5etools` mirrors for every supported shared entity represented by the locally created character, including classes, subclasses, species, feats, standard actions, class and subclass features, spells, items, and magic items, and SHALL materialize missing canonical compendium pages before writing their references into the character note.

#### Scenario: Character has a new species
- **WHEN** the user selects a species that is not in the compendium
- **THEN** the script SHALL download and save its canonical page from 5e.tools before writing the character

#### Scenario: Character has supported missing shared content
- **WHEN** the completed creation data includes a supported missing feat, spell, item, magic item, action, or class feature
- **THEN** the script SHALL synchronize the canonical compendium page and record its returned internal URL without duplicate references

#### Scenario: Content cannot be resolved
- **WHEN** a supported selected entity cannot be resolved unambiguously from 5e.tools
- **THEN** the script SHALL report it and SHALL NOT write a fabricated canonical reference
