---
title: water elemental
draft: false
titulo_pt_br: elemental d'água
visibility: gm
status: draft
tags:
- monstro
- importado
params:
  kind: monster
stats_meta: Large elemental, neutro
stats:
  ac: '14'
  hp: 114 (12d10 + 48)
  speed: 30 ft., swim 90 ft.
  attributes:
    str: 18
    dex: 14
    con: 18
    int: 5
    wis: 10
    cha: 8
  senses: darkvision 60 ft., passive Perception 10
  languages: Aquan
  cr: '5'
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-chat
---

### Características

**Forma Aquática.** O elemental pode entrar no espaço de uma criatura hostil e parar ali. Ele pode se mover por um espaço tão estreito quanto 2,5 centímetros de largura sem se espremer.

**Congelamento.** Se o elemental sofre dano de frio, ele congela parcialmente; seu deslocamento é reduzido em 6 metros até o final do próximo turno dele.

### Ações

**Ataques Múltiplos.** O elemental realiza dois ataques de pancada.

**Pancada.** *Ataque Corpo a Corpo com Arma:* +7 para acertar, alcance 1,5 m, um alvo. *Dano:* 13 ([[2d8+4]]) de dano de concussão.

**Submergir {@recarga 4}.** Cada criatura no espaço do elemental deve realizar um teste de resistência de Força CD 15. Em caso de falha, o alvo sofre 13 ([[2d8+4]]) de dano de concussão. Se for Grande ou menor, também fica agarrado (CD 14 para escapar). Até que esta imobilização termine, o alvo está contido e incapaz de respirar, a menos que consiga respirar água. Se o teste de resistência for bem-sucedido, o alvo é empurrado para fora do espaço do elemental.

O elemental pode agarrar uma criatura Grande ou até duas criaturas Médias ou menores ao mesmo tempo. No início de cada turno do elemental, cada alvo agarrado por ele sofre 13 ([[2d8+4]]) de dano de concussão. Uma criatura a até 1,5 metro do elemental pode puxar uma criatura ou objeto para fora dele realizando uma ação para fazer um teste de Força CD 14 e sendo bem-sucedida.
