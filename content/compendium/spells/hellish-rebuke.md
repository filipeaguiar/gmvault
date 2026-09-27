---
title: Hellish Rebuke
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
  entity_name: Hellish Rebuke
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 378054b8a382cb3f
spell_info:
  level: 1st level
  school: Evocation
  cast_time: 1 reaction
  range: 60 feet
  components: V, S
  ritual: false
  duration: Instantaneous
  level_number: 1
  attack_type: null
  damage_types:
  - fire
  saving_throws:
  - dexterity
  rolls:
  - kind: damage
    notation: 2d10
    label: Dano
    damage_type: fire
    scaling:
      mode: spell_slot
      thresholds:
        '1': 2d10
        '2': 3d10
        '3': 4d10
        '4': 5d10
        '5': 6d10
        '6': 7d10
        '7': 8d10
        '8': 9d10
        '9': 10d10
titulo_pt_br: Repreensão Infernal
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

A criatura que causou dano a você fica momentaneamente cercada por chamas verdes. Ela realiza um Teste de Resistência de Destreza, sofrendo <span class="dice+" data-roll-notation="2d10">2d10</span> de Dano de Fogo em caso de falha no teste de resistência ou metade do dano em caso de sucesso.

## Em Níveis Superiores

### Usando um Espaço de Magia de Nível Superior

O dano aumenta em <span class="dice+" data-roll-notation="2d10">2d10</span> para cada nível do espaço de magia acima do 1º.
