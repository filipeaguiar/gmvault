---
title: Adult Blue Dragon
params:
  kind: monster
draft: true
weight: 10
summary: Rascunho importado de 5e.tools (MM). Requer tradução e revisão editorial.
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
  entity_name: Adult Blue Dragon
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 98a71e29165266f5
stats:
  ac: '19'
  hp: 225 (18d12 + 108)
  speed: walk 40 ft., burrow 30 ft., fly 80 ft.
  attributes:
    str: 25
    dex: 10
    con: 23
    int: 16
    wis: 15
    cha: 19
  saves:
    dex: '+5'
    con: '+11'
    wis: '+7'
    cha: '+9'
  skills:
    perception: '+12'
    stealth: '+5'
  senses: blindsight 60 ft., darkvision 120 ft.
  languages: Common, Draconic
  cr: '16'
stats_meta: Huge dragon L/E
titulo_pt_br: Adult Blue Dragão
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Resistência Lendária (3/Dia)

Se o dragão falhar em um teste de resistência, ele pode escolher ser bem-sucedido em vez disso.

## Ações


### Ataques Múltiplos

O dragão pode usar sua Presença Amedrontadora. Ele então realiza três ataques: um com sua mordida e dois com suas garras.


### Mordida

mw 12 para atingir, alcance 3 m, um alvo. {@h}18 (<span class="dice+" data-roll-notation="2d10+7">2d10 + 7</span>) de dano perfurante mais 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano elétrico.


### Garra

mw 12 para atingir, alcance 1,5 m, um alvo. {@h}14 (<span class="dice+" data-roll-notation="2d6+7">2d6 + 7</span>) de dano cortante.


### Cauda

mw 12 para atingir, alcance 4,5 m, um alvo. {@h}16 (<span class="dice+" data-roll-notation="2d8+7">2d8 + 7</span>) de dano de concussão.


### Presença Amedrontadora

Cada criatura, à escolha do dragão, que esteja a até 36 metros do dragão e ciente dele, deve ser bem-sucedida em um teste de resistência de Sabedoria CD 17 ou ficará amedrontada por 1 minuto. Uma criatura pode repetir o teste de resistência no final de cada um de seus turnos, encerrando o efeito sobre si mesma em caso de sucesso. Se o teste de resistência de uma criatura for bem-sucedido ou o efeito terminar para ela, a criatura fica imune à Presença Amedrontadora do dragão pelas próximas 24 horas.


### Sopro Elétrico 5

O dragão exala eletricidade em uma linha de 27 metros de comprimento e 1,5 metro de largura. Cada criatura nessa linha deve realizar um teste de resistência de Destreza CD 19, sofrendo 66 (<span class="dice+" data-roll-notation="12d10">12d10</span>) de dano elétrico em caso de falha no teste, ou metade desse dano em caso de sucesso.

## Ações Lendárias


### Detectar

O dragão realiza um teste de Sabedoria (Percepção).


### Ataque de Cauda

O dragão realiza um ataque de cauda.


### Ataque de Asas (Custa 2 Ações)

O dragão bate suas asas. Cada criatura a até 3 metros do dragão deve ser bem-sucedida em um teste de resistência de Destreza CD 20 ou sofrerá 14 (<span class="dice+" data-roll-notation="2d6+7">2d6 + 7</span>) de dano de concussão e ficará caída. O dragão pode então voar até metade de seu deslocamento de voo.
