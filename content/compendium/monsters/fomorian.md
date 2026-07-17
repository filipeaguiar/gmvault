---
title: Fomorian
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
  entity_name: Fomorian
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 3851e00ac11df4e4
stats:
  ac: '14'
  hp: 149 (13d12 + 65)
  speed: walk 30 ft.
  attributes:
    str: 23
    dex: 10
    con: 20
    int: 9
    wis: 14
    cha: 6
  saves: {}
  skills:
    perception: '+8'
    stealth: '+3'
  senses: darkvision 120 ft.
  languages: Giant, Undercommon
  cr: '8'
stats_meta: Huge giant C/E
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Fomoriano
---

## Ações

### Ataques Múltiplos

O fomori ataca duas vezes com sua clava pesada ou faz um ataque com a clava pesada e usa Olho Maligno uma vez.

### Clava Pesada

+9 para acertar, alcance 4,5 m, um alvo. *Acerto:* 19 (<span class="dice+" data-roll-notation="3d8+6">3d8 + 6</span>) de dano de concussão.

### Olho Maligno

O fomori força magicamente uma criatura que ele possa ver a até 18 metros dele a realizar um teste de resistência de Carisma CD 14. A criatura sofre 27 (<span class="dice+" data-roll-notation="6d8">6d8</span>) de dano psíquico em caso de falha no teste de resistência, ou metade desse dano em caso de sucesso.

### Maldição do Olho Maligno (Recarrega após um Descanso Curto ou Longo)

Com um olhar, o fomori usa Olho Maligno mas, em caso de falha no teste de resistência, a criatura também é amaldiçoada com deformidades mágicas. Enquanto deformada, a criatura tem seu deslocamento reduzido à metade e sofre desvantagem em testes de atributo, testes de resistência e ataques baseados em Força ou Destreza.

A criatura transformada pode repetir o teste de resistência sempre que terminar um descanso longo, terminando o efeito em caso de sucesso.
