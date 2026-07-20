## Why

As páginas de classe, características e subclasses de Bárbaro, Bardo e Monge ainda misturam inglês e português. Isso impede o compartilhamento seguro de links de escolha de classe com jogadores que usam o vault em português.

## What Changes

- Traduzir manualmente para pt-BR as páginas de classe de Bárbaro, Bardo, Monge e Ladino e suas características diretamente referenciadas.
- Traduzir manualmente todas as páginas de subclasses disponíveis de Bárbaro, Bardo, Monge e Ladino, incluindo conteúdo de XPHB, TCE e XGE, e suas características associadas.
- Preservar YAML front matter, URLs internas, fórmulas, HTML, rolagens e metadados estruturados.
- Expor títulos em português com `titulo_pt_br` sem perder o título canônico de origem.
- Corrigir referências textuais ou HTML inválido encontrados durante a revisão editorial.

## Capabilities

### New Capabilities
- `player-class-content-translation`: Disponibiliza conteúdo de classe, características e subclasses selecionáveis de Bárbaro, Bardo, Monge e Ladino em pt-BR para compartilhamento com jogadores.

### Modified Capabilities
- `draft-translation`: A tradução editorial manual passa a cobrir páginas de classe e subclasses selecionáveis, sem depender do pós-processador automático.

## Impact

- Conteúdo em `content/compendium/classes/` e `content/compendium/rules/`.
- Metadados de exibição dos layouts que preferem `titulo_pt_br`.
- Nenhuma dependência, API, script de importação ou estrutura de URLs será alterada.
