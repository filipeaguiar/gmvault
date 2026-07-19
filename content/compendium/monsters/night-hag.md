---
title: Night Hag
params:
  kind: monster
draft: false
weight: 10
summary: "```yaml\nname: Mestre da Caçada\nsize: Médio\ntype: Fey\nac:\n- 18\n- armadura de couro batido\nhp:\n  average: 271\n  formula: 34\nspeed:\n  walk: 20\n  climb: 20\nstr: 18\ndex: 15\ncon: 18\nint: 12\nwis: 20\ncha: 18\nsave:\n  str: '+9'\n  dex: '+7'\n  wis: '+10'\n  cha: '+9'\nskill:\n  arcanismo: '+6'\n  atletismo: '+9'\n  lidar com animais: '+10'\n  natureza: '+6'\n  percepção: '+10'\n  furtividade: '+9'\n  sobrevivência: '+10'\nresist:\n- ácido\n- fogo\n- relâmpago\n- trovão\n- concussão de armas não mágicas\nimmune:\n- frio\n- veneno\n- envenenado\n- agarrado\n- paralisado\n- enfeitiçado\n- contido\n- exaustão\n- amedrontado\nsenses:\n  visão no escuro 36m: true\n  visão verdadeira 36m: true\n  passivo: 20\nlanguages:\n- Comum\n- Élfico\n- Silvestre\n- fala com bestas\n- fala com plantas\ncr: 18\nspellcasting:\n  name: Conjuração Inata\n  headerEntries:\n  - A habilidade inata de conjuração do mestre da caçada é Sabedoria (CD de resistência de magia 18, +10 para acertar com\
  \ ataques mágicos). O Mestre da Caçada pode conjurar as seguintes magias inatamente, sem necessidade de componentes materiais:\n  spells:\n    3/dia cada:\n    - Tempestade de Gelo\n    - Muralha de Gelo\n    - Mensageiro Animal*\n    1/dia:\n    - Encontrar o Caminho\n    - Tempestade de Vingança\n    - Mover-se Livremente (apenas no Monte das Brumas)\n  ability: sab\ntrait:\n- name: Andaime do Caçador\n  entries:\n  - 'O mestre da caçada tem três cães de caça, um falcão de caça e um cavalo de caça (descritos abaixo). O mestre da caçada pode ver através dos olhos de qualquer um de seus cães de caça ou de sua ave de rapina e falar através deles.'\n- name: Resiliência do Caçador\n  entries:\n  - 'Se o dano reduzir o mestre da caçada a 0 pontos de vida, ele deve fazer uma resistência de Constituição com CD 17 a menos que o dano seja de uma arma mágica ou de um ataque crítico. Caso passe, ele cai para 15 pontos de vida em vez disso.'\n- name: Faro Apurado\n  entries:\n  - 'O mestre da caçada\
  \ tem vantagem em testes de Sabedoria (Percepção) relacionados ao olfato.'\n- name: Mestre do Monte\n  entries:\n  - 'Enquanto estiver no Monte das Brumas, conjurar Mover-se Livremente e não puder ser alvo de adivinhação ou rastreado.'\n- name: Mestre das Bestas\n  entries:\n  - Bestas e feras com Inteligência 3 ou menos têm desvantagem em resistências de Sabedoria contra as magias, traços e ações do mestre da caçada.\naction:\n- name: Ataque Múltiplo\n  entries:\n  - O Mestre da Caçada faz um ataque com seu chicote ou espada longa e um ataque com seu arco longo. Pode usar Chamar a Matilha no lugar de um desses ataques.\n- name: Chicote\n  entries:\n  - |-\n    *Ataque Corpo a Corpo com Arma*: +9 para atingir, alcance 3m, dois alvos. *Acerto*: 9 (1d6 + 6) de dano contundente. O Mestre da Caçada pode puxar um alvo Grande ou menor em até 3m e derrubá-lo.\n    Se o alvo for derrubado, o Mestre da Caçada pode atacar o alvo caído imediatamente com uma ação bônus.\n    O alvo está sob o efeito\
  \ do traço Presa Marcada do Mestre da Caçada.\n- name: Espada Longa\n  entries:\n  - |-\n    *Ataque Corpo a Corpo com Arma*: +9 para atingir, alcance 1,5m, um alvo. *Acerto*: 10 (1d8 + 6) de dano cortante.\n- name: Arco Longo\n  entries:\n  - |-\n    *Ataque à Distância com Arma*: +7 para atingir, alcance 45/180m, um alvo. *Acerto*: 11 (1d8 + 6) de dano perfurante. O alvo está sob o efeito do traço Presa Marcada do Mestre da Caçada.\n- name: Chamar a Matilha\n  entries:\n  - 'O Mestre da Caçada conjura um cão espectral para atacar uma criatura que esteja sob o efeito de Presa Marcada. A matilha invocada se move até 18m e ataca a criatura marcada. *Ataque Corpo a Corpo com Arma*: +9 para acertar, alcance 1,5m, um alvo. *Acerto*: 46 (8d10 + 2) de dano de força. O cão espectral então desaparece.'\n- name: Presa Marcada\n  entries:\n  - 'Ataques à distância e corpo a corpo do Mestre da Caçada marcam a criatura alvo como presa. A marca dura por 1 hora ou até ser removida por uma magia de remover\
  \ maldição ou similar.'\n- name: Chamado do Caçador\n  entries:\n  - 'O Mestre da Caçada emite um chamado estrondoso, que é audível a até 300m. Todos os cães de caça sob seu comando recebem +5 em jogadas de ataque e dano por 3 rodadas. Demora 1 rodada para que todos os cães de caça cheguem ao Mestre da Caçada. Se um cão de caça for morto, o mestre da caçada pode designar um cão de caça líder de matilha para assumir o seu lugar. Esta criatura se tornará um Cão de Caça Líder de Matilha em 1d4 dias.'\nbonus_action:\n- name: Movimento Furtivo\n  entries:\n  - 'O Mestre da Caçada pode usar a ação Esconder-se como uma ação bônus.'\nlegendary_group:\n  name: Mestre da Caçada\n  source: CoS\n  page: 199\nlegendary:\n  legendaryActionsHeader: O Mestre da Caçada pode realizar 3 ações lendárias, escolhendo entre as opções abaixo. Apenas uma opção de ação lendária pode ser usada por vez e somente no final do turno de outra criatura. O Mestre da Caçada recupera as ações lendárias gastas no início de\
  \ seu turno.\n  actions:\n  - name: Golpe de Chicote\n    entries:\n    - O Mestre da Caçada faz um ataque com seu chicote.\n  - name: Avançar (Custa 2 Ações)\n    entries:\n    - O Mestre da Caçada se move até sua velocidade.\n  - name: Invocar a Tempestade (Custa 3 Ações)\n    entries:\n    - 'O Mestre da Caçada conjura Tempestade de Gelo ou Muralha de Gelo.'\nenvironment:\n- Floresta\n- Monte\nsoundClip:\n  type: internal\n  path: bestiary/Mestre da Caçada.mp3\nsubhead: |-\n  ***Alma corrompida pelo medo e solidão nas brumas.***\n  ***Criatura das brumas. Odeia os vivos.***\n  ***Assombra o Monte das Brumas.***\ntraitsMd:\n- '| **Resiliência do Caçador.** Se o dano reduzir o mestre da caçada a 0 pontos de vida, ele deve fazer uma resistência de Constituição com CD 17 a menos que o dano seja de uma arma mágica ou de um ataque crítico. Caso passe, ele cai para 15 pontos de vida em vez disso.'\n- '| **Faro Apurado.** O mestre da caçada tem vantagem em testes de Sabedoria (Percepção) relacionados\
  \ ao olfato.'\n- '| **Mestre do Monte.** Enquanto estiver no Monte das Brumas, conjurar *Mover-se Livremente* e não puder ser alvo de adivinhação ou rastreado.'\n- '| **Mestre das Bestas.** Bestas e feras com Inteligência 3 ou menos têm desvantagem em resistências de Sabedoria contra as magias, traços e ações do mestre da caçada.'\nactionsMd:\n- |-\n  **Ataque Múltiplo.** O Mestre da Caçada faz um ataque com seu chicote ou espada longa e um ataque com seu arco longo. Pode usar Chamar a Matilha no lugar de um desses ataques.\n\n  **Chicote.** *Ataque Corpo a Corpo com Arma*: +9 para atingir, alcance 3m, dois alvos. *Acerto*: 9 (1d6 + 6) de dano contundente. O Mestre da Caçada pode puxar um alvo Grande ou menor em até 3m e derrubá-lo. Se o alvo for derrubado, o Mestre da Caçada pode atacar o alvo caído imediatamente com uma ação bônus. O alvo está sob o efeito do traço Presa Marcada do Mestre da Caçada.\n\n  **Espada Longa.** *Ataque Corpo a Corpo com Arma*: +9 para atingir, alcance 1,5m,\
  \ um alvo. *Acerto*: 10 (1d8 + 6) de dano cortante.\n\n  **Arco Longo.** *Ataque à Distância com Arma*: +7 para atingir, alcance 45/180m, um alvo. *Acerto*: 11 (1d8 + 6) de dano perfurante. O alvo está sob o efeito do traço Presa Marcada do Mestre da Caçada.\n\n  **Chamar a Matilha.** O Mestre da Caçada conjura um cão espectral para atacar uma criatura que esteja sob o efeito de Presa Marcada. A matilha invocada se move até 18m e ataca a criatura marcada. *Ataque Corpo a Corpo com Arma*: +9 para acertar, alcance 1,5m, um alvo. *Acerto*: 46 (8d10 + 2) de dano de força. O cão espectral então desaparece.\n\n  **Presa Marcada.** Ataques à distância e corpo a corpo do Mestre da Caçada marcam a criatura alvo como presa. A marca dura por 1 hora ou até ser removida por uma magia de remover maldição ou similar.\n\n  **Chamado do Caçador.** O Mestre da Caçada emite um chamado estrondoso, que é audível a até 300m. Todos os cães de caça sob seu comando recebem +5 em jogadas de ataque e dano por 3\
  \ rodadas. Demora 1 rodada para que todos os cães de caça cheguem ao Mestre da Caçada. Se um cão de caça for morto, o mestre da caçada pode designar um cão de caça líder de matilha para assumir o seu lugar. Esta criatura se tornará um Cão de Caça Líder de Matilha em 1d4 dias.\nbonus_actionsMd:\n- '**Movimento Furtivo.** O Mestre da Caçada pode usar a ação Esconder-se como uma ação bônus.'\nlegendary_actionsMd:\n- |-\n  O Mestre da Caçada pode realizar 3 ações lendárias, escolhendo entre as opções abaixo. Apenas uma opção de ação lendária pode ser usada por vez e somente no final do turno de outra criatura. O Mestre da Caçada recupera as ações lendárias gastas no início de seu turno.\n\n  **Golpe de Chicote.** O Mestre da Caçada faz um ataque com seu chicote.\n\n  **Avançar (Custa 2 Ações).** O Mestre da Caçada se move até sua velocidade.\n\n  **Invocar a Tempestade (Custa 3 Ações).** O Mestre da Caçada conjura *Tempestade de Gelo* ou *Muralha de Gelo*.\nfluff:\n  type: monstro\n  entries:\n\
  \  - |-\n    Há muito tempo, nas brumas de Baróvia, existiu um homem que amava a caça mais do que tudo. Tão grande era seu amor, que sua essência se fundiu para sempre com as brumas da terra.\n\n    Agora, o Mestre da Caçada cavalga mais uma vez com sua matilha infernal. Nenhuma criatura viva é páreo para sua ira e frustração, e ele não descansará até que todos os vivos à sua volta sejam destruídos ou tenham fugido aterrorizados da floresta.\n  - '*Nota: O Mestre da Caçada foi importado do livro \"Curse of Strahd\", juntamente com suas criaturas companheiras (Falcão de Caça, Cão de Caça e Cavalo de Caça).*'\n  images:\n  - type: image\n    href: bestiary/Mestre da Caçada.webp\n    title: Mestre da Caçada\n  - type: external\n    href: >-\n      https://i1.wp.com/www.ericsfrey.com/wp-content/uploads/2017/12/Bulmahn_Mark_HKV9.jpg\notherSources:\n- source: CoS\n  page: 199\n  name: Mestre da Caçada\n  id: 0fbb9a2a\n  displayName: Mestre da Caçada (CoS)\n  group: monstro\n```"
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
titulo_pt_br: Bruxa da Noite
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


