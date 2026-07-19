---
title: Jackalwere
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
  entity_name: Jackalwere
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 788b6aa30710ad4c
stats:
  ac: '12'
  hp: 18 (4d8)
  speed: walk 40 ft.
  attributes:
    str: 11
    dex: 15
    con: 11
    int: 13
    wis: 11
    cha: 10
  saves: {}
  skills:
    deception: '+4'
    perception: '+2'
    stealth: '+4'
  senses: ''
  languages: Common (can't speak in jackal form)
  cr: 1/2
stats_meta: Medium humanoid C/E
titulo_pt_br: Chacal-homem
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Mudador de Forma

O jackalwere pode usar sua ação para se polimorfar em um humano Médio específico ou em um híbrido de chacal e humanoide, ou voltar à sua forma verdadeira (a de um chacal Pequeno). Exceto pelo tamanho, suas estatísticas são as mesmas em cada forma. Qualquer equipamento que esteja vestindo ou carregando não é transformado. Ele reverte à sua forma verdadeira se morrer.

### Audição e Olfato Aguçados

O jackalwere tem vantagem em testes de Sabedoria (Percepção) que dependem de audição ou olfato.

### Táticas de Matilha

O jackalwere tem vantagem em uma jogada de ataque contra uma criatura se pelo menos um aliado do jackalwere estiver a até 1,5 metro da criatura e o aliado não estiver incapacitado.

## Ações

### Mordida (Apenas na Forma de Chacal ou Híbrida)

mw 4 para atingir, alcance 1,5 metro, um alvo. {@h}4 (<span class="dice+" data-roll-notation="1d4+2">1d4 + 2</span>) de dano perfurante.

### Cimitarra (Apenas na Forma Humana ou Híbrida)

mw 4 para atingir, alcance 1,5 metro, um alvo. {@h}5 (<span class="dice+" data-roll-notation="1d6+2">1d6 + 2</span>) de dano cortante.

### Olhar Sonífero

O jackalwere fita uma criatura que possa ver a até 9 metros de distância. O alvo deve fazer um teste de resistência de Sabedoria CD 10. Em caso de falha no teste de resistência, o alvo sucumbe a um sono mágico, caindo inconsciente por 10 minutos ou até que alguém use uma ação para sacudir o alvo e despertá-lo. Uma criatura que obtiver sucesso no teste de resistência contra este efeito fica imune ao olhar deste jackalwere pelas próximas 24 horas. Mortos-vivos e criaturas imunes a serem enfeitiçadas não são afetados por ele.
