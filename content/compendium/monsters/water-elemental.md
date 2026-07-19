---
title: Water Elemental
params:
  kind: monster
draft: true
weight: 10
summary: Rascunho importado de 5e.tools (MM). Requer tradução e revisão editorial.
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
  entity_name: Water Elemental
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: e43233cef8316bf8
stats:
  ac: '14'
  hp: 114 (12d10 + 48)
  speed: walk 30 ft., swim 90 ft.
  attributes:
    str: 18
    dex: 14
    con: 18
    int: 5
    wis: 10
    cha: 8
  saves: {}
  skills: {}
  senses: darkvision 60 ft.
  languages: Aquan
  cr: '5'
stats_meta: Large elemental N
titulo_pt_br: Elemental da Água
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Forma Aquática

O elemental pode entrar no espaço de uma criatura hostil e parar ali. Ele pode se mover por um espaço de até 2,5 centímetros de largura sem se espremer.


### Congelar

Se o elemental sofrer dano de frio, ele congela parcialmente; seu deslocamento é reduzido em 6 metros até o final do próximo turno dele.

## Ações


### Ataques Múltiplos

O elemental realiza dois ataques de pancada.


### Pancada

Ataque Corpo a Corpo com Arma: +7 para atingir, alcance 1,5 m, um alvo. {@h}13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano de concussão.


### Submersão (Recarga 4)

Cada criatura no espaço do elemental deve realizar um teste de resistência de Força CD 15. Em caso de falha, o alvo sofre 13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano de concussão. Se for Grande ou menor, também fica agarrada (CD 14 para escapar). Até que esse agarrão termine, o alvo fica contido e incapaz de respirar, a menos que possa respirar debaixo d'água. Em caso de sucesso no teste de resistência, o alvo é empurrado para fora do espaço do elemental.

O elemental pode agarrar uma criatura Grande ou até duas criaturas Médias ou menores por vez. No início de cada turno do elemental, cada alvo agarrado por ele sofre 13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano de concussão. Uma criatura a até 1,5 metro do elemental pode usar uma ação para realizar um teste de Força CD 14. Se tiver sucesso, ela puxa uma criatura ou objeto para fora do elemental.
