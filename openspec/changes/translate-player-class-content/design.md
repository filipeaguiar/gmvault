## Context

Os arquivos importados do XPHB preservam títulos canônicos em inglês, mas parte do corpo e dos textos dos links permanece em inglês. O conteúdo será compartilhado diretamente com jogadores, inclusive para a seleção de subclasses de Bárbaro, Bardo, Monge e Ladino, portanto precisa ser legível sem expor caminhos de navegação adicionais.

## Goals / Non-Goals

**Goals:**
- Traduzir manualmente o conteúdo selecionável de Bárbaro, Bardo, Monge e Ladino, inclusive subclasses e características associadas.
- Manter links internos, YAML, HTML, dados de rolagem e fórmulas intactos.
- Usar o glossário editorial e registrar títulos localizados em `titulo_pt_br`.

**Non-Goals:**
- Não executar nem modificar `translate_drafts.py`.
- Não traduzir magias, itens, monstros, campanhas ou classes fora do escopo.
- Não alterar mecânicas, fontes, URLs canônicas ou dados importados.

## Decisions

- **Tradução arquivo a arquivo:** cada Markdown será revisado e editado individualmente. Isso evita alterações em massa e permite preservar construções específicas de cada página.
- **Título canônico preservado:** `title` continua sendo a entidade de origem; `titulo_pt_br` é adicionado ou corrigido para a interface em português. Isso preserva reconciliação de importação e permite exibição localizada.
- **Escopo por referências e fontes:** partir das páginas de Bárbaro, Bardo, Monge e Ladino e seguir as características e subclasses por elas referenciadas em XPHB, TCE e XGE. Características globais compartilhadas serão corrigidas uma vez com texto neutro de classe.
- **Validação editorial e técnica:** após cada grupo de classe, verificar front matter YAML e links; no fim, executar testes de links internos e build Hugo com drafts.

## Risks / Trade-offs

- **Terminologia inconsistente entre páginas antigas** → aplicar `translation_glossary.json` e revisar os títulos apresentados nos links.
- **HTML, dados ou fórmulas danificados por edição textual** → não alterar trechos estruturados; validar YAML e build Hugo.
- **Subclasse incompleta ou não referenciada pela página de classe** → auditar arquivos de subclass e classFeature de XPHB, TCE e XGE cuja origem seja a classe em escopo antes de declarar a etapa concluída.
