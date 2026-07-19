---
title: Ankheg
type: monster
draft: false
weight: 10
tags:
- draft
- importado
- 5etools
visibility: gm
status: ready
source:
  provider: 5e.tools
  book: MM
  entity_type: monster
  entity_name: Ankheg
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: d571da270fdb9dcb
stats:
  ac: '14'
  hp: 39 (6d10 + 6)
  speed: walk 30 ft., burrow 10 ft.
  attributes:
    str: 17
    dex: 11
    con: 13
    int: 1
    wis: 13
    cha: 6
  saves: {}
  skills: {}
  senses: darkvision 60 ft., tremorsense 60 ft.
  languages: ''
  cr: '2'
stats_meta: Large monstrosity U
titulo_pt_br: Ankheg
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Ações

### Mordida

Ataque Corpo a Corpo com Arma: +5 para atingir, alcance 5 pés, um alvo. *Acerto:* 10 (<span class="dice+" data-roll-notation="2d6+3">2d6 + 3</span>) de dano cortante mais 3 (<span class="dice+" data-roll-notation="1d6">1d6</span>) de dano de ácido. Se o alvo for uma criatura Grande ou menor, ela fica agarrada (CD 13). Até este agarrão terminar, o ankheg pode morder apenas a criatura agarrada e tem vantagem nas jogadas de ataque para fazê-lo.

### Spray Ácido {@recharge}

O ankheg cospe ácido em uma linha de 30 pés de comprimento e 5 pés de largura, desde que não tenha nenhuma criatura agarrada. Cada criatura nessa linha deve ser bem-sucedida em um teste de resistência de Destreza CD 13, sofrendo 10 (<span class="dice+" data-roll-notation="3d6">3d6</span>) de dano de ácido em caso de falha no teste de resistência, ou metade desse dano em caso de sucesso.
