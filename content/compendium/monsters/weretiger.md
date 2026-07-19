---
title: Weretiger
type: monster
draft: false
weight: 10
summary: "```yaml\nname: \"Sahuagin Bruxo de Dagon\"\nsize: \"Médio\"\ntype: \"Humanoide\"\nsubtype: \"sahuagin, bruxo\"\nalignment: \"qualquer alinhamento\"\narmor_class: \"15 (armadura de escamas)\"\nhit_points: \"52 (8d8 + 16)\"\nspeed: \"andar 9 m, nadar 12 m\"\ndamage_resistances: \"\"\ncondition_immunities: \"\"\nsenses: \"visão no escuro 36 m\"\nlanguages: \"Comum, Sahuagin\"\nchallenge: \"3 (700 XP)\"\nproficiency_bonus: \"+2\"\nactions:\n  - name: \"Ataque Múltiplo\"\n    text: \"O sahuagin faz dois ataques: um com sua lança e um com sua mordida.\"\n  - name: \"Lança\"\n    text: \"Ataque Corpo a Corpo ou à Distância com Arma: +5 para atingir, alcance 1,5 m ou alcance 6/18 m, um alvo. Acerto: 6 (1d6 + 3) de dano perfurante, ou 7 (1d8 + 3) de dano perfurante se usada com as duas mãos para um ataque corpo a corpo.\"\n  - name: \"Mordida\"\n    text: \"Ataque Corpo a Corpo com Arma: +5 para atingir, alcance 1,5 m, um alvo. Acerto: 5 (1d4 + 3) de dano perfurante.\"\n  - name: \"Toque\
  \ de Dagon (Recarrega 5–6)\"\n    text: \"Ataque Corpo a Corpo com Magia: +5 para atingir, alcance 1,5 m, uma criatura. Acerto: 13 (3d8) de dano necrótico, e o alvo deve ser bem sucedido em um teste de resistência de Sabedoria CD 12 ou ficará amedrontado por 1 minuto. O alvo pode repetir o teste de resistência no final de cada um de seus turnos, terminando o efeito sobre si mesmo com um sucesso.\"\nreactions:\n  - name: \"Frenesi Sanguinário\"\n    text: \"Quando um aliado sahuagin que o bruxo possa ver dentro de 9 metros reduz uma criatura a 0 pontos de vida, o bruxo pode usar sua reação para se mover até metade de seu deslocamento e fazer um ataque com a mordida.\"\nsource: \"5e.tools\"\n```\n\n**Bruxo Sahuagin de Dagon**\n*Humanoide médio (sahuagin, bruxo), qualquer alinhamento*\n\n**Classe de Armadura** 15 (armadura de escamas)\n**Pontos de Vida** 52 (8d8 + 16)\n**Deslocamento** 9 m, natação 12 m\n\n| FOR     | DES     | CON     | INT     | SAB     | CAR     |\n|---------|---------|---------|---------|---------|---------|\n\
  | 16 (+3) | 14 (+2) | 14 (+2) | 10 (+0) | 12 (+1) | 12 (+1) |\n\n**Sentidos** visão no escuro 36 m, Percepção passiva 11\n**Idiomas** Comum, Sahuagin\n**Nível de Desafio** 3 (700 XP) **Bônus de Proficiência** +2\n\n***Respiração Limitada***. O sahuagin pode respirar ar e água, mas precisa estar submerso pelo menos uma vez a cada 4 horas para evitar sufocamento.\n\n***Amigo dos Tubarões.*** O sahuagin pode comandar um tubarão para não atacá-lo usando uma ação bônus. Essa amizade mágica termina se o sahuagin ou seus companheiros atacarem o tubarão.\n\n***Conjuração Inata.*** A habilidade de conjuração inata do bruxo é Carisma (CD de teste de resistência 11, +3 para atingir com ataques mágicos). Ele pode conjurar os seguintes feitiços, sem necessidade de componentes materiais:\n\nÀ vontade: *rajada de veneno*, *taumaturgia*\n1/dia cada: *escuridão*, *invisibilidade*\n\n###### MISSÕES DE DAGON\n| d8  | Missão |\n|-----|--------|\n| 1   | Coletar sacrifícios para Dagon. |\n| 2   | Construir\
  \ um santuário a Dagon em terra. |\n| 3   | Afundar um navio em nome de Dagon. |\n| 4   | Recuperar um artefato roubado do santuário de Dagon. |\n| 5   | Matar um grande monstro marinho que desafia a reivindicação de Dagon sobre um território. |\n| 6   | Capturar um conjurador para que este possa ser transformado em um guardião controlado por Dagon. |\n| 7   | Atacar um kōau marinho que serve a outra entidade. |\n| 8   | Assassinar um aliado terrestre de Dagon que traiu o Príncipe Demônio. |\n\nSahuagin que servem como bruxos de Dagon, o príncipe demônio das profundezas, lideram bandos de guerra em ataques a comunidades costeiras. O sussurro de Dagon os leva a recrutar mais sahuagin para sua adoração, e esses bruxos conquistam seguidores por meio de demonstrações de poder concedido pelo mar.\n\nOs sahuagin são humanoides predatórios semelhantes a tubarões que habitam oceanos, mares escuros e cavernas submarinas. Às vezes chamados de \"demônios do mar\" ou \"lobos do mar\", eles vivem para\
  \ atacar e saquear."
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
  entity_name: Weretiger
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 5500ff1753ce0092
stats:
  ac: '12'
  hp: 120 (16d8 + 48)
  speed: walk 30 ft.
  attributes:
    str: 17
    dex: 15
    con: 16
    int: 10
    wis: 13
    cha: 11
  saves: {}
  skills:
    perception: '+5'
    stealth: '+4'
  senses: darkvision 60 ft.
  languages: Common (can't speak in tiger form)
  cr: '4'
stats_meta: Medium humanoid N
titulo_pt_br: Tigre-lobo
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características


### Transmorfose

O tigre-lobisomem pode usar sua ação para se metamorfosear em um híbrido de tigre e humanoide ou em um tigre, ou de volta à sua forma verdadeira, que é humanoide. Suas estatísticas, exceto pelo tamanho, são as mesmas em cada forma. Qualquer equipamento que esteja vestindo ou carregando não é transformado. Ele reverte à sua forma verdadeira se morrer.


### Audição e Olfato Aguçados

O tigre-lobisomem tem vantagem em testes de Sabedoria (Percepção) que dependem de audição ou olfato.


### Bote (Apenas na Forma de Tigre ou Híbrida)

Se o tigre-lobisomem se mover pelo menos 4,5 metros em linha reta em direção a uma criatura e então atingi-la com um ataque de garra no mesmo turno, o alvo deve ser bem-sucedido em um teste de resistência de Força CD 14 ou será derrubado e ficará caído. Se o alvo estiver caído, o tigre-lobisomem pode fazer um ataque de mordida contra ele como uma ação bônus.

## Ações


### Ataques Múltiplos (Apenas na Forma Humanoide ou Híbrida)

Na forma humanoide, o tigre-lobisomem faz dois ataques com cimitarra ou dois ataques com arco longo. Na forma híbrida, ele pode atacar como um humanoide ou fazer dois ataques de garra.


### Mordida (Apenas na Forma de Tigre ou Híbrida)

Corpo a Corpo com Arma: +5 para acertar, alcance 1,5 m, um alvo. *Acerto:* 8 (1d10 + 3) de dano perfurante. Se o alvo for um humanoide, deve ser bem-sucedido em um teste de resistência de Constituição CD 13 ou será amaldiçoado com licantropia de tigre-lobisomem.


### Garra (Apenas na Forma de Tigre ou Híbrida)

Corpo a Corpo com Arma: +5 para acertar, alcance 1,5 m, um alvo. *Acerto:* 7 (1d8 + 3) de dano cortante.


### Cimitarra (Apenas na Forma Humanoide ou Híbrida)

Corpo a Corpo com Arma: +5 para acertar, alcance 1,5 m, um alvo. *Acerto:* 6 (1d6 + 3) de dano cortante.


### Arco Longo (Apenas na Forma Humanoide ou Híbrida)

Ataque à Distância com Arma: +4 para acertar, alcance 45/180 m, um alvo. *Acerto:* 6 (1d8 + 2) de dano perfurante.
