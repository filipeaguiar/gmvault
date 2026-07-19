---
title: "Detios Canto Baixo"
date: 2026-07-19T21:47:43Z
type: "character"
draft: false
weight: 10
tags:
  - jogador
  - halfling
  - bard
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "Bard"
  class_level: 1
  subclass: ""
  level: 1
  species: "Halfling"
  species_variant: "Ghostwise"
  ac: "13"
  hp: "9"
  hp_max: "9"
  hp_current: "9"
  feat: ""
  feats:
  - Lucky
  size: "Small"
  alignment: "True Neutral"
  dndbeyond_id: ""
  proficiency_bonus: 2
  spell_dc: 0
  spell_attack_bonus: 0
  avatar: ""
  spellcasting:
    mode: known
    ability: ''
    prepared_spell_refs: []
    known_spell_refs: []
    always_prepared_spell_refs: []
    class_spell_refs: []
    bonus_spell_refs:
    - /compendium/spells/minor-illusion/
    - /compendium/spells/vicious-mockery/
    - /compendium/spells/charm-person/
    - /compendium/spells/detect-magic/
    - /compendium/spells/dissonant-whispers/
    - /compendium/spells/healing-word/
    slot_progression:
      1: 2
    pact_slots: {}
    ritual_casting: false
    sources: []
  speed:
    walk: 30
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: "Passive Perception 9"
  passive_senses:
    perception: 9
    investigation: 10
    insight: 9
  languages: "Common"
  saves:
    str: -1
    dex: 5
    con: 1
    int: 0
    wis: -1
    cha: 6
  saves_proficient:
    str: false
    dex: true
    con: false
    int: false
    wis: false
    cha: true
  saves_summary: "Dex +5, Cha +6"
  mods:
    str: -1
    dex: 3
    con: 1
    int: 0
    wis: -1
    cha: 4
  stats:
    str: 8
    dex: 16
    con: 12
    int: 10
    wis: 9
    cha: 18
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
      bonus: 1
      proficient: true
      expertise: false
      stat: wis
    arcana:
      bonus: 0
      proficient: false
      expertise: false
      stat: int
    athletics:
      bonus: -1
      proficient: false
      expertise: false
      stat: str
    deception:
      bonus: 4
      proficient: false
      expertise: false
      stat: cha
    history:
      bonus: 0
      proficient: false
      expertise: false
      stat: int
    insight:
      bonus: -1
      proficient: false
      expertise: false
      stat: wis
    intimidation:
      bonus: 4
      proficient: false
      expertise: false
      stat: cha
    investigation:
      bonus: 0
      proficient: false
      expertise: false
      stat: int
    medicine:
      bonus: -1
      proficient: false
      expertise: false
      stat: wis
    nature:
      bonus: 0
      proficient: false
      expertise: false
      stat: int
    perception:
      bonus: -1
      proficient: false
      expertise: false
      stat: wis
    performance:
      bonus: 6
      proficient: true
      expertise: false
      stat: cha
    persuasion:
      bonus: 6
      proficient: true
      expertise: false
      stat: cha
    religion:
      bonus: 0
      proficient: false
      expertise: false
      stat: int
    sleight-of-hand:
      bonus: 5
      proficient: true
      expertise: false
      stat: dex
    stealth:
      bonus: 3
      proficient: false
      expertise: false
      stat: dex
    survival:
      bonus: 1
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
    - name: Bardic Inspiration
      ref: /compendium/rules/bardic-inspiration/
      max_uses: 0
      reset: ''
      source: class
      roll: 1d6
    - name: Spellcasting
      ref: /compendium/rules/spellcasting/
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
    - name: Costume Clothes
      ref: /compendium/items/costume-clothes/
      quantity: 1
      equipped: false
    - name: Candle
      ref: /compendium/items/candle/
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
    - name: Disguise Kit
      ref: /compendium/items/disguise-kit/
      quantity: 1
      equipped: false
    - name: Leather Armor
      ref: /compendium/items/leather-armor/
      quantity: 1
      equipped: false
    - name: Dagger
      ref: /compendium/items/dagger/
      quantity: 2
      equipped: false
    - name: Entertainer's Pack
      ref: /compendium/items/entertainers-pack/
      quantity: 1
      equipped: false
  spells:
    - ref: /compendium/spells/minor-illusion/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/vicious-mockery/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/charm-person/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/detect-magic/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/dissonant-whispers/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/healing-word/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
  spell_slots:
    1: 2
  class_spells: []
  classes_progression:
    - name: Bard
      level: 1
      subclass: ''

# Relacionamentos
locations: []
factions: []
compendium_refs:
- /compendium/classes/bard/
- /compendium/feats/lucky/
- /compendium/items/backpack/
- /compendium/items/bedroll/
- /compendium/items/candle/
- /compendium/items/costume-clothes/
- /compendium/items/dagger/
- /compendium/items/disguise-kit/
- /compendium/items/entertainers-pack/
- /compendium/items/leather-armor/
- /compendium/items/rations-1-day/
- /compendium/items/waterskin/
- /compendium/rules/action-attack/
- /compendium/rules/action-dash/
- /compendium/rules/action-disengage/
- /compendium/rules/action-dodge/
- /compendium/rules/action-help/
- /compendium/rules/action-hide/
- /compendium/rules/action-use-object/
- /compendium/rules/bardic-inspiration/
- /compendium/rules/spellcasting/
- /compendium/species/halfling/
- /compendium/spells/charm-person/
- /compendium/spells/detect-magic/
- /compendium/spells/dissonant-whispers/
- /compendium/spells/healing-word/
- /compendium/spells/minor-illusion/
- /compendium/spells/vicious-mockery/
spells_usage: []
---

### Biografia
Este personagem foi criado manualmente via script interativo guiado por dados do 5e.tools.

### Equipamentos e Recursos
Ficha básica de V1. Use os comandos estendidos nas próximas fases para adicionar recursos adicionais.
