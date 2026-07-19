## Context

`import_dndbeyond.py` mistura obtenção de uma ficha da API do D&D Beyond com a materialização de referências 5e.tools. `create_character.py` e `edit_character.py` já usam `dnd_utils`, mas não têm um caminho único para garantir todas as entradas que uma ficha local referencia. O vault deve manter fichas existentes renderizáveis e não depender da API do D&D Beyond.

## Goals / Non-Goals

**Goals:**
- Concentrar a sincronização de compêndio de personagens locais em helpers reutilizáveis.
- Permitir que criação e edição materializem classes, espécies, subclasses, talentos, regras/características, ações padrão, magias, itens e itens mágicos antes de registrar referências.
- Oferecer, no editor, uma sincronização explícita da ficha existente para completar referências históricas.
- Remover o importador D&D Beyond e sua documentação como interface suportada.

**Non-Goals:**
- Recriar a importação de fichas pela API D&D Beyond.
- Alterar o modelo editorial do compêndio, traduzir conteúdo automaticamente ou tornar `visibility` um controle de segurança.
- Inferir dados ausentes ou sobrescrever conteúdo editorial quando uma entidade não puder ser resolvida sem ambiguidade.

## Decisions

### Serviço compartilhado de sincronização orientado à ficha
A lógica de resolução atualmente exclusiva do importador será extraída para `dnd_utils` (ou módulo local equivalente) como helpers orientados a entidades e a uma estrutura de `char_info`. Os scripts de criação e edição serão os únicos pontos de entrada. Isto evita duplicar a busca 5e.tools e mantém serialização e fallback canônicos. Copiar a lógica para os dois scripts foi descartado por divergir comportamento e correções.

### Sincronização antes da escrita e ação explícita para fichas existentes
A criação chamará o sincronizador antes de persistir a nova ficha. O editor chamará o sincronizador depois de operações que introduzem referências e disponibilizará uma ação para sincronizar a ficha inteira. Assim, dados legados já gravados não exigem edição manual para obter páginas do compêndio. O sincronizador retornará referências resolvidas e itens não resolvidos, sem fabricar URLs.

### Preservar estado da ficha e páginas editoriais
O serviço só adicionará/deduplicará referências e atualizará entradas operacionais que tenham resolução canônica. Ele não removerá dados legados não resolvidos nem substituirá corpos Markdown, traduções ou metadados editoriais de páginas existentes. Esta escolha favorece compatibilidade e revisão manual sobre uma sincronização destrutiva.

### Remoção do importador como interface pública
`import_dndbeyond.py` será removido junto com chamadas e documentação que o apresentem como comando. Requisitos de importação de ficha serão removidos ou transferidos para os fluxos locais. O histórico de Markdown gerado continuará válido por depender de URLs internas e dados operacionais, não do executável.

## Risks / Trade-offs

- [Cobertura incompleta de formatos legados de `char_info`] → Implementar normalizadores defensivos, relatar entidades não resolvidas e manter os campos originais.
- [Falha de rede ou mudança no mirror] → Tratar cada entidade independentemente, manter referências locais existentes e concluir a operação com relatório de falhas.
- [Sincronização excessiva no fluxo interativo] → Reutilizar páginas locais quando existentes, deduplicar entidades e limitar resolução às referências presentes na ficha.
- [Remoção quebra automações externas] → Documentar a quebra e manter fichas já importadas sem migração obrigatória.

## Migration Plan

1. Introduzir o sincronizador compartilhado e testes unitários com dados/fixtures locais.
2. Integrar criação e edição, incluindo a ação de sincronização completa no editor.
3. Validar criação, edição e renderização de uma ficha existente com referências resolvidas e não resolvidas.
4. Remover `import_dndbeyond.py` e atualizar documentação/especificações.
5. Rollback: restaurar o arquivo removido e reverter as integrações; páginas de compêndio e fichas criadas durante a migração permanecem compatíveis.
