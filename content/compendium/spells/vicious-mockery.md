---
title: Vicious Mockery
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
  entity_name: Vicious Mockery
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: aff97722448891d2
spell_info:
  level: Cantrip
  school: Enchantment
  cast_time: 1 action
  range: 60 feet
  components: V
  duration: Instantaneous
  level_number: 0
  attack_type: null
  damage_types:
  - psychic
  saving_throws:
  - wisdom
  rolls:
  - kind: damage
    notation: 1d6
    label: Dano
    damage_type: psychic
    scaling:
      mode: character_level
      thresholds:
        '1': 1d6
        '5': 2d6
        '11': 3d6
        '17': 4d6
---

You unleash a string of insults laced with subtle enchantments at one creature you can see or hear within range. The target must succeed on a Wisdom saving throw or take <span class="dice+" data-roll-notation="1d6">1d6</span> Psychic damage and have Disadvantage on the next attack roll it makes before the end of its next turn.

## At Higher Levels


### Cantrip Upgrade

The damage increases by <span class="dice+" data-roll-notation="1d6">1d6</span> when you reach levels 5 (<span class="dice+" data-roll-notation="2d6">2d6</span>), 11 (<span class="dice+" data-roll-notation="3d6">3d6</span>), and 17 (<span class="dice+" data-roll-notation="4d6">4d6</span>).
