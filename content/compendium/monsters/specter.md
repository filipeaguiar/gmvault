---
title: Specter
params:
  kind: monster
draft: false
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
  entity_name: Specter
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 0297bf294d3021b5
stats:
  ac: '12'
  hp: 22 (5d8)
  speed: walk 0 ft., fly 50 ft.
  attributes:
    str: 1
    dex: 14
    con: 11
    int: 10
    wis: 10
    cha: 11
  saves: {}
  skills: {}
  senses: darkvision 60 ft.
  languages: understands all languages it knew in life but can't speak
  cr: '1'
stats_meta: Medium undead C/E
titulo_pt_br: Espectro
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Movimento Incorpóreo

O espectro pode mover-se através de outras criaturas e objetos como se fossem 3. Sofre 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano de energia se terminar seu turno dentro de um objeto.


### Sensibilidade à Luz Solar

Enquanto estiver sob a luz do sol, o espectro tem desvantagem em jogadas de ataque, bem como em testes de Sabedoria (Percepção) que dependam da visão.

## Ações


### Sugar a Vida

Ataque Corpo a Corpo com Magia: +4 para atingir, alcance 1,5 m, uma criatura. {@h}10 (<span class="dice+" data-roll-notation="3d6">3d6</span>) de dano necrótico. O alvo deve ser bem-sucedido em um teste de resistência de Constituição CD 10 ou o máximo de pontos de vida dele é reduzido em um valor igual ao dano sofrido. Esta redução dura até que a criatura termine um descanso longo. O alvo morre se este efeito reduzir o máximo de pontos de vida dele a 0.
