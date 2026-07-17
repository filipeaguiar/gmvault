---
title: Ancient Brass Dragon
params:
  kind: monster
draft: true
weight: 10
summary: Conteúdo importado do 5e.tools (MM) e traduzido automaticamente; requer revisão editorial.
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
  entity_name: Ancient Brass Dragon
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 52898fd527d968f6
stats:
  ac: '20'
  hp: 297 (17d20 + 119)
  speed: walk 40 ft., burrow 40 ft., fly 80 ft.
  attributes:
    str: 27
    dex: 10
    con: 25
    int: 16
    wis: 15
    cha: 19
  saves:
    dex: '+6'
    con: '+13'
    wis: '+8'
    cha: '+10'
  skills:
    history: '+9'
    perception: '+14'
    persuasion: '+10'
    stealth: '+6'
  senses: blindsight 60 ft., darkvision 120 ft.
  languages: Common, Draconic
  cr: '20'
stats_meta: Gargantuan dragon C/G
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Dragão de Bronze Ancião
---

## Características

### Resistência Lendária (3/Dia)

Se o dragão falhar em um teste de resistência, ele pode escolher ser bem-sucedido em vez disso.

## Ações

### Ataques Múltiplos

O dragão pode usar sua Presença Amedrontadora. Ele então realiza três ataques: um com sua mordida e dois com suas garras.

### Mordida

mw 14 para atingir, alcance 4,5 m, um alvo. {@h}19 (2d10 + 8) de dano perfurante.

### Garra

mw 14 para atingir, alcance 3 m, um alvo. {@h}15 (2d6 + 8) de dano cortante.

### Cauda

mw 14 para atingir, alcance 6 m, um alvo. {@h}17 (2d8 + 8) de dano de concussão.

### Presença Amedrontadora

Cada criatura, escolhida pelo dragão, que esteja a até 36 metros do dragão e ciente dele deve ser bem-sucedida em um teste de resistência de Sabedoria CD 18 ou ficará amedrontada por 1 minuto. Uma criatura pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesma em caso de sucesso. Se o teste de resistência de uma criatura for bem-sucedido ou o efeito terminar para ela, a criatura fica imune à Presença Amedrontadora do dragão pelas próximas 24 horas.

### Armas de Sopro 5

O dragão usa uma das seguintes armas de sopro:

- {'type': 'item', 'name': 'Sopro de Fogo', 'entry': 'O dragão exala fogo em uma linha de 27 metros de comprimento e 3 metros de largura. Cada criatura nessa linha deve realizar um teste de resistência de Destreza CD 21, sofrendo 56 (16d6) de dano de fogo em caso de falha no teste, ou metade desse dano em caso de sucesso.'}
- {'type': 'item', 'name': 'Sopro de Sono', 'entry': 'O dragão exala gás sonífero em um cone de 27 metros. Cada criatura nessa área deve ser bem-sucedida em um teste de resistência de Constituição CD 21 ou cairá inconsciente por 10 minutos. Este efeito termina para uma criatura se ela sofrer dano ou se alguém usar uma ação para acordá-la.'}

### Mudar Forma

O dragão se polimorfiza magicamente em um humanoide ou besta que tenha um nível de desafio não superior ao seu, ou de volta à sua forma verdadeira. Ele reverte à sua forma verdadeira se morrer. Qualquer equipamento que ele esteja vestindo ou carregando é absorvido ou usado pela nova forma (à escolha do dragão).

Em uma nova forma, o dragão mantém sua tendência, Pontos de Vida, Dados de Vida, capacidade de falar, proficiências, Resistência Lendária, ações de covil e os valores de Inteligência, Sabedoria e Carisma, bem como esta ação. Suas estatísticas e capacidades são, de outra forma, substituídas pelas da nova forma, exceto quaisquer características de classe ou ações lendárias dessa forma.

## Ações Lendárias

### Detectar

O dragão realiza um teste de Sabedoria (Percepção).

### Ataque de Cauda

O dragão realiza um ataque de cauda.

### Ataque de Asas (Custa 2 Ações)

O dragão bate suas asas. Cada criatura a até 4,5 metros do dragão deve ser bem-sucedida em um teste de resistência de Destreza CD 22 ou sofrerá 15 (2d6 + 8) de dano de concussão e ficará caída. O dragão pode então voar até metade do seu deslocamento de voo.
