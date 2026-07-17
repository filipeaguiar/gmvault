---
title: Air Elemental
params:
  kind: monster
draft: true
weight: 10
summary: Conteúdo importado do 5e.tools (MM) e traduzido automaticamente; requer revisão editorial.
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
  entity_name: Air Elemental
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 295d95f1ffa589c3
stats:
  ac: '15'
  hp: 90 (12d10 + 24)
  speed: fly 90 ft.
  attributes:
    str: 14
    dex: 20
    con: 14
    int: 6
    wis: 10
    cha: 6
  saves: {}
  skills: {}
  senses: darkvision 60 ft.
  languages: Auran
  cr: '5'
stats_meta: Large elemental N
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Elemental do Ar
---

## Características

### Forma Aérea

O elemental pode entrar no espaço de uma criatura hostil e parar ali. Ele pode se mover por um espaço tão estreito quanto 1 polegada de largura sem se espremer.

## Ações

### Ataques Múltiplos

O elemental realiza dois ataques de pancada.

### Pancada

mw 8 to hit, alcance 5 ft., um alvo. {@h}14 (<span class="dice+" data-roll-notation="2d8+5">2d8 + 5</span>) dano de concussão.

### Redemoinho 4

Cada criatura no espaço do elemental deve realizar um teste de resistência de Força CD 13. Em caso de falha, o alvo sofre 15 (<span class="dice+" data-roll-notation="3d8+2">3d8 + 2</span>) de dano de concussão e é arremessado a até 20 pés de distância do elemental em uma direção aleatória e fica caído. Se um alvo arremessado atingir um objeto, como uma parede ou chão, o alvo sofre 3 (<span class="dice+" data-roll-notation="1d6">1d6</span>) de dano de concussão para cada 10 pés que foi arremessado. Se o alvo for arremessado contra outra criatura, essa criatura deve ser bem-sucedida em um teste de resistência de Destreza CD 13 ou sofrer o mesmo dano e ficar caída.

Se o teste de resistência for bem-sucedido, o alvo sofre metade do dano de concussão e não é arremessado nem fica caído.
