---
title: Ankheg
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
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Anquegue
---

## Ações

### Mordida

Ataque Corpo a Corpo com Arma: +5 para atingir, alcance 1,5 m, um alvo. *Acerto:* 10 (2d6 + 3) de dano cortante mais 3 (1d6) de dano de ácido. Se o alvo for uma criatura Grande ou menor, ela fica agarrada (CD 13 para escapar). Até esse agarrão terminar, o ankheg só pode morder a criatura agarrada e tem Vantagem nas jogadas de ataque para fazê-lo.

### Borrifo Ácido (Recarga 6)

O ankheg cospe ácido em uma linha de 9 metros de comprimento e 1,5 metro de largura, desde que não tenha nenhuma criatura agarrada. Cada criatura nessa linha deve realizar um teste de resistência de Destreza CD 13, sofrendo 10 (3d6) de dano de ácido em caso de falha, ou metade desse dano em caso de sucesso.
