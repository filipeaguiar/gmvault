---
title: Saber-Toothed Tiger
params:
  kind: monster
draft: false
weight: 10
summary: "Vejo que você enviou um rascunho importado do 5e.tools (Manual dos Monstros) e precisa de tradução e revisão editorial.\n\nNo entanto, a mensagem contém apenas a linha de metadados — o conteúdo real do monstro ou da entrada não foi incluído. \n\nPor favor, cole o texto completo que precisa ser traduzido para que eu possa realizar o trabalho."
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
  entity_name: Saber-Toothed Tiger
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 2f557950e320493d
stats:
  ac: '12'
  hp: 52 (7d10 + 14)
  speed: walk 40 ft.
  attributes:
    str: 18
    dex: 14
    con: 15
    int: 3
    wis: 12
    cha: 8
  saves: {}
  skills:
    perception: '+3'
    stealth: '+6'
  senses: ''
  languages: ''
  cr: '2'
stats_meta: Large beast U
titulo_pt_br: Tigre-dentes-de-sabre
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Faro Apurado

O tigre tem vantagem em testes de Sabedoria (Percepção) que dependem do olfato.

### Bote

Se o tigre se mover pelo menos 20 pés em linha reta em direção a uma criatura e então atingi-la com um ataque de garra no mesmo turno, o alvo deve ser bem-sucedido em um teste de resistência de Força CD 14 ou fica caído. Se o alvo estiver caído, o tigre pode realizar um ataque de mordida contra ele como uma ação bônus.

## Ações

### Mordida

mw 6 para atingir, alcance 5 pés, um alvo. {@h}10 (<span class="dice+" data-roll-notation="1d10+5">1d10 + 5</span>) dano perfurante.

### Garra

mw 6 para atingir, alcance 5 pés, um alvo. {@h}12 (<span class="dice+" data-roll-notation="2d6+5">2d6 + 5</span>) dano cortante.
