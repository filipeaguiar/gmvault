---
title: Gibbering Mouther
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
  entity_name: Gibbering Mouther
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: eca235fc87e81c2c
stats:
  ac: '9'
  hp: 67 (9d8 + 27)
  speed: walk 10 ft., swim 10 ft.
  attributes:
    str: 10
    dex: 8
    con: 16
    int: 3
    wis: 10
    cha: 6
  saves: {}
  skills: {}
  senses: darkvision 60 ft.
  languages: ''
  cr: '2'
stats_meta: Medium aberration N
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Balbuciante
---

## Características

### Chão Aberrante

O chão num raio de 3 metros ao redor do balbuciador é pastoso 3. Cada criatura que começa seu turno nessa área deve ser bem-sucedida em um teste de resistência de Força CD 10 ou terá seu deslocamento reduzido a 0 até o início do próximo turno dela.

### Balbucio

O balbuciador balbucia incoerentemente enquanto puder ver qualquer criatura e não estiver incapacitado. Cada criatura que começa seu turno a até 6 metros do balbuciador e pode ouvir o balbucio deve ser bem-sucedida em um teste de resistência de Sabedoria CD 10. Em caso de falha, a criatura não pode realizar reações até o início do próximo turno dela e rola um <span class="dice+" data-roll-notation="d8">d8</span> para determinar o que ela faz durante seu turno. Em um resultado 1 a 4, a criatura não faz nada. Em um resultado 5 ou 6, a criatura não realiza nem ação nem ação bônus e usa todo o seu movimento para se mover em uma direção determinada aleatoriamente. Em um resultado 7 ou 8, a criatura realiza um ataque corpo a corpo contra uma criatura determinada aleatoriamente dentro de seu alcance ou não faz nada se não puder realizar tal ataque.

## Ações

### Ataques Múltiplos

O balbuciador faz um ataque de mordida e, se puder, usa seu Cuspe Ofuscante.

### Mordida

Ataque Corpo a Corpo com Arma: +2 para atingir, alcance 1,5 m, uma criatura. {'@h'}17 (<span class="dice+" data-roll-notation="5d6">5d6</span>) de dano perfurante. Se o alvo for de tamanho Médio ou menor, ele deve ser bem-sucedido em um teste de resistência de Força CD 10 ou ficará caído. Se o alvo for morto por este dano, ele é absorvido pelo balbuciador.

### Cuspe Ofuscante 5

O balbuciador cospe um glóbulo químico em um ponto que possa ver a até 4,5 metros de si. O glóbulo explode em um clarão ofuscante de luz no impacto. Cada criatura a até 1,5 metro do clarão deve ser bem-sucedida em um teste de resistência de Destreza CD 13 ou ficará cega até o final do próximo turno do balbuciador.
