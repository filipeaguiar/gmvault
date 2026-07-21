---
title: Snilloc's Snowball Swarm
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
  book: XGE
  entity_type: spell
  entity_name: Snilloc's Snowball Swarm
  remote_file: spells/spells-xge.json
  remote_key: spell
  remote_id: b08461d6bf5c8a32
spell_info:
  level: 2nd level
  school: Evocation
  cast_time: 1 action
  range: 90 feet
  components: V, S, M (a piece of ice or a small white rock chip)
  ritual: false
  duration: Instantaneous
  level_number: 2
  attack_type: null
  damage_types:
  - cold
  saving_throws:
  - dexterity
  rolls:
  - kind: damage
    notation: 3d6
    label: Dano
    damage_type: cold
    scaling:
      mode: spell_slot
      thresholds:
        '2': 3d6
        '3': 4d6
        '4': 5d6
        '5': 6d6
        '6': 7d6
        '7': 8d6
        '8': 9d6
        '9': 10d6
---

A flurry of magic snowballs erupts from a point you choose within range. Each creature in a 5-foot-radius sphere centered on that point must make a Dexterity saving throw. A creature takes <span class="dice+" data-roll-notation="3d6">3d6</span> cold damage on a failed save, or half as much damage on a successful one.

## At Higher Levels


### At Higher Levels

When you cast this spell using a spell slot of 3rd level or higher, the damage increases by <span class="dice+" data-roll-notation="3d6">3d6</span> for each slot level above 2nd.
