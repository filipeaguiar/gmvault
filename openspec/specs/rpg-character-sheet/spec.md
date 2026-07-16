# rpg-character-sheet Specification

## Purpose
TBD - created by archiving change rpg-character-sheet. Update Purpose after archive.
## Requirements
### Requirement: Tab Navigation Interface
O sistema SHALL disponibilizar uma barra de abas interativas no topo da visualização da ficha do personagem ("Atributos", "Perícias", "Ações", "Equipamentos", "Grimório" [se conjurador], "Classe", "Características" e "Imagem") para comutação de conteúdo.

#### Scenario: Tab switching activation
- **WHEN** o usuário clica em uma aba na barra de navegação da ficha
- **THEN** o sistema SHALL alternar a visualização ocultando as demais áreas e exibindo apenas a correspondente à aba selecionada, sem realizar recarga de página (através de CSS puro ou Vanilla JS leve).

### Requirement: Square Attribute and Highlight Modifiers
O sistema SHALL exibir cada um dos 6 atributos principais do personagem em um elemento visual quadrado, com destaque visual maior para o modificador calculado e menor para o valor base associado, e também exibir as estatísticas traduzidas em português.

#### Scenario: Render attributes visual boxes
- **WHEN** a ficha do personagem é renderizada no Hugo
- **THEN** o sistema SHALL desenhar Força, Destreza, Constituição, Inteligência, Sabedoria e Carisma em caixas quadradas destacando o modificador (ex: +3) de forma proeminente, exibindo o valor base (ex: 16), e SHALL exibir na mesma aba, de forma destacada e traduzida para o português brasileiro oficial de D&D 5e:
  - Classe de Armadura (AC)
  - Pontos de Vida Atuais e Máximos (HP Máximo)
  - Deslocamento (Speed)
  - Bônus de Proficiência (Proficiency Bonus)
  - Salvaguardas (Saving Throws) de todos os atributos
  - Sentidos Passivos (Passive Senses), incluindo Percepção Passiva (Passive Perception) e outros sentidos cadastrados
  - Ouro acumulado
  - Classe de Dificuldade (DC) de Magia (se aplicável)

### Requirement: Column Skills and Expertise Highlights
O sistema SHALL exibir a lista de perícias do personagem dividida em duas colunas ordenadas alfabeticamente na aba de Perícias, com marcadores visuais diferenciados para indicar proficiência simples ou especialização (expertise).

#### Scenario: Render skills list
- **WHEN** a aba de Perícias é exibida
- **THEN** o sistema SHALL renderizar a lista de todas as perícias (Skills) em 2 colunas, exibindo o bônus total de cada perícia, um indicador visual preenchido se o personagem for proficiente, e um indicador com símbolo alternativo (como uma estrela ou marcação em dobro) caso ele possua especialização (expertise).

### Requirement: Categorized Equipment List
O sistema SHALL exibir o inventário do personagem sob a aba de Equipamentos, dividido de forma estruturada em Armas e Armaduras, Itens Consumíveis e Outros Itens, com ícones dedicados e metadados operacionais.

#### Scenario: Render categorized inventory
- **WHEN** a aba de Equipamentos é exibida
- **THEN** o sistema SHALL listar os itens do personagem em três seções separadas: Armas e Armaduras (com ícones dedicados e fórmulas de rolagem de ataque/dano baseadas nos metadados), Itens Consumíveis (como poções e pergaminhos cujas informações podem ser puxadas e completadas a partir do compêndio correspondente) e Outros Itens (itens gerais de aventura).

### Requirement: Caster Grimoire by Level
O sistema SHALL renderizar a aba de Grimório exclusivamente para personagens capazes de conjurar magias, agrupando suas magias conhecidas por nível.

#### Scenario: Render grimoire cards
- **WHEN** o personagem possuir magias cadastradas em sua ficha e a aba de Grimório for acessada
- **THEN** o sistema SHALL listar todas as magias divididas por nível de círculo (truques, 1º nível, 2º nível, etc.), exibindo cada magia em um card individual com metadados cruciais (tempo de conjuração, alcance, duração, escola e link direto para os detalhes da magia no compêndio).

