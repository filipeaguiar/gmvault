## ADDED Requirements

### Requirement: Character importer generates compendium-driven frontmatter
O `import_dndbeyond.py` SHALL gerar fichas novas com referências internas para conteúdo compartilhado de ações, traços raciais, talentos, características de classe, magias e equipamentos. A ficha SHALL manter no frontmatter apenas identidade, estatísticas e estado operacional específicos do personagem, não descrições completas duplicadas de regras.

#### Scenario: Imported character action references a rule
- **WHEN** o importador encontra uma ação ou característica reutilizável durante a importação de um personagem
- **THEN** ele SHALL criar ou localizar a nota correspondente no compêndio, registrar sua URL interna em `ref` ou `compendium_refs` e gerar a entrada com nome e dados operacionais

#### Scenario: Imported character uses existing compendium content
- **WHEN** a nota traduzida ou revisada já existe no compêndio
- **THEN** a ficha gerada SHALL referenciar essa nota e SHALL NOT copiar seu corpo descritivo para `char_info`

### Requirement: Character importer preserves character-specific operational data
O importador SHALL continuar exportando dados que pertencem ao estado da ficha, como usos máximos, recarga, preparo, quantidade, equipamento, fórmulas de ataque/dano, atributos, perícias, salvaguardas e progressão.

#### Scenario: Operational state survives referential import
- **WHEN** um personagem importado possui uma ação de uso limitado, uma magia preparada ou um item equipado
- **THEN** o frontmatter SHALL preservar `max_uses`/`reset`, `prepared` ou `equipped` e os demais valores operacionais, associando o conteúdo descritivo ao compêndio por referência

### Requirement: Related content processors preserve character references
Scripts auxiliares que processam Markdown de personagens, incluindo `translate_drafts.py`, SHALL preservar URLs internas, campos `ref`, `compendium_refs` e estruturas operacionais, sem traduzir ou expandir essas referências como descrições duplicadas.

#### Scenario: Draft translation keeps character references intact
- **WHEN** um personagem ou nota relacionada passa pelo fluxo de tradução de drafts
- **THEN** as URLs internas, os slugs, os campos `ref` e as listas `compendium_refs` SHALL permanecer semanticamente inalterados, enquanto somente o texto elegível para tradução poderá ser traduzido

#### Scenario: Auxiliary processing preserves operational metadata
- **WHEN** um script auxiliar regrava o frontmatter de uma ficha
- **THEN** ele SHALL preservar `max_uses`, `reset`, `prepared`, `equipped`, `quantity`, fórmulas e demais dados específicos do personagem
