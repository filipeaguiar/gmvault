---
title: Jackalwere
type: monster
draft: false
weight: 10
summary: "```yaml\nname: Choldrith\nsize: Médio\ntype: monstrosidade\nsubtype: null\nalignment: normalmente caótico e mal\nac:\n- ac: 15\n  from:\n    armadura natural: true\nhp:\n  average: 66\n  formula: 12d8 + 12\nspeed:\n  walk: 9 m\n  climb: 9 m\nstats:\n- 12\n- 16\n- 12\n- 10\n- 12\n- 8\nsaves:\n- ability: destreza\n  bonus: 5\n- ability: constituição\n  bonus: 3\n- ability: sabedoria\n  bonus: 3\nsenses:\n- visão no escuro 18 m\n- Percepção passiva 13\nlanguages:\n- Subterrâneo Comum\ncr: '3'\ntrait:\n- name: Colhedor de Presas\n  entries:\n  - type: entries\n    name: Colhedor de Presas\n    entries:\n    - O choldrith pode ter até quatro presas seguradas em suas mãos ou presas em seu\n      corpo, em vez de armas de uma mão. Ele usa estatísticas como as de uma adaga\n      e pode ejetar a presa para fazer um ataque à distância.\n- name: Marcha de Aranha\n  entries:\n  - type: entries\n    name: Marcha de Aranha\n    entries:\n    - O choldrith pode escalar superfícies difíceis,\
  \ inclusive andar de cabeça para\n      baixo no teto, sem precisar fazer um teste de atributo.\n- name: Teia de Andarilho\n  entries:\n  - type: entries\n    name: Teia de Andarilho\n    entries:\n    - O choldrith ignora as restrições de movimento causadas por teias.\naction:\n- name: Adaga\n  entries:\n  - type: entries\n    name: Adaga\n    entries:\n    - '{@atk mw} +5 para atingir, alcance 1,5 m ou alcance 6/18 m, um alvo. {@h}5\n      (1d4 + 3) de dano perfurante mais 10 (3d6) de dano de veneno.'\n- name: Conjuração\n  entries:\n  - type: entries\n    name: Conjuração\n    entries:\n    - O choldrith conjura uma das seguintes magias, usando Sabedoria como sua habilidade\n      de conjuração e CD 11 para suas magias:\n    - type: list\n      items:\n      - À vontade: {@spell thaumaturgy}\n      - 2/magia cada: {@spell darkness}, {@spell web}\nbonus:\n- name: Fúria Demoníaca (2/Dia)\n  entries:\n  - type: entries\n    name: Fúria Demoníaca (2/Dia)\n    entries:\n    - O choldrith\
  \ pode adicionar 1d6 ao dano de cada ataque corpo a corpo que fizer\n      até o início do seu próximo turno. Enquanto essa habilidade estiver ativa, ele\n      também tem resistência a dano de concussão, cortante e perfurante de armas não\n      mágicas.\nflavor:\n- type: entries\n  name: ''\n  entries:\n  - O choldrith governa os soldados chitinosos conhecidos como choldriths, usando-os\n    para capturar humanoides para comida ou sacrifício a Lolth. Provavelmente o híbrido\n    mais bem-sucedido, o choldrith parece um elfo negro rechonchudo com o rosto de\n    uma aranha. Usando seus aracnídeos, os choldriths podem subjugar suas presas com\n    teias e empunhar presas de aranha como punhais mortais. Enquanto alimenta seu\n    rebanho cativo, um choldrith prega que Lolth libertará os cativos se eles provarem\n    que suas almas são superiores às dos drows. Quando um grupo de cativos está devidamente\n    doutrinado, o choldrith manda os choldriths matarem um cativo, que então renascerá\n\
  \    como um novo choldrith, aparentemente curado de sua fé equivocada. À medida que\n    os choldriths continuam sequestrando humanoides, os rituais dos choldriths reúnem\n    os recém-convertidos e os choldriths em um culto a Lolth cada vez maior.\n  source: MM\n  page: 62\n```"
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
