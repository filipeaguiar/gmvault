---
title: Revenant
type: monster
draft: false
weight: 10
tags:
- draft
- importado
- 5etools
visibility: gm
status: ready
source:
  provider: 5e.tools
  book: MM
  entity_type: monster
  entity_name: Revenant
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: b3a1cdcce4a55d4c
stats:
  ac: '13'
  hp: 136 (16d8 + 64)
  speed: walk 30 ft.
  attributes:
    str: 18
    dex: 14
    con: 18
    int: 13
    wis: 16
    cha: 18
  saves:
    str: '+7'
    con: '+7'
    wis: '+6'
    cha: '+7'
  skills: {}
  senses: darkvision 60 ft.
  languages: the languages it knew in life
  cr: '5'
stats_meta: Medium undead N
titulo_pt_br: Renascido
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Regeneração

O revenante recupera 10 pontos de vida no início de seu turno. Se o revenante sofrer dano de fogo ou radiante, esta característica não funcionará no início do próximo turno do revenante. O corpo do revenante é destruído apenas se ele iniciar seu turno com 0 pontos de vida e não regenerar.


### Rejuvenescimento

Quando o corpo do revenante é destruído, sua alma permanece. Após 24 horas, a alma habita e anima outro cadáver humanoide no mesmo plano de existência e recupera todos os seus pontos de vida. Enquanto a alma estiver sem corpo, uma magia desejo pode ser usada para forçar a alma a ir para o pós-vida e não retornar.


### Imunidade a Repelente a Mortos-Vivos

O revenante é imune a efeitos que afastam mortos-vivos.


### Rastreador Vingativo

O revenante sabe a distância e a direção de qualquer criatura contra a qual busca vingança, mesmo que a criatura e o revenante estejam em planos de existência diferentes. Se a criatura rastreada pelo revenante morrer, o revenante saberá.

## Ações


### Ataques Múltiplos

O revenante realiza dois ataques de punho.


### Punho

mw 7 para atingir, alcance 1,5 m, um alvo. {@h}11 (<span class="dice+" data-roll-notation="2d6+4">2d6 + 4</span>) de dano de concussão. Se o alvo for uma criatura contra a qual o revenante jurou vingança, o alvo sofre 14 (<span class="dice+" data-roll-notation="4d6">4d6</span>) de dano de concussão adicionais. Em vez de causar dano, o revenante pode agarrar o alvo (CD para escapar 14), desde que o alvo seja Grande ou menor.


### Olhar Vingativo

O revenante escolhe uma criatura que possa ver a até 9 metros de si e contra a qual tenha jurado vingança. O alvo deve realizar um teste de resistência de Sabedoria CD 15. Em caso de falha, o alvo fica paralisado até o revenante causar dano a ele, ou até o final do próximo turno do revenante. Quando a paralisia termina, o alvo fica amedrontado pelo revenante por 1 minuto. O alvo amedrontado pode repetir o teste de resistência no final de cada um de seus turnos, com desvantagem se puder ver o revenante, terminando a condição de amedrontado sobre si em caso de sucesso.
