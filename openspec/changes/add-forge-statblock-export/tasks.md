## 1. Configurar o output Forge!

- [x] 1.1 Adicionar no `hugo.yaml` o output format `Forge` com media type JSON, base name `statblocks` e path `exports/forge`, habilitado no output da home.
- [x] 1.2 Criar o template `layouts/index.forge.json` para emitir um array JSON válido na URL estável do export.
- [x] 1.3 Criar helper para montar registros Forge com envelope, UUID determinístico, autor, favorito, timestamp e metadados namespaced.

## 2. Mapear personagens e monstros

- [x] 2.1 Descobrir páginas por `kind` efetivo, mantendo compatibilidade com `params.kind`, e incluir todos os personagens e monstros disponíveis.
- [x] 2.2 Mapear `char_info` para os campos Forge de nível, HP, CA, movimento, atributos e perícias.
- [x] 2.3 Mapear `stats`/`stats_meta` de monstros, incluindo ND, HP, CA, velocidade, atributos e perícias, com defaults para dados ausentes.
- [x] 2.4 Implementar ordenação determinística (personagens antes de monstros, depois peso/nome/permalink) e validar unicidade dos IDs.
- [x] 2.5 Mapear `compendium_refs` de itens e itens mágicos para `Z040` e gerar ações em `Z035` somente quando houver dano estruturado.

## 3. Expor links no site

- [x] 3.1 Criar um índice estável para `content/compendium/` e exibir nele o link copiável para `/exports/forge/statblocks.json`.
- [x] 3.2 Adicionar à página de campanha o link copiável para o output `GMVault` específico da própria campanha, respeitando `baseURL`.
- [x] 3.3 Manter os links leves, exibindo somente botões de cópia via Clipboard API e mensagens de status, sem alterar a estrutura do export GM Vault.

## 4. Testes e validação

- [x] 4.1 Adicionar testes de regressão para validar o array Forge, envelope dos registros, presença de personagens e monstros e metadados de Pinky.
- [x] 4.2 Validar ordenação, estabilidade e unicidade dos IDs em builds repetidos.
- [x] 4.3 Validar os links do Compêndio e da campanha no HTML gerado.
- [x] 4.4 Executar `hugo --gc --minify`, validar o JSON com `jq` e executar `PYTHONPATH=. pytest --tb=short -q`.
