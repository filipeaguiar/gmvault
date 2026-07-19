---
title: Behir
type: monster
draft: false
weight: 10
summary: Parece que você enviou um rascunho vazio para tradução. Por favor, cole o texto que deseja que eu traduza e revise editorialmente para que eu possa aplicar as regras de terminologia obrigatória e preservar os elementos protegidos conforme solicitado.
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
titulo_pt_br: Behir
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Ações

### Ataques Múltiplos

O behir faz dois ataques: um com sua mordida e um para constringir.

### Mordida

Ataque Corpo a Corpo: +10 para atingir, alcance 10 feet, um alvo. {@h}22 (<span class="dice+" data-roll-notation="3d10+6">3d10 + 6</span>) de dano perfurante.

### Constrição

Ataque Corpo a Corpo: +10 para atingir, alcance 5 feet, uma criatura Grande ou menor. {@h}17 (<span class="dice+" data-roll-notation="2d10+6">2d10 + 6</span>) de dano de concussão mais 17 (<span class="dice+" data-roll-notation="2d10+6">2d10 + 6</span>) de dano cortante. O alvo fica agarrado (CD 16 para escapar) se o behir já não estiver constringindo uma criatura, e o alvo fica contido até este agarrão terminar.

### Sopro de Relâmpago (Recarga 5)

O behir exala uma linha de relâmpago com 20 feet de comprimento e 5 feet de largura. Cada criatura nessa linha deve fazer um teste de resistência de Destreza CD 16; em caso de falha, sofre 66 (<span class="dice+" data-roll-notation="12d10">12d10</span>) de dano elétrico, ou metade desse dano em caso de sucesso.

### Engolir

O behir faz um ataque de mordida contra um alvo Médio ou menor que esteja agarrando. Se o ataque atingir, o alvo também é engolido e o agarrão termina. Enquanto engolido, o alvo fica cego e contido, tem cobertura total contra ataques e outros efeitos de fora do behir, e sofre 21 (<span class="dice+" data-roll-notation="6d6">6d6</span>) de dano de ácido no início de cada turno do behir. Um behir pode ter apenas uma criatura engolida por vez.

Se o behir sofrer 30 de dano ou mais em um único turno causado pela criatura engolida, ele deve ser bem-sucedido em um teste de resistência de Constituição CD 14 ao final desse turno ou regurgitar a criatura, que cai caída em um espaço a até 10 feet do behir. Se o behir morrer, a criatura engolida não fica mais contida por ele e pode escapar do cadáver usando 15 feet de deslocamento, saindo caída.
