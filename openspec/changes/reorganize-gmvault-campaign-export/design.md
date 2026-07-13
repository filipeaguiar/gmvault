## Context

O exportador atual é gerado pelos partials Hugo `gmvault_campaign_categories.html` e `gmvault_adventure_category.html`. A categoria de cada aventura contém uma categoria intermediária de cenas, e os handouts da campanha são coletados apenas em uma categoria global. Os arquivos Markdown continuam usando a hierarquia editorial atual; somente a árvore serializada do JSON será alterada.

As relações de handouts são armazenadas como URLs internas em `Params.handouts` nas aventuras e cenas. A seção `campaign/handouts` contém tanto materiais gerais quanto retratos de personagens jogadores.

## Goals / Non-Goals

**Goals:**

- Exportar cenas diretamente como itens da categoria da aventura.
- Criar uma categoria `Handouts` dentro de cada aventura quando houver handouts relacionados.
- Resolver handouts declarados no front matter da aventura e de todas as suas cenas.
- Deduplicar handouts dentro de cada aventura quando forem referenciados pela aventura e por múltiplas cenas.
- Manter a categoria `Handouts` na raiz da campanha para handouts não associados a nenhuma aventura, incluindo retratos de personagens jogadores.
- Preservar IDs, URLs, nomes e `visibleToPlayers` através do helper de item existente.
- Manter compatibilidade com hierarquias simplificada, legada e mista de sessões/cenas.

**Non-Goals:**

- Não mover ou renomear arquivos Markdown.
- Não alterar a navegação HTML nem o comportamento de visibilidade do site.
- Não alterar o formato dos itens de página ou os identificadores existentes.
- Não criar uma nova API ou dependência externa.

## Decisions

1. **Cenas como itens diretos da aventura**
   - O partial da aventura continuará descobrindo cenas por `kind` e pelo permalink, mas adicionará cada cena diretamente à lista `items` da aventura.
   - A categoria `Cenas de <aventura>` será removida.
   - Categorias já existentes para outros agrupamentos, como NPCs, serão preservadas para não perder relações existentes.
   - Alternativa rejeitada: manter a categoria de cenas e apenas renomeá-la, pois isso não elimina o nível de navegação solicitado.

2. **Handouts relacionados dentro da aventura**
   - Para cada aventura, serão coletadas as URLs em `adventure.Params.handouts` e em `Params.handouts` de todas as cenas descobertas.
   - Cada URL será resolvida com `site.GetPage`; referências ausentes serão ignoradas no JSON, como ocorre nos agrupamentos estruturados existentes.
   - Uma categoria `Handouts` será adicionada aos itens da aventura quando houver pelo menos um handout resolvido.
   - A lista será deduplicada por permalink/URL dentro da aventura. Um handout compartilhado entre aventuras poderá aparecer nas categorias das aventuras relevantes, mas não será repetido dentro da mesma aventura.
   - Alternativa rejeitada: inferir handouts apenas pela localização física dos arquivos, pois os handouts ficam na seção compartilhada da campanha e não em diretórios filhos das cenas.

3. **Handouts gerais na raiz da campanha**
   - A categoria raiz `Handouts` continuará sendo construída a partir da seção `campaign/handouts`.
   - Ela conterá somente páginas `kind: handout` que não tenham sido associadas a nenhuma aventura por `Params.handouts` da aventura ou de suas cenas.
   - Assim, retratos de personagens jogadores e materiais gerais permanecem na raiz, enquanto materiais de aventura ficam organizados na aventura.
   - Se não houver handouts gerais, a categoria raiz não será emitida.

4. **Compatibilidade e metadados**
   - A descoberta de cenas continuará usando `kind` efetivo, preservando o suporte a front matter legado em `params.kind`.
   - Itens continuarão sendo criados exclusivamente por `gmvault_page_item.html`, preservando IDs determinísticos, URLs e `visibleToPlayers`.

## Risks / Trade-offs

- **[Mudança incompatível para consumidores que procuram a categoria `Cenas de ...`] →** documentar a nova árvore e validar o JSON gerado em testes e no build do site.
- **[Referências de handout ausentes deixam materiais fora da categoria de aventura] →** manter o handout na categoria raiz quando ele não estiver associado por front matter.
- **[Um handout compartilhado entre aventuras pode aparecer em mais de uma aventura] →** deduplicar dentro de cada aventura e documentar que a associação é por aventura, não uma cópia física do arquivo.
- **[Categorias vazias podem poluir a árvore] →** emitir categorias de handouts somente quando a lista de itens resolvidos não estiver vazia.
