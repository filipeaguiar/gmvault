## Why

A página de classe do compêndio apresenta a progressão em um bloco longo e pouco hierárquico, com links que usam o estilo padrão do navegador e títulos sem identidade visual. Isso dificulta consultar rapidamente os níveis, características e subclasses durante uma sessão.

## What Changes

- Reorganizar visualmente a página de progressão de classe em uma apresentação hierárquica e escaneável.
- Agrupar entradas de progressão por nível (`Nível 1`, `Nível 2`, etc.) usando headings e linhas horizontais, evitando uma apresentação baseada em muitos cards.
- Exibir cada característica com seu texto correspondente no compêndio e link interno quando a página existir.
- Aplicar cores consistentes para classe, subclasse, níveis e links do compêndio.
- Substituir links com aparência padrão do navegador por componentes estilizados, mantendo acessibilidade e estados de foco/hover.
- Corrigir links internos Markdown para respeitar o `baseURL` do site e evitar 404 em publicações sob subdiretórios.
- Melhorar o título da página e os títulos das entradas usando tipografia, espaçamento e ícones da biblioteca de ícones já utilizada pelo projeto.
- Evitar títulos redundantes como `Desenvolvimento`, `Progressão da Classe` e `Progressão de Barbarian`, exibindo somente o nome da classe resolvido por `titulo_pt_br` ou `title`.
- Usar somente ícones CSS/RuneScape e texto existente; não adicionar caracteres Unicode decorativos ou emojis.
- Manter responsividade em notebooks, telas pequenas e iframes.
- Preservar o agrupamento por nível quando o conteúdo da classe for reutilizado na página do personagem.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `compendium`: a visualização de páginas de classe e progressão deverá apresentar conteúdo hierárquico e links internos estilizados.

## Impact

- `layouts/partials/kinds/class.html`: estrutura semântica da página de classe, progressão e subclasses.
- `assets/css/main.css`: estilos de títulos, grupos por nível, linhas, links e responsividade da progressão.
- `layouts/_default/_markup/render-link.html`: normalização de links internos com o `baseURL`.
- `dnd_utils.py` e importadores: criação/linkagem de páginas de características de classe ausentes.
- Conteúdo existente em `content/compendium/classes/`: nenhuma alteração de URLs ou front matter deverá ser necessária.
- Build Hugo e testes de renderização HTML/CSS.
