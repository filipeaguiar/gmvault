## Context

Currently, character sheets imported from D&D Beyond only contain basic fields (`class`, `race`, `ac`, `hp`, `stats`, `feat`), leaving speed, saving throws, senses, and languages to be dynamically computed inside the Hugo layout files at compile time. This leads to duplicate and fragile logic (e.g. mapping race names to speed numbers or class names to saving throw proficiencies in Hugo templates). 

Extracting and pre-calculating all these metrics in Python during the import phase simplifies Hugo rendering and makes the markdown files the single source of truth for character statistics.

## Goals / Non-Goals

**Goals:**
- Add size, alignment, speeds (walk, swim, climb, fly, burrow), senses, languages, and saving throw modifiers to the Python D&D Beyond import process.
- Write these fields under `char_info` in the character markdown front matter.
- Update `layouts/partials/helpers/forge_statblock.html` to consume these pre-calculated values directly.
- Re-import all campaign characters to update their front matter metadata.

**Non-Goals:**
- Modifying how NPCs or monsters are imported from 5e.tools.
- Changing the Forge JSON export structure or attributes keys.

## Decisions

### Decision 1: Structured representation in character front matter
We will structure the new attributes under the `char_info` block in the YAML front matter:
```yaml
char_info:
  class: "Bard 2"
  race: "Halfling"
  ac: "14"
  hp: "14"
  size: "Small"
  alignment: "Chaotic Neutral"
  speed:
    walk: 25
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: "Passive Perception 11"
  languages: "Common, Halfling"
  saves:
    str: -1
    dex: 5
    con: 1
    int: 0
    wis: -1
    cha: 6
```
*Rationale:* Storing these as nested structures under `char_info` keeps the front matter clean and makes parsing inside Hugo templates trivial.

### Decision 2: Calculate saves in Python using D&D 2024 rule logic
The Python script will calculate saving throws by:
1. Identifying starting class proficiencies (e.g., Bard gets Dex and Cha; Rogue gets Dex and Int).
2. Adding the proficiency bonus (`+2` for level 1-4) to proficient saves.
3. Adding the respective attribute modifier.
*Rationale:* Implementing class saving throw rules is much simpler and less error-prone in Python than in Hugo template logic.

## Risks / Trade-offs

- **[Risk]** Missing or incomplete data on manually created characters.
  - *Mitigation*: The Hugo template will fallback to default values (e.g., speed 30, no saving throw proficiencies) if these fields are missing.
