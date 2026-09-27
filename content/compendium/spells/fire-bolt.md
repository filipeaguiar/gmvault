---
title: Fire Bolt
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
  entity_name: Fire Bolt
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 91b6628fd540f395
spell_info:
  level: Cantrip
  school: Evocation
  cast_time: 1 action
  range: 120 feet
  components: V, S
  ritual: false
  duration: Instantaneous
  level_number: 0
  attack_type: ranged
  damage_types:
  - fire
  saving_throws: []
  rolls:
  - kind: damage
    notation: 1d10
    label: Dano
    damage_type: fire
    scaling:
      mode: character_level
      thresholds:
        '1': 1d10
        '5': 2d10
        '11': 3d10
        '17': 4d10
titulo_pt_br: Dardo de Fogo
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

Você arremessa uma partícula de fogo em uma criatura ou objeto dentro do alcance. Faça um ataque à distância com magia contra o alvo. Em um acerto, o alvo sofre <span class="dice+" data-roll-notation="1d10">1d10</span> de dano de fogo. Um objeto inflamável atingido por esta magia começa a queimar se não estiver sendo vestido ou carregado.

## Em Níveis Superiores


### Aprimoramento do Truque

O dano aumenta em <span class="dice+" data-roll-notation="1d10">1d10</span> quando você alcança os níveis 5 (<span class="dice+" data-roll-notation="2d10">2d10</span>), 11 (<span class="dice+" data-roll-notation="3d10">3d10</span>) e 17 (<span class="dice+" data-roll-notation="4d10">4d10</span>).
