---
title: Giant Lizard
type: monster
draft: false
weight: 10
summary: "```yaml\nname: Povo Miúdo Astuto\nsize: Pequeno\ntype: humanoide\nsubtype: anão\nalignment: qualquer\nac: []\nhp:\n  formula: 7\n  average: 7\nspeed:\n  walk: 25\nstats: [8, 14, 10, 14, 14, 12]\nsaves:\n  - dex: +4\n  - wis: +4\nskillsaves:\n  - perception: +4\n  - stealth: +6\n  - investigation: +4\n  - insight: +4\ndamage_vulnerabilities: []\ndamage_resistances: []\ndamage_immunities: []\ncondition_immunities: []\nsenses:\n  darkvision: 60\n  passivePerception: 14\nlanguages: Comum, Anão\ncr: 2\nspellcasting:\n  spellcastingType: arcane\n  level: 4\n  ability: int\n  spells:\n    - \"Truque: [[spell|Prestidigitação]], [[spell|Luz]]\"\n    - \"1º (3 espaços): [[spell|Mísseis Mágicos]], [[spell|Enfeitiçar Pessoa]], [[spell|Sono]]\"\n    - \"2º (2 espaços): [[spell|Acalmar Emoções]], [[spell|Invisibilidade]], [[spell|Detectar Pensamentos]]\"\ntraits:\n  - name: Astúcia\n    desc: \"Ação Bônus: O povo miúdo pode usar Desengajar ou Esconder.\"\nactions:\n  - name: Adaga\n    desc:\
  \ \"Ataque Corpo a Corpo ou à Distância: +4 para atingir, alcance 1,5 m ou distância 6/18 m, um alvo. Dano: 4 (1d4 + 2) de dano perfurante.\"\nattachedSpells:\n  - detectar pensamentos\n  - acalmar emoções\n  - invisibilidade\n  - enfeitiçar pessoa\n  - mísseis mágicos\n  - sono\nenvironment: []\nsoundClip: null\nimag"
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
  entity_name: Giant Lizard
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: a91e6bc9e0aca594
stats:
  ac: '12'
  hp: 19 (3d10 + 3)
  speed: walk 30 ft., climb 30 ft.
  attributes:
    str: 15
    dex: 12
    con: 13
    int: 2
    wis: 10
    cha: 5
  saves: {}
  skills: {}
  senses: darkvision 30 ft.
  languages: ''
  cr: 1/4
stats_meta: Large beast U
titulo_pt_br: Lagarto Gigante
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Ações

### Mordida

Ataque Corpo a Corpo com Arma: +4 para atingir, alcance 1,5 m, um alvo. {@h}6 (<span class="dice+" data-roll-notation="1d8+2">1d8 + 2</span>) dano perfurante.
