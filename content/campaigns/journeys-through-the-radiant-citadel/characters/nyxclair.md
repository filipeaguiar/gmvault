---
title: Nyx'Clair
date: 2026-07-09 19:00:00+00:00
params:
  kind: character
draft: false
weight: 10
summary: Elf Warlock 2 importado do D&D Beyond.
tags:
- jogador
- elf
- warlock
visibility: players
status: ready
char_info:
  class: Warlock 2
  race: Elf
  ac: '12'
  hp: '16'
  hp_max: '16'
  hp_current: '16'
  feat: Magic Initiate (Wizard), Sage Ability Score Improvements
  size: Medium
  alignment: Neutral
  dndbeyond_id: '168145599'
  proficiency_bonus: 2
  spell_dc: 12
  spell_attack_bonus: 4
  avatar: /images/campaigns/journeys-through-the-radiant-citadel/handouts/nyx.png
  speed:
    walk: 30
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: Passive Perception 11, Darkvision 60 ft.
  passive_senses:
    perception: 11
    investigation: 14
    insight: 13
  languages: Common, Draconic, Elvish
  saves:
    str: -1
    dex: 1
    con: 2
    int: 2
    wis: 3
    cha: 4
  saves_proficient:
    str: false
    dex: false
    con: false
    int: false
    wis: true
    cha: true
  saves_summary: Wis +3, Cha +4
  mods:
    str: -1
    dex: 1
    con: 2
    int: 2
    wis: 1
    cha: 2
  stats:
    str: 8
    dex: 12
    con: 14
    int: 14
    wis: 12
    cha: 14
  currencies:
    cp: 0
    sp: 0
    gp: 23
    ep: 0
    pp: 0
  skills:
    acrobatics:
      bonus: 1
      proficient: false
      expertise: false
      stat: dex
    animal-handling:
      bonus: 1
      proficient: false
      expertise: false
      stat: wis
    arcana:
      bonus: 4
      proficient: true
      expertise: false
      stat: int
    athletics:
      bonus: -1
      proficient: false
      expertise: false
      stat: str
    deception:
      bonus: 4
      proficient: true
      expertise: false
      stat: cha
    history:
      bonus: 4
      proficient: true
      expertise: false
      stat: int
    insight:
      bonus: 3
      proficient: true
      expertise: false
      stat: wis
    intimidation:
      bonus: 2
      proficient: false
      expertise: false
      stat: cha
    investigation:
      bonus: 4
      proficient: true
      expertise: false
      stat: int
    medicine:
      bonus: 1
      proficient: false
      expertise: false
      stat: wis
    nature:
      bonus: 2
      proficient: false
      expertise: false
      stat: int
    perception:
      bonus: 1
      proficient: false
      expertise: false
      stat: wis
    performance:
      bonus: 2
      proficient: false
      expertise: false
      stat: cha
    persuasion:
      bonus: 2
      proficient: false
      expertise: false
      stat: cha
    religion:
      bonus: 2
      proficient: false
      expertise: false
      stat: int
    sleight-of-hand:
      bonus: 1
      proficient: false
      expertise: false
      stat: dex
    stealth:
      bonus: 1
      proficient: false
      expertise: false
      stat: dex
    survival:
      bonus: 1
      proficient: false
      expertise: false
      stat: wis
  actions:
  - name: Ataque
    ref: /compendium/rules/action-attack/
    max_uses: 0
    reset: ''
  - name: Esconder
    ref: /compendium/rules/action-hide/
    max_uses: 0
    reset: ''
  - name: Desengajar
    ref: /compendium/rules/action-disengage/
    max_uses: 0
    reset: ''
  - name: Disparar
    ref: /compendium/rules/action-dash/
    max_uses: 0
    reset: ''
  - name: Ajudar
    ref: /compendium/rules/action-help/
    max_uses: 0
    reset: ''
  - name: Esquivar
    ref: /compendium/rules/action-dodge/
    max_uses: 0
    reset: ''
  - name: Usar Objeto
    ref: /compendium/rules/action-use-object/
    max_uses: 0
    reset: ''
  - name: Magical Cunning
    max_uses: 1
    reset: Descanso Longo
    source: class
    ref: /compendium/rules/magical-cunning/
  - name: Initiate a Circle Spell
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/initiate-a-circle-spell/
  - name: 'Circle Spell: Augment'
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/circle-spell-augment/
  - name: 'Circle Spell: Distribute'
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/circle-spell-distribute/
  - name: 'Circle Spell: Expand'
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/circle-spell-expand/
  - name: 'Circle Spell: Prolong'
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/circle-spell-prolong/
  - name: 'Circle Spell: Safeguard'
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/circle-spell-safeguard/
  - name: 'Circle Spell: Supplant'
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/circle-spell-supplant/
  - name: 'Pact of the Chain: Attack'
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/pact-of-the-chain-attack/
  equipment:
  - name: Leather
    quantity: 1
    equipped: true
    filter_type: Armor
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/leather-armor/
  - name: Dagger
    quantity: 1
    equipped: false
    filter_type: Weapon
    attack_formula: 1d20 + 1
    damage_formula: 1d4 + 1
    ref: /compendium/items/dagger/
  - name: Dagger
    quantity: 1
    equipped: false
    filter_type: Weapon
    attack_formula: 1d20 + 1
    damage_formula: 1d4 + 1
    ref: /compendium/items/dagger/
  - name: Quarterstaff
    quantity: 1
    equipped: true
    filter_type: Weapon
    attack_formula: 1d20 + 1
    damage_formula: 1d6 + -1
    ref: /compendium/items/quarterstaff/
  - name: Sickle
    quantity: 1
    equipped: false
    filter_type: Weapon
    attack_formula: 1d20 + -1
    damage_formula: 1d4 + -1
    ref: /compendium/items/sickle/
  - name: Parchment
    quantity: 8
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/parchment/
  - name: Backpack
    quantity: 1
    equipped: true
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/backpack/
  - name: Calligrapher's Supplies
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/calligraphers-supplies/
  - name: Robe
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/robe/
  - name: Book
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/book/
  - name: Book
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/book/
  - name: Orb
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/orb/
  - name: Oil
    quantity: 10
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/oil/
  - name: Parchment
    quantity: 10
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/parchment/
  - name: Tinderbox
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/tinderbox/
  - name: Book
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/book/
  - name: Lamp
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/lamp/
  - name: Ink Pen
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/ink-pen/
  - name: Ink
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/ink/
  spells:
  - name: Eldritch Blast
    level: 0
    prepared: false
    usage: Truque
    ref: /compendium/spells/eldritch-blast/
  - name: Guidance
    level: 0
    prepared: false
    usage: Truque
    ref: /compendium/spells/guidance/
  - name: Gust
    level: 0
    prepared: true
    usage: Truque
    ref: /compendium/spells/gust/
  - name: Mage Hand
    level: 0
    prepared: false
    usage: Truque
    ref: /compendium/spells/mage-hand/
  - name: Message
    level: 0
    prepared: true
    usage: Truque
    ref: /compendium/spells/message/
  - name: Ray of Frost
    level: 0
    prepared: true
    usage: Truque
    ref: /compendium/spells/ray-of-frost/
  - name: Charm Person
    level: 1
    prepared: true
    usage: 1x/Descanso Longo
    ref: /compendium/spells/charm-person/
  - name: Find Familiar
    level: 1
    prepared: false
    usage: Ritual
    ref: /compendium/spells/find-familiar/
  - name: Speak with Animals
    level: 1
    prepared: false
    usage: Slot / Ritual
    ref: /compendium/spells/speak-with-animals/
  - name: Unseen Servant
    level: 1
    prepared: false
    usage: Slot / Ritual
    ref: /compendium/spells/unseen-servant/
  classes_progression:
  - name: Warlock
    level: 2
    subclass: ''
