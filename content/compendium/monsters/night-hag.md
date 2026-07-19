---
title: Night Hag
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
  entity_name: Night Hag
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 640e3c159d97a0e8
stats:
  ac: '17'
  hp: 112 (15d8 + 45)
  speed: walk 30 ft.
  attributes:
    str: 18
    dex: 15
    con: 16
    int: 16
    wis: 14
    cha: 16
  saves: {}
  skills:
    deception: '+6'
    insight: '+5'
    perception: '+5'
    stealth: '+5'
  senses: darkvision 120 ft.
  languages: Abyssal, Common, Infernal, Primordial
  cr: '5'
stats_meta: Medium fiend N/E
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Resistência à Magia

A bruxa tem vantagem em testes de resistência contra magias e outros efeitos mágicos.

### Itens de Bruxa da Noite

Uma bruxa da noite carrega dois itens mágicos muito raros que ela deve confeccionar para si mesma. Se qualquer um dos objetos for perdido, a bruxa da noite fará grandes esforços para recuperá-lo, pois criar uma nova ferramenta exige tempo e esforço.

### Pedra do Coração

Esta pedra negra e lustrosa permite que uma bruxa da noite se torne etérea enquanto estiver em sua posse. O toque de uma pedra do coração também cura qualquer doença. Confeccionar uma pedra do coração leva 30 dias.

### Saco das Almas

Quando um humanoide maligno morre como resultado da Assombração de Pesadelo de uma bruxa da noite, a bruxa captura a alma neste saco negro feito de carne costurada. Um saco das almas pode conter apenas uma alma maligna por vez, e somente a bruxa da noite que o confeccionou pode capturar uma alma com ele. Confeccionar um saco das almas leva 7 dias e um sacrifício humanoide (cuja carne é usada para fazer o saco).

## Ações

### Garras (Apenas na Forma de Bruxa)

Ataque Corpo a Corpo com Arma: +7 para atingir, alcance 1,5 m, um alvo. {@h}13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano cortante.

### Mudar de Forma

A bruxa se transforma magicamente em uma humanoide fêmea Pequena ou Média, ou de volta à sua forma verdadeira. Suas estatísticas são as mesmas em cada forma. Qualquer equipamento que esteja usando ou carregando não é transformado. Ela reverte à sua forma verdadeira se morrer.

### Eteridade

A bruxa entra magicamente no Plano Etéreo a partir do Plano Material, ou vice-versa. Para isso, a bruxa precisa ter uma pedra do coração em sua posse.

### Assombração de Pesadelo (1/Dia)

Enquanto estiver no Plano Etéreo, a bruxa toca magicamente um humanoide adormecido no Plano Material. Uma magia proteção contra o bem e o mal conjurada no alvo previne esse contato, assim como um círculo mágico. Enquanto o contato persistir, o alvo tem visões terríveis. Se essas visões durarem pelo menos 1 hora, o alvo não ganha benefício de seu descanso, e seu máximo de pontos de vida é reduzido em 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>). Se esse efeito reduzir o máximo de pontos de vida do alvo a 0, o alvo morre, e se o alvo era maligno, sua alma fica presa no saco das almas da bruxa. A redução no máximo de pontos de vida do alvo dura até ser removida pela magia restauração maior ou magia similar.
