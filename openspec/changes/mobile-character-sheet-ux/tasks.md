## 1. CSS & Responsive Header Adjustments

- [x] 1.1 Adicionar estilos para o cabeçalho compacto (`.vtt-iframe` / `@media (max-width: 600px)`): imagem circular do personagem à esquerda, nome do personagem ao lado com tratamento de estouro (`text-overflow: ellipsis`), e ocultação das pílulas de raça, classe, alinhamento e tamanho.
- [x] 1.2 Ocultar os rótulos de texto ("CA", "HP", "Desloc.", "Prof.") nos emblemas de estatísticas em modo compacto e aplicar as cores funcionais nos ícones (prata para CA, vermelho para HP, verde para Deslocamento e amarelo para Proficiência).

## 2. Tab Navigation Optimizations

- [x] 2.1 Ajustar o layout flex e padding dos botões de abas para caberem 100% em uma única linha sem rolagem horizontal em dispositivos móveis.
- [x] 2.2 Ocultar o botão da aba "Imagem" (`tab-image`) em viewports pequenas e em contexto de iframe de VTT.

## 3. Action Tab & Hierarchy Restructuring

- [x] 3.1 Promover o título "Recursos de Classe" um nível acima no container e simplificar os cards de recursos para exibir apenas o nome e os círculos de marcação.
- [x] 3.2 Relocar a seção de "Slots de Magia" em `character.html` para figurar imediatamente abaixo dos "Recursos de Classe".
- [x] 3.3 Otimizar os cards de armas em modo compacto: exibir o nome e abaixo as rolagens de ataque e dano (sem indicação do tipo de dano), ocultar alcance e tags de propriedades, e reduzir o espaçamento vertical.

## 4. Spell Cards Mobile Enhancement

- [x] 4.1 Atualizar os cards de magia para modo compacto: manter o título e as rolagens calculadas visíveis, movendo tempo de conjuração, alcance, duração e componentes para a visão detalhada.
- [x] 4.2 Estilizar o acionador "Ver Detalhes" dos cards de magia como um botão de `+` posicionado no canto inferior direito do card em visualizações compactas.

## 5. Verification & Testing

- [x] 5.1 Testar a renderização da ficha em mobile e desktop executando `hugo server -D`.
- [x] 5.2 Validar o build de produção sem erros via `hugo --gc --minify`.

## 6. Title Visibility & Flexbox Fixes for Small Viewports

- [x] 6.1 Ajustar o layout dos cabeçalhos dos cards de magias (`.spell-card-header`) de CSS Grid para Flexbox responsivo em telas pequenas / `.vtt-iframe` e forçar exibição proeminente dos títulos de itens, magias, armas, consumíveis e ações (`.spell-card-title`, `.equipment-card-name`, `.consumable-name`).
- [x] 6.2 Validar o build de produção sem erros via `hugo --gc --minify`.