locations: []
factions: []
compendium_refs:
- /compendium/classes/warlock/
- /compendium/feats/magic-initiate/
- /compendium/items/backpack/
- /compendium/items/book/
- /compendium/items/calligraphers-supplies/
- /compendium/items/dagger/
- /compendium/items/ink-pen/
- /compendium/items/ink/
- /compendium/items/lamp/
- /compendium/items/leather-armor/
- /compendium/items/oil/
- /compendium/items/orb/
- /compendium/items/parchment/
- /compendium/items/quarterstaff/
- /compendium/items/robe/
- /compendium/items/sickle/
- /compendium/items/tinderbox/
- /compendium/races/elf/
- /compendium/rules/action-attack/
- /compendium/rules/action-dash/
- /compendium/rules/action-disengage/
- /compendium/rules/action-dodge/
- /compendium/rules/action-help/
- /compendium/rules/action-hide/
- /compendium/rules/action-use-object/
- /compendium/rules/agonizing-blast-eldritch-blast/
- /compendium/rules/circle-spell-augment/
- /compendium/rules/circle-spell-distribute/
- /compendium/rules/circle-spell-expand/
- /compendium/rules/circle-spell-prolong/
- /compendium/rules/circle-spell-safeguard/
- /compendium/rules/circle-spell-supplant/
- /compendium/rules/eldritch-invocation-options/
- /compendium/rules/eldritch-invocations/
- /compendium/rules/initiate-a-circle-spell/
- /compendium/rules/magical-cunning/
- /compendium/rules/otherworldly-patron/
- /compendium/rules/pact-magic/
- /compendium/rules/pact-of-the-chain-attack/
- /compendium/rules/pact-of-the-chain/
- /compendium/rules/pact-of-the-tome/
- /compendium/spells/charm-person/
- /compendium/spells/eldritch-blast/
- /compendium/spells/find-familiar/
- /compendium/spells/guidance/
- /compendium/spells/gust/
- /compendium/spells/mage-hand/
- /compendium/spells/message/
- /compendium/spells/ray-of-frost/
- /compendium/spells/speak-with-animals/
- /compendium/spells/unseen-servant/
spells_usage:
- name: Charm Person
  usage: 1x/Descanso Longo
- name: Eldritch Blast
  usage: Truque
- name: Find Familiar
  usage: Ritual
- name: Guidance
  usage: Truque
- name: Gust
  usage: Truque
- name: Mage Hand
  usage: Truque
- name: Message
  usage: Truque
- name: Ray of Frost
  usage: Truque
- name: Speak with Animals
  usage: Slot / Ritual
- name: Unseen Servant
  usage: Slot / Ritual
---
### Biografia
Este personagem foi importado automaticamente do D&D Beyond. 

### Equipamentos e Recursos
Acesse a ficha completa original no D&D Beyond para acompanhar o inventário de itens e slots de magia em tempo real.
