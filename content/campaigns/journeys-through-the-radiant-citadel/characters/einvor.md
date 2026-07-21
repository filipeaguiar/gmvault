---
title: "Einvor"
date: 2026-07-21T10:59:18Z
type: "character"
draft: false
weight: 10
tags:
  - jogador
  - goliath
  - barbarian
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "Barbarian"
  class_level: 1
  subclass: "Path of the Berserker"
  level: 1
  species: "Goliath"
  species_variant: ""
  ac: "11"
  hp: "14"
  hp_max: "14"
  hp_current: "14"
  feat: ""
  feats:
  - Tough
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
    walk: 35
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: "Passive Perception 10"
  passive_senses:
    perception: 10
    investigation: 9
    insight: 10
  languages: "Common"
  saves:
    str: 4
    dex: 1
    con: 4
    int: -1
    wis: 0
    cha: 0
  saves_proficient:
    str: true
    dex: false
    con: true
    int: false
    wis: false
    cha: false
  saves_summary: "Str +4, Con +4"
  mods:
    str: 2
    dex: 1
    con: 2
    int: -1
    wis: 0
    cha: 0
  stats:
    str: 14
    dex: 12
    con: 14
    int: 8
    wis: 10
    cha: 10
  currencies:
    cp: 0
    sp: 0
    gp: 0
    ep: 0
    pp: 0
  skills:
    acrobatics:
      bonus: 1
      proficient: false
      expertise: false
      stat: dex
    animal-handling:
      bonus: 0
      proficient: false
      expertise: false
      stat: wis
    arcana:
      bonus: -1
      proficient: false
      expertise: false
      stat: int
    athletics:
      bonus: 4
      proficient: true
      expertise: false
      stat: str
    deception:
      bonus: 0
      proficient: false
      expertise: false
      stat: cha
    history:
      bonus: -1
      proficient: false
      expertise: false
      stat: int
    insight:
      bonus: 0
      proficient: false
      expertise: false
      stat: wis
    intimidation:
      bonus: 2
      proficient: true
      expertise: false
      stat: cha
    investigation:
      bonus: -1
      proficient: false
      expertise: false
      stat: int
    medicine:
      bonus: 0
      proficient: false
      expertise: false
      stat: wis
    nature:
      bonus: 1
      proficient: true
      expertise: false
      stat: int
    perception:
      bonus: 0
      proficient: false
      expertise: false
      stat: wis
    performance:
      bonus: 0
      proficient: false
      expertise: false
      stat: cha
    persuasion:
      bonus: 0
      proficient: false
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
      bonus: 1
      proficient: false
      expertise: false
      stat: dex
    survival:
      bonus: 2
      proficient: true
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
    - name: Rage
      ref: /compendium/rules/rage/
      max_uses: 0
      reset: ''
      source: class
    - name: Unarmored Defense
      ref: /compendium/rules/unarmored-defense/
      max_uses: 0
      reset: ''
      source: class
    - name: Weapon Mastery
      ref: /compendium/rules/weapon-mastery/
      max_uses: 0
      reset: ''
      source: class
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
    - name: Greataxe
      ref: /compendium/items/greataxe/
      quantity: 1
      equipped: false
    - name: Handaxe
      ref: /compendium/items/handaxe/
      quantity: 2
      equipped: false
    - name: Handaxe
      ref: /compendium/items/handaxe/
      quantity: 1
      equipped: false
  spells: []
  spell_slots: {}
  class_spells: []
  classes_progression:
    - name: Barbarian
      level: 1
      subclass: Path of the Berserker

# Relacionamentos
locations: []
factions: []
compendium_refs:
- /compendium/classes/barbarian/
- /compendium/feats/tough/
- /compendium/items/backpack/
- /compendium/items/bedroll/
- /compendium/items/greataxe/
- /compendium/items/handaxe/
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
- /compendium/rules/rage/
- /compendium/rules/unarmored-defense/
- /compendium/rules/weapon-mastery/
- /compendium/species/goliath/
spells_usage: []
---

### Biografia
Este personagem foi criado manualmente via script interativo guiado por dados do 5e.tools.

### Equipamentos e Recursos
Ficha básica de V1. Use os comandos estendidos nas próximas fases para adicionar recursos adicionais.
