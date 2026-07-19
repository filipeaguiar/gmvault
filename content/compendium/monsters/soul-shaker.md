---
title: Soul Shaker
type: monster
draft: false
weight: 10
summary: Rascunho importado do 5e.tools (JTTRC). Requer tradução e revisão editorial.
tags:
- draft
- importado
- 5etools
visibility: gm
status: draft
source:
  provider: 5e.tools
  book: JTTRC
  entity_type: monster
  entity_name: Soul Shaker
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 724e33e4dc993fa3
stats:
  ac: '13'
  hp: 76 (8d10 + 32)
  speed: walk 20 ft.
  attributes:
    str: 20
    dex: 8
    con: 18
    int: 8
    wis: 11
    cha: 14
  saves: {}
  skills: {}
  senses: blindsight 60 ft. (blind beyond this radius)
  languages: telepathy 60 ft.
  cr: '4'
stats_meta: Large undead C/E
titulo_pt_br: Abalador de Almas
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Isca Cativante (1/Dia)

O soul shaker pode conjurar a magia *geas*, sem necessidade de componentes e usando Carisma como atributo de conjuração (CD para evitar magia 12).


### Reconstrução

Quando o soul shaker é reduzido a 0 pontos de vida, ele explode em 7 (<span class="dice+" data-roll-notation="1d4+5">1d4 + 5</span>) garras rastejantes. Após 6 (<span class="dice+" data-roll-notation="1d12">1d12</span>) dias, se ao menos duas dessas garras rastejantes estiverem vivas, elas se teleportam para o local da morte do soul shaker e se fundem, então o soul shaker se reforma e recupera todos os seus pontos de vida.


### Natureza Incomum

O soul shaker não requer ar, comida, bebida ou sono.

## Ações


### Agarrão Esmagador

Corpo a Corpo com Arma: 7 para atingir, alcance 1,5 m, um alvo. {@h}14 (<span class="dice+" data-roll-notation="2d8+5">2d8 + 5</span>) de dano de concussão. Se o alvo for uma criatura Média ou menor, ele fica agarrado (escapar 15). O soul shaker pode ter apenas uma criatura agarrada desta forma por vez.

## Ações Bônus


### Consumir Vitalidade

O soul shaker escolhe uma criatura que esteja agarrando. Se o alvo não for um Constructo ou Morto-vivo, ele deve ser bem-sucedido em um teste de resistência de Constituição CD 14 ou sofre 7 (<span class="dice+" data-roll-notation="2d6">2d6</span>) de dano necrótico. O máximo de pontos de vida do alvo é reduzido em uma quantidade igual ao dano necrótico sofrido, e o soul shaker recupera pontos de vida equivalentes. Essa redução dura até o alvo terminar um descanso longo. O alvo morre se seu máximo de pontos de vida for reduzido a 0.
