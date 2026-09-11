---
title: Chromatic Orb
type: spell
draft: false
weight: 10
tags:
- draft
- importado
- 5etools
visibility: public
status: draft
source:
  provider: 5e.tools
  book: XPHB
  entity_type: spell
  entity_name: Chromatic Orb
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 9e78c6da62cc4874
spell_info:
  level: 1st level
  school: Evocation
  cast_time: 1 action
  range: 90 feet
  components: V, S, M (a diamond worth 50+ GP)
  ritual: false
  duration: Instantaneous
  level_number: 1
  attack_type: ranged
  damage_types:
  - acid
  - cold
  - fire
  - lightning
  - poison
  - thunder
  saving_throws: []
  rolls:
  - kind: damage
    notation: 3d8
    label: Dano
    scaling:
      mode: spell_slot
      thresholds:
        '1': 3d8
        '2': 4d8
        '3': 5d8
        '4': 6d8
        '5': 7d8
        '6': 8d8
        '7': 9d8
        '8': 10d8
        '9': 11d8
---

You hurl an orb of energy at a target within range. Choose Acid, Cold, Fire, Lightning, Poison, or Thunder for the type of orb you create, and then make a ranged spell attack against the target. On a hit, the target takes <span class="dice+" data-roll-notation="3d8">3d8</span> damage of the chosen type.

If you roll the same number on two or more of the d8s, the orb leaps to a different target of your choice within 30 feet of the target. Make an attack roll against the new target, and make a new damage roll. The orb can't leap again unless you cast the spell with a level 2+ spell slot.

## At Higher Levels


### Using a Higher-Level Spell Slot

The damage increases by <span class="dice+" data-roll-notation="3d8">3d8</span> for each spell slot level above 1. The orb can leap a maximum number of times equal to the level of the slot expended, and a creature can be targeted only once by each casting of this spell.
