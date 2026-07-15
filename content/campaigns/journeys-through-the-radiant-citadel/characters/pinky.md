---
title: "Pinky"
date: 2026-07-09T19:00:00Z
params:
  kind: "character"
draft: false
weight: 10
summary: "Variant Aasimar Rogue 10 (Thief) importado do D&D Beyond."
tags:
  - jogador
  - aasimar
  - rogue
visibility: "players"
status: "ready"

# Estatísticas Estruturadas
char_info:
  class: "Rogue 10 (Thief)"
  race: "Variant Aasimar"
  ac: "15"
  hp: "68"
  hp_max: "68"
  hp_current: "68"
  feat: "Firearm Specialist, Skill Expert, Alert, Criminal Ability Score Improvements, Skilled, Weapon Mastery"
  size: "Medium"
  alignment: "Lawful Evil"
  dndbeyond_id: "168108495"
  proficiency_bonus: 4
  spell_dc: 0
  spell_attack_bonus: 0
  avatar: "/images/campaigns/journeys-through-the-radiant-citadel/handouts/pinky.png"
  speed:
    walk: 30
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: "Passive Perception 15, Darkvision 60 ft."
  passive_senses:
    perception: 15
    investigation: 13
    insight: 19
  languages: "Celestial, Common, Common Sign Language, Thieves’ Cant"
  saves:
    str: 1
    dex: 8
    con: 4
    int: 7
    wis: 1
    cha: 4
  saves_proficient:
    str: false
    dex: true
    con: false
    int: true
    wis: false
    cha: false
  saves_summary: "Dex +8, Int +7"
  mods:
    str: 1
    dex: 4
    con: 4
    int: 3
    wis: 1
    cha: 4
  stats:
    str: 12
    dex: 18
    con: 19
    int: 16
    wis: 13
    cha: 19
  currencies:
    cp: 0
    sp: 0
    gp: 1000
    ep: 0
    pp: 1000
  skills:
    acrobatics:
      bonus: 8
      proficient: true
      expertise: false
      stat: dex
    animal-handling:
      bonus: 1
      proficient: false
      expertise: false
      stat: wis
    arcana:
      bonus: 3
      proficient: false
      expertise: false
      stat: int
    athletics:
      bonus: 5
      proficient: true
      expertise: false
      stat: str
    deception:
      bonus: 12
      proficient: true
      expertise: true
      stat: cha
    history:
      bonus: 3
      proficient: false
      expertise: false
      stat: int
    insight:
      bonus: 9
      proficient: true
      expertise: true
      stat: wis
    intimidation:
      bonus: 12
      proficient: true
      expertise: true
      stat: cha
    investigation:
      bonus: 3
      proficient: false
      expertise: false
      stat: int
    medicine:
      bonus: 1
      proficient: false
      expertise: false
      stat: wis
    nature:
      bonus: 3
      proficient: false
      expertise: false
      stat: int
    perception:
      bonus: 5
      proficient: true
      expertise: false
      stat: wis
    performance:
      bonus: 4
      proficient: false
      expertise: false
      stat: cha
    persuasion:
      bonus: 12
      proficient: true
      expertise: true
      stat: cha
    religion:
      bonus: 3
      proficient: false
      expertise: false
      stat: int
    sleight-of-hand:
      bonus: 8
      proficient: true
      expertise: false
      stat: dex
    stealth:
      bonus: 12
      proficient: true
      expertise: true
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
    - name: Sneak Attack
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/sneak-attack/
    - name: Cunning Action
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/cunning-action/
    - name: Steady Aim
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/steady-aim/
    - name: 'Sneak Attack: Poison (Cost: 1d6)'
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/sneak-attack-poison-cost-1d6/
    - name: 'Sneak Attack: Trip (Cost: 1d6)'
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/sneak-attack-trip-cost-1d6/
    - name: 'Sneak Attack: Withdraw (Cost: 1d6)'
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/sneak-attack-withdraw-cost-1d6/
    - name: Uncanny Dodge
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/uncanny-dodge/
    - name: 'Fast Hands: Sleight of Hand'
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/fast-hands-sleight-of-hand/
    - name: 'Fast Hands: Utilize'
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/fast-hands-utilize/
    - name: 'Fast Hands: Use Magic Item'
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/fast-hands-use-magic-item/
    - name: 'Sneak Attack: Supreme Sneak (Cost: 1d6)'
      max_uses: 0
      reset: ''
      source: class
      ref: /compendium/rules/sneak-attack-supreme-sneak-cost-1d6/
    - name: Healing Hands
      max_uses: 1
      reset: Descanso Longo
      source: race
      ref: /compendium/rules/healing-hands/
    - name: Firearm Specialist
      max_uses: 1
      reset: Descanso Curto
      source: feat
      ref: /compendium/rules/firearm-specialist/
    - name: Vex (Pistol)
      max_uses: 0
      reset: ''
      source: feat
      ref: /compendium/rules/vex-pistol/
    - name: Slow (Musket)
      max_uses: 0
      reset: ''
      source: feat
      ref: /compendium/rules/slow-musket/
  equipment:
    - name: Musket, +3
      quantity: 1
      equipped: true
      filter_type: Weapon
      attack_formula: 1d20 + 5
      damage_formula: 1d12 + 1
      ref: /compendium/magic-items/musket-3/
    - name: Pistol, +2
      quantity: 1
      equipped: true
      filter_type: Weapon
      attack_formula: 1d20 + 5
      damage_formula: 1d10 + 1
      ref: /compendium/magic-items/pistol-2/
    - name: Padded
      quantity: 1
      equipped: true
      filter_type: Armor
      attack_formula: ''
      damage_formula: ''
      ref: /compendium/items/padded-armor/
    - name: Blunderbuss Bullets
      quantity: 25
      equipped: true
      filter_type: Other Gear
      attack_formula: ''
      damage_formula: ''
      ref: /compendium/items/blunderbuss-bullets/
  spells:
    - name: Light
      level: 0
      prepared: true
      usage: Truque
      ref: /compendium/spells/light/
    - name: Lesser Restoration
      level: 2
      prepared: true
      usage: 1x/Descanso Longo
      ref: /compendium/spells/lesser-restoration/
    - name: Daylight
      level: 3
      prepared: true
      usage: 1x/Descanso Longo
      ref: /compendium/spells/daylight/
  classes_progression:
    - name: Rogue
      level: 10
      subclass: Thief

