## 1. Contrato de dados e auditoria

- [x] 1.1 Catalogar o `char_info` de Pinky, classificando cada campo como dado específico, estado operacional ou conteúdo compartilhado.
- [x] 1.2 Definir e documentar o formato canônico de `ref` para ações, traços, talentos, características, magias e equipamentos, incluindo a precedência entre `ref` da entrada e `compendium_refs`.
- [x] 1.3 Mapear as descrições de ações e características de Pinky para notas existentes e listar as notas do compêndio que precisam ser criadas, traduzidas ou corrigidas.
- [x] 1.4 Atualizar `archetypes/character.md` com a estrutura referencial e os campos operacionais mínimos, sem descrições duplicadas de regras.
- [x] 1.5 Auditar `translate_drafts.py`, `content_roles.py` e demais scripts que regravam ou filtram conteúdo para confirmar a preservação de `ref`, `compendium_refs` e metadados operacionais.

## 2. Conteúdo e migração de Pinky

- [x] 2.1 Criar ou completar notas do compêndio para ações básicas e características reutilizáveis de Pinky que não tenham correspondência válida.
- [x] 2.2 Corrigir referências canônicas de raça, classe, talentos, regras, magias e equipamentos de Pinky, removendo duplicidades somente quando a referência correta estiver validada.
- [x] 2.3 Adicionar `ref` às ações e características de Pinky, preservando `name`, `source`, `max_uses`, `reset`, preparo, quantidade, equipamento e fórmulas.
- [x] 2.4 Remover de Pinky apenas as descrições textuais cobertas por notas resolvíveis do compêndio e manter fallback legado para qualquer item ainda não validado.

## 3. Resolução no layout Hugo

- [x] 3.1 Criar uma parcial auxiliar para resolver URL interna com `site.GetPage` e retornar estado de página resolvida, ausente ou vazia sem interromper o build.
- [x] 3.2 Atualizar a aba de Ações para renderizar conteúdo por `ref`, mantendo o acompanhamento de usos e fallback para `description` legado.
- [x] 3.3 Atualizar as abas de Características e Classe para resolver notas de raça, talentos, regras e características pelo compêndio em vez de depender de descrições no frontmatter.
- [x] 3.4 Atualizar a aba de Equipamentos e o Grimório para usar a página referenciada como fonte de descrição e metadados, preservando os valores específicos da ficha.
- [x] 3.5 Exibir fallback identificável para referências ausentes sem quebrar o build e evitar que a resolução crie navegação indevida para conteúdo GM em contexto player-facing.

## 4. Sincronizador local

- [x] 4.1 Estender `scripts/sync_character.py` para descobrir referências de ações e características e registrar pendências não resolvidas.
- [x] 4.2 Fazer o sincronizador atualizar `ref` e `compendium_refs` apenas após localizar ou criar uma nota utilizável, preservando descrições legadas quando a validação falhar.
- [x] 4.3 Adicionar testes em `tests/test_sync_character.py` para refs ausentes, conteúdo não resolvido, preservação de biografia e preservação de campos manuais.

## 5. Importador de personagens

- [x] 5.1 Atualizar `import_dndbeyond.py` para gerar ações e características com referências internas e sem copiar descrições completas de regras para novas fichas.
- [x] 5.2 Garantir que o importador continue gerando dados operacionais de personagem, incluindo usos, recargas, preparo, equipamento, quantidades, fórmulas, estatísticas e progressão.
- [x] 5.3 Adicionar ou ajustar testes do importador para verificar o formato referencial e a criação/reutilização de notas do compêndio.
- [x] 5.4 Atualizar scripts auxiliares de tradução/processamento para não alterar refs, slugs ou dados operacionais das fichas.

## 6. Migração gradual e validação

- [x] 6.1 Auditar as demais fichas atuais de personagem e migrar somente descrições com correspondência validada no compêndio.
- [x] 6.2 Criar uma ficha de teste a partir do archetype e confirmar que ela usa a mesma estrutura esperada pelo layout e pelo sincronizador.
- [x] 6.3 Executar `pytest` com a suíte relevante e corrigir regressões de importação, sincronização, tradução e renderização.
- [x] 6.4 Executar `hugo -D --gc --minify` e `hugo --gc --minify`, verificando Pinky, referências ausentes e conteúdo player-facing.
- [x] 6.5 Revisar o diff final para confirmar que o corpo Markdown das fichas e os dados operacionais não foram alterados indevidamente.

## 7. Melhorias finais

- [x] 7.1 Adicionar ícones visíveis aos itens individuais da aba de Equipamentos, diferenciando armas, armaduras e outros itens.
- [x] 7.2 Preencher páginas vazias de classes e subclasses a partir das features baixadas do 5e.tools, preservando páginas já revisadas.
- [x] 7.3 Usar automaticamente a imagem do handout local como avatar quando a API não fornecer uma imagem e validar o caso de Pinky.
- [x] 7.4 Validar as melhorias com testes e builds Hugo de desenvolvimento e produção.