### Itens da Bruxa Noturna

Uma bruxa noturna carrega dois itens mágicos muito raros que ela mesma deve criar para si. Se qualquer um dos objetos for perdido, a bruxa noturna fará grandes esforços para recuperá-lo, já que criar uma nova ferramenta leva tempo e esforço.


### Pedra do Coração

Esta gema negra reluzente permite que uma bruxa noturna se torne etérea enquanto estiver em sua posse. O toque de uma MM também cura qualquer doença. Criar uma pedra do coração leva 30 dias.


### Bolsa de Almas

Quando um humanoide maligno morre como resultado do Assombro Noturno de uma bruxa noturna, a bruxa captura a alma nesta bolsa negra feita de carne costurada. Uma MM pode conter apenas uma alma maligna por vez, e somente a bruxa noturna que criou a bolsa pode capturar uma alma com ela. Criar uma bolsa de almas leva 7 dias e um sacrifício humanoide (cuja carne é usada para fazer a bolsa).

## Ações


### Garras (Apenas na Forma de Bruxa)

Corpo a Corpo com Arma: +7 para atingir, alcance 1,5 m, um alvo. Acerto: 13 (<span class="dice+" data-roll-notation="2d8+4">2d8 + 4</span>) de dano cortante.


### Mudar Forma

