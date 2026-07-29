# rpg-character-sheet Specification Delta

## MODIFIED Requirements

### Requirement: Tab Navigation Interface
O sistema SHALL disponibilizar uma barra de abas interativas no topo da visualização da ficha do personagem ("Atributos", "Perícias", "Ações", "Equipamentos", "Grimório" [se conjurador], "Classe", "Características" e "Imagem") para comutação de conteúdo. Em telas pequenas ou iframe de VTT, a barra de abas SHALL caber integralmente em uma linha e a aba "Imagem" SHALL ser ocultada automaticamente.

#### Scenario: Tab switching activation
- **WHEN** o usuário clica em uma aba na barra de navegação da ficha
- **THEN** o sistema SHALL alternar a visualização ocultando as demais áreas e exibindo apenas a correspondente à aba selecionada, sem realizar recarga de página (através de CSS puro ou Vanilla JS leve).

#### Scenario: Mobile single-line tabs
- **WHEN** a ficha é aberta em tela de smartphone (largura <= 600px) ou iframe de VTT
- **THEN** o sistema SHALL ajustar o tamanho dos botões de aba para caberem em uma única linha sem rolagem horizontal
- **AND** a aba "Imagem" SHALL ser ocultada da barra.

### Requirement: VTT Iframe Compatibility
O sistema SHALL suportar a renderização da ficha de personagem em elementos iframe compactos de mesas virtuais de RPG (VTT), ajustando dinamicamente dimensões, margens, barras de rolagem e elementos visuais de cabeçalho e cards para otimizar o uso do espaço útil.

#### Scenario: Adapt rendering in constrained iframe
- **WHEN** a página da ficha de personagem for carregada dentro de um iframe em uma tela de VTT
- **THEN** o sistema SHALL remover margens externas amplas do layout, compactar o espaçamento do menu de abas e aplicar comportamento de rolagem interna suave nas abas (`overflow-y: auto`) para evitar o surgimento de barras de rolagem dupla na interface do usuário.

#### Scenario: Compact header and colored stat icons in VTT iframe
- **WHEN** a ficha é carregada dentro de um iframe VTT
- **THEN** o sistema SHALL renderizar a foto do personagem circular à esquerda com o nome ao lado
- **AND** o sistema SHALL ocultar as pílulas de raça, classe, alinhamento e tamanho
- **AND** o sistema SHALL omitir os rótulos textuais de CA, HP, Desloc. e Prof., exibindo apenas os ícones nas cores prata, vermelho, verde e amarelo respectivamente.
