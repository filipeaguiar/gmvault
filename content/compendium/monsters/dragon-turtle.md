---
title: Dragon Turtle
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
  entity_name: Dragon Turtle
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 4f7662ca14648bdd
stats:
  ac: '20'
  hp: 341 (22d20 + 110)
  speed: walk 20 ft., swim 40 ft.
  attributes:
    str: 25
    dex: 10
    con: 20
    int: 10
    wis: 12
    cha: 12
  saves:
    dex: '+6'
    con: '+11'
    wis: '+7'
  skills: {}
  senses: darkvision 120 ft.
  languages: Aquan, Draconic
  cr: '17'
stats_meta: Gargantuan dragon N
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Dragão Tartaruga
---

## Características

### Anfíbio

A tartaruga-dragão pode respirar ar e água.

## Ações

### Ataques Múltiplos

A tartaruga-dragão realiza três ataques: um com sua mordida e dois com suas garras. Ela pode realizar um ataque de cauda no lugar dos dois ataques de garra.

### Mordida

mw 13 para atingir, alcance 15 ft., um alvo. {@h}26 (<span class="dice+" data-roll-notation="3d12+7">3d12 + 7</span>) de dano perfurante.

### Garra

mw 13 para atingir, alcance 10 ft., um alvo. {@h}16 (<span class="dice+" data-roll-notation="2d8+7">2d8 + 7</span>) de dano cortante.

### Cauda

mw 13 para atingir, alcance 15 ft., um alvo. {@h}26 (<span class="dice+" data-roll-notation="3d12+7">3d12 + 7</span>) de dano de concussão. Se o alvo for uma criatura, ela deve ser bem-sucedida em um teste de resistência de Força CD 20 ou será empurrada até 10 pés para longe da tartaruga-dragão e ficará caída.

### Sopro de Vapor 5

A tartaruga-dragão exala vapor escaldante em um cone de 60 pés. Cada criatura nessa área deve fazer um teste de resistência de Constituição CD 18, sofrendo 52 (<span class="dice+" data-roll-notation="15d6">15d6</span>) de dano de fogo em caso de falha no teste de resistência, ou metade desse dano em caso de sucesso. Estar submerso não concede resistência a este dano.
