---
title: Bakunawa
params:
  kind: monster
draft: false
weight: 10
summary: "```json\n{\n  \"monster\": [\n    {\n      \"name\": \"Marionetista Mecânico\",\n      \"isNpc\": false,\n      \"isNamedEntity\": false,\n      \"isUnique\": false,\n      \"source\": \"JTTRC\",\n      \"page\": 224,\n      \"otherSources\": [\n        {\n          \"source\": \"MCV4EC\"\n        }\n      ],\n      \"size\": [\n        \"M\"\n      ],\n      \"type\": {\n        \"type\": \"constructo\"\n      },\n      \"alignment\": [\n        \"L\",\n        \"M\"\n      ],\n      \"ac\": [\n        {\n          \"ac\": 19,\n          \"from\": [\n            \"armadura natural\"\n          ]\n        }\n      ],\n      \"hp\": {\n        \"average\": 161,\n        \"formula\": \"17d8 + 85\",\n        \"special\": \"reparos\"\n      },\n      \"speed\": {\n        \"walk\": 30,\n        \"climb\": 30\n      },\n      \"str\": 20,\n      \"dex\": 12,\n      \"con\": 20,\n      \"int\": 18,\n      \"wis\": 16,\n      \"cha\": 15,\n      \"save\": {\n        \"dex\": \"+6\",\n\
  \        \"int\": \"+9\",\n        \"wis\": \"+8\"\n      },\n      \"skill\": {\n        \"investigação\": \"+9\",\n        \"percepção\": \"+8\"\n      },\n      \"senses\": [\n        \"visão no escuro 18 m\"\n      ],\n      \"immune\": [\n        \"veneno\",\n        \"psíquico\"\n      ],\n      \"conditionImmune\": [\n        \"enfeitiçado\",\n        \"exaustão\",\n        \"amedrontado\",\n        \"paralisado\",\n        \"petrificado\",\n        \"envenenado\"\n      ],\n      \"languages\": [\n        \"Compreende os idiomas de seu criador mas não fala\"\n      ],\n      \"cr\": \"10\",\n      \"trait\": [\n        {\n          \"name\": \"Sensibilidade a Fios Mágicos\",\n          \"entries\": [\n            \"O marionetista pode sentir precisamente a localização de qualquer criatura que esteja tocando um fio mágico que ele controle (consulte a ação Fios Mágicos). Ele também pode sentir precisamente a localização de qualquer criatura tocada por um fio mágico que esteja conectado\
  \ a um aliado de seu criador.\"\n          ]\n        },\n        {\n          \"name\": \"Mente Mecânica\",\n          \"entries\": [\n            \"O marionetista está imune a qualquer efeito que detectaria suas emoções ou lesse seus pensamentos. Testes de Sabedoria (Intuição) para determinar as intenções ou sinceridade do marionetista são feitos com desvantagem.\"\n          ]\n        },\n        {\n          \"name\": \"Membros Sobressalentes\",\n          \"entries\": [\n            \"Se o marionetista estiver tocando três ou mais fios mágicos que ele controla, ele pode usar seus fios para empunhar até três armas, além de suas próprias mãos e outros membros. Cada arma adicional que ele empunhar pode ser usada para fazer um único ataque como uma ação bônus.\"\n          ]\n        },\n        {\n          \"name\": \"Incomum Natureza\",\n          \"entries\": [\n            \"O marionetista não precisa de ar, comida, água ou sono.\"\n          ]\n        }\n      ],\n      \"action\"\
  : [\n        {\n          \"name\": \"Ataque Múltiplo\",\n          \"entries\": [\n            \"O marionetista realiza três ataques com Lâminas Serrilhadas.\"\n          ]\n        },\n        {\n          \"name\": \"Lâmina Serrilhada\",\n          \"entries\": [\n            \"{atk mw} +9 para atingir, alcance 1,5 m, um alvo. {hit}12 (2d6 + 5) de dano cortante.\"\n          ]\n        }\n      ],\n      \"bonus\": [\n        {\n          \"name\": \"Fios Mágicos\",\n          \"entries\": [\n            \"O marionetista envia fios mágicos para tocar até três bestas, constructos, draconatos, humanoides ou monstruosidades voluntários que ele possa ver a até 18 metros de distância. Enquanto um alvo estiver tocando um fio, o marionetista pode usar uma ação bônus para ativar o fio e mover o alvo até 9 metros para um espaço desocupado. O alvo pode usar sua reação para tentar evitar ser movido, fazendo um teste de resistência de Destreza CD 17. Em um sucesso, o movimento do fio não o afeta,\
  \ e o fio se desprende do alvo. O efeito do fio também termina se o alvo começar seu turno a mais de 18 metros do marionetista ou se o marionetista usar esta ação bônusa novamente.\"\n          ]\n        },\n        {\n          \"name\": \"Reparos (3/Dia)\",\n          \"entries\": [\n            \"O marionetista toca um aliado constructo e passa pelo menos 1 minuto reparando o aliado. O aliado recupera 50 Pontos de Vida ou, se tiver 0 Pontos de Vida, deixa de ter 0 Pontos de Vida e recupera 25 Pontos de Vida.\"\n          ]\n        }\n      ],\n      \"traitTags\": [\n        \"Sensibilidade a Fios Mágicos\",\n        \"Mente Mecânica\",\n        \"Membros Sobressalentes\",\n        \"Incomum Natureza\"\n      ],\n      \"senseTags\": [\n        \"D\"\n      ],\n      \"actionTags\": [\n        \"Ataque Múltiplo\"\n      ],\n      \"languageTags\": [\n        \"CS\"\n      ],\n      \"damageTags\": [\n        \"S\"\n      ],\n      \"miscTags\": [\n        \"MW\"\n      ],\n      \"\
  hasToken\": true,\n      \"hasFluff\": true,\n      \"hasFluffImages\": true\n    }\n  ]\n}\n```"
