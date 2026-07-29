# mobile-character-sheet-layout Specification

## Purpose
Estabelecer os requisitos de interface e experiência de usuário (UI/UX) para a ficha de personagem em dispositivos móveis e em ambientes com limitação severa de espaço (iframes de VTT como Owlbear Rodeo).

## ADDED Requirements

### Requirement: Compact Header for Small Viewports
A ficha de personagem SHALL renderizar um cabeçalho compacto e funcional quando exibida em telas com largura de até 600px ou dentro de um iframe de VTT (`.vtt-iframe`).

#### Scenario: Character image and name layout in compact header
- **WHEN** a ficha é renderizada em tela pequena (largura <= 600px) ou iframe de VTT
- **THEN** a imagem de retrato do personagem SHALL ser exibida em formato circular no lado esquerdo do cabeçalho
- **AND** o nome do personagem SHALL ser posicionado ao lado da imagem, com truncamento via reticências (ellipsis) caso o nome seja excessivamente longo para evitar quebra desordenada de layout.

#### Scenario: Suppress secondary meta pills
- **WHEN** a ficha é renderizada em tela pequena ou iframe de VTT
- **THEN** o layout SHALL ocultar as pílulas de metadados secundários (Raça/Espécie, Classe/Nível, Alinhamento e Tamanho) para priorizar a visibilidade de elementos operacionais.

#### Scenario: Icon-only stat badges with function-based colors
- **WHEN** os emblemas de estatísticas principais (CA, HP, Deslocamento e Proficiência) são exibidos em tela pequena ou iframe de VTT
- **THEN** o layout SHALL ocultar os rótulos textuais ("CA", "HP", "Desloc.", "Prof.")
- **AND** SHALL exibir apenas os ícones e seus valores numéricos correspondentes
- **AND** cada ícone de estatística SHALL ser colorido de acordo com sua função:
  - Prata (`#c0c0c0` / `var(--badge-ac-color)`) para CA (Armadura)
  - Vermelho (`#d9534f` / `var(--badge-hp-color)`) para HP (Pontos de Vida)
  - Verde (`#5cb85c` / `var(--badge-speed-color)`) para Deslocamento
  - Amarelo (`#f0ad4e` / `var(--badge-prof-color)`) para Bônus de Proficiência.

### Requirement: Single-Line Tab Navigation
A barra de navegação por abas SHALL ser ajustada para caber completamente em uma única linha em telas pequenas, sem rolagem horizontal ou margens desnecessárias.

#### Scenario: Single-line tab bar fitting
- **WHEN** a barra de abas da ficha é renderizada em tela pequena ou iframe de VTT
- **THEN** todas as abas visíveis SHALL se ajustar em uma única linha sem quebra de linha e sem rolagem horizontal.

#### Scenario: Hide image tab on small viewports
- **WHEN** a largura da tela for inferior a 600px ou estiver em contexto de iframe VTT
- **THEN** o botão da aba de "Imagem" (`tab-image`) SHALL ser ocultado automaticamente da barra de abas.

### Requirement: Simplified Class Resource Hierarchy
O container de "Recursos de Classe" na aba de Ações SHALL eliminar camadas desnecessárias de aninhamento visual em telas pequenas.

#### Scenario: Direct rendering of resource cards
- **WHEN** a seção de Recursos de Classe for exibida
- **THEN** o título "Recursos de Classe" SHALL residir um nível acima na hierarquia do container
- **AND** cada recurso de classe SHALL ser exibido diretamente como um card individual contendo apenas o nome do recurso e os marcadores circulares de uso.

### Requirement: Compact Weapon Action Display
Os cards de armas na aba de Ações SHALL priorizar as informações operacionais primárias durante a jogatina em telas pequenas.

#### Scenario: Weapon card mobile layout
- **WHEN** os cards de armas forem renderizados em telas pequenas (largura <= 600px)
- **THEN** o card de arma SHALL exibir o nome da arma e, logo abaixo do nome, as estatísticas numéricas/rolagens de Ataque e Dano
- **AND** a indicação de Dano SHALL omitir o texto descritivo do tipo de dano (ex: "cortante", "perfurante")
- **AND** o card SHALL ocultar o alcance da arma, tags e propriedades secundárias (como "Acuidade", "Leve")
- **AND** o espaçamento vertical entre os elementos do card SHALL ser reduzido para o mínimo confortável.

### Requirement: Compact Spell Cards and Detail Drawer
Os cards de magia na aba de Ações ou Grimório SHALL garantir visibilidade do título e rolagens principais em telas pequenas, movendo detalhes secundários para um acionador compacto.

#### Scenario: Spell card mobile header and rolls
- **WHEN** um card de magia for renderizado em telas pequenas
- **THEN** o card SHALL exibir de forma proeminente o título da magia e suas rolagens calculadas de ataque e dano (caso a magia possua tais rolagens)
- **AND** o tempo de conjuração, alcance, duração e componentes SHALL ser movidos para a área interna de detalhes do card.

#### Scenario: Plus icon trigger for spell details
- **WHEN** um card de magia for renderizado em telas pequenas
- **THEN** o acionador "Ver Detalhes" SHALL ser estilizado como um ícone de `+` posicionado no canto inferior direito do card.

### Requirement: Relocated Spell Slots Position
Na aba de Ações, o rastreador de "Slots de Magia" SHALL ser posicionado imediatamente abaixo da seção de "Recursos de Classe".

#### Scenario: Spell slots layout ordering
- **WHEN** a aba de Ações for renderizada para um personagem conjurador
- **THEN** a seção de Slots de Magia SHALL ser posicionada logo abaixo dos Recursos de Classe e antes da lista de Armas e Ações gerais.
