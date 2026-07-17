---
title: Beholder
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
  entity_name: Beholder
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 1bc771170f77fb86
stats:
  ac: '18'
  hp: 180 (19d10 + 76)
  speed: walk 0 ft., fly 20 ft.
  attributes:
    str: 10
    dex: 14
    con: 18
    int: 17
    wis: 15
    cha: 17
  saves:
    int: '+8'
    wis: '+7'
    cha: '+8'
  skills:
    perception: '+12'
  senses: darkvision 120 ft.
  languages: Deep Speech, Undercommon
  cr: '13'
stats_meta: Large aberration L/E
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Beholder
---

## Características


### Cone Antimagia

O olho central do beholder cria uma área de antimagia, como na magia campo antimagia, em um cone de 150 pés. No início de cada um de seus turnos, o beholder decide para qual direção o cone está voltado e se está ativo. A área afeta os raios oculares do próprio beholder.

## Ações


### Mordida

Ataque Corpo a Corpo com Arma: +5 para atingir, alcance 1,5 m, um alvo. {@h}14 (<span class="dice+" data-roll-notation="4d6">4d6</span>) de dano perfurante.


### Raios Oculares

O beholder dispara três dos seguintes raios oculares mágicos aleatoriamente (jogue novamente resultados duplicados), escolhendo de um a três alvos que possa ver, a até 36 metros de distância:

* {'type': 'itemSub', 'name': '1. Raio Enfeitiçante', 'entry': 'A criatura alvo deve ser bem-sucedida em um teste de resistência de Sabedoria CD 16 ou ficará enfeitiçada pelo beholder por 1 hora, ou até que o beholder a machuque.'}

* {'type': 'itemSub', 'name': '2. Raio Paralisante', 'entry': 'A criatura alvo deve ser bem-sucedida em um teste de resistência de Constituição CD 16 ou ficará paralisada por 1 minuto. O alvo pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si em caso de sucesso.'}

* {'type': 'itemSub', 'name': '3. Raio do Medo', 'entry': 'A criatura alvo deve ser bem-sucedida em um teste de resistência de Sabedoria CD 16 ou ficará amedrontada por 1 minuto. O alvo pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si em caso de sucesso.'}

* {'type': 'itemSub', 'name': '4. Raio Lentificador', 'entry': "A criatura alvo deve ser bem-sucedida em um teste de resistência de Destreza CD 16. Em caso de falha, o deslocamento do alvo é reduzido à metade por 1 minuto. Além disso, a criatura não pode realizar reações e, em seu turno, pode realizar uma ação ou uma ação bônus, mas não ambas. A criatura pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si em caso de sucesso."}

* {'type': 'itemSub', 'name': '5. Raio de Enervação', 'entry': 'A criatura alvo deve realizar um teste de resistência de Constituição CD 16, sofrendo 36 (<span class="dice+" data-roll-notation="8d8">8d8</span>) de dano necrótico em caso de falha, ou metade desse dano em caso de sucesso.'}

* {'type': 'itemSub', 'name': '6. Raio Telecinético', 'entries': ["Se o alvo for uma criatura, ela deve ser bem-sucedida em um teste de resistência de Força CD 16 ou o beholder a move até 9 metros em qualquer direção. Ela fica contida pelo aperto telecinético do raio até o início do próximo turno do beholder ou até que o beholder fique incapacitado.", "Se o alvo for um objeto pesando 300 libras ou menos que não esteja sendo vestido ou carregado, ele é movido até 9 metros em qualquer direção. O beholder também pode exercer controle preciso sobre objetos com este raio, como manipular uma ferramenta simples ou abrir uma porta ou recipiente."]}

* {'type': 'itemSub', 'name': '7. Raio do Sono', 'entry': 'A criatura alvo deve ser bem-sucedida em um teste de resistência de Sabedoria CD 16 ou cairá no sono e permanecerá inconsciente por 1 minuto. O alvo acorda se sofrer dano ou se outra criatura usar uma ação para acordá-lo. Este raio não afeta constructos e mortos-vivos.'}

* {'type': 'itemSub', 'name': '8. Raio de Petrificação', 'entry': 'A criatura alvo deve realizar um teste de resistência de Destreza CD 16. Em caso de falha, a criatura começa a se transformar em pedra e fica contida. Ela deve repetir o teste de resistência no final de seu próximo turno. Em caso de sucesso, o efeito termina. Em caso de falha, a criatura fica petrificada até ser libertada pela magia restauração maior ou outra magia.'}

* {'type': 'itemSub', 'name': '9. Raio de Desintegração', 'entries': ['Se o alvo for uma criatura, ela deve ser bem-sucedida em um teste de resistência de Destreza CD 16 ou sofrerá 45 (<span class="dice+" data-roll-notation="10d8">10d8</span>) de dano de energia. Se este dano reduzir a criatura a 0 pontos de vida, seu corpo se transforma em uma pilha de cinzas finas e cinzentas.', 'Se o alvo for um objeto não mágico ou uma criação de energia mágica de tamanho Grande ou menor, ele é desintegrado sem um teste de resistência. Se o alvo for um objeto ou criação de energia mágica de tamanho Enorme ou maior, este raio desintegra um cubo de 3 metros dele.']}

* {'type': 'itemSub', 'name': '10. Raio da Morte', 'entry': 'A criatura alvo deve ser bem-sucedida em um teste de resistência de Destreza CD 16 ou sofrerá 55 (<span class="dice+" data-roll-notation="10d10">10d10</span>) de dano necrótico. O alvo morre se o raio o reduzir a 0 pontos de vida.'}

## Ações Lendárias


### Raio Ocular

O beholder usa um raio ocular aleatório.
