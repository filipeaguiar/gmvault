---
title: Revenant
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
  entity_name: Revenant
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: b3a1cdcce4a55d4c
stats:
  ac: '13'
  hp: 136 (16d8 + 64)
  speed: walk 30 ft.
  attributes:
    str: 18
    dex: 14
    con: 18
    int: 13
    wis: 16
    cha: 18
  saves:
    str: '+7'
    con: '+7'
    wis: '+6'
    cha: '+7'
  skills: {}
  senses: darkvision 60 ft.
  languages: the languages it knew in life
  cr: '5'
stats_meta: Medium undead N
---

## Traits


### Regeneration

The revenant regains 10 hit points at the start of its turn. If the revenant takes fire or radiant damage, this trait doesn't function at the start of the revenant's next turn. The revenant's body is destroyed only if it starts its turn with 0 hit points and doesn't regenerate.


### Rejuvenation

When the revenant's body is destroyed, its soul lingers. After 24 hours, the soul inhabits and animates another humanoid corpse on the same plane of existence and regains all its hit points. While the soul is bodiless, a wish spell can be used to force the soul to go to the afterlife and not return.


### Turn Immunity

The revenant is immune to effects that turn undead.


### Vengeful Tracker

The revenant knows the distance to and direction of any creature against which it seeks revenge, even if the creature and the revenant are on different planes of existence. If the creature being tracked by the revenant dies, the revenant knows.

## Actions


### Multiattack

The revenant makes two fist attacks.


### Fist

mw 7 to hit, reach 5 ft., one target. {@h}11 (<span class="dice+" data-roll-notation="2d6+4">2d6 + 4</span>) bludgeoning damage. If the target is a creature against which the revenant has sworn vengeance, the target takes an extra 14 (<span class="dice+" data-roll-notation="4d6">4d6</span>) bludgeoning damage. Instead of dealing damage, the revenant can grapple the target (escape 14) provided the target is Large or smaller.


### Vengeful Glare

The revenant targets one creature it can see within 30 feet of it and against which it has sworn vengeance. The target must make a 15 Wisdom saving throw. On a failure, the target is paralyzed until the revenant deals damage to it, or until the end of the revenant's next turn. When the paralysis ends, the target is frightened of the revenant for 1 minute. The frightened target can repeat the saving throw at the end of each of its turns, with disadvantage if it can see the revenant, ending the frightened condition on itself on a success.
