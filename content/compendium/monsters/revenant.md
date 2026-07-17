---
title: Revenant
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
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
titulo_pt_br: Aparição
---

## Características

### Regeneração

O revenant recupera 10 pontos de vida no início do seu turno. Se o revenant sofrer dano de fogo ou dano radiante, esta característica não funciona no início do próximo turno do revenant. O corpo do revenant só é destruído se ele iniciar seu turno com 0 pontos de vida e não se regenerar.

### Rejuvenescimento

Quando o corpo do revenant é destruído, sua alma permanece. Após 24 horas, a alma habita e anima outro cadáver humanoide no mesmo plano de existência e recupera todos os seus pontos de vida. Enquanto a alma estiver sem corpo, uma magia desejo pode ser usada para forçar a alma a ir para o pós-vida e não retornar.

### Imunidade a Expulsar Mortos-vivos

O revenant é imune a efeitos que expulsem mortos-vivos.

### Rastreador Vingativo

O revenant sabe a distância e a direção de qualquer criatura da qual busca vingança, mesmo que a criatura e o revenant estejam em planos de existência diferentes. Se a criatura sendo rastreada pelo revenant morrer, o revenant sabe.

## Ações

### Ataques Múltiplos

O revenant faz dois ataques de punho.

### Punho

Ataque Corpo a Corpo com Arma: +7 para atingir, alcance 1,5 m, um alvo. {@h}11 (<span class="dice+" data-roll-notation="2d6+4">2d6 + 4</span>) dano de concussão. Se o alvo for uma criatura contra a qual o revenant jurou vingança, o alvo sofre 14 (<span class="dice+" data-roll-notation="4d6">4d6</span>) de dano de concussão extra. Em vez de causar dano, o revenant pode agarrar o alvo (CD para escapar 14), desde que o alvo seja Grande ou menor.

### Olhar Vingativo

O revenant escolhe uma criatura que possa ver dentro de 9 metros e contra a qual jurou vingança. O alvo deve fazer um teste de resistência de Sabedoria CD 15. Em caso de falha, o alvo fica paralisado até que o revenant cause dano a ele, ou até o final do próximo turno do revenant. Quando a paralisia termina, o alvo fica amedrontado pelo revenant por 1 minuto. O alvo amedrontado pode repetir o teste de resistência no final de cada um de seus turnos, com desvantagem se puder ver o revenant, terminando a condição de amedrontado em si mesmo em caso de sucesso.
