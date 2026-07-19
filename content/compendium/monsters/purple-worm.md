---
title: Purple Worm
type: monster
draft: false
weight: 10
summary: Por favor, forneça o texto do rascunho do 5e.tools (MM) que precisa ser traduzido e revisado editorialmente.
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
  entity_name: Purple Worm
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 094b2ceebe20587c
stats:
  ac: '18'
  hp: 247 (15d20 + 90)
  speed: walk 50 ft., burrow 30 ft.
  attributes:
    str: 28
    dex: 7
    con: 22
    int: 1
    wis: 8
    cha: 4
  saves:
    con: '+11'
    wis: '+4'
  skills: {}
  senses: blindsight 30 ft., tremorsense 60 ft.
  languages: ''
  cr: '15'
stats_meta: Gargantuan monstrosity U
titulo_pt_br: verme púrpura
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Escavador
O verme pode escavar através de rocha sólida com metade do seu deslocamento de escavação e deixa um túnel de 3 metros de diâmetro em seu rastro.

## Ações

### Ataques Múltiplos
O verme realiza dois ataques: um com sua mordida e outro com seu ferrão.

### Mordida
*mw 14 para atingir*, alcance 3 m, um alvo. *Dano:* 22 (<span class="dice+" data-roll-notation="3d8+9">3d8 + 9</span>) de dano perfurante. Se o alvo for uma criatura Grande ou menor, deve ser bem-sucedido em um teste de resistência de Destreza CD 19 ou será engolido pelo verme. Uma criatura engolida fica cega e contida, tem cobertura total contra ataques e outros efeitos externos ao verme e sofre 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) de dano de ácido no início de cada turno do verme.

Se o verme sofrer 30 ou mais pontos de dano em um único turno por parte de uma criatura em seu interior, deve ser bem-sucedido em um teste de resistência de Constituição CD 21 ao final daquele turno ou regurgitará todas as criaturas engolidas, que cairão caídas em um espaço a até 3 metros do verme. Se o verme morrer, uma criatura engolida não estará mais contida por ele e poderá escapar do cadáver utilizando 6 metros de deslocamento, saindo caída.

### Ferrão da Cauda
*mw 14 para atingir*, alcance 3 m, uma criatura. *Dano:* 19 (<span class="dice+" data-roll-notation="3d6+9">3d6 + 9</span>) de dano perfurante, e o alvo deve realizar um teste de resistência de Constituição CD 19, sofrendo 42 (<span class="dice+" data-roll-notation="12d6">12d6</span>) de dano de veneno em caso de falha no teste de resistência, ou metade do dano em caso de sucesso.
