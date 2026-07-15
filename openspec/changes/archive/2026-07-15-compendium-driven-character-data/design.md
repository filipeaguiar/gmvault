## Context

As fichas atuais misturam três categorias no mesmo `char_info`: valores específicos do personagem, estado operacional da sessão e texto reutilizável de regras. Pinky exemplifica o problema: atributos, salvaguardas, perícias, moedas, preparo de magias, usos e fórmulas são dados próprios; já as descrições de `Sneak Attack`, `Cunning Action`, `Healing Hands`, `Firearm Specialist`, `Vex`, `Slow` e ações básicas são conteúdo de regra que pode ser compartilhado. A ficha já possui `compendium_refs` e o layout já resolve algumas páginas para magias, classes, talentos e regras, mas ações e características ainda renderizam texto copiado do frontmatter.

A mudança atravessa conteúdo, templates, o archetype de personagem e todos os fluxos que geram ou transformam fichas. Deve continuar compatível com fichas legadas durante a migração, funcionar sem banco de dados e manter `site.GetPage` como mecanismo de resolução no build. O formato resultante deve ser o padrão para personagens atuais migrados e para personagens futuros criados manualmente ou por importação.

## Goals / Non-Goals

**Goals:**

- Definir uma separação clara entre estado do personagem e conteúdo de regra reutilizável.
- Fazer o layout resolver referências internas do compêndio e renderizar a nota correspondente no build.
- Migrar Pinky como caso de referência, identificando e corrigindo referências ausentes ou ambíguas.
- Fazer o archetype, o importador e `sync_character.py` produzirem e manterem o formato referencial.
- Garantir que scripts auxiliares, como `translate_drafts.py`, preservem URLs internas, `ref`, `compendium_refs` e o estado operacional das fichas.
- Manter fallback legível para referências ausentes e compatibilidade com descrições de fichas antigas.
- Permitir que traduções e correções sejam feitas uma vez na nota do compêndio.

**Non-Goals:**

- Não substituir atributos, salvaguardas, perícias, moedas, HP, CA, preparo, usos, recargas, quantidades ou fórmulas específicos do personagem por páginas do compêndio.
- Não criar autenticação ou tratar `visibility` como mecanismo de segurança.
- Não importar automaticamente todo o compêndio nem alterar em massa fichas sem referência verificável.
- Não resolver entidades por nome de forma silenciosa quando houver uma referência explícita conflitante.

## Decisions

### 1. Referências explícitas no estado operacional

Entradas de `char_info.actions` passarão a aceitar `ref` como fonte do texto e manterão apenas `name` (rótulo local), `ref`, `source`, `max_uses` e `reset`. O layout tentará resolver `ref` com `site.GetPage`. O nome e os dados de uso permanecem na ficha porque podem ser específicos da personagem ou da forma como o recurso é acompanhado.

Equipamentos, magias, classes, raças e talentos continuarão referenciados pelos campos já existentes. Quando o conteúdo da página relacionada for necessário, o template usará a referência da entrada ou a referência correspondente em `compendium_refs`, em vez de copiar descrição para `char_info`.

Alternativa rejeitada: inferir todas as páginas pelo nome em cada renderização. Isso falha com homônimos, variantes de edição e nomes traduzidos; a inferência poderá ser usada apenas pelo importador/sincronizador para preencher uma referência persistida.

### 2. Resolver conteúdo em um helper de template

A resolução será centralizada em uma parcial auxiliar que recebe uma URL interna e retorna a página, com tratamento para página inexistente. A parcial de personagem ficará responsável pela apresentação e pelos dados operacionais, não por repetir regras de resolução para cada categoria.

Quando houver página resolvida, será renderizado o conteúdo da nota correspondente. Quando não houver, o layout exibirá o nome e um aviso/fallback controlado, sem quebrar o build. O fallback da descrição legada será usado somente para fichas antigas que ainda possuem `description`, permitindo migração gradual.

Alternativa rejeitada: copiar o corpo do compêndio para o frontmatter durante o import. Isso preserva justamente a duplicação que a mudança elimina e impede traduções centralizadas.

### 3. Fonte de verdade por categoria

- `char_info`: atributos, modificadores, CA, HP, deslocamentos, sentidos, idiomas, perícias, moedas e estado de uso/preparo/equipamento.
- `compendium_refs` e `ref` por entrada: identidade e conteúdo de regras, itens, magias, talentos, raça, classe e características.
- Corpo da nota do compêndio: descrição traduzível, regras e metadados compartilhados.

