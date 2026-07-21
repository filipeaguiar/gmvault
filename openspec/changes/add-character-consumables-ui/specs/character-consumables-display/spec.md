## ADDED Requirements

### Requirement: Class Consumables Structure in Character Markdown
As fichas de personagens jogadores em Markdown (especialmente Bárbaro, Monge e Feiticeiro) devem conter uma estrutura em seu front matter para armazenar recursos consumíveis específicos da classe. Esta estrutura deve ficar sob a chave `consumables` dentro de `char_info`. Cada item na lista de consumíveis deve ter as seguintes propriedades:
* `name`: Nome legível do recurso (ex: "Fúria", "Pontos de Foco", "Pontos de Feitiçaria").
* `current`: Valor atual do recurso.
* `max`: Valor máximo disponível.
* `type`: Tipo identificador de classe para estilização (ex: `rage`, `focus`, `sorcery_points`).

#### Scenario: Markdown metadata schema definition
- **WHEN** o Markdown da ficha de Durin (Monk) for carregado
- **THEN** ele deve conter a estrutura sob `char_info.consumables` com `name: "Pontos de Foco"`, `current: 3`, `max: 3` e `type: "focus"`.

### Requirement: Consumables visual blocks in HTML rendering
O layout do Hugo de renderização de fichas de personagens deve ler a lista de `consumables` e desenhar blocos visuais de contadores contendo o valor atual, valor máximo e nome do recurso no topo da página do personagem. Estes blocos devem ser posicionados na mesma seção superior dos blocos de slots de magia.

#### Scenario: Visual blocks rendering on webpage
- **WHEN** o site estático do Hugo for compilado e a página de Violeta for acessada no navegador
- **THEN** a seção superior deve renderizar um bloco de contador indicando "Pontos de Feitiçaria: 3 / 3".

### Requirement: Dedicated CSS Styles for Class Consumables
Devem ser criadas regras de estilo CSS dedicadas no arquivo principal de estilo (`assets/css/` ou equivalente) para os contadores visuais de cada classe, utilizando cores temáticas harmoniosas e contrastantes (ex: tons de vermelho/laranja para fúria de bárbaro, tons de azul-celeste/energia para pontos de foco de monge, e roxo/arcano profundo para pontos de feitiçaria de feiticeiro).

#### Scenario: Theme colors application
- **WHEN** os blocos de recursos consumíveis forem desenhados na página
- **THEN** o bloco de Fúria do Bárbaro deve receber a classe CSS `consumable-rage` exibindo cores avermelhadas, e o de Pontos de Foco do Monge deve receber a classe `consumable-focus` com cores azuladas.
