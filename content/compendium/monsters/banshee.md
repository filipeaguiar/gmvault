---
title: Banshee
params:
  kind: monster
draft: false
weight: 10
summary: "{\n  \"name\": \"Chuul\",\n  \"source\": \"MM\",\n  \"page\": 0,\n  \"otherSources\": [],\n  \"size\": \"L\",\n  \"type\": \"aberração\",\n  \"tag\": \"nenhum\",\n  \"alignment\": [\n    \"C\",\n    \"M\"\n  ],\n  \"ac\": [\n    {\n      \"ac\": 16,\n      \"from\": [\n        \"armadura natural\"\n      ]\n    }\n  ],\n  \"hp\": {\n    \"average\": 93,\n    \"formula\": \"11d10 + 33\"\n  },\n  \"speed\": {\n    \"walk\": 30,\n    \"swim\": 30\n  },\n  \"str\": 19,\n  \"dex\": 10,\n  \"con\": 16,\n  \"int\": 5,\n  \"wis\": 11,\n  \"cha\": 5,\n  \"skill\": {\n    \"perception\": \"+4\"\n  },\n  \"senses\": [\n    \"visão no escuro 60 pés\"\n  ],\n  \"passive\": 14,\n  \"immune\": [\n    \"veneno\"\n  ],\n  \"conditionImmune\": [\n    \"envenenado\"\n  ],\n  \"languages\": [\n    \"entende o idioma das profundezas, mas não fala\"\n  ],\n  \"cr\": \"4\",\n  \"trait\": [\n    {\n      \"name\": \"Anfíbio\",\n      \"entries\": [\n        \"O chuul pode respirar ar e água.\"\n     \
  \ ]\n    },\n    {\n      \"name\": \"Sentir Magia\",\n      \"entries\": [\n        \"O chuul sente a presença de magia a até 120 pés de distância. Este traço não funciona enquanto o chuul estiver com a\n        {@condition incapacitated\n        }.\"\n      ]\n    }\n  ],\n  \"action\": [\n    {\n      \"name\": \"Multiataque\",\n      \"entries\": [\n        \"O chuul realiza dois ataques de pinça. Ele pode usar Agarrar no lugar de um ataque de pinça. Se ele tiver uma\n        criatura agarrada, ele também pode usar o Tentáculos Degustadores uma vez.\"\n      ]\n    },\n    {\n      \"name\": \"Pinças\",\n      \"entries\": [\n        \"{@atk mw} {@hit 6} para atingir, alcance 10 pés, um alvo. {@h}{@damage 11 (2d6 + 4)} de dano contundente. Se o alvo\n        for uma criatura Grande ou menor, ela é {@condition grappled\n        } (CD 14 para escapar). Enquanto estiver agarrada, a criatura sofre a condição\n        {@condition restrained\n        }. O chuul tem duas pinças, cada uma\
  \ podendo agarrar uma criatura.\"\n      ]\n    },\n    {\n      \"name\": \"Agarrar\",\n      \"entries\": [\n        \"Uma criatura Grande ou menor que o chuul possa ver em um raio de 5 pés deve ser bem-sucedida em um teste de\n        resistência de Força CD 14 ou sofrerá a condição {@condition grappled\n        } (CD 14 para escapar). Enquanto estiver agarrada, a criatura sofre a condição\n        {@condition restrained\n        }.\"\n      ]\n    },\n    {\n      \"name\": \"Tentáculos Degustadores\",\n      \"entries\": [\n        \"Uma criatura {@condition grappled\n        } pelo chuul deve fazer um teste de resistência de Constituição CD 13. Se falhar, a criatura sofre a condição\n        {@condition poisoned\n        } por 1 minuto. Se o teste de resistência falhar por 5 ou mais, a criatura também sofre a condição\n        {@condition paralyzed\n        } enquanto estiver {@condition poisoned\n        } dessa forma. Uma criatura {@condition poisoned\n        } pode repetir o\
  \ teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesma em\n        caso de sucesso.\"\n      ]\n    }\n  ],\n  \"traitTags\": [\n    \"Anfíbio\",\n    \"Sentir Magia\"\n  ],\n  \"senseTags\": [\n    \"SD\"\n  ],\n  \"actionTags\": [\n    \"Multiataque\"\n  ],\n  \"damageTags\": [\n    \"B\"\n  ],\n  \"conditionInflict\": [\n    \"Agarrado\",\n    \"Paralisado\",\n    \"Envenenado\",\n    \"Contido\"\n  ],\n  \"miscTags\": [\n    \"MW\",\n    \"ALC\"\n  ],\n  \"hasToken\": true,\n  \"legendaryGroup\": {},\n  \"hasFluff\": true,\n  \"hasFluffImages\": true,\n  \"alias\": [\n    \"Chuul\"\n  ],\n  \"markdown\": \"\\n> ## Chuul\\n> *Aberração Grande, Caótico e Maligno*\\n> \\n> ---\\n> \\n> - **Classe de Armadura** 16 (armadura natural)\\n> - **Pontos de Vida** 93 (11d10 + 33)\\n> - **Deslocamento** 30 pés, natação 30 pés\\n> \\n> ---\\n> \\n> |FOR|DES|CON|INT|SAB|CAR|\\n> |:---:|:---:|:---:|:---:|:---:|:---:|\\n> |19 (+4)|10 (+0)|16 (+3)|5 (-3)|11 (+0)|5\
  \ (-3)|\\n> \\n> ---\\n> \\n> - **Perícias** Percepção +4\\n> - **Sentidos** visão no escuro 60 pés, Percepção passiva 14\\n> - **Imunidade a dano** veneno\\n> - **Imunidades a condições** envenenado\\n> - **Idiomas** entende o idioma das profundezas, mas não fala\\n> - **Nível de Desafio** 4 (1.100 XP) *Bônus de Proficiência* +2\\n> \\n> ---\\n> \\n> ***Anfíbio.*** O chuul pode respirar ar e água.\\n> \\n> ***Sentir Magia.*** O chuul sente a presença de magia a até 120 pés de distância. Este traço não funciona enquanto o chuul estiver com a condição {@condition incapacitated}.\\n> \\n> ### Ações\\n> \\n> ***Multiataque.*** O chuul realiza dois ataques de pinça. Ele pode usar Agarrar no lugar de um ataque de pinça. Se ele tiver uma criatura agarrada, ele também pode usar o Tentáculos Degustadores uma vez.\\n> \\n> ***Pinças.*** *Ataque Corpo a Corpo com Arma:* +6 para atingir, alcance 10 pés, um alvo. *Dano:* 11 (2d6 + 4) de dano contundente. Se o alvo for uma criatura Grande ou menor,\
  \ ela é agarrada (CD 14 para escapar). Enquanto estiver agarrada, a criatura sofre a condição contida. O chuul tem duas pinças, cada uma podendo agarrar uma criatura.\\n> \\n> ***Agarrar.*** Uma criatura Grande ou menor que o chuul possa ver em um raio de 5 pés deve ser bem-sucedida em um teste de resistência de Força CD 14 ou sofrerá a condição agarrada (CD 14 para escapar). Enquanto estiver agarrada, a criatura sofre a condição contida.\\n> \\n> ***Tentáculos Degustadores.*** Uma criatura agarrada pelo chuul deve fazer um teste de resistência de Constituição CD 13. Se falhar, a criatura sofre a condição envenenada por 1 minuto. Se o teste de resistência falhar por 5 ou mais, a criatura também sofre a condição paralisada enquanto estiver envenenada dessa forma. Uma criatura envenenada pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesma em caso de sucesso.\\n\"\n}"
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
  entity_name: Banshee
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: b8dfb039ce1ca46f
stats:
  ac: '12'
  hp: 58 (13d8)
  speed: walk 0 ft., fly 40 ft.
  attributes:
    str: 1
    dex: 14
    con: 10
    int: 12
    wis: 11
    cha: 17
  saves:
    wis: '+2'
    cha: '+5'
  skills: {}
  senses: darkvision 60 ft.
  languages: Common, Elvish
  cr: '4'
