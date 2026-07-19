---
title: Lizard
params:
  kind: monster
draft: true
weight: 10
summary: 'Personagens ficam presos em marcas de explosão, etc, nas paredes. Em muitos lugares, o piso está rachado ou desabado, e crateras se formaram.


  A área é fortemente obscurecida por fumaça e neblina até uma altura de 4,5 metros. Criaturas sem a habilidade de enxergar através de áreas fortemente obscurecidas tratam a área como <b>terreno difícil</b>, e criaturas com essa habilidade podem tratar a área como normal.


  Qualquer criatura que sofra dano trovejante enquanto estiver nesta área deve ser bem-sucedida em um teste de Força CD 12 {@status Grappled|condition|TeLe} ou será {@condition empurrada} 3 metros na direção da borda mais próxima da área. Em um sucesso, a criatura não é {@condition empurrada}. O som estrondoso pode ser ouvido a um alcance de 300 metros e atrai criaturas na área.'
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
  entity_name: Lizard
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 21be2f0a456a72bc
stats:
  ac: '10'
  hp: 2 (1d4)
  speed: walk 20 ft., climb 20 ft.
  attributes:
    str: 2
    dex: 11
    con: 10
    int: 1
    wis: 8
    cha: 3
  saves: {}
  skills: {}
  senses: darkvision 30 ft.
  languages: ''
  cr: '0'
stats_meta: Tiny beast U
titulo_pt_br: Lagarto
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

### Mordida

mw 0 para atingir, alcance 5 pés, um alvo. {@h}1 de dano perfurante.
