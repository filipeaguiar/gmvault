---
title: "Durin"
date: 2026-07-21T11:07:43Z
type: "character"
draft: false
weight: 10
tags:
  - jogador
  - dwarf
  - monk
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "Monk"
  class_level: 1
  subclass: "Way of the Drunken Master"
  level: 1
  species: "Dwarf"
  species_variant: ""
  ac: "13"
  hp: "10"
  hp_max: "10"
  hp_current: "10"
  feat: ""
  feats:
  - Crafter
  size: "Medium"
  alignment: "True Neutral"
  dndbeyond_id: ""
  proficiency_bonus: 2
  spell_dc: 0
  avatar: ""
  spellcasting:
    mode: none
    ability: ''
    prepared_spell_refs: []
    known_spell_refs: []
    always_prepared_spell_refs: []
    class_spell_refs: []
    bonus_spell_refs: []
    slot_progression: {}
    pact_slots: {}
    ritual_casting: false
    sources: []
  speed:
    walk: 30
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: "Passive Perception 12, Darkvision 120 ft."
  passive_senses:
    perception: 12
    investigation: 11
    insight: 12
  languages: "Common"
  saves:
    str: 1
    dex: 5
    con: 2
    int: 1
    wis: 2
    cha: 0
  saves_proficient:
    str: true
    dex: true
    con: false
    int: false
    wis: false
    cha: false
  saves_summary: "Str +1, Dex +5"
  mods:
    str: -1
    dex: 3
    con: 2
    int: 1
    wis: 2
    cha: 0
  stats:
    str: 8
    dex: 16
    con: 14
    int: 13
    wis: 15
    cha: 10
  currencies:
    cp: 0
    sp: 0
    gp: 0
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
      bonus: 1
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
      bonus: 3
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
      bonus: 1
      proficient: false
      expertise: false
      stat: int
    medicine:
      bonus: 2
      proficient: false
      expertise: false
      stat: wis
    nature:
      bonus: 1
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
      bonus: 1
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
    - name: Martial Arts
      ref: /compendium/rules/martial-arts/
      max_uses: 0
      reset: ''
      source: class
    - name: Unarmored Defense
      ref: /compendium/rules/unarmored-defense/
      max_uses: 0
      reset: ''
      source: class
    - name: Bonus Unarmed Strike
      ref: /compendium/rules/bonus-unarmed-strike/
      max_uses: 0
      reset: ''
      source: class
    - name: Dexterous Attacks
      ref: /compendium/rules/dexterous-attacks/
      max_uses: 0
      reset: ''
      source: class
    - name: Martial Arts Die
      ref: /compendium/rules/martial-arts-die/
      max_uses: 0
      reset: ''
      source: class
      roll: 1d6
  equipment:
    - name: Backpack
      ref: /compendium/items/backpack/
      quantity: 1
      equipped: false
    - name: Bedroll
      ref: /compendium/items/bedroll/
      quantity: 1
      equipped: false
    - name: Mess Kit
      ref: /compendium/items/mess-kit/
      quantity: 1
      equipped: false
    - name: Tinderbox
      ref: /compendium/items/tinderbox/
      quantity: 1
      equipped: false
    - name: Torch
      ref: /compendium/items/torch/
      quantity: 1
      equipped: false
    - name: Rations (1 Day)
      ref: /compendium/items/rations-1-day/
      quantity: 1
      equipped: false
    - name: Waterskin
      ref: /compendium/items/waterskin/
      quantity: 1
      equipped: false
    - name: Hempen Rope (50 Feet)
      ref: /compendium/items/hempen-rope-50-feet/
      quantity: 1
      equipped: false
    - name: Explorer's Pack
      ref: /compendium/items/explorers-pack/
      quantity: 1
      equipped: false
    - name: Dagger
      ref: /compendium/items/dagger/
      quantity: 5
      equipped: false
  spells: []
  spell_slots: {}
  class_spells: []
  classes_progression:
    - name: Monk
      level: 1
      subclass: Way of the Drunken Master

# Relacionamentos
locations: []
factions: []
compendium_refs:
- /compendium/classes/monk/
- /compendium/feats/crafter/
- /compendium/items/backpack/
- /compendium/items/bedroll/
- /compendium/items/dagger/
- /compendium/items/explorers-pack/
- /compendium/items/hempen-rope-50-feet/
- /compendium/items/mess-kit/
- /compendium/items/rations-1-day/
- /compendium/items/tinderbox/
- /compendium/items/torch/
- /compendium/items/waterskin/
- /compendium/rules/action-attack/
- /compendium/rules/action-dash/
- /compendium/rules/action-disengage/
- /compendium/rules/action-dodge/
- /compendium/rules/action-help/
- /compendium/rules/action-hide/
- /compendium/rules/action-use-object/
- /compendium/rules/bonus-unarmed-strike/
- /compendium/rules/dexterous-attacks/
- /compendium/rules/martial-arts-die/
- /compendium/rules/martial-arts/
- /compendium/rules/unarmored-defense/
- /compendium/species/dwarf/
spells_usage: []
---

### Biografia
Este personagem foi criado manualmente via script interativo guiado por dados do 5e.tools.

### Equipamentos e Recursos
Ficha básica de V1. Use os comandos estendidos nas próximas fases para adicionar recursos adicionais.
