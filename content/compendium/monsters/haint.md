---
title: Haint
params:
  kind: monster
draft: true
weight: 10
summary: Conteúdo importado do 5e.tools (JTTRC) e traduzido automaticamente; requer revisão editorial.
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
  entity_name: Haint
  remote_file: bestiary/bestiary-jttrc.json
  remote_key: monster
  remote_id: 7d340d08ef3f6daa
stats:
  ac: '12'
  hp: 75 (10d8 + 30)
  speed: walk 30 ft., fly 30 ft.
  attributes:
    str: 7
    dex: 15
    con: 17
    int: 10
    wis: 13
    cha: 17
  saves: {}
  skills:
    deception: '+6'
    stealth: '+8'
  senses: darkvision 60 ft.
  languages: any languages it knew in life
  cr: '7'
stats_meta: Medium undead N
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Assombração
---

## Características

### Movimento Incorpóreo
O haint pode se mover através de outras criaturas e objetos como se fossem terreno difícil. Ele sofre 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano de energia se terminar seu turno dentro de um objeto.

### Natureza Incomum
O haint não precisa de ar, comida, bebida ou sono.

## Ações

### Ataques Múltiplos
O haint realiza dois ataques de Toque Doloroso.

### Toque Doloroso
Ataque Corpo a Corpo com Magia: +6 para atingir, alcance 1,5 m, uma criatura. {@h}21 (<span class="dice+" data-roll-notation="4d8+3">4d8 + 3</span>) de dano psíquico.

### Mudar Forma
O haint assume magicamente a aparência do Humanoide que era em vida, mantendo suas estatísticas de jogo. A aparência assumida termina se o haint for reduzido a 0 pontos de vida ou usar uma ação para terminá-la.

## Ações Bônus

### Tristeza Compartilhada
O haint escolhe uma criatura que possa ver a até 60 pés de si que não estiver com todos os seus pontos de vida, compartilhando seu próprio tormento com essa alma sofrida. O alvo deve ser bem-sucedido em um teste de resistência de Sabedoria CD 14 ou ficará incapacitado.

Uma criatura pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesma em caso de sucesso. Se o teste de resistência de uma criatura for bem-sucedido ou o efeito terminar para ela, a criatura fica imune à Tristeza Compartilhada do haint pelas próximas 24 horas.
