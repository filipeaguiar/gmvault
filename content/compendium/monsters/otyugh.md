---
title: Otyugh
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
  entity_name: Otyugh
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: e5696b738ba5a643
stats:
  ac: '14'
  hp: 114 (12d10 + 48)
  speed: walk 30 ft.
  attributes:
    str: 16
    dex: 11
    con: 19
    int: 6
    wis: 13
    cha: 6
  saves:
    con: '+7'
  skills: {}
  senses: darkvision 120 ft.
  languages: Otyugh
  cr: '5'
stats_meta: Large aberration N
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Otyugh
---

## Características


### Telepatia Limitada

O otyugh pode transmitir magicamente mensagens e imagens simples para qualquer criatura a até 36 metros dele que possa entender um idioma. Esta forma de telepatia não permite que a criatura recipiente responda telepaticamente.

## Ações


### Ataques Múltiplos

O otyugh realiza três ataques: um com sua mordida e dois com seus tentáculos.


### Mordida

Ataque Corpo a Corpo com Arma: +6 para atingir, alcance 1,5 m, um alvo. Acerto: 12 (<span class="dice+" data-roll-notation="2d8+3">2d8 + 3</span>) de dano perfurante. Se o alvo for uma criatura, ela deve ser bem-sucedida em um teste de resistência de Constituição CD 15 contra doença ou ficará envenenada até a doença ser curada. A cada 24 horas que se passarem, o alvo deve repetir o teste de resistência, reduzindo seu máximo de pontos de vida em 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) em caso de falha. A doença é curada em caso de sucesso. O alvo morre se a doença reduzir seu máximo de pontos de vida a 0. Esta redução no máximo de pontos de vida do alvo dura até a doença ser curada.


### Tentáculo

Ataque Corpo a Corpo com Arma: +6 para atingir, alcance 3 m, um alvo. Acerto: 7 (<span class="dice+" data-roll-notation="1d8+3">1d8 + 3</span>) de dano de concussão mais 4 (<span class="dice+" data-roll-notation="1d8">1d8</span>) de dano perfurante. Se o alvo for de tamanho Médio ou menor, ele fica agarrado (CD para escapar 13) e contido até o agarrão terminar. O otyugh tem dois tentáculos, cada um podendo agarrar um alvo.


### Golpe de Tentáculo

O otyugh bate criaturas agarradas por ele umas contra as outras ou contra uma superfície sólida. Cada criatura deve ser bem-sucedida em um teste de resistência de Constituição CD 14 ou sofre 10 (<span class="dice+" data-roll-notation="2d6+3">2d6 + 3</span>) de dano de concussão e fica atordoada até o final do próximo turno do otyugh. Em caso de sucesso no teste de resistência, o alvo sofre metade do dano de concussão e não fica atordoado.
