---
title: Knight
type: monster
draft: false
weight: 10
summary: Rascunho importado do 5e.tools (MM). Requer tradução e revisão editorial.
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
  entity_name: Knight
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: c2b9dab93a7ee2c6
stats:
  ac: '18'
  hp: 52 (8d8 + 16)
  speed: walk 30 ft.
  attributes:
    str: 16
    dex: 11
    con: 14
    int: 11
    wis: 11
    cha: 15
  saves:
    con: '+4'
    wis: '+2'
  skills: {}
  senses: ''
  languages: any one language (usually Common)
  cr: '3'
stats_meta: Medium humanoid A
titulo_pt_br: Cavaleiro
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Corajoso

O cavaleiro tem vantagem em testes de resistência contra ser amedrontado.

## Ações

### Ataques Múltiplos

O cavaleiro faz dois ataques corpo a corpo.

### Montante

mw 5 para atingir, alcance 1,5 m, um alvo. {@h}10 (<span class="dice+" data-roll-notation="2d6+3">2d6 + 3</span>) de dano cortante.

### Besta Pesada

rw 2 para atingir, alcance 30/120 m, um alvo. {@h}5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano perfurante.

### Liderança (Recarrega após um Descanso Curto ou Longo)

Durante 1 minuto, o cavaleiro pode proferir um comando especial ou aviso sempre que uma criatura não hostil que ele possa ver a até 9 metros dele fizer uma jogada de ataque ou um teste de resistência. A criatura pode adicionar um <span class="dice+" data-roll-notation="d4">d4</span> à sua jogada, desde que possa ouvir e entender o cavaleiro. Uma criatura pode se beneficiar de apenas um dado de Liderança por vez. Este efeito termina se o cavaleiro estiver incapacitado.

## Reações

### Aparar

O cavaleiro adiciona 2 à sua Classe de Armadura contra um ataque corpo a corpo que o atingiria. Para fazê-lo, o cavaleiro precisa ver o atacante e estar empunhando uma arma corpo a corpo.
