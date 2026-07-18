---
title: Cloaker
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
  entity_name: Cloaker
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 994169514b0cfde4
stats:
  ac: '14'
  hp: 78 (12d10 + 12)
  speed: walk 10 ft., fly 40 ft.
  attributes:
    str: 17
    dex: 15
    con: 12
    int: 13
    wis: 12
    cha: 14
  saves: {}
  skills:
    stealth: '+5'
  senses: darkvision 60 ft.
  languages: Deep Speech, Undercommon
  cr: '8'
stats_meta: Large aberration C/N
---

## Traits


### Damage Transfer

While attached to a creature, the cloaker takes only half the damage dealt to it (rounded down), and that creature takes the other half.


### False Appearance

While the cloaker remains motionless without its underside exposed, it is indistinguishable from a dark leather cloak.


### Light Sensitivity

While in bright light, the cloaker has disadvantage on attack rolls and Wisdom (Perception) checks that rely on sight.

## Actions


### Multiattack

The cloaker makes two attacks: one with its bite and one with its tail.


### Bite

mw 6 to hit, reach 5 ft., one creature. {@h}10 (<span class="dice+" data-roll-notation="2d6+3">2d6 + 3</span>) piercing damage, and if the target is Large or smaller, the cloaker attaches to it. If the cloaker has advantage against the target, the cloaker attaches to the target's head, and the target is blinded and unable to breathe while the cloaker is attached. While attached, the cloaker can make this attack only against the target and has advantage on the attack roll. The cloaker can detach itself by spending 5 feet of its movement. A creature, including the target, can take its action to detach the cloaker by succeeding on a 16 Strength check.


### Tail

mw 6 to hit, reach 10 ft., one creature. {@h}7 (<span class="dice+" data-roll-notation="1d8+3">1d8 + 3</span>) slashing damage.


### Moan

Each creature within 60 feet of the cloaker that can hear its moan and that isn't an aberration must succeed on a 13 Wisdom saving throw or become frightened until the end of the cloaker's next turn. If a creature's saving throw is successful, the creature is immune to the cloaker's moan for the next 24 hours.


### Phantasms (Recharges after a Short or Long Rest)

The cloaker magically creates three illusory duplicates of itself if it isn't in bright light. The duplicates move with it and mimic its actions, shifting position so as to make it impossible to track which cloaker is the real one. If the cloaker is ever in an area of bright light, the duplicates disappear.

Whenever any creature targets the cloaker with an attack or a harmful spell while a duplicate remains, that creature rolls randomly to determine whether it targets the cloaker or one of the duplicates. A creature is unaffected by this magical effect if it can't see or if it relies on senses other than sight.

A duplicate has the cloaker's AC and uses its saving throws. If an attack hits a duplicate, or if a duplicate fails a saving throw against an effect that deals damage, the duplicate disappears.
