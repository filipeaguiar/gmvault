---
title: Roper
params:
  kind: monster
draft: false
weight: 10
summary: "Se a asa de uma borboleta sofre um rasgo, o animal jamais voará novamente. De forma conveniente, para os sprites (Sprite), um pouco de gosma de lesma aplicada na área danificada repara a asa afetada quase imediatamente.\n\nDiminutos Protetores da Floresta. Os sprites são minúsculos seres feéricos que atuam como batedores, espiões e guardiões nas matas. Consideram-se os defensores da floresta, mas são vistos por observadores mais sábios como uma espécie de sistema imunológico — agentes biológicos projetados para proteger as fronteiras de regiões silvestres intactas dos estragos causados por civilizações em expansão ou pela propagação de criaturas malignas.\n\nObservadores da Natureza. Os sprites constroem pequenas moradias nas copas do sub-bosque. Pode ser o oco de uma árvore, um aglomerado de cogumelos, ou uma estrutura improvisada com galhos. Alguns domam animais silvestres e os utilizam como montaria, e todos criam inúmeros esconderijos e clareiras particulares entre a vegetação,\
  \ onde guardam alimentos e tesouros.\n\nAlheios à Mortalidade. Embora sua expectativa de vida natural possa se estender por séculos, os sprites sabem que também podem morrer de velhice. Preferem não pensar nessa possibilidade e, diante de qualquer desconforto relacionado ao tema, simplesmente fogem do assunto.\n\n> ### Sprite Batedor\n> \n> *Miúdo, feérico, qualquer tendência*\n> \n> ---\n> \n> **Classe de Armadura** 15 (armadura de couro)\n> **Pontos de Vida** 10 (4d4)\n> **Deslocamento** 9 m, voo 12 m\n> \n> ---\n> \n> | FOR | DES | CON | INT | SAB | CAR |\n> |:---:|:---:|:---:|:---:|:---:|:---:|\n> | 4 (-3) | 18 (+4) | 10 (+0) | 14 (+2) | 13 (+1) | 11 (+0) |\n> \n> ---\n> \n> **Perícias** Furtividade +8, Investigação +6, Percepção +5\n> **Sentidos** visão no escuro 18 m, Percepção passiva 15\n> **Idiomas** Comum, élfico, silvestre\n> **Nível de Desafio** 1/4 (XP 50)\n> **Bônus de Proficiência** +2\n> \n> ---\n> \n> ***Visão do Coração (Heart Sight).*** O sprite toca uma criatura e descobre\
  \ magicamente o estado emocional atual dela. Se o alvo falhar em um teste de resistência de Carisma CD 10, o sprite também saberá a tendência da criatura. Celtas, feéricos e criaturas imunes a efeitos de enfeitiçamento são automaticamente bem-sucedidos no teste de resistência.\n> \n> ### Ações\n> \n> ***Espada Curta.*** *Ataque Corpo a Corpo com Arma:* +6 para atingir, alcance 1,5 m, um alvo. *Dano:* 7 (1d6 + 4) de dano Perfurante mais 2 (1d4) de dano Venenoso.\n> \n> ***Arco Curto.*** *Ataque à Distância com Arma:* +6 para atingir, alcance 24/96 m, um alvo. *Dano:* 7 (1d6 + 4) de dano Perfurante, e o alvo deve ser bem-sucedido em um teste de resistência de Constituição CD 10 ou sofrerá a condição Envenenado por 1 minuto. Se o teste de resistência falhar por 5 ou mais, o alvo também cairá Inconsciente. O alvo repete o teste de resistência ao final de cada um de seus turnos, terminando o efeito sobre si mesmo em caso de sucesso."
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
  entity_name: Roper
  remote_file: bestiary/bestiary-mm.json
  remote_key: monster
  remote_id: 4245a0198f6b0ac8
stats:
  ac: '20'
  hp: 93 (11d10 + 33)
  speed: walk 10 ft., climb 10 ft.
  attributes:
    str: 18
    dex: 8
    con: 17
    int: 7
    wis: 16
    cha: 6
  saves: {}
  skills:
    perception: '+6'
    stealth: '+5'
  senses: darkvision 60 ft.
  languages: ''
  cr: '5'
stats_meta: Large monstrosity N/E
titulo_pt_br: Estrangulador
translation:
  source_language: en
  target_language: pt-BR
  engine: openai-compatible
  status: machine_translated
  model: deepseek-v4-pro
---

## Características

### Aparência Falsa
Enquanto o roper permanece imóvel, ele é indistinguível de uma formação rochosa comum de caverna, como uma estalagmite.

### Tentáculos Preensores
O roper pode ter até seis tentáculos de cada vez. Cada tentáculo pode ser atacado (CA 20; 10 pontos de vida; imunidade a dano de veneno e dano psíquico). Destruir um tentáculo não causa dano ao roper, que pode projetar um tentáculo substituto no próximo turno dele. Um tentáculo também pode ser quebrado se uma criatura usar uma ação e obtiver sucesso em um teste de Força CD 15 contra ele.

### Escalada de Aranha
O roper pode escalar superfícies difíceis, incluindo de cabeça para baixo no teto, sem precisar fazer um teste de atributo.

## Ações

### Ataques Múltiplos
O roper realiza quatro ataques com seus tentáculos, usa Enrolar e realiza um ataque com sua mordida.

### Mordida
mw 7 para acertar, alcance 1,5 m, um alvo. {@h}22 (4d8 + 4) de dano perfurante.

### Tentáculo
mw 7 para acertar, alcance 15 m, uma criatura. {@h}O alvo fica agarrado (CD para escapar 15). Até o agarrão terminar, o alvo estará contido e terá desvantagem em testes de Força e testes de resistência de Força, e o roper não poderá usar o mesmo tentáculo em outro alvo.

### Enrolar
O roper puxa cada criatura agarrada por ele até 7,5 m diretamente para si.
