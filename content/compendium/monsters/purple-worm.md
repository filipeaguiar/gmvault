---
title: Purple Worm
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
  entity_name: Purple Worm
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 094b2ceebe20587c
stats:
  ac: '18'
  hp: 247 (15d20 + 90)
  speed: walk 50 ft., burrow 30 ft.
  attributes:
    str: 28
    dex: 7
    con: 22
    int: 1
    wis: 8
    cha: 4
  saves:
    con: '+11'
    wis: '+4'
  skills: {}
  senses: blindsight 30 ft., tremorsense 60 ft.
  languages: ''
  cr: '15'
stats_meta: Gargantuan monstrosity U
---

## Traits


### Tunneler

The worm can burrow through solid rock at half its burrow speed and leaves a 10-foot-diameter tunnel in its wake.

## Actions


### Multiattack

The worm makes two attacks: one with its bite and one with its stinger.


### Bite

mw 14 to hit, reach 10 ft., one target. {@h}22 (<span class="dice+" data-roll-notation="3d8+9">3d8 + 9</span>) piercing damage. If the target is a Large or smaller creature, it must succeed on a 19 Dexterity saving throw or be swallowed by the worm. A swallowed creature is blinded and restrained, it has total cover against attacks and other effects outside the worm, and it takes 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) acid damage at the start of each of the worm's turns.

If the worm takes 30 damage or more on a single turn from a creature inside it, the worm must succeed on a 21 Constitution saving throw at the end of that turn or regurgitate all swallowed creatures, which fall prone in a space within 10 feet of the worm. If the worm dies, a swallowed creature is no longer restrained by it and can escape from the corpse by using 20 feet of movement, exiting prone.


### Tail Stinger

mw 14 to hit, reach 10 ft., one creature. {@h}19 (<span class="dice+" data-roll-notation="3d6+9">3d6 + 9</span>) piercing damage, and the target must make a 19 Constitution saving throw, taking 42 (<span class="dice+" data-roll-notation="12d6">12d6</span>) poison damage on a failed save, or half as much damage on a successful one.
