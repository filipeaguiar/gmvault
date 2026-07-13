## 1. Reorganizar categorias de aventuras

- [x] 1.1 Alterar `gmvault_adventure_category.html` para listar cada cena diretamente em `items`, removendo a categoria intermediária `Cenas de <aventura>`.
- [x] 1.2 Preservar a descoberta de cenas por `kind` efetivo nas hierarquias simplificada, legada e mista, sem duplicar páginas.
- [x] 1.3 Preservar categorias existentes da aventura, como NPCs, e manter os IDs e metadados dos itens gerados pelo helper comum.

## 2. Organizar handouts no export

- [x] 2.1 Implementar a coleta de URLs de handouts da aventura e de todas as cenas associadas, resolvendo-as com `site.GetPage`.
- [x] 2.2 Deduplicar handouts por URL dentro de cada aventura e emitir uma categoria `Handouts` somente quando houver itens resolvidos.
- [x] 2.3 Alterar `gmvault_campaign_categories.html` para manter na raiz apenas handouts da campanha não associados a nenhuma aventura, incluindo retratos de personagens jogadores.
- [x] 2.4 Garantir que referências inexistentes e categorias sem itens não causem erro nem sejam emitidas no JSON.

## 3. Testes e validação do JSON

- [x] 3.1 Adicionar testes de regressão que validem cenas diretamente dentro da aventura, ausência da categoria intermediária de cenas e categorias de handouts por aventura.
- [x] 3.2 Validar deduplicação e separação entre handouts de aventura e handouts gerais da raiz.
- [x] 3.3 Executar `hugo --gc --minify`, validar o JSON gerado com `jq` e confirmar compatibilidade com a estrutura legada e simplificada.
- [x] 3.4 Executar a suíte Python com `PYTHONPATH=.` e registrar a nova hierarquia no histórico da mudança.
