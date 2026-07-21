---
title: Frostbite
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
  entity_name: Frostbite
  remote_file: spells/spells-xge.json
  remote_key: spell
  remote_id: 27e938c685e9bcf0
spell_info:
  level: Cantrip
  school: Evocation
  cast_time: 1 action
  range: 60 feet
  components: V, S
  ritual: false
  duration: Instantaneous
  level_number: 0
  attack_type: null
  damage_types:
  - cold
  saving_throws:
  - constitution
  rolls:
  - kind: damage
    notation: 1d6
    label: Dano
    damage_type: cold
    scaling:
      mode: character_level
      thresholds:
        '1': 1d6
        '5': 2d6
        '11': 3d6
        '17': 4d6
---

You cause numbing frost to form on one creature that you can see within range. The target must make a Constitution saving throw. On a failed save, the target takes <span class="dice+" data-roll-notation="1d6">1d6</span> cold damage, and it has disadvantage on the next weapon attack roll it makes before the end of its next turn.

The spell's damage increases by <span class="dice+" data-roll-notation="1d6">1d6</span> when you reach 5th level (<span class="dice+" data-roll-notation="2d6">2d6</span>), 11th level (<span class="dice+" data-roll-notation="3d6">3d6</span>), and 17th level (<span class="dice+" data-roll-notation="4d6">4d6</span>).
