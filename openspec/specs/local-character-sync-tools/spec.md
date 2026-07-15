# local-character-sync-tools Specification

## Purpose
TBD - created by archiving change local-character-sync-tools. Update Purpose after archive.
## Requirements
### Requirement: Local Character Sheet Sync
O sistema SHALL disponibilizar um script utilitário de terminal para sincronizar fichas Markdown editadas manualmente, identificando novos itens, magias, talentos e classes, e importando seus dados ausentes do 5e.tools.

#### Scenario: Sync manually edited character sheet
- **WHEN** o usuário adicionar novas magias, itens, classes ou talentos diretamente no YAML frontmatter da ficha Markdown de um personagem e executar o comando de sincronização
- **THEN** o script SHALL analisar o frontmatter do arquivo, verificar quais itens listados em `spells`, `equipment`, `classes_progression` ou `feats` não possuem o caminho correspondente na lista `compendium_refs` local, baixar as páginas ausentes dos servidores do 5e.tools salvando-as no compêndio como rascunhos, e anexar as novas referências no campo `compendium_refs` do arquivo Markdown sem alterar edições manuais de outros atributos.

