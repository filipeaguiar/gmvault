---
title: Wyvern
params:
  kind: monster
draft: true
weight: 10
summary: Entendido. Por favor, forneça o rascunho importado do 5e.tools (MM) para que eu possa realizar a tradução e a revisão editorial conforme as instruções. Aguardo o texto.
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
  entity_name: Wyvern
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 894a8702c3fa1ab9
stats:
  ac: '13'
  hp: 110 (13d10 + 39)
  speed: walk 20 ft., fly 80 ft.
  attributes:
    str: 19
    dex: 10
    con: 16
    int: 5
    wis: 12
    cha: 6
  saves: {}
  skills:
    perception: '+4'
  senses: darkvision 60 ft.
  languages: ''
  cr: '6'
stats_meta: Large dragon U
titulo_pt_br: Wyvern
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Ações

### Ataques Múltiplos

O wyvern realiza dois ataques: um com sua mordida e outro com seu ferrão. Enquanto estiver voando, ele pode usar suas garras no lugar de um outro ataque.

### Mordida

mw 7 para atingir, alcance 3 m, uma criatura. {@h}11 (<span class="dice+" data-roll-notation="2d6+4">2d6 + 4</span>) de dano perfurante.

### Garras

mw 7 para atingir, alcance 1,5 m, um alvo. {@h}13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano cortante.

### Ferrão

mw 7 para atingir, alcance 3 m, uma criatura. {@h}11 (<span class="dice+" data-roll-notation="2d6+4">2d6 + 4</span>) de dano perfurante. O alvo deve realizar um teste de resistência de Constituição CD 15, sofrendo 24 (<span class="dice+" data-roll-notation="7d6">7d6</span>) de dano de veneno em caso de falha no teste de resistência, ou metade desse dano em caso de sucesso.
