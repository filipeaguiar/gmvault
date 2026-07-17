---
title: Wraith
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
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Aparição
---

## Traços

### Movimento Incorpóreo

A aparição pode mover-se através de outras criaturas e objetos como se fossem terreno difícil. Ela sofre 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano de energia se terminar o turno dela dentro de um objeto.

### Sensibilidade à Luz Solar

Enquanto estiver sob luz solar, a aparição tem desvantagem em jogadas de ataque, bem como em testes de Sabedoria (Percepção) que dependam da visão.

## Ações

### Drenar Vida

Ataque Corpo a Corpo com Arma: +6 para atingir, alcance 1,5 m, uma criatura. *Acerto:* 21 (<span class="dice+" data-roll-notation="4d8+3">4d8 + 3</span>) de dano necrótico. O alvo deve ser bem-sucedido em um teste de resistência de Constituição CD 14 ou ter seu máximo de pontos de vida reduzido em uma quantidade igual ao dano sofrido. Essa redução dura até o alvo terminar um descanso longo. O alvo morre se esse efeito reduzir seu máximo de pontos de vida a 0.

### Criar Espectro

A aparição escolhe um humanoide a até 3 metros dela que esteja morto há não mais que 1 minuto e tenha morrido de forma violenta. O espírito do alvo se ergue como um espectro no espaço do cadáver ou no espaço desocupado mais próximo. O espectro está sob o controle da aparição. A aparição não pode ter mais de sete espectros sob seu controle ao mesmo tempo.
