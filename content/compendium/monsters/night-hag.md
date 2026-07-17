---
title: Night Hag
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
titulo_pt_br: Bruxa da Noite
---

## Características


### Resistência à Magia

A bruxa tem vantagem em testes de resistência contra magias e outros efeitos mágicos.


### Itens da Bruxa Noturna

Uma bruxa noturna carrega dois itens mágicos muito raros que ela mesma deve criar. Se qualquer desses objetos for perdido, a bruxa noturna fará de tudo para recuperá-lo, já que criar uma nova ferramenta demanda tempo e esforço.


### Heartstone

Esta gema negra e reluzente permite que a bruxa noturna se torne etérea enquanto estiver em sua posse. O toque da heartstone também cura qualquer doença. Criar uma heartstone leva 30 dias.


### Soul Bag

Quando um humanoide maligno morre em consequência da Assombração do Pesadelo da bruxa noturna, ela captura a alma neste saco negro feito de carne costurada. Uma soul bag pode conter apenas uma alma maligna por vez, e somente a bruxa noturna que a criou pode capturar uma alma com ela. Criar uma soul bag leva 7 dias e exige o sacrifício de um humanoide (cuja carne é usada para fazer o saco).

## Ações


### Garras (Apenas na Forma de Bruxa)

Ataque corpo a corpo com arma: +7 para atingir, alcance 1,5 m, um alvo. Acerto: 13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano cortante.


### Mudar Forma

A bruxa se transforma magicamente em uma humanoide fêmea de tamanho Pequeno ou Médio, ou de volta à sua forma verdadeira. Suas estatísticas são as mesmas em cada forma. Qualquer equipamento que ela esteja vestindo ou carregando não é transformado. Ela reverte à sua forma verdadeira se morrer.


### Eterealidade

A bruxa entra magicamente no Plano Etéreo vinda do Plano Material, ou vice-versa. Para isso, ela precisa ter uma heartstone em sua posse.


### Assombração do Pesadelo (1/Dia)

Enquanto estiver no Plano Etéreo, a bruxa toca magicamente um humanoide adormecido no Plano Material. Uma magia de proteção contra o bem e o mal conjurada sobre o alvo impede esse contato, assim como um círculo mágico. Enquanto o contato persistir, o alvo tem visões terríveis. Se essas visões durarem pelo menos 1 hora, o alvo não ganha benefício de seu descanso, e seu máximo de pontos de vida é reduzido em 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>). Se esse efeito reduzir o máximo de pontos de vida do alvo a 0, o alvo morre e, se era maligno, sua alma fica presa na soul bag da bruxa. A redução do máximo de pontos de vida do alvo dura até ser removida pela magia restauração maior ou magia similar.
