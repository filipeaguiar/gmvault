---
title: Banshee
type: monster
draft: false
weight: 10
tags:
- draft
- importado
- 5etools
visibility: gm
status: ready
source:
  provider: 5e.tools
  book: MM
  entity_type: monster
  entity_name: Banshee
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: b8dfb039ce1ca46f
stats:
  ac: '12'
  hp: 58 (13d8)
  speed: walk 0 ft., fly 40 ft.
  attributes:
    str: 1
    dex: 14
    con: 10
    int: 12
    wis: 11
    cha: 17
  saves:
    wis: '+2'
    cha: '+5'
  skills: {}
  senses: darkvision 60 ft.
  languages: Common, Elvish
  cr: '4'
stats_meta: Medium undead C/E
titulo_pt_br: Banshee
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Detectar Vida

A banshee pode sentir magicamente a presença de criaturas vivas a até 8 quilômetros de distância que não sejam mortos-vivos ou constructos. Ela sabe a direção geral em que estão, mas não suas localizações exatas.

### Movimento Incorpóreo

A banshee pode se mover através de outras criaturas e objetos como se fossem 3. Ela sofre 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano de energia se terminar seu turno dentro de um objeto.

## Ações

### Toque Corruptor

Ataque Corpo a Corpo com Magia: +4 para atingir, alcance 1,5 m, um alvo. {@h}12 (<span class="dice+" data-roll-notation="3d6+2">3d6 + 2</span>) de dano necrótico.

### Rosto Horripilante

Cada criatura que não seja morto-vivo a até 18 metros da banshee que possa vê-la deve ser bem-sucedida em um teste de resistência de Sabedoria CD 13 ou ficará amedrontada por 1 minuto. Um alvo amedrontado pode repetir o teste de resistência no final de cada um de seus turnos, com desvantagem se a banshee estiver dentro da linha de visão, terminando o efeito sobre si mesmo em caso de sucesso. Se o teste de resistência de um alvo for bem-sucedido ou o efeito terminar para ele, o alvo fica imune ao Rosto Horripilante da banshee pelas próximas 24 horas.

### Lamento (1/Dia)

A banshee libera um lamento pesaroso, desde que não esteja sob luz solar. Este lamento não tem efeito sobre constructos e mortos-vivos. Todas as outras criaturas a até 9 metros dela que possam ouvi-la devem realizar um teste de resistência de Constituição CD 13. Em caso de falha, uma criatura tem seus pontos de vida reduzidos a 0. Em caso de sucesso, uma criatura sofre 10 (<span class="dice+" data-roll-notation="3d6">3d6</span>) de dano psíquico.