tags:
- draft
- importado
- 5etools
visibility: gm
status: draft
source:
  provider: 5e.tools
  book: JTTRC
  entity_type: monster
  entity_name: Bakunawa
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 94bf1eab1bf4a20b
stats:
  ac: '15'
  hp: 150 (12d20 + 24)
  speed: walk 20 ft., fly 60 ft., swim 60 ft.
  attributes:
    str: 21
    dex: 12
    con: 15
    int: 14
    wis: 17
    cha: 16
  saves:
    dex: '+5'
    con: '+6'
    wis: '+7'
  skills: {}
  senses: blindsight 60 ft., darkvision 120 ft.
  languages: Celestial, Common, Draconic
  cr: '12'
stats_meta: Gargantuan dragon N
titulo_pt_br: Bakunawa
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Anfíbio

O bakunawa pode respirar ar e água.

### Resistência Lendária (3/Dia)

Se o bakunawa falhar em um teste de resistência, ele pode escolher ser bem-sucedido em vez disso.

## Ações

### Ataques Múltiplos

O bakunawa realiza um ataque de Mordida e um ataque de Pancada Tempestuosa.

### Mordida

mw 9 para atingir, alcance 3 m, um alvo. {@h}12 (<span class="dice+" data-roll-notation="2d6+5">2d6 + 5</span>) de dano perfurante mais 7 (<span class="dice+" data-roll-notation="2d6">2d6</span>) de dano elétrico. Se o alvo for uma criatura Grande ou menor, ele deve ser bem-sucedido em um teste de resistência de Força CD 17 ou será engolido pelo bakunawa. Uma criatura engolida fica cega e contida, e tem cobertura total contra ataques e outros efeitos fora do bakunawa. No início de cada um dos turnos do bakunawa, cada criatura engolida sofre 10 (<span class="dice+" data-roll-notation="3d6">3d6</span>) de dano elétrico.

A garganta do bakunawa pode conter até duas criaturas por vez. Se o bakunawa sofrer 30 de dano ou mais em um único turno de uma criatura engolida, ele deve ser bem-sucedido em um teste de resistência de Constituição CD 16 no final desse turno ou regurgitará todas as criaturas engolidas, que caem caídas em um espaço dentro de 4,5 metros do bakunawa. Se o bakunawa morrer, uma criatura engolida não estará mais contida por ele e poderá escapar do cadáver usando 4,5 metros de seu deslocamento, saindo caída.

### Pancada Tempestuosa

mw 9 para atingir, alcance 3 m, um alvo. {@h}9 (<span class="dice+" data-roll-notation="1d8+5">1d8 + 5</span>) de dano de concussão mais 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano trovejante, e o alvo é empurrado até 3 metros em uma direção horizontal para longe do bakunawa.

## Ações Lendárias

### Deslize Ágil

O bakunawa voa ou nada até metade de seu deslocamento. Este movimento não provoca ataques de oportunidade.

### Pancada

O bakunawa realiza um ataque de Pancada Tempestuosa.

### Relâmpagos (Custa 3 Ações)

O bakunawa lança raios em até duas criaturas que possa ver dentro de 18 metros de si. Cada alvo deve ser bem-sucedido em um teste de resistência de Destreza CD 15 ou sofrerá 22 (<span class="dice+" data-roll-notation="4d10">4d10</span>) de dano elétrico.
