## Context

Atualmente, as fichas de personagens de RPG (ex: `pinky.md`, `durin.md`) são exibidas usando um layout de fallback genérico do site estático Hugo. Não existe um layout estruturado em `layouts/characters/single.html` que faça as estatísticas se parecerem com uma ficha de RPG real, dificultando o uso prático dessas páginas como referência rápida durante as sessões de jogo. O gmvault prioriza leveza, desempenho em hardware modesto e ausência de frameworks JS pesados (como React ou Next.js).

## Goals / Non-Goals

**Goals:**
- Criar um layout dedicado em `layouts/characters/single.html` específico para os arquivos de tipo `character`.
- Implementar uma interface de 8 abas interativas no topo da página ("Atributos", "Perícias", "Ações", "Equipamentos", "Grimório" [se conjurador], "Classe", "Características" e "Imagem") utilizando HTML/CSS e JavaScript mínimo nativo.
- Renderizar os 6 atributos principais em caixas quadradas (grid responsivo), destacando o modificador no centro e o valor base no canto, acompanhados de HP Máximo, Deslocamento (Speed), Classe de Armadura, bônus de proficiência, salvaguardas (saving throws) e sentidos passivos totalmente traduzidos para pt_br.
- Exibir a lista de perícias em duas colunas com indicadores visuais para Proficiente e Especialista (Expertise) traduzidas em português.
- Apresentar na aba de Ações todas as ações básicas de combate e ações especiais de classe/subclasse, implementando checkboxes dinâmicos para controle visual interativo de usos máximos de recursos de uso limitado.
- Organizar o inventário por categorias (Armas/Armaduras, Consumíveis e Geral), exibindo ícones discretos e fórmulas de ataque/dano.
- Agrupar magias por nível em cards que consultam informações suplementares do compêndio global.
- Apresentar a descrição da progressão de classe/subclasse por nível e as características/talentos traduzidos.
- Suportar renderização ultra-compacta e fluida quando carregada dentro de um `iframe` em painéis de VTT.

**Non-Goals:**
- Não implementar edição dinâmica ou persistência de dados no navegador (as fichas continuam sendo geradas estaticamente via Markdown no Hugo).
- Não utilizar bibliotecas robustas de JS (como jQuery, React, Vue) nem frameworks de CSS pesados.
- Não implementar banco de dados dinâmico ou sistema de autenticação para gerenciamento de fichas.

## Decisions

### 1. Alternância de Abas via Vanilla JS Leve
- **Opção Escolhida**: Uso de um script de Vanilla JS inline mínimo (composto por menos de 15 linhas) associado a botões de controle que aplicam a classe `.active` nos containers de abas correspondentes.
- **Alternativa Considerada**: CSS puro com inputs de rádio escondidos (`input[type="radio"]:checked ~ .tab-content`). Embora funcional e sem JS, essa abordagem incha o DOM com inputs redundantes e prejudica a semântica e a acessibilidade da navegação por abas.

### 2. Estilização do Grid e Quadrados de Atributos
- **Opção Escolhida**: Uso de Grid CSS (`grid-template-columns: repeat(6, 1fr)`) com propriedades flexíveis e media queries para responsividade. Cada caixa de atributo terá bordas bem definidas, cantos levemente arredondados, fundo HSL semi-transparente (integrado ao modo escuro do vault) e destaque proeminente de tamanho de fonte para o modificador.
- **Alternativa Considerada**: Caixas circulares ou formato de lista linear. A lista linear não remete visualmente a fichas clássicas e consome muito espaço vertical. Caixas quadradas oferecem o melhor aproveitamento de tela.

### 3. Resolução e Enriquecimento pelo Compêndio
- **Opção Escolhida**: Uso do recurso `site.GetPage` do Hugo dentro dos templates de layout para buscar os metadados canônicos de itens mágicos, consumíveis e magias cadastrados na lista `compendium_refs` do personagem.
  - Se a página do compêndio existir, o card é renderizado com dados ricos (ex: escola da magia, tempo de conjuração, alcance, descrição curta).
  - Se a página do compêndio não existir, o layout faz um fallback seguro exibindo apenas o nome do item/magia como texto simples (evitando quebras de compilação do Hugo).

### 4. Detecção e Estilização para Iframe VTT
- **Opção Escolhida**: Inserção de uma verificação em JavaScript na inicialização da página (`if (window.self !== window.top) document.documentElement.classList.add('vtt-iframe');`). O CSS correspondente ocultará o cabeçalho global do site, rodapés e navegação externa do gmvault, eliminando margens e maximizando a área de exibição da ficha de RPG dentro do iframe.
- **Alternativa Considerada**: Criar um layout alternativo por query parameter no Hugo (ex: `?layout=vtt`). Isso complicaria a compilação estática do Hugo que gera apenas arquivos HTML estáticos físicos por URL, exigindo lógica adicional de servidor, o que viola a premissa de wiki estática sem backend.

## Risks / Trade-offs

- **[Risco] Quebra de Layout em Telas de Smartphones**: Exibir 6 atributos horizontais e 2 colunas de perícias em telas pequenas causará cortes ou sobreposição de texto.
  - *Mitigação*: Implementar Media Queries estritas no CSS. Em telas menores que 768px, os atributos mudarão para um grid de 3 colunas por 2 linhas (ou 2 colunas por 3 linhas) e a lista de perícias cairá para uma única coluna vertical.
- **[Risco] Ausência de Página de Grimório para Classes Não Conjuradoras**: Personagens marciais (como bárbaros ou ladinos) ficariam com uma aba de Grimório vazia ou desnecessária.
  - *Mitigação*: O Hugo SHALL verificar condicionalmente se o array de magias (`spells` ou referências do compêndio de magias) está povoado na ficha do personagem. Se estiver vazio, a aba "Grimório" será completamente ocultada da interface de navegação.
- **[Risco] Ausência de Imagem/Retrato de Personagem**: Alguns personagens podem não possuir uma imagem correspondente definida em seu frontmatter.
  - *Mitigação*: O layout do Hugo SHALL verificar a presença do campo `image` ou `avatar` no frontmatter. Caso ausente, a aba "Imagem" renderizará uma ilustração heráldica genérica de fallback ou brasão discreto medieval com a mensagem 'Ilustração indisponível'.
- **[Risco] Dupla Barra de Rolagem no Navegador em Visualizações de Iframe**: Se o iframe do VTT for pequeno e a altura do conteúdo da aba selecionada for longa, barras de rolagem duplas (uma para o iframe e outra para a página geral) prejudicarão o uso.
  - *Mitigação*: Aplicar `overflow: hidden` na raiz da página sob a classe `.vtt-iframe` e definir altura do container da ficha como `100vh`, delegando a rolagem exclusivamente para o container interno de conteúdo da aba ativa (`overflow-y: auto`), garantindo uma rolagem única e fluida dentro do frame.
