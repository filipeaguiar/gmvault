---
title: Adult Gold Dragon
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
  entity_name: Adult Gold Dragon
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 1163df6002d21a27
stats:
  ac: '19'
  hp: 256 (19d12 + 133)
  speed: walk 40 ft., fly 80 ft., swim 40 ft.
  attributes:
    str: 27
    dex: 14
    con: 25
    int: 16
    wis: 15
    cha: 24
  saves:
    dex: '+8'
    con: '+13'
    wis: '+8'
    cha: '+13'
  skills:
    insight: '+8'
    perception: '+14'
    persuasion: '+13'
    stealth: '+8'
  senses: blindsight 60 ft., darkvision 120 ft.
  languages: Common, Draconic
  cr: '17'
stats_meta: Huge dragon L/G
---

## Traits


### Amphibious

The dragon can breathe air and water.


### Legendary Resistance (3/Day)

If the dragon fails a saving throw, it can choose to succeed instead.

## Actions


### Multiattack

The dragon can use its Frightful Presence. It then makes three attacks: one with its bite and two with its claws.


### Bite

mw 14 to hit, reach 10 ft., one target. {@h}19 (<span class="dice+" data-roll-notation="2d10+8">2d10 + 8</span>) piercing damage.


### Claw

mw 14 to hit, reach 5 ft., one target. {@h}15 (<span class="dice+" data-roll-notation="2d6+8">2d6 + 8</span>) slashing damage.


### Tail

mw 14 to hit, reach 15 ft., one target. {@h}17 (<span class="dice+" data-roll-notation="2d8+8">2d8 + 8</span>) bludgeoning damage.


### Frightful Presence

Each creature of the dragon's choice that is within 120 feet of the dragon and aware of it must succeed on a 21 Wisdom saving throw or become frightened for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. If a creature's saving throw is successful or the effect ends for it, the creature is immune to the dragon's Frightful Presence for the next 24 hours.


### Breath Weapons 5

The dragon uses one of the following breath weapons.

* {'type': 'item', 'name': 'Fire Breath', 'entry': 'The dragon exhales fire in a 60-foot cone. Each creature in that area must make a 21 Dexterity saving throw, taking 66 (<span class="dice+" data-roll-notation="12d10">12d10</span>) fire damage on a failed save, or half as much damage on a successful one.'}

* {'type': 'item', 'name': 'Weakening Breath', 'entry': 'The dragon exhales gas in a 60-foot cone. Each creature in that area must succeed on a 21 Strength saving throw or have disadvantage on Strength-based attack rolls, Strength checks, and Strength saving throws for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.'}


### Change Shape

The dragon magically polymorphs into a humanoid or beast that has a challenge rating no higher than its own, or back into its true form. It reverts to its true form if it dies. Any equipment it is wearing or carrying is absorbed or borne by the new form (the dragon's choice).

In a new form, the dragon retains its alignment, hit points, Hit Dice, ability to speak, proficiencies, Legendary Resistance, lair actions, and Intelligence, Wisdom, and Charisma scores, as well as this action. Its statistics and capabilities are otherwise replaced by those of the new form, except any class features or legendary actions of that form.

## Legendary Actions


### Detect

The dragon makes a Wisdom (Perception) check.


### Tail Attack

The dragon makes a tail attack.


### Wing Attack (Costs 2 Actions)

The dragon beats its wings. Each creature within 10 feet of the dragon must succeed on a 22 Dexterity saving throw or take 15 (<span class="dice+" data-roll-notation="2d6+8">2d6 + 8</span>) bludgeoning damage and be knocked prone. The dragon can then fly up to half its flying speed.
