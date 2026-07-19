---
title: Mud Mephit
params:
  kind: monster
draft: false
weight: 10
summary: '```markdown

  ## Rastejador da Carcaça

  *Criatura monstruosidade, não alinhado*


  **Classe de Armadura** 13 (armadura natural)

  **Pontos de Vida** 13 (3d6 + 3)

  **Deslocamento** 9 m, escalada 9 m


  |   FOR   |   DES   |   CON   |   INT   |   SAB   |   CAR   |

  |:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|

  | 6 (-2)  | 13 (+1) | 13 (+1) | 4 (-3)  | 10 (+0) | 6 (-2)  |


  **Sentidos** percepção às cegas 9 m (cego além deste raio), Percepção passiva 10

  **Idiomas** —

  **Nível de Desafio** 1/8 (25 XP)


  ***Percepção às Cegas***. O rastejador não pode usar sua visão às cegas enquanto estiver surdo e incapaz de farejar.


  ***Sensível à Luz***. Enquanto estiver sob luz solar intensa, o rastejador tem desvantagem em jogadas de ataque.


  ### Ações

  ***Mordida***. *Ataque Corpo a Corpo com Arma:* +3 para atingir, alcance 1,5 m, um alvo. *Dano:* 3 (1d4 + 1) de dano perfurante.


  ### Reações

  ***Agarrão Ofegante***. *Gatilho:* O rastejador é alvo de um efeito que o forçaria a fazer uma salvaguarda de Destreza. *Resposta:* O rastejador se agarra a uma superfície, passando automaticamente na salvaguarda.

  ```'
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
  entity_name: Mud Mephit
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 3a29f5edfc5f7326
stats:
  ac: '11'
  hp: 27 (6d6 + 6)
  speed: walk 20 ft., fly 20 ft., swim 20 ft.
  attributes:
    str: 8
    dex: 12
    con: 12
    int: 9
    wis: 11
    cha: 7
  saves: {}
  skills:
    stealth: '+3'
  senses: darkvision 60 ft.
  languages: Aquan, Terran
  cr: 1/4
stats_meta: Small elemental N/E
titulo_pt_br: Mefítico de Lama
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Explosão Mortal

Quando o mephit morre, ele explode em uma erupção de lama pegajosa. Cada criatura de tamanho Médio ou menor a até 1,5 metro dele deve ser bem-sucedida em um teste de resistência de Destreza CD 11 ou ficará contida até o final do próximo turno da criatura.


### Falsa Aparência

Enquanto o mephit permanece imóvel, ele é indistinguível de um monte de lama comum.

## Ações


### Punhos

corpo a corpo +3 para acertar, alcance 1,5 m, uma criatura. <i>Dano:</i> 4 (<span class="dice+" data-roll-notation="1d6+1">1d6 + 1</span>) de dano de concussão.


### Sopro de Lama {@recharge}

O mephit arrota lama viscosa em uma criatura a até 1,5 metro dele. Se o alvo for de tamanho Médio ou menor, ele deve ser bem-sucedido em um teste de resistência de Destreza CD 11 ou ficará contido por 1 minuto. Uma criatura pode repetir o teste de resistência no final de cada um de seus turnos, encerrando o efeito sobre si mesma em caso de sucesso.
