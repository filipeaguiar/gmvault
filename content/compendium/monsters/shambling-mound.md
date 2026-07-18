---
title: Shambling Mound
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
  entity_name: Shambling Mound
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 018594a06de9ee95
stats:
  ac: '15'
  hp: 136 (16d10 + 48)
  speed: walk 20 ft., swim 20 ft.
  attributes:
    str: 18
    dex: 8
    con: 16
    int: 5
    wis: 10
    cha: 5
  saves: {}
  skills:
    stealth: '+2'
  senses: blindsight 60 ft. (blind beyond this radius)
  languages: ''
  cr: '5'
stats_meta: Large plant U
---

## Traits


### Lightning Absorption

Whenever the shambling mound is subjected to lightning damage, it takes no damage and regains a number of hit points equal to the lightning damage dealt.

## Actions


### Multiattack

The shambling mound makes two slam attacks. If both attacks hit a Medium or smaller target, the target is grappled (escape 14), and the shambling mound uses its Engulf on it.


### Slam

mw 7 to hit, reach 5 ft., one target. {@h}13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) bludgeoning damage.


### Engulf

The shambling mound engulfs a Medium or smaller creature grappled by it. The engulfed target is blinded, restrained, and unable to breathe, and it must succeed on a 14 Constitution saving throw at the start of each of the mound's turns or take 13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) bludgeoning damage. If the mound moves, the engulfed target moves with it. The mound can have only one creature engulfed at a time.
