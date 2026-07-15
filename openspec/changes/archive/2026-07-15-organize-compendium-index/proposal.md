## Why

A página do Compêndio Global atualmente depende de uma lista única de cards e seções, o que dificulta localizar rapidamente um tipo específico de conteúdo quando há muitos arquivos Markdown. O projeto já possui categorias naturais nos diretórios e metadados editoriais no front matter, mas essas informações ainda não são usadas de forma consistente para organizar a navegação.

## What Changes

- Organizar o índice principal do compêndio em seções visuais para os tipos canônicos de conteúdo: monstros, itens, itens mágicos, classes, espécies, talentos, magias, antecedentes, condições e regras.
- Exibir quantidade de páginas por seção e preservar título, resumo, ícone e metadados relevantes.
- Organizar índices de seções com muitos filhos por grupos derivados do front matter e do diretório, usando `params.kind` como fonte canônica e `tags`/metadados disponíveis como apoio.
- Padronizar novos geradores, archetypes e conteúdo mantido pelo projeto para gravar `kind` dentro de `params`.
- Manter leitura compatível de páginas legadas que ainda tenham `kind` no topo, sem continuar gerando esse formato.
- Separar o controle de publicação do Hugo (`draft`) do estado de tradução (`status: draft` e `translation`), permitindo que páginas públicas do compêndio apareçam mesmo enquanto aguardam revisão/tradução.
- Migrar páginas públicas do compêndio que usam `draft: true` para `draft: false`, preservando `status: draft` quando a tradução ainda estiver pendente.
- Manter ordenação determinística por `weight` e título dentro de cada grupo.
- Preservar o filtro de visibilidade para que índices públicos não criem navegação para conteúdo `gm` ou sem visibilidade explícita.
- Definir fallback para páginas legadas sem metadados suficientes, mantendo-as navegáveis sem falha de build.
- Melhorar o CSS dos grupos e cards para leitura rápida em telas largas, notebooks e iframes estreitos.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `compendium`: os índices do compêndio passarão a organizar e agrupar páginas com base nas categorias e metadados disponíveis.
- `index-layout`: os índices de seção terão grupos, contagens e ordenação determinística sem perder adaptação a telas estreitas.
- `content-model`: `params.kind` será o formato canônico para páginas novas e mantidas pelo projeto, com leitura legada de `kind` no topo.

## Impact

- `layouts/partials/kinds/compendium_index.html`: organização do índice global e contagem das seções.
- `layouts/partials/child_pages.html` e possíveis novos partials: agrupamento e renderização de páginas filhas.
- `assets/css/main.css` e/ou `assets/css/character-sheet.css`: estilos dos grupos, cards e responsividade.
- Front matter existente: leitura canônica de `params.kind`, com fallback temporário para `kind` no topo em arquivos legados; `draft` controlará somente o build do Hugo, enquanto `status`/`translation` controlarão revisão e tradução.
- Build Hugo e testes de renderização/ordenação dos índices.
- `translate_drafts.py` e páginas públicas do compêndio, para preservar a tradução pendente sem excluir conteúdo público do build.