stats_meta: Medium undead C/E
titulo_pt_br: Banshee
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Detectar Vida

A banshee pode sentir magicamente a presença de criaturas vivas a até 8 quilômetros de distância que não sejam mortos-vivos ou constructos. Ela sabe a direção geral em que estão, mas não suas localizações exatas.

### Movimento Incorpóreo

A banshee pode se mover através de outras criaturas e objetos como se fossem 3. Ela sofre 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano de energia se terminar seu turno dentro de um objeto.

## Ações

### Toque Corruptor

Ataque Corpo a Corpo com Magia: +4 para atingir, alcance 1,5 m, um alvo. {@h}12 (<span class="dice+" data-roll-notation="3d6+2">3d6 + 2</span>) de dano necrótico.

### Rosto Horripilante

Cada criatura que não seja morto-vivo a até 18 metros da banshee que possa vê-la deve ser bem-sucedida em um teste de resistência de Sabedoria CD 13 ou ficará amedrontada por 1 minuto. Um alvo amedrontado pode repetir o teste de resistência no final de cada um de seus turnos, com desvantagem se a banshee estiver dentro da linha de visão, terminando o efeito sobre si mesmo em caso de sucesso. Se o teste de resistência de um alvo for bem-sucedido ou o efeito terminar para ele, o alvo fica imune ao Rosto Horripilante da banshee pelas próximas 24 horas.

### Lamento (1/Dia)

A banshee libera um lamento pesaroso, desde que não esteja sob luz solar. Este lamento não tem efeito sobre constructos e mortos-vivos. Todas as outras criaturas a até 9 metros dela que possam ouvi-la devem realizar um teste de resistência de Constituição CD 13. Em caso de falha, uma criatura tem seus pontos de vida reduzidos a 0. Em caso de sucesso, uma criatura sofre 10 (<span class="dice+" data-roll-notation="3d6">3d6</span>) de dano psíquico.
