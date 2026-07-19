## Context

O compêndio possui 455 arquivos Markdown: um `_index.md` reservado e 454 páginas de entidade. A varredura atual encontrou 171 referências diretas em `content/campaigns/` e mais 20 dependências internas alcançáveis a partir delas, totalizando 191 entidades necessárias e 263 entidades sem uso. Os geradores atuais consultam subconjuntos do 5e.tools, escolhem frequentemente a primeira entidade homônima e não persistem a fonte selecionada, o que torna ambígua a distinção entre PHB/XPHB e MM/XMM.

O conteúdo deve continuar leve, estático e editável em Markdown. O 5e.tools será a única fonte externa de conteúdo descritivo do compêndio. Tradução é uma etapa posterior, não deve publicar páginas automaticamente e usará o glossário editorial controlado.

## Goals / Non-Goals

**Goals:**

- calcular o fechamento transitivo das páginas realmente necessárias;
- resolver cada entidade em dados atuais do 5e.tools com fonte determinística;
- reconstruir páginas no schema vigente sem alterar URLs usadas;
- excluir páginas fora do fechamento após validação;
- oferecer DeepSeek V4 Pro no fluxo interativo de tradução;
- atualizar o glossário a partir de lacunas observadas no corpus selecionado;
- garantir rollback simples por Git e por staging.

**Non-Goals:**

- importar todo o catálogo do 5e.tools;
- retraduzir campanhas ou fichas de personagens;
- publicar automaticamente material importado ou traduzido;
- substituir referências de campanha por entidades XMM quando JttRC declara MM ou outra fonte;
- usar D&D Beyond, wikis, livros digitais ou outras fontes para preencher descrições do compêndio.

## Decisions

### 1. Seleção por fechamento transitivo

Um scanner produzirá referências-raiz a partir de URLs `/compendium/.../` encontradas recursivamente no YAML e no corpo Markdown de campanhas e personagens. Em seguida, seguirá referências encontradas nas páginas necessárias do próprio compêndio até atingir ponto fixo.

Isso preserva 20 regras usadas indiretamente pelas classes Rogue e Warlock. Considerar apenas as 171 referências diretas quebraria conteúdo incorporado das classes. O manifesto, e não números codificados no script, será a autoridade em cada execução.

### 2. Manifesto antes de qualquer remoção

O fluxo terá fases separadas: `scan`, `resolve`, `generate`, `validate` e `promote`. O manifesto registrará URL, kind, nome canônico, fonte, arquivo remoto, status de resolução e motivo da escolha. `promote` não será permitido enquanto houver referência sem resolução, colisão de slug ou validação inválida.

A alternativa de sobrescrever durante o download foi rejeitada porque impediria revisão e tornaria falhas de rede destrutivas.

### 3. Política determinística de fontes

A seleção seguirá esta ordem contextual:

1. fonte explicitamente declarada pela referência de JttRC ou por outro dado-fonte;
2. `XPHB` para entidades de regras de personagem quando houver versão aplicável;
3. `PHB` como fallback;
4. fonte preferencial específica do tipo, como `MPMM` para Goblin;
5. outra fonte 5e.tools somente quando o manifesto registrar a escolha sem ambiguidade.

Para monstros e itens referenciados por JttRC, a fonte declarada no livro tem precedência sobre versões mais novas de mesmo nome. A fonte escolhida será persistida para evitar que a ordem dos arrays remotos altere resultados futuros.

### 4. Proveniência estruturada

Cada página gerada terá metadados estruturais de origem, incluindo provedor `5e.tools`, tipo, nome canônico, código da publicação e caminho/identificador remoto. `title` permanecerá canônico em inglês e `titulo_pt_br` será produzido pela tradução quando solicitado. Páginas reconstruídas permanecerão em draft/status draft até revisão.

### 5. Geradores compartilhados por tipo

A reconstrução reutilizará funções de parsing por entidade, em vez de manter serializações divergentes entre importadores. Magias, monstros, itens, itens mágicos, classes, espécies, talentos e regras terão normalizadores específicos que preencham seus blocos estruturados vigentes. Importadores de campanha e personagem chamarão a mesma camada.

### 6. Exclusão apenas na promoção

Os 263 arquivos de entidade atualmente fora do fechamento serão listados no manifesto e removidos apenas durante `promote`, depois do backup lógico/diff e de todas as validações. `_index.md` e diretórios reservados não serão tratados como entidades removíveis. Arquivos novos criados após o scan exigirão novo scan antes da promoção.

### 7. DeepSeek V4 Pro como opção explícita

O menu de tradução permitirá selecionar perfis/modelos, incluindo `deepseek-v4-pro` no endpoint oficial OpenAI-compatible. O alias `deepseek-chat` não será o perfil recomendado. A chave continuará vindo de `DEEPSEEK_API_KEY`; nenhum segredo será versionado. O modelo usado continuará registrado em `translation.model`.

### 8. Auditoria de glossário orientada ao corpus

Antes da tradução, uma etapa extrairá termos frequentes e termos mecânicos do conteúdo inglês selecionado e comparará com `required_translations`, `contextual_terms`, `protected_terms` e `forbidden_outputs`. O resultado será um relatório revisável; alterações automáticas no glossário não serão promovidas sem testes e revisão. A validação pós-tradução continuará procurando tokens vazados e saídas proibidas.

## Risks / Trade-offs

- **[Fonte homônima incorreta]** → exigir fonte no manifesto e falhar em ambiguidades não cobertas pela política.
- **[Remoção de página necessária indiretamente]** → usar fechamento transitivo, validar todos os links e permitir promoção somente com manifesto atualizado.
- **[Mudança remota do mirror]** → persistir código de fonte, arquivo remoto e identidade da entidade no manifesto/página.
- **[Custo elevado da tradução V4 Pro]** → dry-run, estimativa de candidatos, tradução somente do staging e execução explícita com `--apply`.
- **[Conteúdo comercial]** → manter drafts e exigir revisão editorial antes de publicação.
- **[Tradução corromper schema]** → proteger toda proveniência e blocos mecânicos estruturais; traduzir apenas campos textuais permitidos.
- **[Conflito com mudanças locais em andamento]** → promover por conjunto controlado e revisar o diff, sem apagar alterações fora de `content/compendium/`.

## Migration Plan

1. Implementar scanner, manifesto e validadores sem alterar conteúdo.
2. Executar scan e confirmar o fechamento e a lista de exclusão.
3. Resolver todas as entidades no 5e.tools e revisar fontes selecionadas.
4. Gerar as páginas reconstruídas em staging.
5. Auditar/atualizar o glossário e testar o perfil DeepSeek V4 Pro sem traduzir o conteúdo definitivo.
6. Traduzir o staging mantendo todos os arquivos como drafts.
7. Validar YAML, schema, slugs, referências, ausência de tags 5e.tools não processadas, Hugo com e sem drafts e testes Python.
8. Promover staging e remover entidades fora do fechamento em uma única operação controlada.
9. Revisar o diff e repetir os builds.

Rollback: restaurar `content/compendium/`, manifesto e glossário pelo Git. Nenhum arquivo de campanha ou personagem será reescrito pela promoção.

## Open Questions

- A política específica para fontes não-PHB além de Goblin deverá ser confirmada pelo manifesto quando houver mais de uma alternativa equivalente.
- O modelo `deepseek-v4-pro` deve ser opção recomendada, mas a ativação como perfil padrão local continuará sendo decisão do operador para controlar custos.