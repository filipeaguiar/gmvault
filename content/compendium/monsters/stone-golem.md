---
title: Stone Golem
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
  entity_name: Stone Golem
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: d89615192796206a
stats:
  ac: '17'
  hp: 178 (17d10 + 85)
  speed: walk 30 ft.
  attributes:
    str: 22
    dex: 9
    con: 20
    int: 3
    wis: 11
    cha: 1
  saves: {}
  skills: {}
  senses: darkvision 120 ft.
  languages: understands the languages of its creator but can't speak
  cr: '10'
stats_meta: Large construct U
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Golem de Pedra
---

## Características


### Forma Imutável

O golem é imune a qualquer magia ou efeito que alteraria sua forma.


### Resistência à Magia

O golem tem Vantagem em testes de resistência contra magias e outros efeitos mágicos.


### Armas Mágicas

Os ataques com arma do golem são mágicos.

## Ações


### Ataques Múltiplos

O golem realiza dois ataques de pancada.


### Pancada

mw 10 para atingir, alcance 1,5 m, um alvo. {@h}19 (<span class="dice+" data-roll-notation="3d8+6">3d8 + 6</span>) de dano de concussão.


### Lentidão 5

O golem escolhe uma ou mais criaturas que possa ver, a até 3 m de distância. Cada alvo deve ser bem-sucedido em um teste de resistência de Sabedoria CD 17 contra esta magia. Em caso de falha no teste de resistência, o alvo não pode usar reações, seu deslocamento é reduzido à metade e ele não pode realizar mais de um ataque em seu turno. Além disso, o alvo pode usar uma ação ou uma ação bônus em seu turno, não ambas. Estes efeitos duram 1 minuto. O alvo pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesmo em caso de sucesso no teste de resistência.
