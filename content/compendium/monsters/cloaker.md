---
title: Cloaker
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
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Manto Vivo
---

## Características

### Transferência de Dano

Enquanto está preso a uma criatura, o cloaker sofre apenas metade do dano causado a ele (arredondado para baixo), e aquela criatura sofre a outra metade.

### Aparência Falsa

Enquanto o cloaker permanece imóvel sem que sua parte inferior esteja exposta, ele é indistinguível de uma capa de couro escura.

### Sensibilidade à Luz

Enquanto estiver sob luz intensa, o cloaker tem desvantagem em jogadas de ataque e em testes de Sabedoria (Percepção) que dependam da visão.

## Ações

### Ataques Múltiplos

O cloaker realiza dois ataques: um com sua mordida e outro com sua cauda.

### Mordida

mw 6 para atingir, alcance 1,5 m, uma criatura. {@h}10 (<span class="dice+" data-roll-notation="2d6+3">2d6 + 3</span>) de dano perfurante e, se o alvo for Grande ou menor, o cloaker se prende a ele. Se o cloaker tiver vantagem contra o alvo, ele se prende à cabeça do alvo, e o alvo fica cego e incapaz de respirar enquanto o cloaker estiver preso. Enquanto está preso, o cloaker pode fazer este ataque apenas contra o alvo e tem vantagem na jogada de ataque. O cloaker pode se soltar gastando 1,5 metro de seu deslocamento. Uma criatura, incluindo o alvo, pode usar sua ação para soltar o cloaker sendo bem-sucedida em um teste de Força CD 16.

### Cauda

mw 6 para atingir, alcance 3 m, uma criatura. {@h}7 (<span class="dice+" data-roll-notation="1d8+3">1d8 + 3</span>) de dano cortante.

### Gemido

Cada criatura a até 18 metros do cloaker que possa ouvir seu gemido e que não seja uma aberração deve ser bem-sucedida em um teste de resistência de Sabedoria CD 13 ou ficará amedrontada até o final do próximo turno do cloaker. Se o teste de resistência de uma criatura for bem-sucedido, a criatura fica imune ao gemido do cloaker pelas próximas 24 horas.

### Fantasmagoria (Recarrega após um Descanso Curto ou Longo)

O cloaker cria magicamente três duplicatas ilusórias de si mesmo se não estiver sob luz intensa. As duplicatas se movem com ele e imitam suas ações, mudando de posição para tornar impossível rastrear qual cloaker é o verdadeiro. Se o cloaker estiver em uma área de luz intensa, as duplicatas desaparecem.

Sempre que qualquer criatura mirar o cloaker com um ataque ou uma magia prejudicial enquanto uma duplicata permanecer, essa criatura rola aleatoriamente para determinar se mira no cloaker ou em uma das duplicatas. Uma criatura não é afetada por este efeito mágico se não puder enxergar ou se depender de outros sentidos que não a visão.

Uma duplicata tem a mesma Classe de Armadura do cloaker e usa seus testes de resistência. Se um ataque atingir uma duplicata, ou se uma duplicata falhar em um teste de resistência contra um efeito que cause dano, a duplicata desaparece.
