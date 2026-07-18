---
title: Behir
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
  entity_name: Behir
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: b78b8a92bc5fff6a
stats:
  ac: '17'
  hp: 168 (16d12 + 64)
  speed: walk 50 ft., climb 40 ft.
  attributes:
    str: 23
    dex: 16
    con: 18
    int: 7
    wis: 14
    cha: 12
  saves: {}
  skills:
    perception: '+6'
    stealth: '+7'
  senses: darkvision 90 ft.
  languages: Draconic
  cr: '11'
stats_meta: Huge monstrosity N/E
---

## Actions


### Multiattack

The behir makes two attacks: one with its bite and one to constrict.


### Bite

mw 10 to hit, reach 10 ft., one target. {@h}22 (<span class="dice+" data-roll-notation="3d10+6">3d10 + 6</span>) piercing damage.


### Constrict

mw 10 to hit, reach 5 ft., one Large or smaller creature. {@h}17 (<span class="dice+" data-roll-notation="2d10+6">2d10 + 6</span>) bludgeoning damage plus 17 (<span class="dice+" data-roll-notation="2d10+6">2d10 + 6</span>) slashing damage. The target is grappled (escape 16) if the behir isn't already constricting a creature, and the target is restrained until this grapple ends.


### Lightning Breath 5

The behir exhales a line of lightning that is 20 feet long and 5 feet wide. Each creature in that line must make a 16 Dexterity saving throw, taking 66 (<span class="dice+" data-roll-notation="12d10">12d10</span>) lightning damage on a failed save, or half as much damage on a successful one.


### Swallow

The behir makes one bite attack against a Medium or smaller target it is grappling. If the attack hits, the target is also swallowed, and the grapple ends. While swallowed, the target is blinded and restrained, it has total cover against attacks and other effects outside the behir, and it takes 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) acid damage at the start of each of the behir's turns. A behir can have only one creature swallowed at a time.

If the behir takes 30 damage or more on a single turn from the swallowed creature, the behir must succeed on a 14 Constitution saving throw at the end of that turn or regurgitate the creature, which falls prone in a space within 10 feet of the behir. If the behir dies, a swallowed creature is no longer restrained by it and can escape from the corpse by using 15 feet of movement, exiting prone.
