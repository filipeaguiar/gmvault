## ADDED Requirements

### Requirement: Character rule content is resolved from compendium references
A ficha de personagem SHALL use referências internas (`ref` ou `compendium_refs`) para resolver no compêndio o conteúdo compartilhado de ações, traços raciais, talentos, características de classe, magias e equipamentos. O layout SHALL use `site.GetPage` durante o build e renderizar o conteúdo da página resolvida sem copiar a descrição para o frontmatter.

#### Scenario: Pinky action uses a compendium page
- **WHEN** uma ação de Pinky possui `ref: /compendium/rules/sneak-attack/`
- **THEN** a ficha SHALL renderizar o título e o conteúdo da nota resolvida do compêndio, mantendo na ficha apenas o nome e os dados operacionais da ação

#### Scenario: Referenced spell and equipment use canonical content
- **WHEN** uma magia ou equipamento da ficha possui uma referência interna válida
- **THEN** o layout SHALL obter descrição e metadados da página correspondente do compêndio, sem exigir uma descrição textual duplicada em `char_info`

### Requirement: Character layout handles unresolved references safely
O layout da ficha SHALL tratar referências inexistentes ou páginas indisponíveis como falha não fatal de renderização. Deve exibir pelo menos o nome ou caminho bruto como fallback e somente usar `description` legado quando a ficha antiga não possuir conteúdo resolvível.

#### Scenario: Missing compendium page
- **WHEN** uma entrada de ação ou característica aponta para uma página inexistente
- **THEN** o build SHALL concluir sem erro e a ficha SHALL exibir um fallback identificável para revisão editorial

#### Scenario: Legacy character remains renderable
- **WHEN** uma ficha antiga possui `description` no frontmatter e não possui `ref` resolvível
- **THEN** o layout SHALL renderizar a descrição legada até que a ficha seja migrada

### Requirement: Character frontmatter separates personal state from shared rules
Novas fichas e fichas migradas SHALL manter no frontmatter apenas dados específicos ou operacionais do personagem, incluindo usos máximos, recarga, preparo, quantidade, equipamento e fórmulas. Descrições reutilizáveis de regras SHALL residir em notas do compêndio e ser referenciadas por URL interna.

#### Scenario: Operational action data is preserved
- **WHEN** uma ação possui `name`, `ref`, `source`, `max_uses` e `reset`
- **THEN** a ficha SHALL usar os campos operacionais para exibir o acompanhamento da ação e SHALL obter sua descrição da página `ref`

#### Scenario: Shared description is absent from migrated frontmatter
- **WHEN** uma descrição de Pinky corresponde a uma nota validada do compêndio
- **THEN** a migração SHALL remover a cópia textual de `char_info` e preservar a referência e os dados específicos da personagem
