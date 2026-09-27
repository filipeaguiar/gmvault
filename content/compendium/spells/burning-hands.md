---
title: Burning Hands
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
  entity_name: Burning Hands
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 862f2a13f2ca5f92
spell_info:
  level: 1st level
  school: Evocation
  cast_time: 1 action
  range: 15 feet
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
    notation: 3d6
    label: Dano
    damage_type: fire
    scaling:
      mode: spell_slot
      thresholds:
        '1': 3d6
        '2': 4d6
        '3': 5d6
        '4': 6d6
        '5': 7d6
        '6': 8d6
        '7': 9d6
        '8': 10d6
        '9': 11d6
titulo_pt_br: Mãos Flamejantes
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

Uma fina lâmina de chamas irrompe de você. Cada criatura em um Cone de 4,5 metros realiza um teste de resistência de Destreza, sofrendo <span class="dice+" data-roll-notation="3d6">3d6</span> de dano de fogo em caso de falha no teste de resistência, ou metade do dano em caso de sucesso.

Objetos inflamáveis no Cone que não estejam sendo vestidos ou carregados começam a queimar.

## Em Níveis Superiores

### Usando um Espaço de Magia de Nível Superior

O dano aumenta em <span class="dice+" data-roll-notation="3d6">3d6</span> para cada nível de espaço de magia acima do 1º.
