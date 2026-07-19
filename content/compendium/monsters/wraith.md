---
title: Wraith
params:
  kind: monster
draft: true
weight: 10
summary: Claro. Por favor, forneça o texto do rascunho importado de 5e.tools (MM) para que eu possa realizar a tradução e a revisão editorial conforme as regras especificadas.
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
  entity_name: Wraith
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 8d40c17d4aac4470
stats:
  ac: '13'
  hp: 67 (9d8 + 27)
  speed: walk 0 ft., fly 60 ft.
  attributes:
    str: 6
    dex: 16
    con: 16
    int: 12
    wis: 14
    cha: 15
  saves: {}
  skills: {}
  senses: darkvision 60 ft.
  languages: the languages it knew in life
  cr: '5'
stats_meta: Medium undead N/E
titulo_pt_br: Wraith
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Movimento Incorpóreo

A aparição pode se mover através de outras criaturas e objetos como se fossem 3. Ela sofre 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano de energia se terminar seu turno dentro de um objeto.


### Sensibilidade à Luz Solar

Enquanto estiver sob luz solar, a aparição tem desvantagem em jogadas de ataque, bem como em testes de Sabedoria (Percepção) que dependem da visão.

## Ações


### Drenar Vida

Ataque Corpo a Corpo com Arma: 6 para acertar, alcance 1,5 m, uma criatura. {@h}21 (<span class="dice+" data-roll-notation="4d8+3">4d8 + 3</span>) de dano necrótico. O alvo deve ser bem-sucedido em um teste de resistência de Constituição CD 14 ou seu máximo de pontos de vida é reduzido em uma quantidade igual ao dano sofrido. Esta redução dura até o alvo terminar um descanso longo. O alvo morre se este efeito reduzir seu máximo de pontos de vida a 0.


### Criar Espectro

A aparição escolhe um humanoide a até 3 metros dela que esteja morto por não mais de 1 minuto e tenha morrido de forma violenta. O espírito do alvo se ergue como um espectro no espaço de seu cadáver ou no espaço desocupado mais próximo. O espectro está sob o controle da aparição. A aparição não pode ter mais de sete espectros sob seu controle ao mesmo tempo.
