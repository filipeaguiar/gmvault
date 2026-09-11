---
title: Burning Hands
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
  entity_name: Burning Hands
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 862f2a13f2ca5f92
spell_info:
  level: 1st level
  school: Evocation
  cast_time: 1 action
  range: 15 feet
  components: V, S
  ritual: false
  duration: Instantaneous
  level_number: 1
  attack_type: null
  damage_types:
  - fire
  saving_throws:
  - dexterity
  rolls:
  - kind: damage
    notation: 3d6
    label: Dano
    damage_type: fire
    scaling:
      mode: spell_slot
      thresholds:
        '1': 3d6
        '2': 4d6
        '3': 5d6
        '4': 6d6
        '5': 7d6
        '6': 8d6
        '7': 9d6
        '8': 10d6
        '9': 11d6
---

A thin sheet of flames shoots forth from you. Each creature in a 15-foot Cone makes a Dexterity saving throw, taking <span class="dice+" data-roll-notation="3d6">3d6</span> Fire damage on a failed save or half as much damage on a successful one.

Flammable objects in the Cone that aren't being worn or carried start burning.

## At Higher Levels


### Using a Higher-Level Spell Slot

The damage increases by <span class="dice+" data-roll-notation="3d6">3d6</span> for each spell slot level above 1.
