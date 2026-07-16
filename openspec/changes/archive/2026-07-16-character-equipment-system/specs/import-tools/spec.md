## ADDED Requirements

### Requirement: Character importer structures advanced metadata in compendium item pages
O script de importação de personagem `import_dndbeyond.py` SHALL gravar propriedades detalhadas de itens (como alcance, tipo de dano, propriedades de armas/armaduras, e modificadores mágicos de atributos/CA) sob `item_info` no frontmatter das respectivas páginas de compêndio criadas ou sincronizadas.

#### Scenario: Weapons are created in compendium with details
- **WHEN** o importador cria ou atualiza um item de arma no compêndio
- **THEN** ele SHALL incluir sob `item_info` campos para `type: "Weapon"`, `damage` (ex: 1d6), `damage_type` (ex: piercing), `properties` (ex: finesse, light), e `range` (ex: 20/60).

#### Scenario: Magic items are created in compendium with modifiers
- **WHEN** o importador cria ou atualiza um item mágico no compêndio que concede atributos fixos, bônus ou CA
- **THEN** ele SHALL incluir sob `item_info.modifiers` as estruturas `stat_override`, `stat_bonus`, `ac_bonus` ou `save_bonus`.

### Requirement: Character importer references compendium items in character frontmatter
O importador SHALL salvar a lista de equipamentos sob `char_info.equipment` no frontmatter do personagem contendo apenas referências para o compêndio e dados operacionais básicos.

#### Scenario: Inventory items are mapped to character equipment list
- **WHEN** um personagem é importado com itens no inventário
- **THEN** a lista de equipamentos gerada no frontmatter do personagem SHALL listar cada item contendo apenas `name`, `ref` (apontando para a página do compêndio correspondente), `quantity` e `equipped` (indicando se está ativo/vestido).
