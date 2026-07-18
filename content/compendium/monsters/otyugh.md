---
title: Otyugh
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
  entity_name: Otyugh
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: e5696b738ba5a643
stats:
  ac: '14'
  hp: 114 (12d10 + 48)
  speed: walk 30 ft.
  attributes:
    str: 16
    dex: 11
    con: 19
    int: 6
    wis: 13
    cha: 6
  saves:
    con: '+7'
  skills: {}
  senses: darkvision 120 ft.
  languages: Otyugh
  cr: '5'
stats_meta: Large aberration N
---

## Traits


### Limited Telepathy

The otyugh can magically transmit simple messages and images to any creature within 120 feet of it that can understand a language. This form of telepathy doesn't allow the receiving creature to telepathically respond.

## Actions


### Multiattack

The otyugh makes three attacks: one with its bite and two with its tentacles.


### Bite

mw 6 to hit, reach 5 ft., one target. {@h}12 (<span class="dice+" data-roll-notation="2d8+3">2d8 + 3</span>) piercing damage. If the target is a creature, it must succeed on a 15 Constitution saving throw against disease or become poisoned until the disease is cured. Every 24 hours that elapse, the target must repeat the saving throw, reducing its hit point maximum by 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) on a failure. The disease is cured on a success. The target dies if the disease reduces its hit point maximum to 0. This reduction to the target's hit point maximum lasts until the disease is cured.


### Tentacle

mw 6 to hit, reach 10 ft., one target. {@h}7 (<span class="dice+" data-roll-notation="1d8+3">1d8 + 3</span>) bludgeoning damage plus 4 (<span class="dice+" data-roll-notation="1d8">1d8</span>) piercing damage. If the target is Medium or smaller, it is grappled (escape 13) and restrained until the grapple ends. The otyugh has two tentacles, each of which can grapple one target.


### Tentacle Slam

The otyugh slams creatures grappled by it into each other or a solid surface. Each creature must succeed on a 14 Constitution saving throw or take 10 (<span class="dice+" data-roll-notation="2d6+3">2d6 + 3</span>) bludgeoning damage and be stunned until the end of the otyugh's next turn. On a successful save, the target takes half the bludgeoning damage and isn't stunned.
