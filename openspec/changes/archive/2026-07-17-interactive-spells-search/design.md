## Context

Adicionar magias a fichas estáticas requer esforço duplo: importar os dados estruturados corretos (backend) e exibi-los de forma interativa (frontend). Além disso, os Spell Slots (espaços de magia) do personagem devem ser calculados com precisão baseado no nível e classe para evitar edições manuais exaustivas.

## Goals / Non-Goals

**Goals:**
- **Backend (Slots)**: Embutir uma tabela simples de progressão de Full Casters / Half Casters / Pact Magic. O script calculará automaticamente os slots baseado na classe/nível informados e injetará `spell_slots` no frontmatter YAML do markdown.
- **Backend (Spells)**: Busca interativa (via `dnd_utils.py`) e inclusão automatizada no compêndio e na ficha Markdown.
- **Frontend (UI)**: Layout limpo agrupando magias por nível.
- **Frontend (UX)**: O Hugo renderizará Checkboxes de "Spell Slots" rastreáveis lendo diretamente do dicionário `spell_slots` injetado no YAML.
- **VTT**: Integração com a extensão customizada do Owlbear (botão/link com tag `data-roll-notation`) gerada dinamicamente pelo Hugo na descrição da magia para rolagem dos dados.

**Non-Goals:**
- Não iremos persistir as marcações diárias de magias preparadas e slots gastos feitas no frontend. O estado viverá em `localStorage` ou no DOM da página até ser limpo/recarregado, servindo apenas para a sessão atual.

## Decisions

- **Cálculo de Slots**: Será feito no backend (`interactive_cli.py` ou `dnd_utils.py`) cruzando a classe e o nível (informados na criação). Essa é a forma mais resiliente para sites estáticos, pois os slots viram um dicionário YAML estático (ex: `spell_slots: {1: 4, 2: 3}`) fácil de corrigir manualmente caso ocorra um Homebrew.
- **DOM Structure**: Cada magia será renderizada num container. Teremos duas divs pai: `#prepared-spells` e `#class-spells`.
- **Vanilla JS**: O script JS vai apenas procurar checkboxes marcados no `#class-spells` e clonar ou mover os nós HTML (accordions) para o `#prepared-spells`.
- **Accordions**: Usaremos `details`/`summary` nativos.
- **Integração de Dados**: Se a magia importada do 5e.tools possui arrays de rolagem de dano/cura (como `["8d6"]` para fireball), injetaremos a class `dice+` e o data attribute para o VTT.

## Risks / Trade-offs

- **Risk**: Classes multiclasse requerem cálculo avançado de spell slots (somar níveis totais de conjurador).
- **Mitigation**: Na primeira iteração, faremos o cálculo assumindo conjurador de classe única (Single Class). Se houver multiclasse, o usuário pode corrigir os slots editando o arquivo markdown manualmente.
