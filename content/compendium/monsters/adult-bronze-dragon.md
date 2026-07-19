---
title: Adult Bronze Dragon
params:
  kind: monster
draft: false
weight: 10
summary: "```json\n{\n\t\"name\": \"Garra Rastejante\",\n\t\"isNpc\": false,\n\t\"isNamedCreature\": false,\n\t\"source\": \"MM\",\n\t\"page\": 71,\n\t\"basicRules\": true,\n\t\"otherSources\": [\n\t\t{\n\t\t\t\"source\": \"PaBTSO\"\n\t\t},\n\t\t{\n\t\t\t\"source\": \"SatO\"\n\t\t},\n\t\t{\n\t\t\t\"source\": \"ToFW\"\n\t\t}\n\t],\n\t\"subtitle\": \"Pequeno Constructo, Neutro e Maligno\",\n\t\"size\": [\n\t\t\"P\"\n\t],\n\t\"type\": {\n\t\t\"type\": \"constructo\",\n\t\t\"tags\": [\n\t\t\t\"Garra Rastejante\"\n\t\t]\n\t},\n\t\"alignment\": [\n\t\t\"N\",\n\t\t\"M\"\n\t],\n\t\"ac\": [\n\t\t{\n\t\t\t\"ac\": 12,\n\t\t\t\"from\": [\n\t\t\t\t\"armadura natural\"\n\t\t\t]\n\t\t}\n\t],\n\t\"hp\": {\n\t\t\"formula\": \"2d4 - 2\",\n\t\t\"average\": 2\n\t},\n\t\"speed\": {\n\t\t\"walk\": 20,\n\t\t\"climb\": 20\n\t},\n\t\"str\": 13,\n\t\"dex\": 14,\n\t\"con\": 9,\n\t\"int\": 5,\n\t\"wis\": 10,\n\t\"cha\": 4,\n\t\"conditionImmune\": [\n\t\t\"enfeitiçado\",\n\t\t\"exaustão\",\n\t\t\"envenenado\"\n\t],\n\
  \t\"senses\": [\n\t\t\"visão às cegas 30 ft. (cego além desse raio)\"\n\t],\n\t\"passive\": 10,\n\t\"languages\": [\n\t\t\"compreende o Comum mas não pode falar\"\n\t],\n\t\"cr\": \"0\",\n\t\"trait\": [\n\t\t{\n\t\t\t\"name\": \"Sensibilidade à Luz Solar\",\n\t\t\t\"entries\": [\n\t\t\t\t\"A garra moribunda sofre desvantagem em jogadas de ataque e testes de Sabedoria (Percepção) que dependam da visão enquanto estiver sob luz solar direta.\"\n\t\t\t]\n\t\t},\n\t\t{\n\t\t\t\"name\": \"Vínculo com a Fonte\",\n\t\t\t\"entries\": [\n\t\t\t\t\"A garra rastejante tem um vínculo telepático com seu mestre. Enquanto a garra estiver dentro de 1,6 km de seu mestre, ela pode transmitir o que sente. O mestre pode comandar a garra como uma ação bônus.\"\n\t\t\t]\n\t\t}\n\t],\n\t\"action\": [\n\t\t{\n\t\t\t\"name\": \"Garra\",\n\t\t\t\"entries\": [\n\t\t\t\t\"{atk m} +3 para atingir, alcance 5 ft., um alvo. {hit}3 ({@dice 1d4 + 1}) de dano por esmagamento ou por contusão (à escolha do mestre).\"\n\t\t\
  \t]\n\t\t}\n\t],\n\t\"traitTags\": [\n\t\t\"Sunlight Sensitivity\"\n\t],\n\t\"senseTags\": [\n\t\t\"B\"\n\t],\n\t\"actionTags\": [\n\t\t\"Claw\"\n\t],\n\t\"miscTags\": [\n\t\t\"MW\",\n\t\t\"AOE\"\n\t],\n\t\"hasToken\": true,\n\t\"hasFluff\": true,\n\t\"hasFluffImages\": true,\n\t\"isCopyStart\": true,\n\t\"isCopyEnd\": true,\n\t\"fluff\": {\n\t\t\"name\": \"Garra Rastejante\",\n\t\t\"source\": \"MM\",\n\t\t\"entries\": [\n\t\t\t{\n\t\t\t\t\"type\": \"entries\",\n\t\t\t\t\"name\": \"GARRA RASTEJANTE ENCAPUZADA\",\n\t\t\t\t\"entries\": [\n\t\t\t\t\t\"Alguns necromantes cobrem suas garras rastejantes com uma mortalha de pano. A mortalha de cor escura envolve uma figura humanoide, criando um disfarce convincente. Um observador não pode ver o rosto escondido sob o capuz, que tem apenas dois pequenos olhos vermelhos brilhantes que denunciam a natureza sobrenatural de uma garra rastejante encapuzada.\"\n\t\t\t\t]\n\t\t\t},\n\t\t\t{\n\t\t\t\t\"type\": \"image\",\n\t\t\t\t\"href\": {\n\t\t\t\t\t\
  \"type\": \"internal\",\n\t\t\t\t\t\"path\": \"bestiary/MM/Hooded Crawling Claw.webp\"\n\t\t\t\t},\n\t\t\t\t\"title\": \"Uma Garra Rastejante Encapuçada\",\n\t\t\t\t\"width\": 556,\n\t\t\t\t\"height\": 639\n\t\t\t},\n\t\t\t{\n\t\t\t\t\"type\": \"entries\",\n\t\t\t\t\"entries\": [\n\t\t\t\t\t\"As garras rastejantes são as mãos decepadas de assassinos, animadas por magia negra para que possam continuar sua obra assassina. Um necromante ritualisticamente prepara uma mão cortada, mergulhando-a em uma mistura de óleos e incrustando unhas afiadas com runas. O ritual conclui com um feitiço de {@spell animate dead}, mas o poder do feitiço é canalizado através do necromante e convoca para a mão cortada o espírito vingativo do assassino que a empunhava. A pessoa pode ser um assassino contratado, um serial killer ou até mesmo um trabalhador comum com desejo de matar. Se o espírito estiver disposto ou for forçado a retornar, as garras rastejantes resultantes são leais ao necromante e seguem suas ordens.\"\
  ,\n\t\t\t\t\t\"As garras rastejantes são assassinos engenhosos. Elas podem escalar superfícies verticais, se esgueirar por fendas e surpreender suas vítimas. Elas cumprem suas ordens sem medo de morrer, atacando com força terrível. Elas podem atacar com suas unhas e estrangular suas vítimas com força implacável, ou agarrar armas e brandi-las. Embora uma garra não possua a inteligência de seu espírito ligado, ela ainda possui uma porção de sua malícia e tendências violentas. Deixada por conta própria, ela pode tentar enganar seu mestre ou encontrar maneiras de satisfazer seus desejos homicidas perturbados.\",\n\t\t\t\t\t\"Garras rastejantes podem agir em nome de seus mestres, comumente encontradas em companhia de uma variedade de criaturas mortas-vivas. Muitos necromantes usam suas garras como espiões ou assassinos, enviando-as para se infiltrar em acampamentos ou escalar muros para eliminar inimigos enquanto dormem. Alguns vilões astutos amarram mortalhas nelas para disfarçá-las como figuras\
  \ encapuzadas ou as empregam em conjunto com criaturas ilusórias para confundir aventureiros incautos.\"\n\t\t\t\t]\n\t\t\t},\n\t\t\t{\n\t\t\t\t\"type\": \"image\",\n\t\t\t\t\"href\": {\n\t\t\t\t\t\"type\": \"internal\",\n\t\t\t\t\t\"path\": \"bestiary/MM/Crawling Claw.webp\"\n\t\t\t\t},\n\t\t\t\t\"title\": \"Uma Garra Rastejante\",\n\t\t\t\t\"width\": 748,\n\t\t\t\t\"height\": 692\n\t\t\t}\n\t\t]\n\t},\n\t\"copyright\": \"Tradução não oficial para português do conteúdo de SRD 5.1 ( CC-BY-4.0 ). Apoie os criadores, adquira o livro de regras oficial em inglês na Wizards of the Coast.\",\n\t\"environment\": [\n\t\t\"deserto\",\n\t\t\"floresta\",\n\t\t\"grama\",\n\t\t\"montanha\",\n\t\t\"pântano\",\n\t\t\"subterrâneo\",\n\t\t\"urbano\"\n\t]\n}\n```"
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
  entity_name: Adult Bronze Dragon
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: d8e41857ee60cd48
stats:
  ac: '19'
  hp: 212 (17d12 + 102)
  speed: walk 40 ft., fly 80 ft., swim 40 ft.
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
    insight: '+7'
    perception: '+12'
    stealth: '+5'
  senses: blindsight 60 ft., darkvision 120 ft.
  languages: Common, Draconic
  cr: '15'
