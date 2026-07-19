---
title: Ray of Frost
params:
  kind: spell
draft: false
weight: 10
summary: Draft imported from 5e.tools (XPHB). Requires translation and editorial review.
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
  entity_name: Ray of Frost
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 4cc9181c11843cdb
spell_info:
  level: Cantrip
  school: Evocation
  cast_time: 1 action
  range: 60 feet
  components: V, S
  duration: Instantaneous
  level_number: 0
  attack_type: ranged
  damage_types:
  - cold
  saving_throws: []
  rolls:
  - kind: damage
    notation: 1d8
    label: Dano
    damage_type: cold
    scaling:
      mode: character_level
      thresholds:
        '1': 1d8
        '5': 2d8
        '11': 3d8
        '17': 4d8
---

A frigid beam of blue-white light streaks toward a creature within range. Make a ranged spell attack against the target. On a hit, it takes <span class="dice+" data-roll-notation="1d8">1d8</span> Cold damage, and its Speed is reduced by 10 feet until the start of your next turn.

## At Higher Levels


### Cantrip Upgrade

The damage increases by <span class="dice+" data-roll-notation="1d8">1d8</span> when you reach levels 5 (<span class="dice+" data-roll-notation="2d8">2d8</span>), 11 (<span class="dice+" data-roll-notation="3d8">3d8</span>), and 17 (<span class="dice+" data-roll-notation="4d8">4d8</span>).