### Requirement: Character Portrait Tab
O sistema SHALL renderizar na última aba da ficha ("Imagem") a ilustração oficial do personagem em tamanho de destaque.

#### Scenario: Render character avatar image
- **WHEN** a última aba ("Imagem") for ativada pelo usuário
- **THEN** o sistema SHALL ler a URL ou caminho do arquivo da imagem especificada no frontmatter do personagem (ex: `image` ou `avatar`) e exibi-la de forma centralizada e redimensionada na aba, com um fallback amigável caso a imagem esteja ausente.

### Requirement: Character Actions Tracker
O sistema SHALL renderizar a aba de Ações exibindo as ações padrão de combate e exploração do personagem combinadas com ações especiais de sua classe/subclasse, incluindo o controle visual de recursos de uso limitado.

#### Scenario: Render actions with limited use checkboxes
- **WHEN** a aba de Ações for ativada
- **THEN** o sistema SHALL listar todas as ações padrão (Ataque, Conconjurar Magia, Desengajar, Disparar, Esconder, Ajudar, Usar Objeto, Esquivar) e as ações especiais de classe/subclasse do personagem, e desenhar caixas de marcação (checkboxes) clicáveis correspondentes à quantidade total máxima de usos permitidos dos recursos limitados (ex: Fúria, Inspiração Bárdica, Canalizar Divindade) para fins de acompanhamento interativo.

### Requirement: Class and Subclass Progression
O sistema SHALL exibir a aba de Classe contendo detalhes sobre a descrição da classe e subclasse do personagem e o que se obtém em cada nível de progressão.

#### Scenario: Render subclass and level benefits
- **WHEN** a aba de Classe for ativada
- **THEN** o sistema SHALL exibir de forma hierárquica e estruturada os nomes e as descrições da classe e subclasse, acompanhados de uma tabela ou lista cronológica descrevendo os recursos, talentos e atributos obtidos em cada nível alcançado.

### Requirement: Features and Traits Translation
O sistema SHALL exibir na aba de Características todos os traços raciais, características de classe e talentos do personagem traduzidos para o português brasileiro oficial de D&D 5e.

#### Scenario: Render translated traits list
- **WHEN** a aba de Características for ativada
- **THEN** o sistema SHALL exibir a lista completa de características de raça, classe e talentos do personagem (Features & Traits), traduzindo termos técnicos de jogo para o português brasileiro de forma consistente.

### Requirement: VTT Iframe Compatibility
O sistema SHALL suportar a renderização da ficha de personagem em elementos iframe compactos de mesas virtuais de RPG (VTT), ajustando dinamicamente dimensões, margens e barras de rolagem.

#### Scenario: Adapt rendering in constrained iframe
- **WHEN** a página da ficha de personagem for carregada dentro de um iframe em uma tela de VTT
- **THEN** o sistema SHALL remover margens externas amplas do layout, compactar o espaçamento do menu de abas e aplicar comportamento de rolagem interna suave nas abas (`overflow-y: auto`) para evitar o surgimento de barras de rolagem dupla na interface do usuário.

### Requirement: Character rule content is resolved from compendium references
A ficha de personagem SHALL use referências internas (`ref` ou `compendium_refs`) para resolver no compêndio o conteúdo compartilhado de ações, traços raciais, talentos, características de classe, magias e equipamentos. O layout SHALL use `site.GetPage` durante o build e renderizar o conteúdo da página resolvida sem copiar a descrição para o frontmatter.

#### Scenario: Pinky action uses a compendium page
- **WHEN** uma ação de Pinky possui `ref: /compendium/rules/sneak-attack/`
- **THEN** a ficha SHALL renderizar o título e o conteúdo da nota resolvida do compêndio, mantendo na ficha apenas o nome e os dados operacionais da ação

