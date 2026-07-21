# monster-rolls-and-combat-tracker Specification

## Purpose
TBD - created by archiving change add-monster-rolls-and-combat-tracker. Update Purpose after archive.
## Requirements
### Requirement: Monster Statblock Roll Enhancement
O template de statblock de monstro (`statblock.html`) SHALL renderizar atributos de rolagem com as propriedades `data-roll-notation` e `class="roll-ready"` para todos os modificadores de atributos, testes de resistência e perícias.

#### Scenario: Attribute modifiers become rollable
- **WHEN** a página do monstro Aboleth for renderizada no Hugo
- **THEN** o valor do modificador de Força `+5` deve possuir a propriedade `data-roll-notation="1d20+5"`.

### Requirement: Global Javascript Roll Engine
O script JavaScript global `roll-engine.js` SHALL ser carregado em todas as páginas do site. Ele MUST interceptar cliques em qualquer elemento que possua `data-roll-notation`. Se estiver rodando dentro de um iframe, ele SHALL enviar o pedido via `postMessage`. Se estiver rodando fora de um iframe (navegador normal), ele MUST calcular a rolagem localmente e exibir o resultado formatado em um toast de notificação no canto da tela.

#### Scenario: Clicking rollable element outside iframe
- **WHEN** o usuário clicar no botão de ataque do monstro fora de um iframe
- **THEN** um toast elegante no canto da tela deve exibir o resultado da rolagem contendo os dados individuais e o total.

### Requirement: Auto-Parsing of Dice Formulas in Actions
O script `roll-engine.js` SHALL realizar um parsing automático no conteúdo textual do bloco de estatísticas do monstro para identificar padrões de bônus de ataque (como `+X para acertar` ou `+X to hit`) e fórmulas de dados (como `XdY+Z` ou `XdY`), convertendo-os dinamicamente em elementos roláveis `[data-roll-notation]`.

#### Scenario: Action details formula enhancement
- **WHEN** a descrição do ataque da cauda do Aboleth contendo `(3d6 + 5)` for carregada na página
- **THEN** a fórmula `3d6 + 5` deve ser automaticamente convertida em um link com `data-roll-notation="3d6+5"`.

### Requirement: Single-Screen Combat Tracker
O site SHALL fornecer uma página de combate `/combat/` (Combat Tracker). A página MUST carregar de forma assíncrona o catálogo de monstros em `statblocks.json`. Ela MUST disponibilizar uma caixa de notas de texto livre onde o GM digita os monstros do combate (ex: "2 Bandit, 1 Acolyte"). O sistema MUST renderizar instantaneamente os statblocks de todos os monstros especificados na mesma tela, oferecendo contadores rápidos de HP individualizados e rolagens integradas via `roll-engine.js`.

#### Scenario: Parsing notes and rendering monsters
- **WHEN** o GM digita "2 Bandit" no Combat Tracker
- **THEN** a tela deve instanciar e exibir dois blocos de estatísticas de Bandit com nomes distintos ("Bandit 1", "Bandit 2") e inputs individuais para controle de HP atual.

