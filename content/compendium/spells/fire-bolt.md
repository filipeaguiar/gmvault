---
title: Fire Bolt
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
  entity_name: Fire Bolt
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 91b6628fd540f395
spell_info:
  level: Cantrip
  school: Evocation
  cast_time: 1 action
  range: 120 feet
  components: V, S
  ritual: false
  duration: Instantaneous
  level_number: 0
  attack_type: ranged
  damage_types:
  - fire
  saving_throws: []
  rolls:
  - kind: damage
    notation: 1d10
    label: Dano
    damage_type: fire
    scaling:
      mode: character_level
      thresholds:
        '1': 1d10
        '5': 2d10
        '11': 3d10
        '17': 4d10
---

You hurl a mote of fire at a creature or an object within range. Make a ranged spell attack against the target. On a hit, the target takes <span class="dice+" data-roll-notation="1d10">1d10</span> Fire damage. A flammable object hit by this spell starts burning if it isn't being worn or carried.

## At Higher Levels


### Cantrip Upgrade

The damage increases by <span class="dice+" data-roll-notation="1d10">1d10</span> when you reach levels 5 (<span class="dice+" data-roll-notation="2d10">2d10</span>), 11 (<span class="dice+" data-roll-notation="3d10">3d10</span>), and 17 (<span class="dice+" data-roll-notation="4d10">4d10</span>).
