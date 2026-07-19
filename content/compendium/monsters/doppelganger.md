---
title: Doppelganger
params:
  kind: monster
draft: true
weight: 10
summary: Entendido! Envie o texto do rascunho importado do 5e.tools (MM) para que eu possa realizar a tradução e a revisão editorial para português do Brasil, aplicando a terminologia padrão de D&D 5e.
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
  entity_name: Doppelganger
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 7f1eb92e105a2621
stats:
  ac: '14'
  hp: 52 (8d8 + 16)
  speed: walk 30 ft.
  attributes:
    str: 11
    dex: 18
    con: 14
    int: 11
    wis: 12
    cha: 14
  saves: {}
  skills:
    deception: '+6'
    insight: '+3'
  senses: darkvision 60 ft.
  languages: Common
  cr: '3'
stats_meta: Medium monstrosity N
titulo_pt_br: Doppelganger
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Metamorfo

O doppelganger pode usar sua ação para se transformar em um humanoide Pequeno ou Médio que tenha visto, ou voltar à sua forma verdadeira. Suas estatísticas, exceto seu tamanho, são as mesmas em cada forma. Qualquer equipamento que esteja vestindo ou carregando não é transformado. Ele reverte à sua forma verdadeira se morrer.

### Emboscador

No primeiro round de combate, o doppelganger tem vantagem nas jogadas de ataque contra qualquer criatura que tenha surpreendido.

### Ataque Surpresa

Se o doppelganger surpreende uma criatura e a atinge com um ataque durante o primeiro round de combate, o alvo sofre 10 (<span class="dice+" data-roll-notation="3d6">3d6</span>) de dano extra do ataque.

## Ações

### Ataques Múltiplos

O doppelganger realiza dois ataques corpo a corpo.

### Pancada

mw 6 to hit, alcance 1,5 m, um alvo. {@h}7 (<span class="dice+" data-roll-notation="1d6+4">1d6 + 4</span>) de dano de concussão.

### Ler Pensamentos

O doppelganger lê magicamente os pensamentos superficiais de uma criatura a até 18 metros dele. O efeito pode penetrar barreiras, mas 90 cm de madeira ou terra, 60 cm de pedra, 5 cm de metal ou uma fina lâmina de chumbo o bloqueiam. Enquanto o alvo estiver no alcance, o doppelganger pode continuar lendo seus pensamentos, contanto que a concentração do doppelganger não seja quebrada (como se estivesse se concentrando em uma magia). Enquanto lê a mente do alvo, o doppelganger tem vantagem em testes de Sabedoria (Intuição) e Carisma (Enganação, Intimidação e Persuasão) contra o alvo.
