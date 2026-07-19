---
title: Aurumvorax
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
  entity_name: Aurumvorax
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 130aa656026d549e
stats:
  ac: '15'
  hp: 36 (8d6 + 8)
  speed: walk 30 ft., burrow 20 ft.
  attributes:
    str: 14
    dex: 13
    con: 12
    int: 3
    wis: 12
    cha: 6
  saves:
    str: '+4'
    con: '+3'
  skills:
    perception: '+3'
    stealth: '+3'
  senses: darkvision 60 ft.
  languages: ''
  cr: '2'
stats_meta: Small monstrosity U
titulo_pt_br: Aurumvorax
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Escavador
O aurumvorax pode escavar através de rocha sólida e metal com metade do seu deslocamento de escavação e deixa um túnel de 5 pés de diâmetro em seu rastro.

## Ações

### Ataques Múltiplos
O aurumvorax realiza um ataque de Mordida e dois ataques de Garra.

### Mordida
mw 4 para atingir, alcance 5 pés, um alvo. {@h}6 (<span class="dice+" data-roll-notation="1d8+2">1d8 + 2</span>) de dano perfurante. Se o alvo for uma criatura usando qualquer tipo de armadura, o aurumvorax recupera 4 (<span class="dice+" data-roll-notation="1d6+1">1d6 + 1</span>) pontos de vida.

### Garra
mw 5 para atingir, alcance 5 pés, um alvo. {@h}5 (<span class="dice+" data-roll-notation="1d6+2">1d6 + 2</span>) de dano cortante. Se o alvo for uma criatura Média ou menor, ela fica agarrada (escapar 12). Até esse agarrão terminar, o aurumvorax não pode usar seu ataque de Garra contra outro alvo e, quando se move, pode arrastar a criatura agarrada consigo, sem que seu deslocamento seja reduzido à metade.
