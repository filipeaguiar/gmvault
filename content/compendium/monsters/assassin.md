---
title: Assassin
params:
  kind: monster
draft: false
weight: 10
summary: 'Percebi que você enviou apenas a nota técnica sobre o rascunho importado do 5e.tools (MM), mas não incluiu o texto que precisa ser traduzido e revisado editorialmente.


  Por favor, cole o conteúdo do rascunho para que eu possa realizar a tradução e a revisão editorial conforme solicitado. Assim que receber o texto, aplicarei:


  - As traduções obrigatórias da terminologia D&D 5e

  - A preservação rigorosa de Markdown, HTML, YAML, URLs, shortcodes, tabelas, números, dados e tokens ZXQ

  - A manutenção dos nomes próprios protegidos (como 5e.tools)

  - A eliminação de quaisquer saídas proibidas


  Aguardo o envio do material.'
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
  entity_name: Assassin
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 9509d5d3a05c6a57
stats:
  ac: '15'
  hp: 78 (12d8 + 24)
  speed: walk 30 ft.
  attributes:
    str: 11
    dex: 16
    con: 14
    int: 13
    wis: 11
    cha: 10
  saves:
    dex: '+6'
    int: '+4'
  skills:
    acrobatics: '+6'
    deception: '+3'
    perception: '+3'
    stealth: '+9'
  senses: ''
  languages: Thieves' cant plus any two languages
  cr: '8'
stats_meta: Medium humanoid L/NX/C/NY/E
titulo_pt_br: Assassino
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Assassinar

Durante seu primeiro turno, o assassino tem Vantagem nas jogadas de ataque contra qualquer criatura que ainda não tenha agido. Qualquer acerto que o assassino fizer contra uma criatura surpresa é um acerto crítico.

### Evasão

Se o assassino for alvo de um efeito que permita que ele faça um teste de resistência de Destreza para sofrer apenas metade do dano, o assassino em vez disso não sofre dano se for bem-sucedido no teste de resistência e sofre apenas metade do dano se falhar.

### Ataque Furtivo (1/Turno)

O assassino causa um dano extra de 14 (<span class="dice+" data-roll-notation="4d6">4d6</span>) quando atinge um alvo com um ataque com arma e tem Vantagem na jogada de ataque, ou quando o alvo está a até 1,5 metro de um aliado do assassino que não esteja incapacitado e o assassino não tiver Desvantagem na jogada de ataque.

## Ações

### Ataques Múltiplos

O assassino faz dois ataques com espada curta.

### Espada Curta

corpo a corpo +6 para atingir, alcance de 1,5 metro, um alvo. {@h}6 (<span class="dice+" data-roll-notation="1d6+3">1d6 + 3</span>) de dano perfurante, e o alvo deve fazer um teste de resistência de Constituição CD 15, sofrendo 24 (<span class="dice+" data-roll-notation="7d6">7d6</span>) de dano de veneno em caso de falha no teste, ou metade desse dano em caso de sucesso.

### Besta Leve

à distância +6 para atingir, alcance de 24/96 metros, um alvo. {@h}7 (<span class="dice+" data-roll-notation="1d8+3">1d8 + 3</span>) de dano perfurante, e o alvo deve fazer um teste de resistência de Constituição CD 15, sofrendo 24 (<span class="dice+" data-roll-notation="7d6">7d6</span>) de dano de veneno em caso de falha no teste, ou metade desse dano em caso de sucesso.
