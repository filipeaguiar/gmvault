---
title: Beholder
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
  entity_name: Beholder
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 1bc771170f77fb86
stats:
  ac: '18'
  hp: 180 (19d10 + 76)
  speed: walk 0 ft., fly 20 ft.
  attributes:
    str: 10
    dex: 14
    con: 18
    int: 17
    wis: 15
    cha: 17
  saves:
    int: '+8'
    wis: '+7'
    cha: '+8'
  skills:
    perception: '+12'
  senses: darkvision 120 ft.
  languages: Deep Speech, Undercommon
  cr: '13'
stats_meta: Large aberration L/E
---

## Traits


### Antimagic Cone

The beholder's central eye creates an area of antimagic, as in the antimagic field spell, in a 150-foot cone. At the start of each of its turns, the beholder decides which way the cone faces and whether the cone is active. The area works against the beholder's own eye rays.

## Actions


### Bite

mw 5 to hit, reach 5 ft., one target. {@h}14 (<span class="dice+" data-roll-notation="4d6">4d6</span>) piercing damage.


### Eye Rays

The beholder shoots three of the following magical eye rays at random (reroll duplicates), choosing one to three targets it can see within 120 feet of it:

* {'type': 'itemSub', 'name': '1. Charm Ray', 'entry': 'The targeted creature must succeed on a 16 Wisdom saving throw or be charmed by the beholder for 1 hour, or until the beholder harms the creature.'}

* {'type': 'itemSub', 'name': '2. Paralyzing Ray', 'entry': 'The targeted creature must succeed on a 16 Constitution saving throw or be paralyzed for 1 minute. The target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.'}

* {'type': 'itemSub', 'name': '3. Fear Ray', 'entry': 'The targeted creature must succeed on a 16 Wisdom saving throw or be frightened for 1 minute. The target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.'}

* {'type': 'itemSub', 'name': '4. Slowing Ray', 'entry': "The targeted creature must succeed on a 16 Dexterity saving throw. On a failed save, the target's speed is halved for 1 minute. In addition, the creature can't take reactions, and it can take either an action or a bonus action on its turn, not both. The creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success."}

* {'type': 'itemSub', 'name': '5. Enervation Ray', 'entry': 'The targeted creature must make a 16 Constitution saving throw, taking 36 (<span class="dice+" data-roll-notation="8d8">8d8</span>) necrotic damage on a failed save, or half as much damage on a successful one.'}

* {'type': 'itemSub', 'name': '6. Telekinetic Ray', 'entries': ["If the target is a creature, it must succeed on a 16 Strength saving throw or the beholder moves it up to 30 feet in any direction. It is restrained by the ray's telekinetic grip until the start of the beholder's next turn or until the beholder is incapacitated.", "If the target is an object weighing 300 pounds or less that isn't being worn or carried, it is moved up to 30 feet in any direction. The beholder can also exert fine control on objects with this ray, such as manipulating a simple tool or opening a door or a container."]}

* {'type': 'itemSub', 'name': '7. Sleep Ray', 'entry': 'The targeted creature must succeed on a 16 Wisdom saving throw or fall asleep and remain unconscious for 1 minute. The target awakens if it takes damage or another creature takes an action to wake it. This ray has no effect on constructs and undead.'}

* {'type': 'itemSub', 'name': '8. Petrification Ray', 'entry': 'The targeted creature must make a 16 Dexterity saving throw. On a failed save, the creature begins to turn to stone and is restrained. It must repeat the saving throw at the end of its next turn. On a success, the effect ends. On a failure, the creature is petrified until freed by the greater restoration spell or other magic.'}

* {'type': 'itemSub', 'name': '9. Disintegration Ray', 'entries': ['If the target is a creature, it must succeed on a 16 Dexterity saving throw or take 45 (<span class="dice+" data-roll-notation="10d8">10d8</span>) force damage. If this damage reduces the creature to 0 hit points, its body becomes a pile of fine gray dust.', 'If the target is a Large or smaller nonmagical object or creation of magical force, it is disintegrated without a saving throw. If the target is a Huge or larger object or creation of magical force, this ray disintegrates a 10-foot cube of it.']}

* {'type': 'itemSub', 'name': '10. Death Ray', 'entry': 'The targeted creature must succeed on a 16 Dexterity saving throw or take 55 (<span class="dice+" data-roll-notation="10d10">10d10</span>) necrotic damage. The target dies if the ray reduces it to 0 hit points.'}

## Legendary Actions


### Eye Ray

The beholder uses one random eye ray.
