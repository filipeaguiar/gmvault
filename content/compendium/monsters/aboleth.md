---
title: Aboleth
params:
  kind: monster
draft: true
weight: 10
summary: "```markdown\n---\nname: Manes\nsize: Tiny\ntype: fiend\nsubtype: demon\ntags:\n  - demon\nalignment: chaotic evil\nac: 9\nhp: 9\nhit_dice: 2d6 + 2\nspeed: 20 ft.\nstats:\n  - 10\n  - 11\n  - 12\n  - 5\n  - 8\n  - 3\ndamage_resistances: cold, fire, lightning\ndamage_immunities: poison\ncondition_immunities: charmed, frightened, poisoned\nsenses: darkvision 60 ft., passive Perception 9\nlanguages: understands Abyssal but can't speak\ncr: 0.125\nreaction:\n  - name: '**Acidic Ichor.**'\n    desc: When the manes is slain, its dissolving body sprays acid in a 5-foot line in a direction of its choosing. Each creature in that area must succeed on a DC 10 Dexterity saving throw or take 2 (1d4) acid damage.\n\"trait\":\n  - name: '**Death Throes.**'\n    desc: When the manes dies, it leaves behind a cloud of vapor that dissipates at the end of the turn, and a crawling mass of maggots that rapidly dissipates.\nattacks:\n  - name: '**Claw.**'\n    desc: \"_Melee Weapon Attack:_ +2 to hit,\
  \ reach 5 ft., one target. _Hit:_ 5 (2d4) slashing damage.\"\n\"spellcasting\":\n  - name: '**Spellcasting.**'\n    desc: \"The manes's innate spellcasting ability is Charisma (spell save DC 8). It can innately cast the following spells, requiring no material components:\\n\\nAt will: _[dancing lights](/spells/dancing-lights/)_\\n1/day each: _[darkness](/spells/darkness/)_ (centered on self only), _[faerie fire](/spells/faerie-fire/)_\"\n```\n\n**Manes**são as almas de humanos, elfos, anões e outros mortais que foram enviados para o Abismo após a morte. Eles são as formas de vida demoníacas mais baixas, atormentados e caóticos, mas não totalmente sem propósito. Os senhores demônios constantemente os transformam em formas mais poderosas de demônios, enquanto os próprios manes buscam constantemente infligir sofrimento e morte a outros para escapar de sua miséria."
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
  entity_name: Aboleth
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: db56ad72a7edb04a
stats:
  ac: '17'
  hp: 135 (18d10 + 36)
  speed: walk 10 ft., swim 40 ft.
  attributes:
    str: 21
    dex: 9
    con: 15
    int: 18
    wis: 15
    cha: 18
  saves:
    con: '+6'
    int: '+8'
    wis: '+6'
  skills:
    history: '+12'
    perception: '+10'
  senses: darkvision 120 ft.
  languages: Deep Speech, telepathy 120 ft.
  cr: '10'
stats_meta: Large aberration L/E
titulo_pt_br: Aboleth
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Anfíbio
O aboleth pode respirar ar e água.

### Nuvem Mucosa
Enquanto submerso, o aboleth é cercado por um muco transformador. Uma criatura que toca o aboleth ou que o atinge com um ataque corpo a corpo enquanto está a até 5 pés dele deve ser bem-sucedida em um teste de resistência de Constituição CD 14. Em caso de falha, a criatura fica doente por 1d4 horas. A criatura doente só pode respirar debaixo d'água.

### Telepatia Sondadora
Se uma criatura se comunicar telepaticamente com o aboleth, o aboleth descobre os maiores desejos da criatura se puder vê-la.

## Ações

### Ataques Múltiplos
O aboleth faz três ataques com os tentáculos.

### Tentáculo
Ataque Corpo a Corpo com Arma: +9 para acertar, alcance 10 pés, um alvo. Acerto: 12 (2d6 + 5) de dano de concussão. Se o alvo for uma criatura, ela deve ser bem-sucedida em um teste de resistência de Constituição CD 14 ou fica doente. A doença não tem efeito por 1 minuto e pode ser removida por qualquer magia que cure doenças. Após 1 minuto, a pele da criatura doente se torna translúcida e viscosa, a criatura não pode recuperar pontos de vida a menos que esteja submersa, e a doença pode ser removida apenas por curar ou outra magia de cura de doença de 6º círculo ou superior. Quando a criatura está fora de um corpo d'água, ela sofre 6 (1d12) de dano de ácido a cada 10 minutos, a menos que umidade seja aplicada à pele antes que 10 minutos tenham se passado.

### Cauda
Ataque Corpo a Corpo com Arma: +9 para acertar, alcance 10 pés, um alvo. Acerto: 15 (3d6 + 5) de dano de concussão.

### Escravizar (3/Dia)
O aboleth escolhe uma criatura que possa ver, dentro de 30 pés dele. O alvo deve ser bem-sucedido em um teste de resistência de Sabedoria CD 14 ou fica encantado magicamente pelo aboleth até que ele morra ou até que esteja em um plano de existência diferente do alvo. O alvo enfeitiçado está sob o controle do aboleth e não pode usar reações, e o aboleth e o alvo podem se comunicar telepaticamente entre si a qualquer distância.

Sempre que o alvo enfeitiçado sofre dano, ele pode repetir o teste de resistência. Em caso de sucesso, o efeito termina. Não mais que uma vez a cada 24 horas, o alvo também pode repetir o teste de resistência quando estiver a pelo menos 1 milha de distância do aboleth.

## Ações Lendárias

### Detectar
O aboleth faz um teste de Sabedoria (Percepção).

### Golpe de Cauda
O aboleth faz um ataque com a cauda.

### Dreno Psíquico (Custa 2 Ações)
Uma criatura enfeitiçada pelo aboleth sofre 10 (3d6) de dano psíquico, e o aboleth recupera pontos de vida iguais ao dano sofrido pela criatura.