#### Scenario: Referenced spell and equipment use canonical content
- **WHEN** uma magia ou equipamento da ficha possui uma referência interna válida
- **THEN** o layout SHALL obter descrição e metadados da página correspondente do compêndio, sem exigir uma descrição textual duplicada em `char_info`

### Requirement: Character layout handles unresolved references safely
O layout da ficha SHALL tratar referências inexistentes ou páginas indisponíveis como falha não fatal de renderização. Deve exibir pelo menos o nome ou caminho bruto como fallback e somente usar `description` legado quando a ficha antiga não possuir conteúdo resolvível.

#### Scenario: Missing compendium page
- **WHEN** uma entrada de ação ou característica aponta para uma página inexistente
- **THEN** o build SHALL concluir sem erro e a ficha SHALL exibir um fallback identificável para revisão editorial

#### Scenario: Legacy character remains renderable
- **WHEN** uma ficha antiga possui `description` no frontmatter e não possui `ref` resolvível
- **THEN** o layout SHALL renderizar a descrição legada até que a ficha seja migrada

### Requirement: Character frontmatter separates personal state from shared rules
Novas fichas e fichas migradas SHALL manter no frontmatter apenas dados específicos ou operacionais do personagem, incluindo usos máximos, recarga, preparo, quantidade, equipamento e fórmulas. Descrições reutilizáveis de regras SHALL residir em notas do compêndio e ser referenciadas por URL interna.

#### Scenario: Operational action data is preserved
- **WHEN** uma ação possui `name`, `ref`, `source`, `max_uses` e `reset`
- **THEN** a ficha SHALL usar os campos operacionais para exibir o acompanhamento da ação e SHALL obter sua descrição da página `ref`

#### Scenario: Shared description is absent from migrated frontmatter
- **WHEN** uma descrição de Pinky corresponde a uma nota validada do compêndio
- **THEN** a migração SHALL remover a cópia textual de `char_info` e preservar a referência e os dados específicos da personagem

### Requirement: Character roll values support progressive enhancement
The character sheet SHALL render eligible saving throw bonuses, skill bonuses, attack formulas, damage formulas, and explicitly configured action formulas as readable text with structured roll metadata. The values SHALL remain non-interactive reference content by default and SHALL become controls only after a validated extension bridge confirms Dice+ availability.

#### Scenario: Character sheet opens in a normal browser
- **WHEN** no compatible Owlbear character extension bridge is available
- **THEN** roll bonuses and formulas SHALL remain readable text and SHALL NOT display a separate roll button or unavailable interactive control.

#### Scenario: Character sheet opens with Dice+ ready
- **WHEN** the controlled extension completes a valid bridge handshake and confirms Dice+ readiness
- **THEN** eligible values SHALL become keyboard-accessible controls while preserving the same visible number or formula as their label.

#### Scenario: Action has no structured formula
- **WHEN** an action contains descriptive rules but no explicit valid dice notation
- **THEN** the sheet SHALL keep that action as reference content and SHALL NOT infer a roll from prose.

### Requirement: Enhanced roll controls use the visible value as the action
The sheet SHALL use the displayed bonus or dice formula itself as the enhanced roll control and SHALL NOT add a separate textual button labelled “Rolar”. Each enhanced control SHALL expose an accessible label describing the associated skill, save, attack, damage, or action.

#### Scenario: Skill bonus is enhanced
- **WHEN** a skill with bonus `+7` is enabled by the extension bridge
- **THEN** the visible `+7` SHALL be the clickable and keyboard-focusable control with an accessible name identifying the skill test.

#### Scenario: Weapon formulas are enhanced
- **WHEN** a weapon has explicit attack and damage formulas and Dice+ is available
- **THEN** each displayed formula SHALL independently trigger its corresponding attack or damage roll without adding a separate roll button.

### Requirement: Enhanced roll values use minimal visual states
An enhanced roll value SHALL use a small square border to indicate that the visible number or formula is interactive. It SHALL expose a temporary pending state without inserting roll totals, summaries, errors, symbols, or history into the character sheet. Dice+ SHALL remain responsible for displaying roll outcomes.