A bruxa se transforma magicamente em uma fêmea humanoide Pequena ou Média, ou de volta à sua forma verdadeira. Suas estatísticas são as mesmas em cada forma. Qualquer equipamento que ela esteja vestindo ou carregando não é transformado. Ela reverte à sua forma verdadeira se morrer.


### Eteridade

A bruxa entra magicamente no Plano Etéreo a partir do Plano Material, ou vice-versa. Para fazê-lo, a bruxa deve ter uma pedra do coração em sua posse.


### Assombro Noturno (1/Dia)

Enquanto no Plano Etéreo, a bruxa toca magicamente um humanoide adormecido no Plano Material. Uma magia de proteção contra o bem e o mal conjurada no alvo impede este contato, assim como um círculo mágico. Enquanto o contato persistir, o alvo tem visões terríveis. Se estas visões durarem pelo menos 1 hora, o alvo não ganha nenhum benefício de seu descanso, e seus Pontos de Vida máximos são reduzidos em 5 (<span class="dice+" data-roll-notation="1d10">1d10</span>). Se este efeito reduzir os Pontos de Vida máximos do alvo a 0, o alvo morre e, se o alvo era maligno, sua alma fica presa na bolsa de almas da bruxa. A redução nos Pontos de Vida máximos do alvo dura até ser removida pela magia restauração maior ou magia similar.
