---
title: Mud Mephit
type: monster
draft: false
weight: 10
tags:
- draft
- importado
- 5etools
visibility: gm
status: ready
source:
  provider: 5e.tools
  book: MM
  entity_type: monster
  entity_name: Mud Mephit
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 3a29f5edfc5f7326
stats:
  ac: '11'
  hp: 27 (6d6 + 6)
  speed: walk 20 ft., fly 20 ft., swim 20 ft.
  attributes:
    str: 8
    dex: 12
    con: 12
    int: 9
    wis: 11
    cha: 7
  saves: {}
  skills:
    stealth: '+3'
  senses: darkvision 60 ft.
  languages: Aquan, Terran
  cr: 1/4
stats_meta: Small elemental N/E
titulo_pt_br: Mefítico de Lama
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Explosão Mortal

Quando o mephit morre, ele explode em uma erupção de lama pegajosa. Cada criatura de tamanho Médio ou menor a até 1,5 metro dele deve ser bem-sucedida em um teste de resistência de Destreza CD 11 ou ficará contida até o final do próximo turno da criatura.


### Falsa Aparência

Enquanto o mephit permanece imóvel, ele é indistinguível de um monte de lama comum.

## Ações


### Punhos

corpo a corpo +3 para acertar, alcance 1,5 m, uma criatura. <i>Dano:</i> 4 (<span class="dice+" data-roll-notation="1d6+1">1d6 + 1</span>) de dano de concussão.


### Sopro de Lama {@recharge}

O mephit arrota lama viscosa em uma criatura a até 1,5 metro dele. Se o alvo for de tamanho Médio ou menor, ele deve ser bem-sucedido em um teste de resistência de Destreza CD 11 ou ficará contido por 1 minuto. Uma criatura pode repetir o teste de resistência no final de cada um de seus turnos, encerrando o efeito sobre si mesma em caso de sucesso.
