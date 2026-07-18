---
title: Gibbering Mouther
params:
  kind: monster
draft: true
weight: 10
summary: Draft imported from 5e.tools (MM). Requires translation and editorial review.
tags:
- draft
- importado
- 5etools
visibility: gm
status: draft
source:
  provider: 5e.tools
  book: MM
  entity_type: monster
  entity_name: Gibbering Mouther
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: eca235fc87e81c2c
stats:
  ac: '9'
  hp: 67 (9d8 + 27)
  speed: walk 10 ft., swim 10 ft.
  attributes:
    str: 10
    dex: 8
    con: 16
    int: 3
    wis: 10
    cha: 6
  saves: {}
  skills: {}
  senses: darkvision 60 ft.
  languages: ''
  cr: '2'
stats_meta: Medium aberration N
---

## Traits


### Aberrant Ground

The ground in a 10-foot radius around the mouther is doughlike 3. Each creature that starts its turn in that area must succeed on a 10 Strength saving throw or have its speed reduced to 0 until the start of its next turn.


### Gibbering

The mouther babbles incoherently while it can see any creature and isn't incapacitated. Each creature that starts its turn within 20 feet of the mouther and can hear the gibbering must succeed on a 10 Wisdom saving throw. On a failure, the creature can't take reactions until the start of its next turn and rolls a <span class="dice+" data-roll-notation="d8">d8</span> to determine what it does during its turn. On a 1 to 4, the creature does nothing. On a 5 or 6, the creature takes no action or bonus action and uses all its movement to move in a randomly determined direction. On a 7 or 8, the creature makes a melee attack against a randomly determined creature within its reach or does nothing if it can't make such an attack.

## Actions


### Multiattack

The gibbering mouther makes one bite attack and, if it can, uses its Blinding Spittle.


### Bites

mw 2 to hit, reach 5 ft., one creature. {@h}17 (<span class="dice+" data-roll-notation="5d6">5d6</span>) piercing damage. If the target is Medium or smaller, it must succeed on a 10 Strength saving throw or be knocked prone. If the target is killed by this damage, it is absorbed into the mouther.


### Blinding Spittle 5

The mouther spits a chemical glob at a point it can see within 15 feet of it. The glob explodes in a blinding flash of light on impact. Each creature within 5 feet of the flash must succeed on a 13 Dexterity saving throw or be blinded until the end of the mouther's next turn.
