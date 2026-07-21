---
title: Ice Knife
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
  entity_name: Ice Knife
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: dd5be09e791c4e42
spell_info:
  level: 1st level
  school: Conjuration
  cast_time: 1 action
  range: 60 feet
  components: S, M (a drop of water or a piece of ice)
  ritual: false
  duration: Instantaneous
  level_number: 1
  attack_type: ranged
  damage_types:
  - cold
  - piercing
  saving_throws:
  - dexterity
  rolls:
  - kind: damage
    notation: 1d10
    label: Dano
  - kind: damage
    notation: 2d6
    label: Dano
    scaling:
      mode: spell_slot
      thresholds:
        '1': 2d6
        '2': 3d6
        '3': 4d6
        '4': 5d6
        '5': 6d6
        '6': 7d6
        '7': 8d6
        '8': 9d6
        '9': 10d6
---

You create a shard of ice and fling it at one creature within range. Make a ranged spell attack against the target. On a hit, the target takes <span class="dice+" data-roll-notation="1d10">1d10</span> Piercing damage. Hit or miss, the shard then explodes. The target and each creature within 5 feet of it must succeed on a Dexterity saving throw or take <span class="dice+" data-roll-notation="2d6">2d6</span> Cold damage.

## At Higher Levels


### Using a Higher-Level Spell Slot

The Cold damage increases by <span class="dice+" data-roll-notation="2d6">2d6</span> for each spell slot level above 1.
