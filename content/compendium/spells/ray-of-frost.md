---
title: Ray of Frost
params:
  kind: spell
draft: true
weight: 10
summary: Conteúdo importado do 5e.tools (XPHB) e traduzido automaticamente; requer revisão editorial.
tags:
- draft
- importado
- 5etools
visibility: public
status: draft
source:
  provider: 5e.tools
  book: XPHB
  entity_type: spell
  entity_name: Ray of Frost
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: 4cc9181c11843cdb
spell_info:
  level: Cantrip
  school: Evocation
  cast_time: 1 action
  range: 60 feet
  components: V, S
  duration: Instantaneous
  level_number: 0
  attack_type: ranged
  damage_types:
  - cold
  saving_throws: []
  rolls:
  - kind: damage
    notation: 1d8
    label: Dano
    damage_type: cold
    scaling:
      mode: character_level
      thresholds:
        '1': 1d8
        '5': 2d8
        '11': 3d8
        '17': 4d8
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

Um raio gélido de luz branco-azulada avança em direção a uma criatura dentro do alcance. Faça um ataque à distância com magia contra o alvo. Em caso de acerto, ele sofre <span class="dice+" data-roll-notation="1d8">1d8</span> de Dano de Frio e seu XPHB é reduzido em 3 metros até o início do seu próximo turno.

## Em Círculos Superiores

### Aprimoramento de Truque

O dano aumenta em <span class="dice+" data-roll-notation="1d8">1d8</span> quando você atinge os níveis 5 (<span class="dice+" data-roll-notation="2d8">2d8</span>), 11 (<span class="dice+" data-roll-notation="3d8">3d8</span>) e 17 (<span class="dice+" data-roll-notation="4d8">4d8</span>).
