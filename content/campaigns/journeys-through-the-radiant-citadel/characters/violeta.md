---
title: Violeta
date: 2026-07-09 19:00:00+00:00
params:
  kind: character
draft: false
weight: 10
summary: Human Sorcerer 1 importado do D&D Beyond.
tags:
- jogador
- human
- sorcerer
visibility: players
status: ready
char_info:
  class: Sorcerer 1
  race: Human
  ac: '11'
  hp: '9'
  hp_max: '9'
  hp_current: '9'
  feat: Magic Initiate (Cleric), Magic Initiate (Wizard), Sage Ability Score Improvements
  size: Medium
  alignment: Neutral
  dndbeyond_id: '168153030'
  proficiency_bonus: 2
  spell_dc: 12
  spell_attack_bonus: 4
  avatar: /images/campaigns/journeys-through-the-radiant-citadel/handouts/violeta.png
  speed:
    walk: 30
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: Passive Perception 11
  passive_senses:
    perception: 11
    investigation: 9
    insight: 13
  languages: Common, Netherese, Turmic
  saves:
    str: 0
    dex: 1
    con: 5
    int: -1
    wis: 1
    cha: 4
  saves_proficient:
    str: false
    dex: false
    con: true
    int: false
    wis: false
    cha: true
  saves_summary: Con +5, Cha +4
  mods:
    str: 0
    dex: 1
    con: 3
    int: -1
    wis: 1
    cha: 2
  stats:
    str: 10
    dex: 13
    con: 16
    int: 8
    wis: 13
    cha: 15
  currencies:
    cp: 0
    sp: 0
    gp: 36
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
      bonus: 1
      proficient: true
      expertise: false
      stat: int
    athletics:
      bonus: 0
      proficient: false
      expertise: false
      stat: str
    deception:
      bonus: 2
      proficient: false
      expertise: false
      stat: cha
    history:
      bonus: 1
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
      bonus: -1
      proficient: false
      expertise: false
      stat: int
    medicine:
      bonus: 1
      proficient: false
      expertise: false
      stat: wis
    nature:
      bonus: -1
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
      bonus: 4
      proficient: true
      expertise: false
      stat: cha
    religion:
      bonus: -1
      proficient: false
      expertise: false
      stat: int
    sleight-of-hand:
      bonus: 1
      proficient: false
      expertise: false
      stat: dex
    stealth:
      bonus: 3
      proficient: true
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
  - name: Innate Sorcery
    max_uses: 2
    reset: Descanso Longo
    source: class
    ref: /compendium/rules/innate-sorcery/
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
  equipment:
  - name: Dagger
    quantity: 1
    equipped: true
    filter_type: Weapon
    attack_formula: 1d20 + 3
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
    attack_formula: 1d20 + 2
    damage_formula: 1d6 + 0
    ref: /compendium/items/quarterstaff/
  - name: Spear
    quantity: 1
    equipped: true
    filter_type: Weapon
    attack_formula: 1d20 + 2
    damage_formula: 1d6 + 0
    ref: /compendium/items/spear/
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
  - name: Crystal
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/crystal/
  - name: Oil
    quantity: 2
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/oil/
  - name: Rations
    quantity: 10
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/rations/
  - name: Rope
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/rope/
  - name: Tinderbox
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/tinderbox/
  - name: Torch
    quantity: 10
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/torch/
  - name: Waterskin
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/waterskin/
  - name: Caltrops
    quantity: 20
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/caltrops/
  - name: Crowbar
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/crowbar/
  spells:
  - name: Acid Splash
    level: 0
    prepared: true
    usage: Truque
    ref: /compendium/spells/acid-splash/
  - name: Light
    level: 0
    prepared: false
    usage: Truque
    ref: /compendium/spells/light/
  - name: Mending
    level: 0
    prepared: true
    usage: Truque
    ref: /compendium/spells/mending/
  - name: Prestidigitation
    level: 0
    prepared: false
    usage: Truque
    ref: /compendium/spells/prestidigitation/
  - name: Shocking Grasp
    level: 0
    prepared: false
    usage: Truque
    ref: /compendium/spells/shocking-grasp/
  - name: Sorcerous Burst
    level: 0
    prepared: false
    usage: Truque
  - name: Spare the Dying
    level: 0
    prepared: true
    usage: Truque
    ref: /compendium/spells/spare-the-dying/
  - name: Thaumaturgy
    level: 0
    prepared: true
    usage: Truque
    ref: /compendium/spells/thaumaturgy/
  - name: Bane
    level: 1
    prepared: true
    usage: 1x/Descanso Longo
    ref: /compendium/spells/bane/
  - name: Burning Hands
    level: 1
    prepared: false
    usage: Slot de Magia
    ref: /compendium/spells/burning-hands/
  - name: Detect Magic
    level: 1
    prepared: false
    usage: Slot / Ritual
    ref: /compendium/spells/detect-magic/
  - name: Mage Armor
    level: 1
    prepared: true
    usage: 1x/Descanso Longo
    ref: /compendium/spells/mage-armor/
  classes_progression:
  - name: Sorcerer
    level: 1
    subclass: ''
