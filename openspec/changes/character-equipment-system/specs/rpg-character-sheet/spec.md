## ADDED Requirements

### Requirement: Character sheet dynamically calculates attributes and AC from equipped items
The character sheet template SHALL calculate attributes (Strength, Dexterity, etc.) and Armor Class (AC) by dynamically applying modifiers and stat overrides from all currently equipped items in `char_info.equipment`.

#### Scenario: Equipped item overrides an attribute score
- **WHEN** the character has an equipped item with `modifiers.stat_override` (e.g. strength: 21)
- **THEN** the character's calculated Strength score SHALL be set to the overridden value (e.g. 21) if it is higher than their base score, and all derived bonuses, saving throws, and skill checks SHALL update dynamically.

#### Scenario: Equipped item modifies Armor Class
- **WHEN** o personagem possui itens equipados contendo `modifiers.ac_bonus` (como um escudo com +2 ou anel de proteção com +1)
- **THEN** a Classe de Armadura (CA) calculada da personagem SHALL somar esses bônus ativos à base da armadura e modificador de Destreza.

### Requirement: Equipment tab renders advanced item properties and active status
A aba de Equipamentos da ficha de personagem SHALL exibir propriedades detalhadas para armas (alcance, tipo de dano, propriedades como finesse/versátil) e armaduras (categoria de armadura) e diferenciar visualmente itens equipados (ativos) dos não equipados (inativos).

#### Scenario: Weapon properties and range are displayed in UI
- **WHEN** uma arma é exibida na aba de Equipamentos
- **THEN** o layout SHALL renderizar seu alcance, tipo de dano e propriedades textuais de forma organizada sob ou ao lado do nome do item.

#### Scenario: Visual cues distinguish equipped items
- **WHEN** a lista de equipamentos é desenhada
- **THEN** itens equipados SHALL possuir indicador visual ativo de equipagem (como um ícone de checkbox marcado ou opacidade cheia), enquanto itens não equipados devem ser exibidos com opacidade reduzida ou indicação textual explícita de inatividade.
