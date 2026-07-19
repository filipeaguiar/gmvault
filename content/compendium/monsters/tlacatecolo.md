---
title: Tlacatecolo
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
  entity_name: Tlacatecolo
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 78069ba15ca284fb
stats:
  ac: '13'
  hp: 78 (12d8 + 24)
  speed: walk 30 ft., fly 30 ft.
  attributes:
    str: 12
    dex: 17
    con: 14
    int: 10
    wis: 15
    cha: 10
  saves:
    dex: '+6'
    con: '+5'
  skills:
    perception: '+5'
    stealth: '+6'
  senses: darkvision 120 ft.
  languages: Abyssal, Common
  cr: '5'
stats_meta: Medium fiend N/E
titulo_pt_br: Tlacatecolo
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Resistência à Magia

O tlacatecolo tem vantagem em testes de resistência contra magias e outros efeitos mágicos.

## Ações

### Ataques Múltiplos

O tlacatecolo realiza dois ataques de Garra.

### Garra

Ataque Corpo a Corpo com Arma: +6 para atingir, alcance 1,5 m, um alvo. {@h}8 (<span class="dice+" data-roll-notation="1d8+3">1d8 + 3</span>) de dano perfurante mais 14 (<span class="dice+" data-roll-notation="3d8">3d8</span>) de dano de veneno.

### Mudar Forma

O tlacatecolo se transforma magicamente em uma coruja Média, mantendo suas estatísticas de jogo (exceto pelo tamanho). Esta transformação termina se o tlacatecolo for reduzido a 0 pontos de vida ou se usar sua ação para terminá-la.

### Ventos da Peste (Apenas na Forma de Corruptor; Recarga 5–6)

O tlacatecolo emite um vento gélido e carregado de doença em uma linha de 18 metros de comprimento e 3 metros de largura. Cada criatura nessa área deve ser bem-sucedida em um teste de resistência de Constituição CD 13 ou sofre 26 (<span class="dice+" data-roll-notation="4d12">4d12</span>) de dano de frio e fica envenenada.

Enquanto estiver envenenada dessa forma, a criatura não pode recuperar pontos de vida. No final de cada hora, a criatura deve ser bem-sucedida em um teste de resistência de Constituição CD 13 ou ganha 1 nível de exaustão. Se a criatura estiver sob luz solar direta quando fizer este teste de resistência, ela é bem-sucedida automaticamente.

Se a criatura for alvo de uma magia que termina um veneno ou doença, como restauração menor, enquanto a criatura não estiver sob luz solar direta, o efeito não termina.
