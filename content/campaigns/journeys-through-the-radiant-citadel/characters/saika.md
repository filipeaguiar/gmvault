---
title: "Saika"
date: 2026-09-11T20:26:59Z
type: "character"
draft: false
weight: 10
tags:
  - jogador
  - tiefling
  - sorcerer
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "Sorcerer"
  class_level: 4
  subclass: "Wild Magic Sorcery"
  level: 4
  species: "Tiefling"
  species_variant: "Asmodeus"
  ac: "12"
  hp: "26"
  hp_max: "26"
  hp_current: "26"
  feat: ""
  feats:
  - name: "Atiradora de Magias"
    ref: /compendium/feats/spell-sniper/
  size: "Medium"
  alignment: "Chaotic Good"
  dndbeyond_id: ""
  proficiency_bonus: 2
  spell_dc: 13
  avatar: "/images/campaigns/journeys-through-the-radiant-citadel/characters/portrait-saika.png"
  full_art: "/images/campaigns/journeys-through-the-radiant-citadel/characters/saika.png"
  spellcasting:
    mode: prepared
    kind: prepared
    ability: cha
    can_prepare: true
    prepared_spell_refs:
    - /compendium/spells/shield/
    - /compendium/spells/mage-armor/
    - /compendium/spells/burning-hands/
    - /compendium/spells/magic-missile/
    - /compendium/spells/misty-step/
    - /compendium/spells/scorching-ray/
    - /compendium/spells/suggestion/
    known_spell_refs:
    - /compendium/spells/fire-bolt/
    - /compendium/spells/mage-hand/
    - /compendium/spells/minor-illusion/
    - /compendium/spells/prestidigitation/
    - /compendium/spells/ray-of-frost/
    always_prepared_spell_refs:
    - /compendium/spells/thaumaturgy/
    - /compendium/spells/hellish-rebuke/
    class_spell_refs: []
    bonus_spell_refs:
    - /compendium/spells/thaumaturgy/
    - /compendium/spells/hellish-rebuke/
    slot_progression:
      1: 4
      2: 3
    pact_slots: {}
    ritual_casting: false
    sources: []
  speed:
    walk: 30
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: "Passive Perception 10, Darkvision 60 ft."
  passive_senses:
    perception: 10
    investigation: 11
    insight: 10
  languages: "Common"
  saves:
    str: -1
    dex: 2
    con: 4
    int: 1
    wis: 0
    cha: 5
  saves_proficient:
    str: false
    dex: false
    con: true
    int: false
    wis: false
    cha: true
  saves_summary: "Con +4, Cha +5"
  mods:
    str: -1
    dex: 2
    con: 2
    int: 1
    wis: 0
    cha: 3
  stats:
    str: 8
    dex: 14
    con: 14
    int: 12
    wis: 10
    cha: 17
  currencies:
    cp: 0
    sp: 0
    gp: 0
    ep: 0
    pp: 0
  skills:
    acrobatics:
      bonus: 2
      proficient: false
      expertise: false
      stat: dex
    animal-handling:
      bonus: 0
      proficient: false
      expertise: false
      stat: wis
    arcana:
      bonus: 3
      proficient: true
      expertise: false
      stat: int
    athletics:
      bonus: -1
      proficient: false
      expertise: false
      stat: str
    deception:
      bonus: 5
      proficient: true
      expertise: false
      stat: cha
    history:
      bonus: 3
      proficient: true
      expertise: false
      stat: int
    insight:
      bonus: 0
      proficient: false
      expertise: false
      stat: wis
    intimidation:
      bonus: 3
      proficient: false
      expertise: false
      stat: cha
    investigation:
      bonus: 1
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
      proficient: false
      expertise: false
      stat: int
    perception:
      bonus: 0
      proficient: false
      expertise: false
      stat: wis
    performance:
      bonus: 3
      proficient: false
      expertise: false
      stat: cha
    persuasion:
      bonus: 5
      proficient: true
      expertise: false
      stat: cha
    religion:
      bonus: 1
      proficient: false
      expertise: false
      stat: int
    sleight-of-hand:
      bonus: 2
      proficient: false
      expertise: false
      stat: dex
    stealth:
      bonus: 2
      proficient: false
      expertise: false
      stat: dex
    survival:
      bonus: 0
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
    - name: Spellcasting
      ref: /compendium/rules/sorcerer-spellcasting/
      max_uses: 0
      reset: ''
      source: class
    - name: Font of Magic
      ref: /compendium/rules/sorcerer-font-of-magic/
      max_uses: 0
      reset: ''
      source: class
    - name: Pontos de Feitiçaria
      ref: /compendium/rules/sorcerer-sorcery-points/
      max_uses: 4
      reset: long_rest
      source: class
    - name: 'Metamagic: Subtle Spell'
      ref: /compendium/rules/metamagic-subtle-spell/
      max_uses: 0
      reset: ''
      source: class
    - name: 'Metamagic: Empowered Spell'
      ref: /compendium/rules/metamagic-empowered-spell/
      max_uses: 0
      reset: ''
      source: class
    - name: Innate Sorcery
      ref: /compendium/rules/innate-sorcery/
      max_uses: 2
      reset: long_rest
      source: class
    - name: Sorcerer Subclass
      ref: /compendium/rules/sorcerer-subclass/
      max_uses: 0
      reset: ''
      source: class
    - name: Wild Magic Sorcery
      ref: /compendium/rules/wild-magic-sorcery/
      max_uses: 0
      reset: ''
      source: class
    - name: Tides of Chaos
      ref: /compendium/rules/tides-of-chaos/
      max_uses: 1
      reset: spell_slot_or_long_rest
      source: class
    - name: Wild Magic Surge
      ref: /compendium/rules/wild-magic-surge-2024/
      max_uses: 0
      reset: ''
      source: class
    - name: Hellish Rebuke
      ref: /compendium/spells/hellish-rebuke/
      max_uses: 1
      reset: long_rest
      source: species
  equipment:
    - name: Backpack
      ref: /compendium/items/backpack/
      quantity: 1
      equipped: false
    - name: Book
      ref: /compendium/items/book/
      quantity: 1
      equipped: false
    - name: Ink (1-Ounce Bottle)
      ref: /compendium/items/ink-1-ounce-bottle/
      quantity: 1
      equipped: false
    - name: Ink Pen
      ref: /compendium/items/ink-pen/
      quantity: 1
      equipped: false
    - name: Parchment (One Sheet)
      ref: /compendium/items/parchment-one-sheet/
      quantity: 1
      equipped: false
    - name: Dagger
      ref: /compendium/items/dagger/
      quantity: 1
      equipped: true
    - name: Crystal
      ref: /compendium/items/crystal/
      quantity: 1
      equipped: false
  spells:
    - ref: /compendium/spells/fire-bolt/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/mage-hand/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/minor-illusion/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/prestidigitation/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/ray-of-frost/
      availability: known
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/shield/
      availability: prepared
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/mage-armor/
      availability: prepared
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/burning-hands/
      availability: prepared
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/magic-missile/
      availability: prepared
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/misty-step/
      availability: prepared
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/scorching-ray/
      availability: prepared
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/suggestion/
      availability: prepared
      source: class
      usage: 1 action
      can_prepare: false
    - ref: /compendium/spells/thaumaturgy/
      availability: granted
      source: species
      usage: at will
      can_prepare: false
    - ref: /compendium/spells/hellish-rebuke/
      availability: granted
      source: species
      usage: 1/long rest
      can_prepare: false
  spell_slots:
    1: 4
    2: 3
  class_spells: []
  classes_progression:
    - name: Sorcerer
      level: 4
      subclass: Wild Magic Sorcery

