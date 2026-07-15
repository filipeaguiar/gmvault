## ADDED Requirements

### Requirement: Character archetype uses compendium-driven structure
O archetype `archetypes/character.md` SHALL gerar novas fichas com campos separados para dados específicos, estado operacional e referências de conteúdo compartilhado. O formato gerado SHALL incluir `compendium_refs` e estruturas referenciais para ações, equipamentos e magias, sem inserir descrições completas de regras no frontmatter.

#### Scenario: New manual character starts with referential fields
- **WHEN** um editor cria uma ficha usando o archetype de personagem
- **THEN** o arquivo SHALL conter a estrutura de `char_info` e referências necessária para apontar ao compêndio, além de campos operacionais editáveis, sem um bloco de descrição duplicada de regra

#### Scenario: Archetype remains usable before references are known
- **WHEN** uma nova ficha é criada antes de suas regras específicas serem identificadas
- **THEN** o archetype SHALL permitir listas vazias ou refs pendentes sem inserir texto fictício, e o sincronizador SHALL poder completar as referências posteriormente

### Requirement: Character content contract applies to generated and authored pages
O modelo de conteúdo SHALL tratar o formato referencial como contrato para fichas migradas, fichas criadas manualmente e fichas geradas por importadores, mantendo compatibilidade de leitura para descrições legadas durante a migração.

#### Scenario: Generated and manual pages use the same shape
- **WHEN** uma ficha é criada pelo archetype ou por `import_dndbeyond.py`
- **THEN** ambas SHALL usar os mesmos campos referenciais e operacionais esperados pelo layout de personagem

#### Scenario: Legacy page remains readable
- **WHEN** uma ficha existente ainda contém descrição no frontmatter e não possui uma ref resolvível
- **THEN** os layouts SHALL continuar renderizando essa ficha até que a migração seja validada
