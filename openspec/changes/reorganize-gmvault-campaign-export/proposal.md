## Why

O JSON da campanha cria uma categoria intermediária de cenas (`Aventuras → Aventura → Cenas`), embora essa pasta não represente uma entidade útil para a importação no GM Vault. Além disso, os handouts são apresentados apenas na raiz da campanha, dificultando localizar os materiais específicos de cada aventura; handouts de personagens jogadores devem continuar disponíveis na raiz.

## What Changes

- **BREAKING** Remover a categoria intermediária `Cenas de <aventura>` do export GM Vault.
- Listar as cenas diretamente dentro da categoria da respectiva aventura.
- Criar uma categoria de handouts dentro de cada aventura, contendo os handouts relacionados à aventura e às suas cenas.
- Manter uma categoria `Handouts` na raiz da campanha para materiais gerais e retratos/fichas de personagens jogadores.
- Evitar duplicação de páginas quando um handout for referenciado por mais de uma cena ou pela aventura.
- Preservar IDs estáveis, URLs e o sinalizador `visibleToPlayers` dos itens exportados.

## Capabilities

### New Capabilities

<!-- Nenhuma capacidade totalmente nova; a exportação existente será reorganizada. -->

### Modified Capabilities

- `gm-vault-export`: alterar a hierarquia exportada para colocar cenas diretamente nas aventuras e separar handouts por aventura, mantendo handouts gerais na raiz da campanha.

## Impact

- `layouts/partials/helpers/gmvault_campaign_categories.html` e `layouts/partials/helpers/gmvault_adventure_category.html`.
- Especificação e testes do formato JSON do GM Vault.
- Arquivo gerado `campaigns/<campaign-slug>/gm-vault.json` e consumidores que dependem da hierarquia atual.
- O site HTML e os arquivos Markdown não terão sua hierarquia de conteúdo alterada; a mudança é restrita à exportação JSON.
