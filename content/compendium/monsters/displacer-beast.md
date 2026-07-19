---
title: Displacer Beast
params:
  kind: monster
draft: true
weight: 10
summary: Estou pronto para traduzir o rascunho importado do 5e.tools (MM). Por favor, forneça o texto a ser traduzido.
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
  entity_name: Displacer Beast
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 374ff851ddf2f9f7
stats:
  ac: '13'
  hp: 85 (10d10 + 30)
  speed: walk 40 ft.
  attributes:
    str: 18
    dex: 15
    con: 16
    int: 6
    wis: 12
    cha: 8
  saves: {}
  skills: {}
  senses: darkvision 60 ft.
  languages: ''
  cr: '3'
stats_meta: Large monstrosity L/E
titulo_pt_br: Besta Deslocadora
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Evitação
Se a fera deslocadora for submetida a um efeito que permita a ela fazer um teste de resistência para sofrer apenas metade do dano, em vez disso, ela não sofre dano se for bem-sucedida no teste de resistência, e sofre apenas metade do dano se falhar.

### Deslocamento
A fera deslocadora projeta uma ilusão mágica que a faz parecer estar próxima à sua localização real, fazendo com que as jogadas de ataque contra ela tenham desvantagem. Se for atingida por um ataque, esta característica é anulada até o final do seu próximo turno. Esta característica também é anulada enquanto a fera deslocadora estiver incapacitada ou tiver deslocamento 0.

## Ações

### Ataques Múltiplos
A fera deslocadora realiza dois ataques com seus tentáculos.

### Tentáculo
Ataque Corpo a Corpo com Arma: +6 para atingir, alcance 3 m, um alvo. {@h}7 (<span class="dice+" data-roll-notation="1d6+4">1d6 + 4</span>) de dano de concussão mais 3 (<span class="dice+" data-roll-notation="1d6">1d6</span>) de dano perfurante.
