---
title: young red dragon
draft: false
titulo_pt_br: dragão vermelho jovem
visibility: gm
status: draft
tags:
- monstro
- importado
params:
  kind: monster
stats_meta: Large dragon, caótico e mau
stats:
  ac: '18'
  hp: 178 (17d10 + 85)
  speed: 40 ft., climb 40 ft., fly 80 ft.
  attributes:
    str: 23
    dex: 10
    con: 21
    int: 14
    wis: 11
    cha: 19
  saves: Dex +4, Con +9, Wis +4, Cha +8
  skills: Perception +8, Stealth +4
  senses: blindsight 30 ft., darkvision 120 ft., passive Perception 18
  languages: Common, Draconic
  cr: '10'
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-chat
---

### Ações

**Ataques Múltiplos.** O dragão realiza três ataques: um com sua mordida e dois com suas garras.

**Mordida.** *Ataque Corpo a Corpo com Arma:* +10 para acertar, alcance 3 m, um alvo. *Dano:* 17 ([[2d10+6]]) dano perfurante mais 3 ([[1d6]]) dano de fogo.

**Garra.** *Ataque Corpo a Corpo com Arma:* +10 para acertar, alcance 1,5 m, um alvo. *Dano:* 13 ([[2d6+6]]) dano cortante.

**Sopro de Fogo {@recharge 5}.** O dragão exala fogo em um cone de 9 metros. Cada criatura nessa área deve realizar um teste de resistência de Destreza CD 17, sofrendo 56 ([[16d6]]) dano de fogo em caso de falha, ou metade desse dano em caso de sucesso.
