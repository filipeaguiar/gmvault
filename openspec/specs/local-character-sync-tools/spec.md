# local-character-sync-tools Specification

## Purpose
TBD - created by archiving change local-character-sync-tools. Update Purpose after archive.
## Requirements
### Requirement: Local Character Sheet Sync
O sistema SHALL disponibilizar um script utilitário de terminal para sincronizar fichas Markdown editadas manualmente, identificando novos itens, magias, talentos e classes, e importando seus dados ausentes do 5e.tools.

#### Scenario: Sync manually edited character sheet
- **WHEN** o usuário adicionar novas magias, itens, classes ou talentos diretamente no YAML frontmatter da ficha Markdown de um personagem e executar o comando de sincronização
- **THEN** o script SHALL analisar o frontmatter do arquivo, verificar quais itens listados em `spells`, `equipment`, `classes_progression` ou `feats` não possuem o caminho correspondente na lista `compendium_refs` local, baixar as páginas ausentes dos servidores do 5e.tools salvando-as no compêndio como rascunhos, e anexar as novas referências no campo `compendium_refs` do arquivo Markdown sem alterar edições manuais de outros atributos.

### Requirement: Local character sync maintains references for shared character content
O sincronizador local SHALL identificar ações e características reutilizáveis listadas no frontmatter, além de magias, equipamentos, classes, raças e talentos, e SHALL garantir que cada entidade tenha uma referência interna canônica no compêndio quando houver correspondência inequívoca.

#### Scenario: Sync adds a missing action reference
- **WHEN** uma ficha contém uma ação com nome conhecido, mas sem `ref` e sem a referência correspondente em `compendium_refs`
- **THEN** o sincronizador SHALL localizar ou criar a nota do compêndio, adicionar a referência canônica e atualizar a entrada da ação sem alterar a biografia ou outros campos manuais

#### Scenario: Sync reports unresolved shared content
- **WHEN** o nome de uma ação ou característica não possui correspondência inequívoca no compêndio
- **THEN** o sincronizador SHALL manter o conteúdo existente, reportar a pendência e SHALL NOT apagar silenciosamente a descrição ou inventar uma referência

### Requirement: Local character sync removes duplicated descriptions only after validation
O sincronizador SHALL preservar descrições legadas por padrão e só poderá removê-las quando a referência interna estiver resolvida e a nota correspondente tiver conteúdo utilizável.

#### Scenario: Validated migration of a legacy description
- **WHEN** uma entrada possui `description` legado e a referência validada resolve uma nota não vazia
- **THEN** o sincronizador SHALL poder converter a entrada para o formato referencial, preservar os dados operacionais e manter intacto o corpo Markdown da ficha

#### Scenario: Missing page preserves legacy data
- **WHEN** a página referenciada não existe ou está vazia
- **THEN** o sincronizador SHALL manter a descrição legada e informar a falha sem danificar a ficha

