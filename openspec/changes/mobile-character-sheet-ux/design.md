## Context

Muitos jogadores utilizam dispositivos móveis (smartphones) para consultar e manipular suas fichas de personagem durante as sessões de RPG de mesa. Além disso, no contexto de VTT (Virtual Tabletop, como o Owlbear Rodeo), a ficha é frequentemente exibida em um `iframe` compacto dentro da janela do jogo. Na implementação atual, a ficha renderizada em viewports pequenas sofre de acúmulo de metadados, títulos e rótulos de texto extensos, cards aninhados desnecessariamente, abas com rolagem e elementos cruciais (como slots de magia) posicionados no rodapé da página.

Esta proposta define as alterações de layout CSS responsivo e marcação Hugo HTML para solucionar esses gargalos de espaço e usability.

## Goals / Non-Goals

**Goals:**
- Proporcionar uma interface ultra-compacta, legível e altamente funcional para smartphones e iframes VTT.
- Ocultar rótulos textuais de estatísticas secundárias (CA, HP, Desloc., Prof.) e utilizar ícones coloridos por função (prata, vermelho, verde, amarelo).
- Garantir que a barra de navegação por abas caiba em uma única linha sem rolagem horizontal ou quebras.
- Ocultar a aba "Imagem" em viewports pequenas/VTT.
- Exibir a imagem do personagem de forma circular no canto esquerdo com o nome ao lado (tratando nomes longos com ellipsis).
- Simplificar a hierarquia do container de "Recursos de Classe", removendo cards aninhados.
- Reorganizar a aba de Ações posicionando os "Slots de Magia" logo abaixo dos "Recursos de Classe", antes das Armas.
- Otimizar cards de armas em mobile (exibindo nome, ataque e dano abaixo do nome, sem rótulo de tipo de dano, sem propriedades/tags nem alcance).
- Otimizar cards de magia em mobile (exibindo título e rolagens calculadas, movendo tempo, alcance, duração e componentes para a descrição expansível ativada por botão `+` no canto inferior direito).
- Garantir visibilidade proeminente e incondicional de todos os títulos de itens, magias, armas, consumíveis e ações em telas pequenas.

**Non-Goals:**
- Modificar o visual desktop/computador convencional da ficha (onde todas as informações completas, pílulas de raça/classe e tags continuam visíveis).
- Alterar as mecânicas de rolagem de dados ou integração com o Owlbear Dice+.
- Reestruturar o schema de dados YAML/frontmatter dos personagens.

## Decisions

### 1. CSS Media Queries e Classe `.vtt-iframe`
- **Decisão:** Aplicar as regras de otimização mobile/compacta combinando a media query `@media (max-width: 600px)` e a classe `.vtt-iframe`.
- **Justificativa:** Garante que tanto celulares comuns quanto janelas de iframe em Owlbear Rodeo se beneficiem das otimizações.
- **Alternativas consideradas:** Usar apenas media query de largura. Rejeitado porque iframes em monitores de alta resolução podem ter larguras maiores porém com altura ou proporção restrita no VTT.

### 2. Cabeçalho Circular e Nome Truncado
- **Decisão:** Em visões compactas, transformar `.char-portrait-img` em `border-radius: 50%`, `width: 44px`, `height: 44px` (flex flex-row) e alinhar ao lado o nome `<h1>` com `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;`.
- **Justificativa:** Economiza espaço vertical massivo do cabeçalho e mantém o nome visível sem empurrar o conteúdo principal para baixo.

### 3. Cores Funcionais dos Ícones do Header
- **Decisão:** Rótulos textuais `CA`, `HP`, `Desloc.`, `Prof.` recebem `display: none` em compact/iframe. Os ícones `<i class="ra ...">` recebem cores distintas:
  - CA (`ra-shield`): `color: #c0c0c0;` (Prata)
  - HP (`ra-health`): `color: #d9534f;` (Vermelho)
  - Deslocamento (`ra-boot-stomp`): `color: #5cb85c;` (Verde)
  - Proficiência (`ra-lightning-bolt`): `color: #f0ad4e;` (Amarelo)
- **Justificativa:** A diferenciação por cor e formato do ícone é instantaneamente identificável pelos jogadores, dispensando o texto do rótulo e economizando espaço horizontal.

### 4. Ajuste da Barra de Abas e Ocultação da Aba Imagem
- **Decisão:** `.char-tabs-nav` utiliza `display: flex; gap: 2px; justify-content: space-between;` com `button.char-tab-btn` com padding reduzido (`padding: 6px 4px; flex: 1; min-width: 0;`). O botão `[onclick*="tab-image"]` recebe `display: none;`.
- **Justificativa:** Evita rolagem horizontal nas abas e mantém todas as abas de jogatina (Atributos, Perícias, Ações, Equipamentos, Classe, Características) visíveis em uma única fileira.

### 5. Reorganização dos Slots de Magia na Aba de Ações
- **Decisão:** Na partial Hugo `layouts/partials/kinds/character.html`, mover a inclusão de `{{ partial "helpers/character-spell-slots.html" . }}` de baixo de tudo para logo após a seção de `Recursos de Classe`.
- **Justificativa:** Conjuradores precisam acessar e marcar seus slots de magia frequentemente durante o combate; deixá-los abaixo de todas as ações e armas prejudica o fluxo de jogo.

### 6. Simplificação de Cards de Armas e Magias
- **Decisão (Armas):** Em mobile, `.weapon-card` oculta `.equipment-badges` secundários, `.equipment-properties` (tags) e o stat de alcance. Exibe o nome e abaixo uma linha flex com o Ataque (`+X`) e Dano (`XdY+Z`), omitindo o rótulo de tipo de dano.
- **Decisão (Magias):** `.spell-card` garante exibição do título e `.spell-card-rolls`. Oculta `.spell-card-facts` (tempo, alcance, duração) e `.spell-card-traits` por padrão em telas compactas. O acionador `<details>` / `<summary>` é estilizado como um pequeno botão de `+` posicionado via `position: absolute; bottom: 8px; right: 8px;`.

### 7. Layout Flexbox para Títulos de Cards em Viewports Pequenas
- **Decisão:** Sobrescrever a regra de CSS Grid de `.spell-card-header` (`grid-template-columns: auto minmax(12rem, 1fr) auto`) em telas pequenas / `.vtt-iframe` para `display: flex; flex-wrap: wrap; align-items: center; gap: 8px;` e forçar visibilidade em bloco (`display: block; font-size: 1.0rem; font-weight: 700; color: var(--text-color);`) para `.spell-card-title`, `.equipment-card-name` e `.consumable-name`.
- **Justificativa:** Elimina o esmagamento de colunas CSS Grid (`minmax(12rem, 1fr)`) que fazia os títulos de magias e itens desaparecerem quando a largura do container/iframe era inferior a 320px.

## Risks / Trade-offs

- **[Risco] Ocultar rótulos de estatísticas (CA, HP, etc.) pode confundir jogadores iniciantes.**
  - *Mitigação:* Usar atributos `title` HTML nos emblemas para suporte a tooltip quando houver hover/touch longo, mantendo a legenda clara.
- **[Risco] Ocultação de tipo de dano e propriedades da arma em mobile.**
  - *Mitigação:* As propriedades continuam disponíveis ao expandir os detalhes da arma ou visualizá-la no compêndio; a visualização compacta é intencionalmente focada na velocidade das jogadas de combate.