stats_meta: Huge dragon L/G
titulo_pt_br: Dragão de Bronze Adulto
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Anfíbio

O dragão pode respirar ar e água.


### Resistência Lendária (3/Dia)

Se o dragão falhar em um teste de resistência, ele pode escolher ser bem-sucedido em vez disso.

## Ações


### Ataques Múltiplos

O dragão pode usar sua Presença Amedrontadora. Ele então realiza três ataques: um com sua mordida e dois com suas garras.


### Mordida

mw 12 para atingir, alcance 3 m, um alvo. {@h}18 (<span class="dice+" data-roll-notation="2d10+7">2d10 + 7</span>) de dano perfurante.


### Garra

mw 12 para atingir, alcance 1,5 m, um alvo. {@h}14 (<span class="dice+" data-roll-notation="2d6+7">2d6 + 7</span>) de dano cortante.


### Cauda

mw 12 para atingir, alcance 4,5 m, um alvo. {@h}16 (<span class="dice+" data-roll-notation="2d8+7">2d8 + 7</span>) de dano de concussão.


### Presença Amedrontadora

Cada criatura da escolha do dragão que esteja a até 36 metros do dragão e consciente dele deve ser bem-sucedida em um teste de resistência de Sabedoria CD 17 ou ficará amedrontada por 1 minuto. Uma criatura pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesma em caso de sucesso. Se o teste de resistência de uma criatura for bem-sucedido ou o efeito terminar para ela, a criatura fica imune à Presença Amedrontadora do dragão pelas próximas 24 horas.


