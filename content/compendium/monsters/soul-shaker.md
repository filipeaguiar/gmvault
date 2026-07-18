---
title: Soul Shaker
params:
  kind: monster
draft: true
weight: 10
summary: Draft imported from 5e.tools (JTTRC). Requires translation and editorial review.
tags:
- draft
- importado
- 5etools
visibility: gm
status: draft
source:
  provider: 5e.tools
  book: JTTRC
  entity_type: monster
  entity_name: Soul Shaker
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 724e33e4dc993fa3
stats:
  ac: '13'
  hp: 76 (8d10 + 32)
  speed: walk 20 ft.
  attributes:
    str: 20
    dex: 8
    con: 18
    int: 8
    wis: 11
    cha: 14
  saves: {}
  skills: {}
  senses: blindsight 60 ft. (blind beyond this radius)
  languages: telepathy 60 ft.
  cr: '4'
stats_meta: Large undead C/E
---

## Traits


### Enthralled Lure (1/Day)

The soul shaker can cast the geas spell, requiring no spell components and using Charisma as the spellcasting ability (spell save 12).


### Reconstruction

When the soul shaker is reduced to 0 hit points, it explodes into 7 (<span class="dice+" data-roll-notation="1d4+5">1d4 + 5</span>) crawling claws. After 6 (<span class="dice+" data-roll-notation="1d12">1d12</span>) days, if at least two of those crawling claws are alive, they teleport to the location of the soul shaker's death and merge together, whereupon the soul shaker reforms and regains all its hit points.


### Unusual Nature

The soul shaker doesn't require air, food, drink, or sleep.

## Actions


### Crushing Grasp

mw 7 to hit, reach 5 ft., one target. {@h}14 (<span class="dice+" data-roll-notation="2d8+5">2d8 + 5</span>) bludgeoning damage. If the target is a Medium or smaller creature, it is grappled (escape 15). The soul shaker can have only one creature grappled in this way at a time.

## Bonus Actions


### Consume Vitality

The soul shaker targets a creature it is grappling. If the target is not a Construct or an Undead, the target must succeed on a 14 Constitution saving throw or take 7 (<span class="dice+" data-roll-notation="2d6">2d6</span>) necrotic damage. The target's hit point maximum is reduced by an amount equal to the necrotic damage taken, and the soul shaker regains hit points equal to that amount. This reduction lasts until the target finishes a long rest. The target dies if its hit point maximum is reduced to 0.
