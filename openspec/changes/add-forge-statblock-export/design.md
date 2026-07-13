## Context

O Hugo já gera `gm-vault.json` para páginas home e section, e os dados de personagens e monstros são armazenados em front matter YAML. Personagens usam `char_info` (`class`, `race`, `ac`, `hp`, `stats`) e monstros importados usam `stats_meta` e `stats` (`ac`, `hp`, `speed`, `attributes`, `skills`, `senses`, `languages`, `cr`).

A extensão Forge! importa uma lista JSON de registros com `id`, `name`, `author`, `metadata`, `favorite` e `updatedAt`. Os campos `metadata` usam chaves namespaced `com.battle-system.forge/*`, incluindo as chaves compactas `Z002`, `Z004`–`Z035` demonstradas no export de Pinky.

## Goals / Non-Goals

**Goals:**

- Gerar automaticamente `exports/forge/statblocks.json` durante cada build do Hugo.
- Exportar todos os pages efetivos `character` e `monster`, inclusive monstros que ainda tenham dados estruturados incompletos.
- Produzir uma lista JSON válida e compatível com o envelope observado no export do Forge!.
- Mapear atributos, HP, CA, movimento, nível/ND e perícias para as chaves Forge conhecidas.
- Usar IDs determinísticos para evitar novos registros duplicados a cada build.
- Expor URLs copiáveis do export Forge! no Compêndio e do export GM Vault na página da campanha.

**Non-Goals:**

- Não alterar o conteúdo Markdown nem completar automaticamente statblocks que não possuem dados de origem.
- Não depender de framework JavaScript, backend, banco de dados ou biblioteca Python no build do Hugo; uma pequena ação inline de clipboard é permitida na interface.
- Não substituir ou modificar o formato existente de `gm-vault.json`.
- Não prometer sincronização bidirecional com o Owlbear Rodeo.
- Não inferir campos Forge cujo significado não está demonstrado; campos sem origem confiável usarão valores vazios ou defaults documentados.

## Decisions

1. **Output Hugo dedicado e estável**
   - Adicionar o output format `Forge` com media type `application/json`, base name `statblocks` e path `exports/forge`.
   - Habilitar esse output na home, usando `layouts/index.forge.json`, para que um único arquivo contenha personagens e monstros de todo o site.
   - A URL pública será `/exports/forge/statblocks.json` e não será criada manualmente em `static/`.
   - Alternativa rejeitada: gerar JSON por script pós-build, pois isso adicionaria uma etapa externa e poderia ficar divergente do conteúdo renderizado.

2. **Envelope e ordenação do Forge!**
   - O template emitirá um array JSON na raiz.
   - Cada item terá `id`, `name`, `author`, `metadata`, `favorite` e `updatedAt`.
   - IDs serão UUIDs determinísticos em formato textual, derivados do MD5 do permalink; personagens e monstros não mudarão de ID entre builds.
   - Personagens serão emitidos antes dos monstros; cada grupo será ordenado por `weight`, título localizado e permalink.
   - Personagens terão `in-party: true` e `favorite: true`; monstros terão `in-party: false` e `favorite: false`, permitindo que o Forge diferencie os grupos sem depender apenas da ordem.

3. **Mapeamento dos dados estruturados**
   - `Z002` e `com.battle-system.forge/name` receberão o nome localizado.
   - `Z004` receberá o nível do personagem ou o ND do monstro quando puder ser convertido para número.
   - `Z005` e `Z006` receberão HP máximo e atual; o valor será extraído do primeiro número do campo `hp`, com fallback vazio quando ausente.
   - `Z007` receberá CA numérica quando disponível.
   - `Z008` e `Z009` receberão o primeiro valor numérico do movimento, com fallback vazio.
   - `Z017`–`Z022` receberão Força, Destreza, Constituição, Inteligência, Sabedoria e Carisma.
   - `Z035` receberá perícias estruturadas como uma lista de objetos Forge com `id`, `name` e `description`.
   - O nome, `in-party`, `fabd` e demais chaves de envelope serão incluídos conforme o exemplo fornecido. Campos que não puderem ser derivados com segurança permanecerão vazios ou usarão zero somente quando o Forge exigir um valor numérico.
   - O conteúdo textual original continuará na página Markdown; a primeira versão não tentará converter automaticamente todas as ações e regras em campos compactos desconhecidos do Forge.

4. **Links de exportação**
   - A página raiz do Compêndio terá um índice Markdown estável e exibirá um link absoluto/copíavel para `/exports/forge/statblocks.json`.
   - A página de campanha usará o output format `GMVault` da própria página para obter o permalink correto de `gm-vault.json`, respeitando `baseURL` e o slug da campanha.
   - Cada URL será armazenada no atributo de dados do botão e exibida somente por um botão `Copiar URL` com `navigator.clipboard.writeText`; o endereço não será mostrado visualmente. Em caso de falha, o botão exibirá apenas uma mensagem de status.

5. **Compatibilidade de conteúdo**
   - A descoberta de tipos usará o helper `kind.html`, mantendo fallback para `params.kind` legado.
   - Páginas sem `stats` completos ainda serão exportadas com sua identidade e valores disponíveis, em vez de serem silenciosamente descartadas.
   - O export será validado como JSON e terá testes para personagens, monstros, IDs estáveis, ordenação e links.

## Risks / Trade-offs

- **[O significado de algumas chaves `Z` do Forge não está documentado no repositório] →** mapear apenas as chaves demonstradas e documentar defaults; preservar a origem Markdown para revisão manual.
- **[Monstros sem `stats` completos terão statblocks parciais] →** incluir todos os monstros com campos vazios e testar que nenhum page é perdido.
- **[O Forge pode alterar o schema compacto em versões futuras] →** manter o envelope isolado em um partial/template e validar contra um fixture do export fornecido.
- **[IDs determinísticos podem colidir se dois pages tiverem o mesmo permalink efetivo] →** derivar o ID do permalink completo e testar unicidade no export.
- **[Links públicos expõem conteúdo conforme a visibilidade do site] →** manter o comportamento editorial atual; a URL é pública e não é autenticação.

## Migration Plan

1. Adicionar o output Forge e os templates/helpers sem alterar o output GM Vault existente.
2. Criar o índice do Compêndio e os links nas páginas.
3. Executar `hugo --gc --minify`, validar o array JSON e revisar o fixture resultante no Forge!.
4. Em caso de rollback, remover o output `Forge`, os templates e os links; os Markdown e o `gm-vault.json` continuam válidos.

## Open Questions

- Confirmar em uma importação real do Owlbear Rodeo se `Z005`/`Z006` representam HP máximo/atual e se `Z008`/`Z009` representam movimento normal/máximo. A primeira implementação deve manter esses campos configuráveis em um helper isolado.
