---
title: Fomorian
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
  entity_name: Fomorian
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 3851e00ac11df4e4
stats:
  ac: '14'
  hp: 149 (13d12 + 65)
  speed: walk 30 ft.
  attributes:
    str: 23
    dex: 10
    con: 20
    int: 9
    wis: 14
    cha: 6
  saves: {}
  skills:
    perception: '+8'
    stealth: '+3'
  senses: darkvision 120 ft.
  languages: Giant, Undercommon
  cr: '8'
stats_meta: Huge giant C/E
---

## Actions


### Multiattack

The fomorian attacks twice with its greatclub or makes one greatclub attack and uses Evil Eye once.


### Greatclub

mw 9 to hit, reach 15 ft., one target. {@h}19 (<span class="dice+" data-roll-notation="3d8+6">3d8 + 6</span>) bludgeoning damage.


### Evil Eye

The fomorian magically forces a creature it can see within 60 feet of it to make a 14 Charisma saving throw. The creature takes 27 (<span class="dice+" data-roll-notation="6d8">6d8</span>) psychic damage on a failed save, or half as much damage on a successful one.


### Curse of the Evil Eye (Recharges after a Short or Long Rest)

With a stare, the fomorian uses Evil Eye, but on a failed save, the creature is also cursed with magical deformities. While deformed, the creature has its speed halved and has disadvantage on ability checks, saving throws, and attacks based on Strength or Dexterity.

The transformed creature can repeat the saving throw whenever it finishes a long rest, ending the effect on a success.
