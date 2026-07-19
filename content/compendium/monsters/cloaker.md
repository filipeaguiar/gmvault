---
title: Cloaker
type: monster
draft: false
weight: 10
summary: Por favor, forneça o texto do rascunho importado do 5e.tools (Monster Manual) que você deseja que eu traduza e revise editorialmente. Estou pronto para processar o conteúdo assim que você compartilhá-lo.
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
  entity_name: Cloaker
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 994169514b0cfde4
stats:
  ac: '14'
  hp: 78 (12d10 + 12)
  speed: walk 10 ft., fly 40 ft.
  attributes:
    str: 17
    dex: 15
    con: 12
    int: 13
    wis: 12
    cha: 14
  saves: {}
  skills:
    stealth: '+5'
  senses: darkvision 60 ft.
  languages: Deep Speech, Undercommon
  cr: '8'
stats_meta: Large aberration C/N
titulo_pt_br: Manto Anímico
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Transferência de Dano
Enquanto estiver agarrado a uma criatura, o cloaker sofre apenas metade do dano causado a ele (arredondado para baixo) e essa criatura sofre a outra metade.

### Aparência Falsa
Enquanto o cloaker permanecer imóvel sem expor a parte inferior, ele é indistinguível de uma capa de couro escura.

### Sensibilidade à Luz
Enquanto estiver sob luz intensa, o cloaker tem desvantagem em jogadas de ataque e testes de Sabedoria (Percepção) que dependam da visão.

## Ações

### Ataques Múltiplos
O cloaker realiza dois ataques: um com sua mordida e um com sua cauda.

### Mordida
*Ataque Corpo a Corpo com Arma*: +6 para atingir, alcance 1,5 m, uma criatura. *Acerto*: 10 (2d6+3) de dano perfurante e, se o alvo for Grande ou menor, o cloaker se agarra a ele. Se o cloaker tiver vantagem contra o alvo, ele se agarra à cabeça do alvo, e o alvo fica cego e incapaz de respirar enquanto o cloaker estiver agarrado. Enquanto estiver agarrado, o cloaker pode realizar este ataque apenas contra o alvo e tem vantagem na jogada de ataque. O cloaker pode se soltar gastando 1,5 metro de seu deslocamento. Uma criatura, incluindo o alvo, pode usar sua ação para soltar o cloaker sendo bem-sucedida em um teste de Força CD 16.

### Cauda
*Ataque Corpo a Corpo com Arma*: +6 para atingir, alcance 3 m, uma criatura. *Acerto*: 7 (1d8+3) de dano cortante.

### Lamento
Cada criatura a até 18 metros do cloaker que possa ouvir seu lamento e que não seja uma aberração deve ser bem-sucedida em um teste de resistência de Sabedoria CD 13 ou ficará amedrontada até o final do próximo turno do cloaker. Se o teste de resistência de uma criatura for bem-sucedido, a criatura fica imune ao lamento do cloaker pelas próximas 24 horas.

### Fantasmas (Recarga após um Descanso Curto ou Longo)
O cloaker cria magicamente três duplicatas ilusórias de si mesmo se não estiver sob luz intensa. As duplicatas se movem com ele e imitam suas ações, mudando de posição para tornar impossível rastrear qual cloaker é o verdadeiro. Se o cloaker estiver em uma área de luz intensa, as duplicatas desaparecem.

Sempre que qualquer criatura escolher o cloaker como alvo de um ataque ou magia prejudicial enquanto uma duplicata permanecer, essa criatura rola aleatoriamente para determinar se escolhe como alvo o cloaker ou uma das duplicatas. Uma criatura não é afetada por esse efeito mágico se não puder ver ou se depender de sentidos que não a visão.

Uma duplicata tem a mesma Classe de Armadura do cloaker e usa os testes de resistência dele. Se um ataque atingir uma duplicata, ou se uma duplicata falhar em um teste de resistência contra um efeito que cause dano, a duplicata desaparece.
