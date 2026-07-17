---
title: Tlexolotl
params:
  kind: monster
draft: true
weight: 10
summary: Conteúdo importado do 5e.tools (JTTRC) e traduzido automaticamente; requer revisão editorial.
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
  entity_name: Tlexolotl
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 61a6dde4c602817e
stats:
  ac: '15'
  hp: 104 (11d12 + 33)
  speed: walk 40 ft.
  attributes:
    str: 25
    dex: 10
    con: 17
    int: 7
    wis: 13
    cha: 9
  saves: {}
  skills: {}
  senses: darkvision 120 ft., tremorsense 120 ft.
  languages: Ignan
  cr: '10'
stats_meta: Huge elemental N
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Tlexolotl
---

## Características


### Aura de Fogo

No início de cada turno do tlexolotl, cada criatura a até 3 metros dele sofre 7 (<span class="dice+" data-roll-notation="2d6">2d6</span>) de dano de fogo, e objetos inflamáveis nessa aura que não estejam sendo vestidos ou carregados incendeiam. Uma criatura que toque o tlexolotl ou o atinja com um ataque corpo a corpo enquanto estiver a até 1,5 metro dele sofre 7 (<span class="dice+" data-roll-notation="2d6">2d6</span>) de dano de fogo.


### Iluminação

O tlexolotl emite luz intensa em um raio de 9 metros e penumbra por mais 9 metros.


### Regeneração

O tlexolotl recupera 10 pontos de vida no início de seu turno. Se o tlexolotl sofrer dano de frio ou for imerso em água, esta característica não funciona no início do próximo turno do tlexolotl. O tlexolotl morre somente se começar seu turno com 0 pontos de vida e não se regenerar.

## Ações


### Ataques Múltiplos

O tlexolotl realiza um ataque de Mordida e um ataque de Cauda.


### Mordida

mw 11 para atingir, alcance 3 m, um alvo. {@h}12 (<span class="dice+" data-roll-notation="1d10+7">1d10 + 7</span>) de dano perfurante mais 18 (<span class="dice+" data-roll-notation="4d8">4d8</span>) de dano de fogo.


### Cauda

mw 11 para atingir, alcance 3 m, um alvo. {@h}11 (<span class="dice+" data-roll-notation="1d8+7">1d8 + 7</span>) de dano de concussão mais 14 (<span class="dice+" data-roll-notation="4d6">4d6</span>) de dano de fogo. Se o alvo for uma criatura Grande ou menor, ela deve ser bem-sucedida em um teste de resistência de Força CD 19 ou será empurrada até 3 metros para longe do tlexolotl e ficará caída.


### Piroclasma (Recarga 5)

Jorros de lava derretida irrompem do corpo do tlexolotl. Cada criatura em uma esfera de 9 metros de raio centrada no tlexolotl deve fazer um teste de resistência de Destreza CD 15. Em caso de falha no teste de resistência, uma criatura sofre 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) de dano de fogo e 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) de dano de concussão. Em caso de sucesso no teste de resistência, uma criatura sofre metade do dano.