Para Pinky, ações básicas e características sem nota correspondente receberão notas de regra reutilizáveis ou referências para notas existentes. Itens cujo caminho atual estiver incorreto ou duplicado serão corrigidos para uma única referência canônica, sem apagar o item do inventário.

### 4. Migração e compatibilidade

A primeira migração será auditável: comparar cada descrição de Pinky com as notas referenciadas, criar/completar notas faltantes, adicionar `ref` e remover somente texto duplicado comprovadamente coberto pelo compêndio. Fichas legadas que ainda tenham `description` continuarão renderizando por fallback.

O importador deve escrever o novo formato para fichas novas. O sincronizador deve adicionar refs faltantes e preservar corpo Markdown e demais campos manuais. A remoção de descrições de fichas existentes será feita apenas quando houver uma referência resolvida e validada.

### 5. Archetype como contrato para fichas futuras

`archetypes/character.md` será atualizado para conter a forma mínima referencial: entradas de ações e equipamentos com `ref` quando conhecidos, campos operacionais separados e nenhum bloco de descrição de regra. O archetype não tentará preencher regras específicas de uma classe; ele fornecerá a estrutura e instruções para que referências sejam adicionadas pelo editor ou pelo sincronizador.

Alternativa rejeitada: deixar o archetype como um exemplo textual genérico e depender de cada importador para definir o formato. Isso perpetua divergências entre fichas manuais e importadas.

### 6. Tradução e visibilidade

A tradução será aplicada nas notas do compêndio, não na ficha. Páginas necessárias para uma ficha player-facing devem ser publicáveis e ter conteúdo seguro para jogadores; referências GM não serão expostas como navegação automática. `translate_drafts.py` deve proteger URLs, campos `ref` e listas de referências e continuar traduzindo somente conteúdo textual elegível das notas. O layout deve manter o fallback bruto para diagnóstico durante desenvolvimento, sem tratar isso como proteção de conteúdo.

## Risks / Trade-offs

- **[Referência ausente ou slug incorreto]** → Validar todas as refs de Pinky no build, exibir fallback não fatal e fazer o sincronizador reportar referências não resolvidas.
- **[Mudança do texto compartilhado altera várias fichas]** → Tratar o compêndio como fonte de verdade, revisar notas antes de publicar e manter o diff de migração pequeno e auditável.
- **[Descrições legadas podem divergir da nota]** → Não remover texto automaticamente; exigir correspondência de uma página resolvida antes de apagar a cópia.
- **[Páginas do compêndio em draft não aparecem em build de produção]** → Criar/ajustar notas com status editorial adequado antes de depender delas em fichas públicas e testar builds com e sem drafts.
- **[Compatibilidade com dados gerados em formatos diferentes]** → Aceitar referências em entradas estruturadas e em `compendium_refs`, preservando fallback para `params.kind` e frontmatter legado.
- **[Regras específicas de armas ou talentos não têm nota granular]** → Reusar a nota da entidade quando suficiente; criar uma nota de regra específica apenas quando a propriedade não puder ser representada sem ambiguidade.

## Migration Plan

1. Auditar Pinky, listar cada descrição e classificar como dado específico, regra compartilhada ou conteúdo ainda sem nota.
2. Corrigir/criar notas do compêndio e referências canônicas para as regras reutilizáveis.
3. Atualizar o layout para resolver refs e manter fallback legado.
4. Atualizar o archetype de personagem e validar a criação de uma ficha nova com a estrutura referencial.
5. Refatorar Pinky e validar `hugo -D --gc --minify` e `hugo --gc --minify`.
6. Atualizar importador, sincronizador, tradutor de drafts e testes para geração, resolução, tradução e preservação de fichas antigas.
7. Auditar as demais fichas e migrar somente entradas com correspondência validada.

Rollback: restaurar os arquivos de conteúdo e templates do commit anterior. Como a migração preserva fallback, uma reversão parcial de conteúdo não deve impedir o build.

## Open Questions

- Quais ações básicas devem ter notas próprias no compêndio e quais podem compartilhar uma nota de regras gerais?
- O campo `ref` deve ser obrigatório para toda ação nova ou o sincronizador poderá criar uma referência somente quando encontrar correspondência inequívoca?
- As notas de itens mágicos existentes, como `musket-3` e `pistol-2`, devem permanecer em `magic-items` ou ser normalizadas junto às notas de itens base?
