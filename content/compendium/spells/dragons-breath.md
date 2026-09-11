---
title: Dragon's Breath
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
  entity_name: Dragon's Breath
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 79a653ca1b5dc43e
spell_info:
  level: 2nd level
  school: Transmutation
  cast_time: 1 bonus action
  range: Touch
  components: V, S, M (a hot pepper)
  ritual: false
  duration: Concentration, up to 1 minute
  level_number: 2
  attack_type: null
  damage_types:
  - acid
  - cold
  - fire
  - lightning
  - poison
  saving_throws:
  - dexterity
  rolls:
  - kind: damage
    notation: 3d6
    label: Dano
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

You touch one willing creature, and choose Acid, Cold, Fire, Lightning, or Poison. Until the spell ends, the target can take a Magic action to exhale a 15-foot Cone. Each creature in that area makes a Dexterity saving throw, taking <span class="dice+" data-roll-notation="3d6">3d6</span> damage of the chosen type on a failed save or half as much damage on a successful one.

## At Higher Levels


### Using a Higher-Level Spell Slot

The damage increases by <span class="dice+" data-roll-notation="3d6">3d6</span> for each spell slot level above 2.
