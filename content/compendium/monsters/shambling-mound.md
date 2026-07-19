---
title: Shambling Mound
type: monster
draft: false
weight: 10
tags:
- draft
- importado
- 5etools
visibility: gm
status: ready
source:
  provider: 5e.tools
  book: MM
  entity_type: monster
  entity_name: Shambling Mound
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 018594a06de9ee95
stats:
  ac: '15'
  hp: 136 (16d10 + 48)
  speed: walk 20 ft., swim 20 ft.
  attributes:
    str: 18
    dex: 8
    con: 16
    int: 5
    wis: 10
    cha: 5
  saves: {}
  skills:
    stealth: '+2'
  senses: blindsight 60 ft. (blind beyond this radius)
  languages: ''
  cr: '5'
stats_meta: Large plant U
titulo_pt_br: Monturo Ambulante
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Absorção de Eletricidade

Sempre que o montículo ambulante for alvo de dano elétrico, ele não sofre dano e recupera um número de pontos de vida igual ao dano elétrico causado.

## Ações

### Ataques Múltiplos

O montículo ambulante realiza dois ataques de pancada. Se ambos os ataques atingirem um alvo Médio ou menor, o alvo fica agarrado (CD para escapar 14) e o montículo ambulante usa Engolfar nele.

### Pancada

+7 para atingir, alcance 1,5 m, um alvo. Acerto: 13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano de concussão.

### Engolfar

O montículo ambulante engolfa uma criatura Média ou menor que esteja agarrada por ele. O alvo engolfado fica cego, contido e incapaz de respirar, e deve ser bem-sucedido em um teste de resistência de Constituição CD 14 no início de cada turno do montículo ou sofre 13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano de concussão. Se o montículo se mover, o alvo engolfado se move com ele. O montículo pode ter apenas uma criatura engolfada por vez.
