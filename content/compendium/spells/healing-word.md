---
title: Healing Word
type: spell
draft: false
weight: 10
tags:
- draft
- importado
- 5etools
visibility: public
status: ready
source:
  provider: 5e.tools
  book: XPHB
  entity_type: spell
  entity_name: Healing Word
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: c0de0c232e4afb10
spell_info:
  level: 1º nível
  school: Abjuração
  cast_time: 1 ação bônus
  range: 60 pés
  components: V
  duration: Instantâneo
  level_number: 1
  attack_type: null
  damage_types: []
  saving_throws: []
  rolls:
  - kind: healing
    notation: 2d4
    label: Cura
    scaling:
      mode: spell_slot
      thresholds:
        '1': 2d4
        '2': 4d4
        '3': 6d4
        '4': 8d4
        '5': 10d4
        '6': 12d4
        '7': 14d4
        '8': 16d4
        '9': 18d4
titulo_pt_br: Palavra de Cura
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

Uma criatura à sua escolha que você possa ver dentro do alcance recupera Pontos de Vida iguais a <span class="dice+" data-roll-notation="2d4">2d4</span> mais seu modificador de atributo de conjuração.

## Em Níveis Superiores


### Usando um Espaço de Magia de Nível Superior

A cura aumenta em <span class="dice+" data-roll-notation="2d4">2d4</span> para cada nível de espaço de magia acima do 1º.