# Relacionamentos
locations: []
factions: []
compendium_refs:
- /compendium/classes/sorcerer/
- /compendium/feats/spell-sniper/
- /compendium/items/backpack/
- /compendium/items/book/
- /compendium/items/crystal/
- /compendium/items/dagger/
- /compendium/items/ink-1-ounce-bottle/
- /compendium/items/ink-pen/
- /compendium/items/parchment-one-sheet/
- /compendium/rules/action-attack/
- /compendium/rules/action-dash/
- /compendium/rules/action-disengage/
- /compendium/rules/action-dodge/
- /compendium/rules/action-help/
- /compendium/rules/action-hide/
- /compendium/rules/action-use-object/
- /compendium/rules/innate-sorcery/
- /compendium/rules/metamagic-empowered-spell/
- /compendium/rules/metamagic-subtle-spell/
- /compendium/rules/sorcerer-subclass/
- /compendium/rules/sorcerer-font-of-magic/
- /compendium/rules/sorcerer-sorcery-points/
- /compendium/rules/sorcerer-spellcasting/
- /compendium/rules/tides-of-chaos/
- /compendium/rules/wild-magic-sorcery/
- /compendium/rules/wild-magic-surge-2024/
- /compendium/species/tiefling/
- /compendium/spells/burning-hands/
- /compendium/spells/fire-bolt/
- /compendium/spells/hellish-rebuke/
- /compendium/spells/mage-armor/
- /compendium/spells/mage-hand/
- /compendium/spells/magic-missile/
- /compendium/spells/minor-illusion/
- /compendium/spells/misty-step/
- /compendium/spells/prestidigitation/
- /compendium/spells/ray-of-frost/
- /compendium/spells/scorching-ray/
- /compendium/spells/shield/
- /compendium/spells/suggestion/
- /compendium/spells/thaumaturgy/
spells_usage: []
---

### Biografia
Este personagem foi criado manualmente via script interativo guiado por dados do 5e.tools.

### Equipamentos e Recursos
Ficha básica de V1. Use os comandos estendidos nas próximas fases para adicionar recursos adicionais.
