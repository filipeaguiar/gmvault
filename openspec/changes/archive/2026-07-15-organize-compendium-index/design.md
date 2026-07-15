## Context

O índice global usa `layouts/partials/kinds/compendium_index.html` para renderizar o conteúdo introdutório e `layouts/partials/child_pages.html` para listar páginas filhas em cards. A listagem atual já filtra visibilidade e ordena por `weight`/título, mas trata a navegação como uma grade única.

O conteúdo do compêndio é organizado principalmente por diretórios (`monsters`, `items`, `magic-items`, `classes`, `species`, `feats`, `spells`, `backgrounds`, `conditions` e `rules`). As páginas usam `kind` dentro de `params`, além de `tags`, `status`, `visibility`, `summary` e `weight`. Há compatibilidade histórica para `kind` no topo. A solução deve padronizar a escrita em `params.kind`, manter leitura temporária do formato legado, sem banco de dados ou JavaScript pesado.

## Goals / Non-Goals

**Goals:**

- Tornar o índice global escaneável por categoria, com grupos visuais e contagem de páginas.
- Organizar páginas dentro de seções grandes usando metadados existentes e fallback previsível para conteúdo legado.
- Preservar os filtros de visibilidade para navegação pública e de jogadores.
- Reutilizar a ordenação determinística já usada pelo projeto.
- Manter uma implementação leve, baseada em partials Hugo e CSS.

**Non-Goals:**

- Não criar banco de dados, API ou painel administrativo.
- Não exigir que todos os Markdown recebam novos campos de front matter.
- Não implementar busca textual completa ou indexação client-side nesta mudança.
- Não publicar drafts de campanhas ou conteúdo GM; a migração de publicação será limitada a páginas públicas do compêndio.
- Não alterar URLs, slugs ou a estrutura física do compêndio.
- Não tratar `visibility` como mecanismo de autenticação.

## Decisions

### 1. Usar diretório e `params.kind` como fontes de categorização

O índice principal tratará cada seção direta de `content/compendium/` como uma categoria canônica. Nos índices internos, o agrupamento usará `params.kind` como fonte principal e aceitará `kind` no topo somente como fallback legado; na ausência desses campos, usará o diretório/seção atual. Archetypes, scripts e páginas mantidas pelo projeto deverão gravar o campo dentro de `params`.

Alternativa descartada: exigir um novo campo `category` em todos os arquivos. Isso aumentaria o trabalho editorial e quebraria a compatibilidade com importações antigas.

### 2. Centralizar a resolução do kind

O helper `layouts/partials/helpers/kind.html` será a fonte de resolução para templates, preferindo `.Params.params.kind` e aceitando `.Params.kind` apenas para conteúdo legado. Geradores e archetypes serão auditados para que novos arquivos não criem `kind` no topo.

### 3. Separar a montagem dos grupos da apresentação dos cards

A lógica de classificação e filtragem ficará em um partial auxiliar reutilizável, enquanto `compendium_index.html` e `child_pages.html` cuidarão da composição visual. Cada grupo receberá título, ícone, contagem e páginas ordenadas.

Alternativa descartada: duplicar a lógica em cada template de seção, pois isso aumentaria divergências entre índices.

### 4. Manter a ordenação existente dentro de cada grupo

As páginas visíveis serão ordenadas primeiro por `weight` crescente e depois por título, preservando o comportamento de consulta durante sessões de jogo. A contagem de cada grupo será calculada depois da filtragem de visibilidade, para não revelar páginas GM em índices públicos.

Alternativa descartada: ordenar apenas alfabeticamente, pois isso perderia a prioridade editorial já expressa por `weight`.

### 5. Separar publicação Hugo de tradução

`draft` será tratado como controle de inclusão no build Hugo. Para páginas públicas do compêndio, `draft: false` permitirá a navegação mesmo quando `status: draft` ou `translation.status` indicar que a tradução/revisão está pendente. O tradutor deverá considerar `status: draft` como pendência e preservar o valor de `draft` ao gravar o arquivo. Páginas de campanhas, GM ou visibilidade desconhecida continuarão com `draft: true` quando ainda não estiverem publicadas.

Alternativa descartada: configurar Hugo globalmente com `buildDrafts`, pois isso incluiria rascunhos de campanhas e conteúdo do mestre.

### 6. Usar CSS responsivo sem JavaScript

Os grupos usarão uma grade CSS adaptável, com uma coluna em telas estreitas e múltiplas colunas quando houver espaço. O conteúdo continuará funcionando sem JavaScript.

Alternativa descartada: filtros client-side com JavaScript, pois não são necessários para a primeira organização e aumentariam o peso e a complexidade do site.

## Risks / Trade-offs

- **[Risco]** Páginas com `kind` ausente podem cair em grupos genéricos. → **Mitigação:** usar o diretório da seção como fallback e manter uma categoria "Outros".
- **[Risco]** Metadados legados em `params.kind` podem ser ignorados por templates novos. → **Mitigação:** centralizar a resolução através do helper `helpers/kind.html` existente.
- **[Risco]** Contagens podem diferir entre builds com e sem drafts. → **Mitigação:** documentar que as contagens refletem o conjunto de páginas do build atual, mantendo a regra normal do Hugo.
- **[Risco]** Muitos grupos podem aumentar a altura da página. → **Mitigação:** usar cabeçalhos compactos, cards leves e grade responsiva; não expandir conteúdo completo no índice.

## Migration Plan

1. Atualizar o helper, archetypes, geradores e conteúdo mantido pelo projeto para escrever `params.kind`.
2. Preservar o fallback de leitura para páginas legadas com `kind` no topo.
3. Atualizar o fluxo de tradução para usar `status: draft` como pendência e preservar `draft` durante a gravação.
4. Migrar somente páginas públicas do compêndio para `draft: false`.
5. Implementar os partials e estilos da nova organização.
6. Validar o índice global e pelo menos uma seção grande com `hugo --gc --minify` e `hugo -D --gc --minify`.
7. Comparar navegação pública e GM para confirmar que páginas GM não aparecem no contexto público.
8. Reverter removendo o partial auxiliar e restaurando a chamada anterior de `child_pages.html`, caso a organização cause regressão visual.

## Open Questions

- O agrupamento por `kind` deve ser exibido somente em seções grandes ou em todas as seções? A proposta assume que grupos vazios não são renderizados e que seções com apenas um grupo continuam legíveis.
- A taxonomia visual inicial usará os nomes canônicos em português definidos pelo diretório e pelos ícones já existentes; novos tipos de compêndio deverão cair em "Outros" até receberem mapeamento específico.
