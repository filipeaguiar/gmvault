---
title: Dissonant Whispers
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
  entity_name: Dissonant Whispers
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: a34a372a40ca7c94
spell_info:
  level: 1st level
  school: Enchantment
  cast_time: 1 action
  range: 60 feet
  components: V
  duration: Instantaneous
  level_number: 1
  attack_type: null
  damage_types:
  - psychic
  saving_throws:
  - wisdom
  rolls:
  - kind: damage
    notation: 3d6
    label: Dano
    damage_type: psychic
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

One creature of your choice that you can see within range hears a discordant melody in its mind. The target makes a Wisdom saving throw. On a failed save, it takes <span class="dice+" data-roll-notation="3d6">3d6</span> Psychic damage and must immediately use its Reaction, if available, to move as far away from you as it can, using the safest route. On a successful save, the target takes half as much damage only.

## At Higher Levels


### Using a Higher-Level Spell Slot

The damage increases by <span class="dice+" data-roll-notation="3d6">3d6</span> for each spell slot level above 1.
