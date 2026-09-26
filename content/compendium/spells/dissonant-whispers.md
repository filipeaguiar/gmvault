---
title: Dissonant Whispers
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
  entity_name: Dissonant Whispers
  remote_file: spells/spells-xphb.json
  remote_key: spell
  remote_id: a34a372a40ca7c94
spell_info:
  level: 1º nível
  school: Encantamento
  cast_time: 1 ação
  range: 60 pés
  components: V
  duration: Instantâneo
  level_number: 1
  attack_type: null
  damage_types:
  - psychic
  saving_throws:
  - wisdom
  rolls:
  - kind: damage
    notation: 3d6
    label: Dano
    damage_type: psychic
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
titulo_pt_br: Sussurros Dissonantes
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

Uma criatura à sua escolha que você possa ver, dentro do alcance, ouve uma melodia discordante em sua mente. O alvo realiza um teste de resistência de Sabedoria. Em caso de falha no teste de resistência, ele sofre <span class="dice+" data-roll-notation="3d6">3d6</span> de Dano Psíquico e deve imediatamente usar sua Reação, se disponível, para se afastar o máximo possível de você, usando a rota mais segura. Em caso de sucesso no teste de resistência, o alvo sofre apenas metade do dano.

## Em Níveis Superiores


### Usando um Espaço de Magia de Nível Superior

O dano aumenta em <span class="dice+" data-roll-notation="3d6">3d6</span> para cada nível de espaço de magia acima do 1º.
