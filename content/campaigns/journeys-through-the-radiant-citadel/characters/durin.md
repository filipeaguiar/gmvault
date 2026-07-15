---
title: Durin
date: 2026-07-09 19:00:00+00:00
params:
  kind: character
draft: false
weight: 10
summary: Dwarf Monk 2 importado do D&D Beyond.
tags:
- jogador
- dwarf
- monk
visibility: players
status: ready
char_info:
  class: Monk 2
  race: Dwarf
  ac: '15'
  hp: '17'
  hp_max: '17'
  hp_current: '17'
  feat: Nenhum
  size: Medium
  alignment: Neutral
  dndbeyond_id: '168106464'
  proficiency_bonus: 2
  spell_dc: 0
  spell_attack_bonus: 0
  avatar: /images/campaigns/journeys-through-the-radiant-citadel/handouts/durin.png
  speed:
    walk: 40
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: Passive Perception 12, Darkvision 120 ft.
  passive_senses:
    perception: 12
    investigation: 12
    insight: 12
  languages: Common, Common Sign Language, Dwarvish
  saves:
    str: 1
    dex: 5
    con: 2
    int: 2
    wis: 2
    cha: 0
  saves_proficient:
    str: true
    dex: true
    con: false
    int: false
    wis: false
    cha: false
  saves_summary: Str +1, Dex +5
  mods:
    str: -1
    dex: 3
    con: 2
    int: 2
    wis: 2
    cha: 0
  stats:
    str: 8
    dex: 16
    con: 14
    int: 14
    wis: 15
    cha: 10
  currencies:
    cp: 0
    sp: 0
    gp: 36
    ep: 0
    pp: 0
  skills:
    acrobatics:
      bonus: 3
      proficient: false
      expertise: false
      stat: dex
    animal-handling:
      bonus: 2
      proficient: false
      expertise: false
      stat: wis
    arcana:
      bonus: 2
      proficient: false
      expertise: false
      stat: int
    athletics:
      bonus: 1
      proficient: true
      expertise: false
      stat: str
    deception:
      bonus: 0
      proficient: false
      expertise: false
      stat: cha
    history:
      bonus: 4
      proficient: true
      expertise: false
      stat: int
    insight:
      bonus: 2
      proficient: false
      expertise: false
      stat: wis
    intimidation:
      bonus: 0
      proficient: false
      expertise: false
      stat: cha
    investigation:
      bonus: 2
      proficient: false
      expertise: false
      stat: int
    medicine:
      bonus: 2
      proficient: false
      expertise: false
      stat: wis
    nature:
      bonus: 2
      proficient: false
      expertise: false
      stat: int
    perception:
      bonus: 2
      proficient: false
      expertise: false
      stat: wis
    performance:
      bonus: 0
      proficient: false
      expertise: false
      stat: cha
    persuasion:
      bonus: 2
      proficient: true
      expertise: false
      stat: cha
    religion:
      bonus: 2
      proficient: false
      expertise: false
      stat: int
    sleight-of-hand:
      bonus: 3
      proficient: false
      expertise: false
      stat: dex
    stealth:
      bonus: 5
      proficient: true
      expertise: false
      stat: dex
    survival:
      bonus: 2
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
  - name: Unarmed Strike
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/unarmed-strike/
  - name: Focus Points
    max_uses: 2
    reset: Descanso Curto
    source: class
    ref: /compendium/rules/focus-points/
  - name: Flurry of Blows
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/flurry-of-blows/
  - name: Patient Defense
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/patient-defense/
  - name: Step of the Wind
    max_uses: 0
    reset: ''
    source: class
    ref: /compendium/rules/step-of-the-wind/
  - name: Uncanny Metabolism
    max_uses: 1
    reset: Descanso Longo
    source: class
    ref: /compendium/rules/uncanny-metabolism/
  - name: Stonecunning (Tremorsense)
    max_uses: 0
    reset: Descanso Longo
    source: race
    ref: /compendium/rules/stonecunning-tremorsense/
  equipment:
  - name: Dagger
    quantity: 1
    equipped: false
    filter_type: Weapon
    attack_formula: 1d20 + 3
    damage_formula: 1d4 + 3
    ref: /compendium/items/dagger/
  - name: Dagger
    quantity: 1
    equipped: false
    filter_type: Weapon
    attack_formula: 1d20 + 3
    damage_formula: 1d4 + 3
    ref: /compendium/items/dagger/
  - name: Dagger
    quantity: 1
    equipped: false
    filter_type: Weapon
    attack_formula: 1d20 + 3
    damage_formula: 1d4 + 3
    ref: /compendium/items/dagger/
  - name: Dagger
    quantity: 1
    equipped: false
    filter_type: Weapon
    attack_formula: 1d20 + 3
    damage_formula: 1d4 + 3
    ref: /compendium/items/dagger/
  - name: Dagger
    quantity: 1
    equipped: false
    filter_type: Weapon
    attack_formula: 1d20 + 3
    damage_formula: 1d4 + 3
    ref: /compendium/items/dagger/
  - name: Spear
    quantity: 1
    equipped: true
    filter_type: Weapon
    attack_formula: 1d20 + 1
    damage_formula: 1d6 + -1
    ref: /compendium/items/spear/
  - name: Clothes, Fine
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
  - name: Signet Ring
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/signet-ring/
  - name: Backpack
    quantity: 1
    equipped: true
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/backpack/
  - name: Brewer's Supplies
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/brewers-supplies/
  - name: Flute
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/flute/
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
  - name: Bedroll
    quantity: 1
    equipped: false
    filter_type: Other Gear
    attack_formula: ''
    damage_formula: ''
    ref: /compendium/items/bedroll/
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
  spells: []
  classes_progression:
  - name: Monk
    level: 2
    subclass: ''
locations: []
factions: []
compendium_refs:
- /compendium/classes/monk/
- /compendium/items/backpack/
- /compendium/items/bedroll/
- /compendium/items/brewers-supplies/
- /compendium/items/dagger/
- /compendium/items/flute/
- /compendium/items/oil/
- /compendium/items/rations/
- /compendium/items/rope/
- /compendium/items/signet-ring/
- /compendium/items/spear/
- /compendium/items/tinderbox/
- /compendium/items/torch/
- /compendium/items/waterskin/
- /compendium/races/dwarf/
- /compendium/rules/action-attack/
- /compendium/rules/action-dash/
- /compendium/rules/action-disengage/
- /compendium/rules/action-dodge/
- /compendium/rules/action-help/
- /compendium/rules/action-hide/
- /compendium/rules/action-use-object/
- /compendium/rules/bonus-unarmed-strike/
- /compendium/rules/dedicated-weapon/
- /compendium/rules/dexterous-attacks/
- /compendium/rules/flurry-of-blows/
- /compendium/rules/focus-points/
- /compendium/rules/ki/
- /compendium/rules/martial-arts-die/
- /compendium/rules/martial-arts/
- /compendium/rules/monks-focus/
- /compendium/rules/patient-defense/
- /compendium/rules/step-of-the-wind/
- /compendium/rules/stonecunning-tremorsense/
- /compendium/rules/unarmed-strike/
- /compendium/rules/unarmored-defense/
- /compendium/rules/unarmored-movement/
- /compendium/rules/uncanny-metabolism/
spells_usage: []
---
### Biografia
Este personagem foi importado automaticamente do D&D Beyond. 

### Equipamentos e Recursos
Acesse a ficha completa original no D&D Beyond para acompanhar o inventário de itens e slots de magia em tempo real.