### Armas de Sopro 5

O dragão usa uma das seguintes armas de sopro.

* {'type': 'item', 'name': 'Sopro Elétrico', 'entry': 'O dragão exala eletricidade em uma linha de 27 metros de comprimento e 1,5 metro de largura. Cada criatura nessa linha deve realizar um teste de resistência de Destreza CD 19, sofrendo 66 (<span class="dice+" data-roll-notation="12d10">12d10</span>) de dano elétrico em caso de falha no teste, ou metade desse dano em caso de sucesso.'}

* {'type': 'item', 'name': 'Sopro de Repulsão', 'entry': 'O dragão exala energia de repulsão em um cone de 9 metros. Cada criatura nessa área deve ser bem-sucedida em um teste de resistência de Força CD 19. Em caso de falha no teste, a criatura é empurrada 18 metros para longe do dragão.'}


### Mudar Forma

O dragão se transforma magicamente em um humanoide ou besta que tenha um Nível de Desafio não superior ao seu próprio, ou de volta à sua forma verdadeira. Ele reverte à sua forma verdadeira se morrer. Qualquer equipamento que esteja vestindo ou carregando é absorvido ou carregado pela nova forma (à escolha do dragão).

Em uma nova forma, o dragão mantém sua tendência, Pontos de Vida, Dados de Vida, capacidade de falar, proficiências, Resistência Lendária, ações de covil e valores de Inteligência, Sabedoria e Carisma, bem como esta ação. Suas estatísticas e capacidades são, de outra forma, substituídas pelas da nova forma, exceto quaisquer características de classe ou ações lendárias dessa forma.

## Ações Lendárias


### Detectar

O dragão realiza um teste de Sabedoria (Percepção).


### Ataque de Cauda

O dragão realiza um ataque de cauda.


### Ataque de Asas (Custa 2 Ações)

O dragão bate suas asas. Cada criatura a até 3 metros do dragão deve ser bem-sucedida em um teste de resistência de Destreza CD 20 ou sofre 14 (<span class="dice+" data-roll-notation="2d6+7">2d6 + 7</span>) de dano de concussão e fica caída. O dragão pode então voar até metade de seu deslocamento de voo.
