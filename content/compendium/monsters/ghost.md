---
title: Ghost
params:
  kind: monster
draft: true
weight: 10
summary: Rascunho importado do 5e.tools (MM). Requer tradução e revisão editorial.
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
  entity_name: Ghost
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: e7e10ac09214e1ef
stats:
  ac: '11'
  hp: 45 (10d8)
  speed: walk 0 ft., fly 40 ft.
  attributes:
    str: 7
    dex: 13
    con: 10
    int: 10
    wis: 12
    cha: 17
  saves: {}
  skills: {}
  senses: darkvision 60 ft.
  languages: any languages it knew in life
  cr: '4'
stats_meta: Medium undead A
titulo_pt_br: Espectro
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Visão Etérea

O fantasma pode ver 18 metros no Plano Etéreo quando está no Plano Material, e vice-versa.


### Movimento Incorpóreo

O fantasma pode se mover através de outras criaturas e objetos como se fossem 3. Ele sofre 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>) de dano de energia se terminar seu turno dentro de um objeto.

## Ações


### Toque Murchador

Ataque Corpo a Corpo com Arma: +5 para atingir, alcance 1,5 m, um alvo. {@h}17 (<span class="dice+" data-roll-notation="4d6+3">4d6 + 3</span>) de dano necrótico.


### Eterealidade

O fantasma entra no Plano Etéreo a partir do Plano Material, ou vice-versa. Ele fica visível no Plano Material enquanto estiver na Fronteira Etérea, e vice-versa, mas não pode afetar nem ser afetado por nada no outro plano.


### Aparição Horripilante

Cada criatura que não seja morto-vivo a até 18 metros do fantasma que possa vê-lo deve ser bem-sucedida em um teste de resistência de Sabedoria CD 13 ou fica amedrontada por 1 minuto. Se o teste falhar por 5 ou mais, o alvo também envelhece <span class="dice+" data-roll-notation="1d4×10">1d4 × 10</span> anos. Um alvo amedrontado pode repetir o teste de resistência no final de cada um de seus turnos, terminando a condição de amedrontado sobre si mesmo em caso de sucesso. Se o teste de resistência do alvo for bem-sucedido ou o efeito terminar para ele, o alvo fica imune a esta Aparição Horripilante do fantasma pelas próximas 24 horas. O efeito de envelhecimento pode ser revertido com uma magia *restauração maior*, mas apenas dentro de 24 horas após ter ocorrido.


### Possessão {@recharge}

Um humanoide que o fantasma possa ver a até 1,5 metro de si deve ser bem-sucedido em um teste de resistência de Carisma CD 13 ou ser possuído pelo fantasma; o fantasma então desaparece, e o alvo fica incapacitado e perde o controle de seu corpo. O fantasma agora controla o corpo, mas não priva o alvo de sua consciência. O fantasma não pode ser alvo de nenhum ataque, magia ou outro efeito, exceto aqueles que viram mortos-vivos, e mantém sua tendência, Inteligência, Sabedoria, Carisma e imunidade a ser enfeitiçado e amedrontado. Ele, de outra forma, usa as estatísticas do alvo possuído, mas não ganha acesso ao conhecimento, características de classe ou proficiências do alvo.

A possessão dura até o corpo cair a 0 pontos de vida, o fantasma terminá-la como uma ação bônus, ou o fantasma ser virado ou forçado a sair por um efeito como a magia *dissipar o mal e o bem*. Quando a possessão termina, o fantasma reaparece em um espaço desocupado a até 1,5 metro do corpo. O alvo fica imune a esta Possessão do fantasma por 24 horas após ser bem-sucedido no teste de resistência ou após o fim da possessão.
