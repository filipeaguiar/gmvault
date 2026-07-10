## Why

A hierarquia conceitual `Aventuras → Sessões → Cenas` está correta, mas a implementação física atual cria nesting excessivo com diretórios indexadores intermediários (`sessions/` e `scenes/`) em cada aventura e sessão. Isso aumenta o número de `_index.md`, dificulta navegação manual, deixa URLs longas e torna os importadores mais complexos.

## What Changes

- Investigar e implementar uma hierarquia física mais simples mantendo a hierarquia conceitual `Aventuras → Sessões → Cenas`.
- Reduzir diretórios meramente indexadores quando possível.
- Definir um modelo canônico mais curto para novas campanhas/importações.
- Manter compatibilidade de leitura/renderização com a estrutura antiga durante transição.
- Atualizar layouts, partials e export GMVault para reconhecer a estrutura simplificada.
- Atualizar `import_campaign.py` como ponto principal da mudança, pois a maior parte do nesting é gerada automaticamente por ele.
- Atualizar archetypes para novos conteúdos manuais seguirem a mesma estrutura.
- Não remover o conceito de aventura, sessão ou cena.
- Não introduzir banco de dados, backend ou JavaScript pesado.

## Capabilities

### New Capabilities
- `campaign-hierarchy-simplification`: estrutura física simplificada para campanhas mantendo a semântica de aventura, sessão e cena.

### Modified Capabilities
- `content-model`: altera o modelo canônico esperado para arquivos de aventuras, sessões e cenas, preservando compatibilidade com estrutura legada.
- `index-layout`: atualiza navegação automática para funcionar com a hierarquia simplificada.
- `gm-vault-export`: atualiza exportação para detectar sessões e cenas no modelo simplificado e legado.
- `import-tools`: atualiza importadores para criar a nova estrutura física simplificada.

## Impact

- Conteúdo em `content/campaigns/**/adventures/**`.
- Importador `import_campaign.py`, especialmente `create_adventure_structure`, `create_session_structure` e os pontos que gravam cenas.
- Archetypes de `adventure`, `session` e `scene`.
- Layouts e partials que navegam por filhos e seções.
- Exportadores JSON em `layouts/index.gm-vault.json` e `layouts/_default/list.gmvault.json`.
- Possível criação de script de migração ou modo compatível para conteúdo legado.
