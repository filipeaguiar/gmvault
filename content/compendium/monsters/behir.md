---
title: Behir
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
  entity_name: Behir
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: b78b8a92bc5fff6a
stats:
  ac: '17'
  hp: 168 (16d12 + 64)
  speed: walk 50 ft., climb 40 ft.
  attributes:
    str: 23
    dex: 16
    con: 18
    int: 7
    wis: 14
    cha: 12
  saves: {}
  skills:
    perception: '+6'
    stealth: '+7'
  senses: darkvision 90 ft.
  languages: Draconic
  cr: '11'
stats_meta: Huge monstrosity N/E
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Behir
---

## Ações

### Ataques Múltiplos

O behir realiza dois ataques: um com sua mordida e outro para constringir.


### Mordida

Ataque Corpo a Corpo com Arma: +10 de acerto, alcance 3 m, um alvo. *Acerto:* 22 (<span class="dice+" data-roll-notation="3d10+6">3d10+6</span>) de dano perfurante.


### Constrição

Ataque Corpo a Corpo com Arma: +10 de acerto, alcance 1,5 m, uma criatura Grande ou menor. *Acerto:* 17 (<span class="dice+" data-roll-notation="2d10+6">2d10+6</span>) de dano de concussão mais 17 (<span class="dice+" data-roll-notation="2d10+6">2d10+6</span>) de dano cortante. O alvo fica agarrado (CD 16 para escapar) se o behir ainda não estiver constringindo uma criatura, e o alvo fica contido até que este agarrão termine.


### Sopro Elétrico (Recarga 5–6)

O behir exala uma linha de eletricidade com 6 metros de comprimento e 1,5 metro de largura. Cada criatura nessa linha deve realizar um teste de resistência de Destreza CD 16, sofrendo 66 (<span class="dice+" data-roll-notation="12d10">12d10</span>) de dano elétrico em caso de falha no teste, ou metade desse dano em caso de sucesso.


### Engolir

O behir realiza um ataque de mordida contra um alvo Médio ou menor que esteja agarrado por ele. Se o ataque acertar, o alvo também é engolido e o agarrão termina. Enquanto estiver engolido, o alvo fica cego e contido, tem cobertura total contra ataques e outros efeitos fora do behir e sofre 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) de dano de ácido no início de cada turno do behir. Um behir só pode ter uma criatura engolida por vez.

Se o behir sofrer 30 ou mais de dano em um único turno da criatura engolida, ele deve ser bem-sucedido em um teste de resistência de Constituição CD 14 no final desse turno ou regurgitará a criatura, que fica caída em um espaço a até 3 metros do behir. Se o behir morrer, uma criatura engolida não estará mais contida por ele e poderá escapar do cadáver usando 4,5 metros de deslocamento, saindo caída.
