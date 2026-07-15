## 1. Padronização de `params.kind`

- [x] 1.1 Atualizar `layouts/partials/helpers/kind.html` para priorizar `.Params.params.kind` e usar `.Params.kind` somente como fallback legado.
- [x] 1.2 Auditar layouts, archetypes e scripts geradores/importadores para garantir que todo conteúdo novo seja gravado com `params.kind`, sem criar `kind` no topo do front matter.
- [x] 1.3 Adicionar validação ou teste que identifique páginas mantidas pelo projeto com `kind` no topo e confirme a compatibilidade de leitura do formato legado.
- [x] 1.4 Atualizar `translate_drafts.py` para considerar `status: draft` como tradução pendente e preservar o valor de `draft` ao gravar o arquivo.
- [x] 1.5 Migrar páginas `visibility: public` do compêndio que usam `draft: true` para `draft: false`, mantendo `status: draft` e os metadados de tradução quando aplicáveis.

## 2. Organização dos índices do compêndio

- [x] 2.1 Criar um partial auxiliar para resolver categorias, filtrar visibilidade e montar grupos de páginas com base em `params.kind`, `tags` e diretório de fallback.
- [x] 2.2 Atualizar `layouts/partials/kinds/compendium_index.html` para exibir seções canônicas do compêndio com ícone, resumo, quantidade de páginas visíveis e link para o índice da seção.
- [x] 2.3 Atualizar `layouts/partials/child_pages.html` ou criar partials específicos para renderizar páginas agrupadas por categoria, mantendo ordenação por `weight` e título e fallback para páginas sem metadados.
- [x] 2.4 Garantir que índices públicos e de jogadores não exibam nem contabilizem páginas `gm` ou com visibilidade desconhecida.

## 3. Apresentação visual

- [x] 3.1 Adicionar estilos para cabeçalhos de grupo, contadores, cards de categoria e separação visual entre grupos.
- [x] 3.2 Ajustar o layout responsivo para manter os grupos legíveis em notebooks, telas pequenas e iframes sem overflow horizontal.

## 4. Validação

- [x] 4.1 Criar testes de renderização para o índice global, uma seção com muitos itens e uma seção com páginas sem `summary` ou `kind` explícito.
- [x] 4.2 Executar `hugo --gc --minify` e `hugo -D --gc --minify`, verificando ordenação, contagens, links e filtragem de visibilidade.
- [x] 4.3 Testar que o tradutor ainda encontra páginas públicas com `status: draft` e que rascunhos de campanha/GM continuam excluídos do build de produção.
