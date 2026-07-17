---
title: Adult Gold Dragon
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
  entity_name: Adult Gold Dragon
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 1163df6002d21a27
stats:
  ac: '19'
  hp: 256 (19d12 + 133)
  speed: walk 40 ft., fly 80 ft., swim 40 ft.
  attributes:
    str: 27
    dex: 14
    con: 25
    int: 16
    wis: 15
    cha: 24
  saves:
    dex: '+8'
    con: '+13'
    wis: '+8'
    cha: '+13'
  skills:
    insight: '+8'
    perception: '+14'
    persuasion: '+13'
    stealth: '+8'
  senses: blindsight 60 ft., darkvision 120 ft.
  languages: Common, Draconic
  cr: '17'
stats_meta: Huge dragon L/G
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Dragão Dourado Adulto
---

## Características


### Anfíbio

O dragão pode respirar ar e água.


### Resistência Lendária (3/Dia)

Se o dragão falhar em um teste de resistência, ele pode escolher ser bem-sucedido em vez disso.

## Ações


### Ataques Múltiplos

O dragão pode usar sua Presença Amedrontadora. Em seguida, ele faz três ataques: um com sua mordida e dois com suas garras.


### Mordida

mw 14 para atingir, alcance 10 pés, um alvo. {@h}19 (<span class="dice+" data-roll-notation="2d10+8">2d10 + 8</span>) de dano perfurante.


### Garra

mw 14 para atingir, alcance 5 pés, um alvo. {@h}15 (<span class="dice+" data-roll-notation="2d6+8">2d6 + 8</span>) de dano cortante.


### Cauda

mw 14 para atingir, alcance 15 pés, um alvo. {@h}17 (<span class="dice+" data-roll-notation="2d8+8">2d8 + 8</span>) de dano de concussão.


### Presença Amedrontadora

Cada criatura à escolha do dragão que esteja a até 120 pés do dragão e ciente dele deve ser bem-sucedida em um teste de resistência de Sabedoria CD 21 ou ficará amedrontada por 1 minuto. Uma criatura pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesma em caso de sucesso. Se o teste de resistência de uma criatura for bem-sucedido ou o efeito terminar para ela, a criatura fica imune à Presença Amedrontadora do dragão pelas próximas 24 horas.


### Armas de Sopro 5

O dragão usa uma das seguintes armas de sopro.

* {'type': 'item', 'name': 'Sopro de Fogo', 'entry': 'O dragão exala fogo em um cone de 60 pés. Cada criatura na área deve fazer um teste de resistência de Destreza CD 21, sofrendo 66 (<span class="dice+" data-roll-notation="12d10">12d10</span>) de dano de fogo em caso de falha no teste, ou metade do dano em caso de sucesso.'}

* {'type': 'item', 'name': 'Sopro Enfraquecedor', 'entry': 'O dragão exala gás em um cone de 60 pés. Cada criatura na área deve ser bem-sucedida em um teste de resistência de Força CD 21 ou terá desvantagem em jogadas de ataque baseadas em Força, testes de Força e testes de resistência de Força por 1 minuto. Uma criatura pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesma em caso de sucesso.'}


### Mudar Forma

O dragão se transforma magicamente em um humanoide ou em uma besta que tenha um Nível de Desafio não superior ao seu, ou de volta à sua forma verdadeira. Ele retorna à sua forma verdadeira se morrer. Qualquer equipamento que esteja vestindo ou carregando é absorvido ou usado pela nova forma (à escolha do dragão).

Na nova forma, o dragão mantém sua tendência, Pontos de Vida, Dados de Vida, capacidade de falar, proficiências, Resistência Lendária, ações de covil e valores de Inteligência, Sabedoria e Carisma, bem como esta ação. Suas estatísticas e capacidades, fora isso, são substituídas pelas da nova forma, exceto quaisquer características de classe ou ações lendárias dessa forma.

## Ações Lendárias


### Detectar

O dragão faz um teste de Sabedoria (Percepção).


### Ataque de Cauda

O dragão faz um ataque de cauda.


### Ataque de Asas (Custa 2 Ações)

O dragão bate suas asas. Cada criatura a até 10 pés do dragão deve ser bem-sucedida em um teste de resistência de Destreza CD 22 ou sofre 15 (<span class="dice+" data-roll-notation="2d6+8">2d6 + 8</span>) de dano de concussão e fica caída. O dragão pode então voar até metade do seu deslocamento de voo.
