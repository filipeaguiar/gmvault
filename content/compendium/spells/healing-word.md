---
title: Healing Word
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
  entity_name: Healing Word
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: c0de0c232e4afb10
spell_info:
  level: 1st level
  school: Abjuration
  cast_time: 1 bonus action
  range: 60 feet
  components: V
  duration: Instantaneous
  level_number: 1
  attack_type: null
  damage_types: []
  saving_throws: []
  rolls:
  - kind: healing
    notation: 2d4
    label: Cura
    scaling:
      mode: spell_slot
      thresholds:
        '1': 2d4
        '2': 4d4
        '3': 6d4
        '4': 8d4
        '5': 10d4
        '6': 12d4
        '7': 14d4
        '8': 16d4
        '9': 18d4
---

A creature of your choice that you can see within range regains Hit Points equal to <span class="dice+" data-roll-notation="2d4">2d4</span> plus your spellcasting ability modifier.

## At Higher Levels


### Using a Higher-Level Spell Slot

The healing increases by <span class="dice+" data-roll-notation="2d4">2d4</span> for each spell slot level above 1.
