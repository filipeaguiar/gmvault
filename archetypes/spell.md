---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
weight: 10
summary: "Magia ou feitiço do compêndio."
tags: []
visibility: "public"
status: "ready"

spell_info:
  level: "1º nível"
  level_number: 1
  school: "Abjuração"
  cast_time: "1 ação"
  range: "Pessoal"
  components: "V, S"
  duration: "1 minuto"
  attack_type: null
  damage_types: []
  saving_throws: []
  rolls: []
  # Exemplo de rolagem escalada por slot:
  # rolls:
  #   - kind: damage
  #     notation: "2d6"
  #     label: "Dano"
  #     damage_type: fire
  #     scaling:
  #       mode: spell_slot
  #       thresholds:
  #         "1": "2d6"
  #         "2": "3d6"
type: "spell"
---

Insira os efeitos da magia aqui.
