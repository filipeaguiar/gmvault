## Why

A divisão de Aventura -> Sessão -> Cenas adiciona complexidade desnecessária tanto na navegação manual do usuário quanto na serialização e exportação de dados para o `gm-vault`. O agrupamento direto de Aventura -> Cenas torna o planejamento do mestre e a visualização do site mais ágeis e leves.

## What Changes

- Remoção do nível intermediário "Sessão" no layout visual da aventura, listando as Cenas diretamente na timeline de preparativos.
- Achatamento do layout de exportação JSON (`gm-vault.json`), de modo a agrupar as cenas e handouts correspondentes diretamente sob a respectiva aventura.
- Adaptação do importador Python para gerar e persistir os stubs das cenas diretamente na pasta raiz da aventura, em vez de aninhá-los em subpastas `001-inicio`.
- Ajustes de retrocompatibilidade para que cenas antigas (aninhadas sob pastas de sessões legadas) continuem sendo indexadas e exibidas de forma transparente na timeline direta da Aventura.

## Capabilities

### New Capabilities

### Modified Capabilities
- `import-tools`: Mapeamento físico de novos capítulos de aventuras no disco estruturado diretamente sob a raiz da aventura, sem subpastas de sessão.
- `index-layout`: Exibição direta das cenas/tópicos na linha do tempo de preparos de jogo na página da aventura.
- `gm-vault-export`: Exportação do JSON do `gm-vault` agrupando as cenas diretamente sob a aventura correspondente.

## Impact

- Código do importador `import_campaign.py` (Modo 2 de Antologia).
- Layouts do Hugo `layouts/partials/kinds/adventure.html` e `layouts/partials/helpers/gmvault_adventure_category.html`.
- Arquivos de testes em `tests/test_adventure_introduction_rendering.py`.