#### Scenario: Value becomes rollable
- **WHEN** Dice+ readiness is confirmed
- **THEN** each eligible value SHALL receive a small square border, visible focus, and an accessible action label without changing its displayed text.

#### Scenario: Roll starts
- **WHEN** the player activates an enhanced value
- **THEN** that value SHALL indicate a pending roll and SHALL prevent duplicate activation until result, error, or timeout.

#### Scenario: Roll succeeds
- **WHEN** a matching Dice+ result returns through the extension bridge
- **THEN** the originating value SHALL return to ready state without displaying the total or summary in the sheet.

#### Scenario: Roll fails or times out
- **WHEN** a matching error returns or the request exceeds its timeout
- **THEN** the originating value SHALL return to ready state without inserting an error message into the sheet.

### Requirement: Character bridge messages are versioned and correlated
The character client SHALL communicate with the parent extension using a versioned message envelope and unique request and roll identifiers. It SHALL accept responses only from the parent window, expected origin, supported protocol version, and matching pending identifier.

#### Scenario: Matching result arrives
- **WHEN** the parent sends a valid result for a pending request and roll ID
- **THEN** the sheet SHALL clear the pending state only from the action that originated that request.

#### Scenario: Unrelated message arrives
- **WHEN** the sheet receives a message from another origin, another window, an unsupported version, or an unknown identifier
- **THEN** it SHALL ignore the message without changing any roll state.

#### Scenario: Sheet unloads
- **WHEN** the character page is unloaded or its controller is destroyed
- **THEN** it SHALL remove message listeners, clear timers, and reject or discard pending requests safely.

### Requirement: Character sheet dynamically calculates attributes and AC from resolved compendium items
The character sheet template SHALL calculate attributes (Strength, Dexterity, etc.) and Armor Class (AC) by dynamically resolving each equipment item in `char_info.equipment` to its compendium page via `ref`, and applying its modifiers and properties.

#### Scenario: Equipped magic item in compendium overrides an attribute score
- **WHEN** the character has an equipped item in `char_info.equipment` referencing a compendium page with `item_info.modifiers.stat_override` (e.g. strength: 21)
- **THEN** the character's calculated Strength score SHALL be set to the overridden value (e.g. 21) if it is higher than their base score, and all derived modifiers, saving throws, and skill checks SHALL update dynamically.

#### Scenario: Equipped shield/armor in compendium modifies Armor Class
- **WHEN** the character has an equipped item referencing a compendium page with armor properties (e.g. `item_info.type: "Shield"` and `item_info.armor_class: 2`, or `item_info.type: "Light Armor"` and `item_info.armor_class: 11`)
- **THEN** the calculated Armor Class (AC) SHALL dynamically sum these values, applying Dexterity limits correctly (medium armor capped at +2, heavy armor ignoring Dex mod, shield added as bonus).

#### Scenario: Equipped magic item in compendium adds save/AC bonuses
- **WHEN** the character has an equipped item referencing a compendium page with `item_info.modifiers.ac_bonus` or `item_info.modifiers.save_bonus`
- **THEN** these active bonuses SHALL be dynamically added to the calculated AC and saving throws.

### Requirement: Equipment tab resolves detailed properties and active status from compendium
The Equipment tab UI SHALL resolve the detailed properties of each item (weapon properties, range, damage type, armor category) from its compendium page via `ref` and render them, showing active visual cues for equipped items.

#### Scenario: Weapon details are resolved from the compendium
- **WHEN** a weapon with a valid `ref` is displayed in the Equipment tab
- **THEN** the template SHALL fetch and render its properties (e.g. finesse, light), range, and damage type from the compendium page.

#### Scenario: Item has no compendium ref
- **WHEN** an item in `char_info.equipment` lacks a `ref` or is unresolved
- **THEN** the layout SHALL render its inline name and base fields as fallback without causing build-time errors.

