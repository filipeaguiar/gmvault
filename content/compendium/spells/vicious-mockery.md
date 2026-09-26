---
title: Vicious Mockery
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
  entity_name: Vicious Mockery
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: aff97722448891d2
spell_info:
  level: Truque
  school: Encantamento
  cast_time: 1 ação
  range: 60 pés
  components: V
  duration: Instantâneo
  level_number: 0
  attack_type: null
  damage_types:
  - psychic
  saving_throws:
  - wisdom
  rolls:
  - kind: damage
    notation: 1d6
    label: Dano
    damage_type: psychic
    scaling:
      mode: character_level
      thresholds:
        '1': 1d6
        '5': 2d6
        '11': 3d6
        '17': 4d6
titulo_pt_br: Zombaria Viciosa
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

Você desfere uma série de insultos entrelaçados com encantamentos sutis a uma criatura que você possa ver ou ouvir dentro do alcance. O alvo deve ser bem-sucedido em um teste de resistência de Sabedoria ou sofre <span class="dice+" data-roll-notation="1d6">1d6</span> de dano psíquico e tem Desvantagem na próxima jogada de ataque que fizer antes do final do próximo turno dele.

## Em Níveis Superiores

### Aprimoramento do Truque

O dano aumenta em <span class="dice+" data-roll-notation="1d6">1d6</span> quando você atinge os níveis 5 (<span class="dice+" data-roll-notation="2d6">2d6</span>), 11 (<span class="dice+" data-roll-notation="3d6">3d6</span>) e 17 (<span class="dice+" data-roll-notation="4d6">4d6</span>).
