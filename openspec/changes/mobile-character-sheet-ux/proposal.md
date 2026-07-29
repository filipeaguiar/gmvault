## Why

Quando a ficha de personagem é visualizada em telas pequenas de smartphones dentro do iframe do Owlbear Rodeo, o espaço útil de tela é extremamente limitado. A interface atual apresenta excesso de metadados, rótulos de texto redundantes, hierarquias de cards com aninhamento desnecessário, cards de magia sem título/rolagens e elementos fora de ordem (como slots de magia no final da aba de ações).

Esta mudança otimiza a experiência em telas pequenas e contextos de iframe VTT, focando exclusivamente na praticidade e fluidez durante a jogatina em mobile, sem prejudicar a visualização em telas maiores.

## What Changes

- **Header Compacto em Mobile (`.vtt-iframe` / `@media (max-width: 600px)`):**
  - **Imagem e Nome:** Imagem do personagem exibida circularmente no lado esquerdo com o nome ao lado, tratando adequadamente nomes longos com quebra/ellipsis legível.
  - **Ocultação de Pills Secundárias:** Oculta as pílulas de raça, classe, alinhamento e tamanho em visões compactas/iframe VTT.
  - **Badges de Atributos Vitais:** Oculta os rótulos de texto ("CA", "HP", "Desloc.", "Prof.") e mantém apenas os ícones com cores funcionais específicas:
    - Prata (`#c0c0c0` / `var(--badge-ac-color)`) para CA (Armadura);
    - Vermelho (`#d9534f` / `var(--badge-hp-color)`) para HP (Vida);
    - Verde (`#5cb85c` / `var(--badge-speed-color)`) para Deslocamento;
    - Amarelo (`#f0ad4e` / `var(--badge-prof-color)`) for Bônus de Proficiência.
- **Navegação por Abas (Tab Bar):**
  - Ajusta os botões para caberem 100% em uma única linha sem rolagem horizontal ou espaçamento desnecessário.
  - Oculta a aba "Imagem" (`tab-image`) em telas pequenas/iframe VTT para economizar espaço de aba.
- **Estrutura da Aba de Ações e Recursos (Tab Actions):**
  - **Hierarquia de Recursos de Classe:** Promove o título "Recursos de Classe" para o nível superior do container, removendo aninhamentos de cards e exibindo diretamente o card do recurso com nome e círculos de marcação.
  - **Armas em Visão Compacta:** Exibe o nome da arma e, logo abaixo, as rolagens de ataque e dano (sem indicação de tipo de dano). Oculta tags/propriedades, alcances e selos secundários em telas menores (acessíveis em telas maiores). Reduz o espaçamento vertical para o mínimo confortável.
  - **Cards de Magia:** Garante a exibição do título da magia e das rolagens de ataque e dano apropriadas para o nível atual do personagem. Move tempo de conjuração, alcance, duração e componentes para a visão detalhada. Converte o acionador "Ver detalhes" em um botão de `+` posicionado no canto inferior direito do card.
  - **Posicionamento de Slots de Magia:** Reloca a seção de "Slots de Magia" para aparecer logo abaixo dos "Recursos de Classe", antes das Armas e Ações gerais.

## Capabilities

### New Capabilities
- `mobile-character-sheet-layout`: Define os comportamentos responsivos, otimizações visuais e reorganização hierárquica da ficha de personagem em visões compactas e iframes de VTT (Owlbear Rodeo).

### Modified Capabilities
- `rpg-character-sheet`: Ajustes no layout base do header, navegação de abas, renderização de cards de magia, armas e recursos consumíveis em dispositivos mobile.

## Impact

- `layouts/partials/kinds/character.html`: Ajustes na estrutura HTML dos headers, abas, reorganização dos slots de magia acima das armas, otimização das armas e integração com os partials de magias.
- `layouts/partials/helpers/character-spell-card.html`: Ajuste na exibição responsiva de cards de magia (título visível, botão `+` no canto inferior direito para expandir detalhes).
- `assets/css/character-sheet.css`: Estilização CSS responsiva para cores de ícones (prata, vermelho, verde, amarelo), layout de header circular com nome, navegação por abas em uma linha, aninhamento simplificado de recursos e supressão de rótulos/tags em telas pequenas.
