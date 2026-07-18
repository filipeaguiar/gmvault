---
title: Ankheg
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
  entity_name: Ankheg
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: d571da270fdb9dcb
stats:
  ac: '14'
  hp: 39 (6d10 + 6)
  speed: walk 30 ft., burrow 10 ft.
  attributes:
    str: 17
    dex: 11
    con: 13
    int: 1
    wis: 13
    cha: 6
  saves: {}
  skills: {}
  senses: darkvision 60 ft., tremorsense 60 ft.
  languages: ''
  cr: '2'
stats_meta: Large monstrosity U
---

## Actions


### Bite

mw 5 to hit, reach 5 ft., one target. {@h}10 (<span class="dice+" data-roll-notation="2d6+3">2d6 + 3</span>) slashing damage plus 3 (<span class="dice+" data-roll-notation="1d6">1d6</span>) acid damage. If the target is a Large or smaller creature, it is grappled (escape 13). Until this grapple ends, the ankheg can bite only the grappled creature and has advantage on attack rolls to do so.


### Acid Spray {@recharge}

The ankheg spits acid in a line that is 30 feet long and 5 feet wide, provided that it has no creature grappled. Each creature in that line must make a 13 Dexterity saving throw, taking 10 (<span class="dice+" data-roll-notation="3d6">3d6</span>) acid damage on a failed save, or half as much damage on a successful one.
