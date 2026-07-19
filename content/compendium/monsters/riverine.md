---
title: Riverine
params:
  kind: monster
draft: false
weight: 10
summary: Rascunho importado do 5e.tools (JTTRC). Requer tradução e revisão editorial.
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
  entity_name: Riverine
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 061d06f1d868ea7a
stats:
  ac: '14'
  hp: 204 (24d10 + 72)
  speed: walk 30 ft., swim 60 ft.
  attributes:
    str: 20
    dex: 19
    con: 17
    int: 12
    wis: 16
    cha: 21
  saves:
    int: '+5'
    wis: '+7'
    cha: '+9'
  skills:
    insight: '+7'
    nature: '+5'
    perception: '+7'
  senses: blindsight 60 ft.
  languages: Aquan, Common, Sylvan
  cr: '12'
stats_meta: Large fey A
titulo_pt_br: Riverine
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Anfíbio

O riverino pode respirar ar e água.

### Resistência Lendária (3/Dia)

Se o riverino falhar em um teste de resistência, ele pode escolher obter sucesso em vez disso.

## Ações

### Ataques Múltiplos

O riverino realiza dois ataques de Golpe Inundante.

### Golpe Inundante

Ataque corpo a corpo com arma: +9 para atingir, alcance 3 m, um alvo. {@h}14 (<span class="dice+" data-roll-notation="2d8+5">2d8+5</span>) de dano de concussão mais 10 (<span class="dice+" data-roll-notation="3d6">3d6</span>) de dano de frio.

## Ações Bônus

### Passo do Redemoinho

O riverino se teletransporta magicamente para um espaço desocupado que possa ver a até 9 metros de si mesmo. Tanto o espaço que ele deixa quanto o seu destino devem estar dentro ou sobre a superfície da água.

## Ações Lendárias

### Ímpeto do Redemoinho

O riverino usa seu Passo do Redemoinho. Imediatamente após se teletransportar, cada criatura a até 1,5 m do espaço de destino do riverino sofre 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano de frio.

### Dilúvio Furioso (Custa 2 Ações)

O riverino libera uma torrente de água fluvial em uma linha de 9 m de comprimento e 1,5 m de largura. Cada criatura na área deve realizar um teste de resistência de Destreza CD 17. Em caso de falha no teste de resistência, a criatura sofre 11 (<span class="dice+" data-roll-notation="2d10">2d10</span>) de dano de concussão e fica caída. Em caso de sucesso no teste de resistência, a criatura sofre metade do dano e não fica caída.
