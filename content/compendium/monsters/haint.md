---
title: Haint
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
  entity_name: Haint
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 7d340d08ef3f6daa
stats:
  ac: '12'
  hp: 75 (10d8 + 30)
  speed: walk 30 ft., fly 30 ft.
  attributes:
    str: 7
    dex: 15
    con: 17
    int: 10
    wis: 13
    cha: 17
  saves: {}
  skills:
    deception: '+6'
    stealth: '+8'
  senses: darkvision 60 ft.
  languages: any languages it knew in life
  cr: '7'
stats_meta: Medium undead N
---

## Traits


### Incorporeal Movement

The haint can move through other creatures and objects as if they were difficult terrain. It takes 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) force damage if it ends its turn inside an object.


### Unusual Nature

The haint doesn't require air, food, drink, or sleep.

## Actions


### Multiattack

The haint makes two Sorrowful Touch attacks.


### Sorrowful Touch

ms 6 to hit, reach 5 ft., one creature. {@h}21 (<span class="dice+" data-roll-notation="4d8+3">4d8 + 3</span>) psychic damage.


### Change Shape

The haint magically assumes the appearance of the Humanoid it was in life, while retaining its game statistics. The assumed appearance ends if the haint is reduced to 0 hit points or uses an action to end it.

## Bonus Actions


### Shared Sorrow

The haint targets one creature it can see within 60 feet of itself that is missing any hit points, sharing its own torment with this pained soul. The target must succeed on a 14 Wisdom saving throw or be incapacitated.

A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. If a creature's saving throw is successful or the effect ends for it, the creature is immune to the haint's Shared Sorrow for the next 24 hours.
