## ADDED Requirements

### Requirement: Character importer structures advanced equipment metadata
O script de importação de personagem `import_dndbeyond.py` SHALL extrair e mapear propriedades avançadas de equipamentos (como alcance, tipo de dano, propriedades de armas/armaduras, e modificadores mágicos de atributos/CA) do inventário obtido da API do D&D Beyond e gravá-los de forma estruturada sob `char_info.equipment` no frontmatter do personagem.

#### Scenario: Weapons are imported with advanced metadata
- **WHEN** `import_dndbeyond.py` processa armas do inventário de um personagem
- **THEN** ele SHALL extrair e preencher propriedades como `range` (ex: 20/60 para arremesso), `damage_type` (ex: perfurante), `properties` (ex: finesse, arremesso) e `category` (ex: simples, marcial).

#### Scenario: Equipped items with magic modifiers are imported
- **WHEN** `import_dndbeyond.py` processa itens de inventário equipados que possuem modificadores mágicos ativos de atributos ou CA
- **THEN** ele SHALL extrair esses modificadores da definição do item (ex: definir força para 21, adicionar +1 em destreza, ou adicionar +1 na CA) e mapeá-los em um objeto estruturado `modifiers` na entrada do equipamento.
