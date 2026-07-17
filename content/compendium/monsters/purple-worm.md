---
title: Purple Worm
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
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Verme Púrpura
---

## Características

### Escavador

A criatura pode escavar através de rocha sólida com metade do seu deslocamento de escavação e deixa um túnel de 3 metros de diâmetro em seu rastro.

## Ações

### Ataques Múltiplos

A criatura realiza dois ataques: um com sua mordida e outro com seu ferrão.

### Mordida

mw 14 para atingir, alcance 3 m, um alvo. {@h}22 (<span class="dice+" data-roll-notation="3d8+9">3d8 + 9</span>) de dano perfurante. Se o alvo for uma criatura Grande ou menor, deve ser bem-sucedido em um teste de resistência de Destreza CD 19 ou será engolido pela criatura. Uma criatura engolida fica cega e contida, tem cobertura total contra ataques e outros efeitos fora da criatura, e sofre 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) de dano de ácido no início de cada turno da criatura.

Se a criatura sofrer 30 de dano ou mais em um único turno de uma criatura dentro dela, a criatura deve ser bem-sucedida em um teste de resistência de Constituição CD 21 no final desse turno ou regurgitará todas as criaturas engolidas, que caem e ficam caídas em um espaço a até 3 metros da criatura. Se a criatura morrer, uma criatura engolida não estará mais contida por ela e poderá escapar do cadáver usando 6 metros de movimento, saindo caída.

### Ferrão da Cauda

mw 14 para atingir, alcance 3 m, uma criatura. {@h}19 (<span class="dice+" data-roll-notation="3d6+9">3d6 + 9</span>) de dano perfurante, e o alvo deve realizar um teste de resistência de Constituição CD 19, sofrendo 42 (<span class="dice+" data-roll-notation="12d6">12d6</span>) de dano de veneno em caso de falha no teste, ou metade desse dano em caso de sucesso.
