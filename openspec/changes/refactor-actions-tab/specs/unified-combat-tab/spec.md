## ADDED Requirements

### Requirement: Exibição Consolidada da Aba de Ações
A aba de "Ações e Recursos" (`tab-actions`) SHALL exibir, em uma única página, os principais elementos de combate do personagem na seguinte ordem:
1. Recursos de Classe (Class Consumables / Features)
2. Espaços de Magia (Spell Slots / Pact Slots)
3. Ataques Físicos e Ações Físicas
4. Magias (Grimório resumido)

#### Scenario: Visualização principal da ficha de personagem em combate
- **WHEN** o usuário clica na aba de "Ações e Recursos" (ícone de machado)
- **THEN** a tela renderiza primeiramente os contadores de recursos de classe
- **THEN** logo abaixo exibe os checkboxes de espaços de magia (spell slots)
- **THEN** exibe os ataques de armas físicas
- **THEN** exibe a lista de magias conhecidas ou preparadas

### Requirement: Design Responsivo e Otimizado para Mobile e Iframes
O layout da aba consolidada SHALL ser desenhado de forma responsiva, acomodando-se em telas pequenas (como celulares e o iframe de overlay do Owlbear Rodeo) sem quebrar o layout, exigindo preferencialmente apenas rolagem vertical (sem rolagem horizontal indesejada).

#### Scenario: Uso da ficha em um smartphone ou no VTT
- **WHEN** a tela possui largura reduzida (ex: 400px de largura)
- **THEN** os grids de ataques, botões de espaços de magia e recursos de classe se ajustam para `flex-direction: column` ou grades menores sem transbordar horizontalmente.
- **THEN** todos os elementos mantêm legibilidade e facilidade de toque nas caixas de seleção.
