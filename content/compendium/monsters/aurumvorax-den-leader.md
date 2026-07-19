---
title: Aurumvorax Den Leader
params:
  kind: monster
draft: true
weight: 10
summary: Estou pronto para receber o rascunho importado do 5e.tools (JTTRC) e realizar a tradução com revisão editorial. Por favor, envie o texto a ser trabalhado.
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
  entity_name: Aurumvorax Den Leader
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: c6523d0f3189c9e5
stats:
  ac: '16'
  hp: 52 (8d8 + 16)
  speed: walk 40 ft., burrow 20 ft.
  attributes:
    str: 18
    dex: 14
    con: 14
    int: 3
    wis: 13
    cha: 8
  saves:
    str: '+6'
    con: '+4'
  skills:
    perception: '+3'
    stealth: '+4'
  senses: darkvision 60 ft.
  languages: ''
  cr: '4'
stats_meta: Medium monstrosity U
titulo_pt_br: Líder da Toca Aurumvorax
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Líder de Matilha

Os aliados do aurumvorax têm vantagem em jogadas de ataque enquanto estiverem a até 3 metros do aurumvorax, desde que ele não esteja incapacitado.


### Escavador

O aurumvorax pode escavar rocha sólida e metal com metade do seu deslocamento de escavação, deixando um túnel de 1,5 metros de diâmetro por onde passa.

## Ações


### Ataques Múltiplos

O aurumvorax faz um ataque de Mordida e dois ataques de Garra.


### Mordida

+6 para atingir, alcance 1,5 m, um alvo. {@h}13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano perfurante. Se o alvo for uma criatura vestindo armadura de qualquer tipo, o aurumvorax ganha um dos seguintes benefícios à sua escolha:


### Frenesi

O aurumvorax tem vantagem em jogadas de ataque até o início do próximo turno dele.


### Revigorar

O aurumvorax recupera 6 (<span class="dice+" data-roll-notation="1d8+2">1d8 + 2</span>) pontos de vida.


### Garra

+6 para atingir, alcance 1,5 m, um alvo. {@h}11 (<span class="dice+" data-roll-notation="2d6+4">2d6 + 4</span>) de dano cortante. Se o alvo for uma criatura Grande ou menor, fica agarrado (CD para escapar 14). Até este agarrão terminar, o aurumvorax não pode usar seu ataque de Garra em outro alvo e, ao se mover, pode arrastar a criatura agarrada com ele, sem que seu deslocamento seja reduzido à metade.
