## ADDED Requirements

### Requirement: Class Consumables Structure in Character Markdown
A ficha de personagem jogador em Markdown MUST conter uma estrutura sob `char_info.consumables` para armazenar recursos consumíveis de classe. Esta estrutura SHALL conter as chaves `name`, `current`, `max` e `type`.

#### Scenario: Markdown metadata schema definition
- **WHEN** o Markdown da ficha de Durin (Monk) for carregado
- **THEN** ele deve conter a estrutura sob `char_info.consumables` com `name: "Pontos de Foco"`, `current: 3`, `max: 3` e `type: "focus"`.

### Requirement: Consumables visual blocks in HTML rendering
O layout do Hugo de renderização de fichas de personagens SHALL ler a lista de `consumables` e MUST desenhar blocos visuais de contadores contendo o valor atual, valor máximo e nome do recurso no topo da página do personagem.

#### Scenario: Visual blocks rendering on webpage
- **WHEN** o site estático do Hugo for compilado e a página de Violeta for acessada no navegador
- **THEN** a seção superior deve renderizar um bloco de contador indicando "Pontos de Feitiçaria: 3 / 3".

### Requirement: Dedicated CSS Styles for Class Consumables
Regras de estilo CSS dedicadas SHALL ser declaradas para cada tipo de classe (`badge-rage`, `badge-focus`, `badge-sorcery`) no arquivo de estilo principal e MUST aplicar cores temáticas correspondentes.

#### Scenario: Theme colors application
- **WHEN** os blocos de recursos consumíveis forem desenhados na página
- **THEN** o bloco de Fúria do Bárbaro deve receber a classe CSS `consumable-rage` exibindo cores avermelhadas, e o de Pontos de Foco do Monge deve receber a classe `consumable-focus` com cores azuladas.
