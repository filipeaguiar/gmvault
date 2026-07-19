---
title: Otyugh
type: monster
draft: false
weight: 10
summary: Rascunho importado do 5e.tools (MM). Requer tradução e revisão editorial.
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
  entity_name: Otyugh
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: e5696b738ba5a643
stats:
  ac: '14'
  hp: 114 (12d10 + 48)
  speed: walk 30 ft.
  attributes:
    str: 16
    dex: 11
    con: 19
    int: 6
    wis: 13
    cha: 6
  saves:
    con: '+7'
  skills: {}
  senses: darkvision 120 ft.
  languages: Otyugh
  cr: '5'
stats_meta: Large aberration N
titulo_pt_br: Otyugh
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Telepatia Limitada

O otyugh pode transmitir magicamente mensagens simples e imagens para qualquer criatura a até 120 pés dele que possa entender um idioma. Esta forma de telepatia não permite que a criatura receptora responda telepaticamente.

## Ações


### Ataques Múltiplos

O otyugh realiza três ataques: um com sua mordida e dois com seus tentáculos.


### Mordida

Ataque Corpo a Corpo com Arma: +6 para atingir, alcance 5 pés, um alvo. {@h}12 (<span class="dice+" data-roll-notation="2d8+3">2d8 + 3</span>) de dano perfurante. Se o alvo for uma criatura, deve ser bem-sucedido em um teste de resistência de Constituição CD 15 contra doença ou fica envenenado até que a doença seja curada. A cada 24 horas passadas, o alvo deve repetir o teste de resistência, reduzindo seu máximo de Pontos de Vida em 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) em caso de falha. A doença é curada em caso de sucesso. O alvo morre se a doença reduzir seu máximo de Pontos de Vida a 0. Esta redução nos Pontos de Vida máximos do alvo perdura até que a doença seja curada.


### Tentáculo

Ataque Corpo a Corpo com Arma: +6 para atingir, alcance 10 pés, um alvo. {@h}7 (<span class="dice+" data-roll-notation="1d8+3">1d8 + 3</span>) de dano de concussão mais 4 (<span class="dice+" data-roll-notation="1d8">1d8</span>) de dano perfurante. Se o alvo for Médio ou menor, fica agarrado (CD 13 para escapar) e contido até que o agarrão termine. O otyugh tem dois tentáculos, cada um podendo agarrar um alvo.


### Pancada com os Tentáculos

O otyugh esmaga criaturas agarradas por ele contra outra criatura ou uma superfície sólida. Cada criatura deve ser bem-sucedida em um teste de resistência de Constituição CD 14 ou sofre 10 (<span class="dice+" data-roll-notation="2d6+3">2d6 + 3</span>) de dano de concussão e fica atordoada até o final do próximo turno do otyugh. Em caso de sucesso no teste, o alvo sofre metade do dano de concussão e não fica atordoado.
