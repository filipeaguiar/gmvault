---
title: Roper
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
  entity_name: Roper
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 4245a0198f6b0ac8
stats:
  ac: '20'
  hp: 93 (11d10 + 33)
  speed: walk 10 ft., climb 10 ft.
  attributes:
    str: 18
    dex: 8
    con: 17
    int: 7
    wis: 16
    cha: 6
  saves: {}
  skills:
    perception: '+6'
    stealth: '+5'
  senses: darkvision 60 ft.
  languages: ''
  cr: '5'
stats_meta: Large monstrosity N/E
titulo_pt_br: Estrangulador
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Aparência Falsa
Enquanto o roper permanece imóvel, ele é indistinguível de uma formação rochosa comum de caverna, como uma estalagmite.

### Tentáculos Preensores
O roper pode ter até seis tentáculos de cada vez. Cada tentáculo pode ser atacado (CA 20; 10 pontos de vida; imunidade a dano de veneno e dano psíquico). Destruir um tentáculo não causa dano ao roper, que pode projetar um tentáculo substituto no próximo turno dele. Um tentáculo também pode ser quebrado se uma criatura usar uma ação e obtiver sucesso em um teste de Força CD 15 contra ele.

### Escalada de Aranha
O roper pode escalar superfícies difíceis, incluindo de cabeça para baixo no teto, sem precisar fazer um teste de atributo.

## Ações

### Ataques Múltiplos
O roper realiza quatro ataques com seus tentáculos, usa Enrolar e realiza um ataque com sua mordida.

### Mordida
mw 7 para acertar, alcance 1,5 m, um alvo. {@h}22 (4d8 + 4) de dano perfurante.

### Tentáculo
mw 7 para acertar, alcance 15 m, uma criatura. {@h}O alvo fica agarrado (CD para escapar 15). Até o agarrão terminar, o alvo estará contido e terá desvantagem em testes de Força e testes de resistência de Força, e o roper não poderá usar o mesmo tentáculo em outro alvo.

### Enrolar
O roper puxa cada criatura agarrada por ele até 7,5 m diretamente para si.
