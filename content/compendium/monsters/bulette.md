---
title: Bulette
params:
  kind: monster
draft: false
weight: 10
summary: Desculpe, não recebi nenhum texto para traduzir. Por favor, forneça o conteúdo do rascunho importado do 5e.tools para que eu possa realizar a tradução e revisão editorial.
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
  entity_name: Bulette
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 2c9f3747ded59f3a
stats:
  ac: '17'
  hp: 94 (9d10 + 45)
  speed: walk 40 ft., burrow 40 ft.
  attributes:
    str: 19
    dex: 11
    con: 21
    int: 2
    wis: 10
    cha: 5
  saves: {}
  skills:
    perception: '+6'
  senses: darkvision 60 ft., tremorsense 60 ft.
  languages: ''
  cr: '5'
stats_meta: Large monstrosity U
titulo_pt_br: Bulette
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Salto Parado

O salto em distância do bulette é de até 9 metros e o salto em altura é de até 4,5 metros, com ou sem impulso.

## Ações


### Mordida

Ataque Corpo a Corpo com Arma: +7 para atingir, alcance 1,5 metro, um alvo. {@h}30 (<span class="dice+" data-roll-notation="4d12+4">4d12 + 4</span>) de dano perfurante.


### Salto Mortal

Se o bulette saltar pelo menos 4,5 metros como parte do seu movimento, ele pode usar esta ação para aterrissar em um espaço que contenha uma ou mais outras criaturas. Cada uma dessas criaturas deve ser bem-sucedida em um teste de resistência de Força ou Destreza CD 16 (escolha do alvo) ou ficará caída e sofrerá 14 (<span class="dice+" data-roll-notation="3d6+4">3d6 + 4</span>) de dano de concussão mais 14 (<span class="dice+" data-roll-notation="3d6+4">3d6 + 4</span>) de dano cortante. Em caso de sucesso no teste de resistência, a criatura sofre apenas metade do dano, não fica caída e é empurrada 1,5 metro para fora do espaço do bulette, para um espaço desocupado da escolha da criatura. Se não houver espaço desocupado ao alcance, a criatura cai no espaço do bulette.
