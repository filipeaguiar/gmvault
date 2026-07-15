---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
params:
  kind: "character"
draft: false
weight: 10
summary: "Ficha/Perfil de personagem do jogador."
tags: []
visibility: "players"
status: "ready"

# Dados específicos e estado operacional. Regras compartilhadas usam refs do compêndio.
char_info:
  class: "Guerreiro 1"
  race: "Humano"
  ac: "10"
  hp: "10"
  hp_max: "10"
  hp_current: "10"
  feat: ""
  size: ""
  alignment: ""
  proficiency_bonus: 2
  spell_dc: 0
  spell_attack_bonus: 0
  speed:
    walk: 30
    fly: 0
    swim: 0
    climb: 0
    burrow: 0
  senses: ""
  passive_senses: {}
  languages: ""
  saves: {}
  saves_proficient: {}
  saves_summary: ""
  mods:
    str: 0
    dex: 0
    con: 0
    int: 0
    wis: 0
    cha: 0
  stats:
    str: 10
    dex: 10
    con: 10
    int: 10
    wis: 10
    cha: 10
  currencies:
    cp: 0
    sp: 0
    gp: 0
    ep: 0
    pp: 0
  skills: {}
  # Exemplo: {name: "Ataque Furtivo", ref: "/compendium/rules/sneak-attack/", source: class, max_uses: 0, reset: ""}
  actions: []
  # Exemplo: {name: "Arco curto", ref: "/compendium/items/shortbow/", quantity: 1, equipped: true, filter_type: Weapon}
  equipment: []
  # Exemplo: {name: "Luz", level: 0, prepared: true, ref: "/compendium/spells/light/", usage: "Truque"}
  spells: []
  classes_progression: []

factions: []
locations: []
compendium_refs: []
spells_usage: []
---

### Biografia
Insira a biografia e descrição narrativa do personagem do jogador aqui.

### Equipamentos e Recursos
Registre no frontmatter somente o estado operacional. Descrições de regras e itens devem ser mantidas no compêndio e referenciadas por URL interna.
