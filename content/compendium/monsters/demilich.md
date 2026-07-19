---
title: Demilich
params:
  kind: monster
draft: true
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
  entity_name: Demilich
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 8774eba43ff3d4e8
stats:
  ac: '20'
  hp: 80 (32d4)
  speed: walk 0 ft., fly 30 ft.
  attributes:
    str: 1
    dex: 20
    con: 10
    int: 20
    wis: 17
    cha: 20
  saves:
    con: '+6'
    int: '+11'
    wis: '+9'
    cha: '+11'
  skills: {}
  senses: truesight 120 ft.
  languages: ''
  cr: '18'
stats_meta: Tiny undead N/E
titulo_pt_br: Semilich
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Evasão

Se o demilich for submetido a um efeito que permita que ele faça um teste de resistência para sofrer apenas metade do dano, ele, em caso de sucesso no teste de resistência, não sofre dano, e em caso de falha, sofre apenas metade do dano.


### Resistência Lendária (3/Dia)

Se o demilich falhar em um teste de resistência, ele pode escolher ser bem-sucedido.


### Imunidade a Expulsão

O demilich é imune a efeitos que expulsam mortos-vivos.

## Ações


### Uivo

O demilich emite um uivo horripilante. Cada criatura em um raio de 30 pés do demilich que possa ouvir o uivo deve ser bem-sucedida em um teste de resistência de Constituição CD 15 ou cair para 0 pontos de vida. Em caso de sucesso no teste de resistência, a criatura fica amedrontada até o final do próximo turno dela.


### Drenar Vida

O demilich escolhe até três criaturas que possa ver em um raio de 10 pés. Cada alvo deve ser bem-sucedido em um teste de resistência de Constituição CD 19 ou sofrer 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) de dano necrótico, e o demilich recupera pontos de vida iguais ao dano total causado a todos os alvos.

## Ações Lendárias


### Voo

O demilich voa até metade do seu deslocamento de voo.


### Nuvem de Poeira

O demilich revolve magicamente seus restos empoeirados. Cada criatura em um raio de 10 pés do demilich, incluindo aquelas atrás de cobertura, deve ser bem-sucedida em um teste de resistência de Constituição CD 15 ou ficar cega até o final do próximo turno do demilich. Uma criatura que seja bem-sucedida no teste de resistência fica imune a este efeito até o final do próximo turno do demilich.


### Drenar Energia (Custa 2 Ações)

Cada criatura em um raio de 30 pés do demilich deve fazer um teste de resistência de Constituição CD 15. Em caso de falha no teste de resistência, o máximo de pontos de vida da criatura é magicamente reduzido em 10 (<span class="dice+" data-roll-notation="3d6">3d6</span>). Se o máximo de pontos de vida de uma criatura for reduzido a 0 por este efeito, a criatura morre. O máximo de pontos de vida de uma criatura pode ser restaurado com a magia restauração maior ou magia similar.


### Maldição Vil (Custa 3 Ações)

O demilich escolhe uma criatura que possa ver em um raio de 30 pés. O alvo deve ser bem-sucedido em um teste de resistência de Sabedoria CD 15 ou ser amaldiçoado magicamente. Até a maldição terminar, o alvo tem desvantagem em jogadas de ataque e testes de resistência. O alvo pode repetir o teste de resistência no final de cada um de seus turnos, terminando a maldição em caso de sucesso.
