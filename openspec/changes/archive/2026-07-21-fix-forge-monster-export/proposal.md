## Why

Atualmente, a exportação de fichas de monstros para o Battle System Forge (no layout `forge_statblock.html`) apresenta falhas críticas que resultam em fichas zeradas ou corrompidas. Isso ocorre porque o layout assume que dados como salvamentos e perícias são strings simples (enquanto o reconstrutor de compêndio os gera como mapas/dicionários no YAML), a regex de velocidade de caminhada descarta a informação quando precedida da palavra "walk", e o parser de características/ações não suporta a nova estrutura de cabeçalhos markdown (`##` e `###`). 
Esta mudança corrige e robustece esses parsers de forma retrocompatível.

## What Changes

- **Suporte a Saves e Skills estruturados**: Ajuste em `forge_statblock.html` para verificar se `saves` e `skills` no front matter são dicionários/mapas. Se sim, processá-los estruturalmente; se forem strings, manter o fallback por expressões regulares.
- **Extração de Velocidade Robusta**: Correção na regex de extração da velocidade de caminhada para identificar `"walk [digitos]"` mesmo em strings com múltiplos deslocamentos, mantendo compatibilidade com strings de dígitos isolados.
- **Parser Hierárquico de Ações e Características**: Atualização do parser de corpo markdown de monstros para segmentar por cabeçalhos nível 2 (`## Ações`, `## Características`) e extrair as ações individuais por cabeçalhos nível 3 (`### Nome da Ação`), mantendo o fallback para a estrutura legada baseada em negritos (`**Nome.**`).

## Capabilities

### New Capabilities
- `forge-statblock-export-fixes`: Correção e robustecimento dos mecanismos de parse do exportador de statblocks do Forge para resolver falhas em salvamentos, perícias, velocidades e habilidades de monstros.

### Modified Capabilities
*Nenhuma* (a estrutura de geração do compêndio ou o importador de campanhas não terão seus esquemas de dados alterados).

## Impact

- Afeta exclusivamente o template de layout Hugo [layouts/partials/helpers/forge_statblock.html](file:///home/filipe/Documentos/Projetos/gmvault/layouts/partials/helpers/forge_statblock.html).
- Sem impacto em bancos de dados, builds do Hugo, ou na renderização do site para leitura humana.
