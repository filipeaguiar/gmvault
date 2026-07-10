## Why

As páginas de índice serão usadas dentro de um iframe no aplicativo de mestrar RPG, então precisam oferecer navegação previsível, ordenada e legível em largura reduzida. A navegação também deve evitar que páginas voltadas a jogadores exponham caminhos para páginas `gm`, reduzindo risco de spoilers por cliques acidentais.

## What Changes

- Melhorar o layout de páginas de índice/lista para funcionar como navegação precisa de wiki dentro de iframe.
- Ordenar itens de índice de forma determinística por `weight` e título, com agrupamento visual consistente.
- Tornar cards/listas responsivos para larguras estreitas, alternando de grade para coluna compacta sem overflow horizontal.
- Garantir que páginas `visibility: players` ou `visibility: public` não exibam navegação, filhos ou relações que levem a páginas `visibility: gm`.
- Corrigir a leitura de `kind` para suportar conteúdo existente que usa `params.kind` e conteúdo/archetypes que usam `kind` no topo.
- Não introduzir frameworks JavaScript, backend, banco de dados ou tema externo.

## Capabilities

### New Capabilities
- `index-layout`: comportamento de layout, ordenação e responsividade das páginas de índice/lista.

### Modified Capabilities
- `navigation-and-visibility`: restringe navegação gerada em páginas player/public para não apontar para páginas GM e mantém breadcrumbs ocultos nesses contextos.
- `content-model`: normaliza a interpretação de `kind` entre front matter de topo e `params.kind` legado.
- `site-shell`: reforça suporte responsivo para iframe e larguras reduzidas no shell visual.

## Impact

- Layouts Hugo em `layouts/_default/list.html`, `layouts/partials/child_pages.html`, `layouts/partials/breadcrumbs.html`, `layouts/partials/relationships.html` e possivelmente `layouts/_default/single.html`.
- Partials de tipo em `layouts/partials/kinds/` caso dependam diretamente de `.Params.kind`.
- CSS em `assets/css/main.css` para comportamento responsivo de listas, cards e metadados.
- Conteúdo existente que usa `params.kind` deverá continuar funcionando sem migração obrigatória.
