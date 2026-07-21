## Why

Durin (Monk), Einvor (Barbarian) e Violeta (Sorcerer) dependem de recursos consumíveis cruciais de suas respectivas classes (Pontos de Foco, Fúria e Pontos de Feitiçaria). Atualmente, estes recursos não são exibidos com o devido destaque nas fichas de personagem em HTML, dificultando o rastreamento e consumo em tempo real durante as sessões.

## What Changes

* **Destaque Visual Superior:** Adicionar blocos de contadores visuais no topo das fichas de personagem (logo abaixo dos metadados principais e ao lado dos espaços de magia).
* **CSS Temático Customizado:** Criar estilos CSS dedicados para cada tipo de recurso (Fúria, Foco, Pontos de Feitiçaria) para dar apelo visual condizente com a classe.
* **Mapeamento de Dados:** Estruturar estes consumíveis nas fichas Markdown dos personagens (com propriedades de valor atual e valor máximo) para alimentação automática no Hugo e no site.

## Capabilities

### New Capabilities
- `character-consumables-display`: Rastreamento estrutural e renderização visual rica dos contadores de recursos de classe no topo das fichas.

### Modified Capabilities
<!-- Nenhuma -->

## Impact

* **Layouts:** Edição nos layouts das fichas de personagem (`layouts/character/single.html` ou parciais correlatas).
* **Fichas:** Modificações nos arquivos Markdown dos personagens jogadores para definir os novos campos.
* **Assets:** Atualização em `assets/css/` para os novos estilos visuais.
