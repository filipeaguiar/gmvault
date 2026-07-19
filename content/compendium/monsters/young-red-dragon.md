---
title: Young Red Dragon
params:
  kind: monster
draft: false
weight: 10
summary: Entendido. Por favor, forneça o texto a ser traduzido. Estou pronto para aplicar as regras de tradução e terminologia especificadas.
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
  entity_name: Young Red Dragon
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: d99bf94e3dc953a3
stats:
  ac: '18'
  hp: 178 (17d10 + 85)
  speed: walk 40 ft., climb 40 ft., fly 80 ft.
  attributes:
    str: 23
    dex: 10
    con: 21
    int: 14
    wis: 11
    cha: 19
  saves:
    dex: '+4'
    con: '+9'
    wis: '+4'
    cha: '+8'
  skills:
    perception: '+8'
    stealth: '+4'
  senses: blindsight 30 ft., darkvision 120 ft.
  languages: Common, Draconic
  cr: '10'
stats_meta: Large dragon C/E
titulo_pt_br: Dragão Vermelho Jovem
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Ações

### Ataques Múltiplos

O dragão realiza três ataques: um com sua mordida e dois com suas garras.

### Mordida

mw 10 para atingir, alcance 10 pés, um alvo. {@h}17 (<span class="dice+" data-roll-notation="2d10+6">2d10 + 6</span>) de dano perfurante mais 3 (<span class="dice+" data-roll-notation="1d6">1d6</span>) de dano de fogo.

### Garra

mw 10 para atingir, alcance 5 pés, um alvo. {@h}13 (<span class="dice+" data-roll-notation="2d6+6">2d6 + 6</span>) de dano cortante.

### Sopro de Fogo 5

O dragão exala fogo em um cone de 30 pés. Cada criatura nessa área deve realizar um teste de resistência de Destreza CD 17, sofrendo 56 (<span class="dice+" data-roll-notation="16d6">16d6</span>) de dano de fogo em caso de falha no teste de resistência, ou metade desse dano em caso de sucesso.
