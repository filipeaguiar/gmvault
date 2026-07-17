---
title: Roper
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
  entity_name: Roper
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 4245a0198f6b0ac8
stats:
  ac: '20'
  hp: 93 (11d10 + 33)
  speed: walk 10 ft., climb 10 ft.
  attributes:
    str: 18
    dex: 8
    con: 17
    int: 7
    wis: 16
    cha: 6
  saves: {}
  skills:
    perception: '+6'
    stealth: '+5'
  senses: darkvision 60 ft.
  languages: ''
  cr: '5'
stats_meta: Large monstrosity N/E
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Roper
---

## Características


### Aparência Falsa

Enquanto o roper permanecer imóvel, ele é indistinguível de uma formação normal de caverna, como uma estalagmite.


### Tentáculos Agarradores

O roper pode ter até seis tentáculos por vez. Cada tentáculo pode ser atacado (CA 20; 10 pontos de vida; imunidade a dano de veneno e dano psíquico). Destruir um tentáculo não causa dano ao roper, que pode estender um tentáculo substituto no próximo turno dele. Um tentáculo também pode ser quebrado se uma criatura usar uma ação e for bem-sucedida em um teste de Força CD 15 contra ele.


### Escalada de Aranha

O roper pode escalar superfícies difíceis, inclusive de cabeça para baixo em tetos, sem precisar fazer um teste de atributo.

## Ações


### Ataques Múltiplos

O roper faz quatro ataques com seus tentáculos, usa Reel e faz um ataque com sua mordida.


### Mordida

mw 7 para acertar, alcance 5 pés, um alvo. {@h}22 (<span class="dice+" data-roll-notation="4d8+4">4d8 + 4</span>) de dano perfurante.


### Tentáculo

mw 7 para acertar, alcance 50 pés, uma criatura. {@h}O alvo fica agarrado (escapar CD 15). Até a condição de agarrado terminar, o alvo está contido e tem desvantagem em testes de Força e testes de resistência de Força, e o roper não pode usar o mesmo tentáculo em outro alvo.


### Reel

O roper puxa cada criatura agarrada por ele até 25 pés diretamente em sua direção.
