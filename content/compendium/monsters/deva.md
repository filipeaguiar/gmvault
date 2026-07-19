---
title: Deva
params:
  kind: monster
draft: false
weight: 10
summary: "```yaml\nname: Enviado Mercenário\nisNpc: true\nhasToken: true\nisNamedCreature: false\nsource: MM\npage: 218\nsize:\n  - M\n  - S\ntype:\n  - humanoide\n  - elfo\n  - qualquer espécie\nalignment:\n  - L\n  - N\n  - E\nac:\n  - from:\n      - armadura de couro batido\n    ac: 15\nhp:\n  average: 44\n  formula: 8d8 + 8\nspeed:\n  walk: 30\nstr: 11\ndex: 14\ncon: 12\nint: 14\nwis: 12\ncha: 16\nskill:\n  deception: +7\n  investigation: +4\n  perception: +4\n  persuasion: +7\nsenses:\n  darkvision: 60\nlanguages:\n  - Comum\n  - Dracônico\n  - Élfico\n  - qualquer outro idioma\ncr: \"4\"\ntrait:\n  - name: Metamagia\n    entries:\n      - O enviado possui três opções de Metamagia da classe de Feiticeiro, que pode usar com um bônus de +3 em testes de Carisma para usá-las. O enviado tem 3 Pontos de Feitiçaria para usar com Metamagia. O máximo de Pontos de Feitiçaria que pode gastar em uma opção é 3. Ele recupera os Pontos de Feitiçaria gastos quando termina um Descanso Longo.\n  - name:\
  \ Conjuração\n    entries:\n      - O enviado conjura uma das seguintes magias, usando Carisma como a habilidade de conjuração (CD do teste de resistência de magia {@dc 14}):|O enviado conjura uma das seguintes magias, usando Carisma como a habilidade de conjuração:\n      - à vontade: {@spell detect magic}, {@spell light}, {@spell mage hand}, {@spell message}, {@spell prestidigitation}\n      - 1/dia cada: {@spell charm person}, {@spell invisibility} (apenas em si mesmo), {@spell suggestion}\naction:\n  - name: Multiataque\n    entries:\n      - O enviado realiza dois ataques de Raio Radiante e usa Presença Ameaçadora ou Teleporte.\n  - name: Raio Radiante\n    entries:\n      - \"{@atk mw,rw} {@hit +5} para atingir, alcance 60 pés, um alvo. {@h}{@dice 2d8 + 3} de dano Radiante.\"\n  - name: Presença Ameaçadora\n    entries:\n      - O enviado escolhe uma criatura que possa ver em um raio de 30 pés. O alvo deve fazer um teste de resistência de Sabedoria CD {@dc 14}. Se falhar, o alvo\
  \ fica na condição {@condition frightened} até o final do próximo turno do enviado.\n  - name: Teleporte\n    entries:\n      - O enviado teleporta-se até 30 pés para um espaço desocupado que possa ver, desde que o espaço esteja iluminado ou na escuridão. O enviado pode transportar uma criatura voluntária de tamanho Médio ou menor que esteja tocando. A criatura é teleportada para um espaço a até 5 pés do espaço de destino do enviado.\nreaction:\n  - name: Proteção Mágica (Recarga 6)\n    entries:\n      - Quando o enviado ou outra criatura a até 5 pés dele é atingida por uma jogada de ataque, o enviado concede um bônus de +3 na CA do alvo contra aquele ataque, podendo fazer com que ele erre.\ntraitTags:\n  - Metamagic\n  - Spellcasting\nsenseTags:\n  - D\nlanguageTags:\n  - C\n  - DR\n  - E\n  - X\ndamageTags: []\nmiscTags:\n  - arcane\n  - humanoid\n```"
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
  entity_name: Deva
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 574bfc4bd5d920f2
stats:
  ac: '17'
  hp: 136 (16d8 + 64)
  speed: walk 30 ft., fly 90 ft.
  attributes:
    str: 18
    dex: 18
    con: 18
    int: 17
    wis: 20
    cha: 20
  saves:
    wis: '+9'
    cha: '+9'
  skills:
    insight: '+9'
    perception: '+9'
  senses: darkvision 120 ft.
  languages: all, telepathy 120 ft.
  cr: '10'
stats_meta: Medium celestial L/G
titulo_pt_br: Deva
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Armas Angelicais

Os ataques com arma do deva são mágicos. Quando o deva atinge com qualquer arma, ela causa um adicional de <span class="dice+" data-roll-notation="4d8">4d8</span> de dano radiante (incluído no ataque).


### Resistência à Magia

O deva tem vantagem em testes de resistência contra magias e outros efeitos mágicos.

## Ações


### Ataques Múltiplos

O deva realiza dois ataques corpo a corpo.


### Maça

mw 8 para atingir, alcance 1,5 m, um alvo. {@h}7 (<span class="dice+" data-roll-notation="1d6+4">1d6 + 4</span>) de dano de concussão mais 18 (<span class="dice+" data-roll-notation="4d8">4d8</span>) de dano radiante.


### Toque Curativo (3/Dia)

O deva toca outra criatura. O alvo recupera magicamente 20 (<span class="dice+" data-roll-notation="4d8+2">4d8 + 2</span>) pontos de vida e é libertado de qualquer maldição, doença, veneno, cegueira ou surdez.


### Mudar de Forma

O deva se transforma magicamente em um humanoide ou besta que tenha um nível de desafio igual ou inferior ao seu, ou de volta à sua forma verdadeira. Ele reverte à sua forma verdadeira se morrer. Qualquer equipamento que esteja vestindo ou carregando é absorvido ou usado pela nova forma (escolha do deva).

Em uma nova forma, o deva mantém suas estatísticas de jogo e capacidade de falar, mas sua CA, modos de deslocamento, Força, Destreza e sentidos especiais são substituídos pelos da nova forma, e ele ganha quaisquer estatísticas e capacidades (exceto características de classe, ações lendárias e ações de covil) que a nova forma possua, mas que ele não tenha.