# Relacionamentos
locations: []
factions: []
compendium_refs:
- /compendium/classes/rogue/
- /compendium/classes/thief/
- /compendium/feats/alert/
- /compendium/feats/skill-expert/
- /compendium/feats/skilled/
- /compendium/feats/weapon-master/
- /compendium/items/blunderbuss-bullets/
- /compendium/items/padded-armor/
- /compendium/magic-items/musket-3/
- /compendium/magic-items/pistol-2/
- /compendium/races/aasimar/
- /compendium/rules/action-attack/
- /compendium/rules/action-dash/
- /compendium/rules/action-disengage/
- /compendium/rules/action-dodge/
- /compendium/rules/action-help/
- /compendium/rules/action-hide/
- /compendium/rules/action-use-object/
- /compendium/rules/cunning-action/
- /compendium/rules/cunning-strike/
- /compendium/rules/evasion/
- /compendium/rules/expertise/
- /compendium/rules/fast-hands-sleight-of-hand/
- /compendium/rules/fast-hands-use-magic-item/
- /compendium/rules/fast-hands-utilize/
- /compendium/rules/fast-hands/
- /compendium/rules/firearm-specialist/
- /compendium/rules/healing-hands/
- /compendium/rules/poison-cost-1d6/
- /compendium/rules/reliable-talent/
- /compendium/rules/second-story-work/
- /compendium/rules/slow-musket/
- /compendium/rules/sneak-attack-poison-cost-1d6/
- /compendium/rules/sneak-attack-supreme-sneak-cost-1d6/
- /compendium/rules/sneak-attack-trip-cost-1d6/
- /compendium/rules/sneak-attack-withdraw-cost-1d6/
- /compendium/rules/sneak-attack/
- /compendium/rules/steady-aim/
- /compendium/rules/supreme-sneak/
- /compendium/rules/thief/
- /compendium/rules/thieves-cant/
- /compendium/rules/trip-cost-1d6/
- /compendium/rules/uncanny-dodge/
- /compendium/rules/vex-pistol/
- /compendium/rules/weapon-mastery/
- /compendium/rules/withdraw-cost-1d6/
- /compendium/spells/daylight/
- /compendium/spells/lesser-restoration/
- /compendium/spells/light/
spells_usage:
- name: Daylight
  usage: 1x/Descanso Longo
- name: Lesser Restoration
  usage: 1x/Descanso Longo
- name: Light
  usage: Truque
---

### Biografia
Este personagem foi importado automaticamente do D&D Beyond. 

### Equipamentos e Recursos
Acesse a ficha completa original no D&D Beyond para acompanhar o inventário de itens e slots de magia em tempo real.