locations: []
factions: []
compendium_refs:
- /compendium/classes/sorcerer/
- /compendium/feats/magic-initiate/
- /compendium/items/backpack/
- /compendium/items/book/
- /compendium/items/calligraphers-supplies/
- /compendium/items/caltrops/
- /compendium/items/crowbar/
- /compendium/items/crystal/
- /compendium/items/dagger/
- /compendium/items/oil/
- /compendium/items/parchment/
- /compendium/items/quarterstaff/
- /compendium/items/rations/
- /compendium/items/robe/
- /compendium/items/rope/
- /compendium/items/spear/
- /compendium/items/tinderbox/
- /compendium/items/torch/
- /compendium/items/waterskin/
- /compendium/races/human/
- /compendium/rules/action-attack/
- /compendium/rules/action-dash/
- /compendium/rules/action-disengage/
- /compendium/rules/action-dodge/
- /compendium/rules/action-help/
- /compendium/rules/action-hide/
- /compendium/rules/action-use-object/
- /compendium/rules/circle-spell-augment/
- /compendium/rules/circle-spell-distribute/
- /compendium/rules/circle-spell-expand/
- /compendium/rules/circle-spell-prolong/
- /compendium/rules/circle-spell-safeguard/
- /compendium/rules/circle-spell-supplant/
- /compendium/rules/initiate-a-circle-spell/
- /compendium/rules/innate-sorcery/
- /compendium/rules/spellcasting/
- /compendium/spells/acid-splash/
- /compendium/spells/bane/
- /compendium/spells/burning-hands/
- /compendium/spells/detect-magic/
- /compendium/spells/light/
- /compendium/spells/mage-armor/
- /compendium/spells/mending/
- /compendium/spells/prestidigitation/
- /compendium/spells/shocking-grasp/
- /compendium/spells/spare-the-dying/
- /compendium/spells/thaumaturgy/
spells_usage:
- name: Acid Splash
  usage: Truque
- name: Bane
  usage: 1x/Descanso Longo
- name: Burning Hands
  usage: Slot de Magia
- name: Detect Magic
  usage: Slot / Ritual
- name: Light
  usage: Truque
- name: Mage Armor
  usage: 1x/Descanso Longo
- name: Mending
  usage: Truque
- name: Prestidigitation
  usage: Truque
- name: Shocking Grasp
  usage: Truque
- name: Sorcerous Burst
  usage: Truque
- name: Spare the Dying
  usage: Truque
- name: Thaumaturgy
  usage: Truque
---
### Biografia
Este personagem foi importado automaticamente do D&D Beyond. 

### Equipamentos e Recursos
Acesse a ficha completa original no D&D Beyond para acompanhar o inventário de itens e slots de magia em tempo real.
