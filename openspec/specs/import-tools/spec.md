# import-tools Specification

## Purpose
Define the behavior expected from repository import scripts that generate Hugo Markdown content from external RPG data.
## Requirements
### Requirement: Import scripts generate Markdown content
Repository import scripts SHALL transform supported external RPG data into Hugo Markdown files with YAML front matter and body content.

#### Scenario: Script imports campaign material
- **WHEN** `import_campaign.py` is run with supported source data and target options
- **THEN** it SHALL create campaign-scoped Markdown files under `content/campaigns/<campaign-slug>/`

#### Scenario: Script imports compendium material
- **WHEN** `import_dndbeyond.py` fetches or receives supported compendium references
- **THEN** it SHALL create Markdown files under the appropriate `content/compendium/` subsection

### Requirement: Import scripts slugify generated paths
Import scripts SHALL convert names into URL-safe slugs for generated Markdown filenames and cross-reference paths.

#### Scenario: Name contains spaces or accents
- **WHEN** a generated entity name contains spaces, accents, or punctuation
- **THEN** the script SHALL normalize it into a lower-case ASCII slug suitable for a Hugo path

### Requirement: Import scripts clean source-specific tags
Import scripts SHALL convert supported source markup tags into plain Markdown, links, dice notation, or readable text.

#### Scenario: Source text contains dice tags
- **WHEN** imported source text contains recognized dice or damage notation
- **THEN** the generated Markdown SHALL preserve it in the vault's dice-friendly notation

#### Scenario: Source text contains unresolved tags
- **WHEN** imported source text contains recognized RPG entity tags
- **THEN** the script SHALL emit readable display text and collect references when supported

### Requirement: Import workflow supports optional draft translation
The repository import workflow SHALL support an optional post-processing step that translates imported draft Markdown pages without changing the import scripts' primary responsibility of generating structured content.

#### Scenario: Import creates draft English content
- **WHEN** an import script creates Markdown pages with `draft: true`
- **THEN** those pages SHALL be eligible for later processing by the draft translation script

#### Scenario: Translation is not requested
- **WHEN** a maintainer runs an import script without running the translation script
- **THEN** the import script SHALL continue to generate Markdown content without requiring Argos Translate

#### Scenario: Translation script is run after import
- **WHEN** a maintainer runs the draft translation script after importing content
- **THEN** the workflow SHALL preserve the imported content structure while translating eligible draft text for editorial review

### Requirement: Campaign importer generates simplified adventure hierarchy
`import_campaign.py` SHALL generate new campaign adventure content using the simplified physical hierarchy for sessions and scenes.

#### Scenario: Import creates adventure session
- **WHEN** `import_campaign.py` creates a session for an imported adventure
- **THEN** it SHALL write the session as `content/campaigns/<campaign-slug>/adventures/<adventure-slug>/<session-slug>/_index.md`

#### Scenario: Import creates session scene
- **WHEN** `import_campaign.py` creates a scene for an imported session in Modo 2
- **THEN** it SHALL write the scene directly under the adventure directory as `<scene-slug>.md`

#### Scenario: Import creates adventure support indexes
- **WHEN** `import_campaign.py` imports a new adventure
- **THEN** it SHALL NOT create mandatory `sessions/_index.md` or `scenes/_index.md` pages for the simplified hierarchy

### Requirement: Campaign importer enriches location markdown files
O script de importação de campanhas (`import_campaign.py`) SHALL gerar arquivos markdown ricos para localidades sob `content/campaigns/<campaign-slug>/locations/`, contendo front matter estruturado e corpo de texto descritivo quando disponível na origem.

#### Scenario: Enriquecimento de localidade durante a importação
- **WHEN** `import_campaign.py` é executado com uma aventura contendo localizações válidas
- **THEN** ele SHALL escrever metadados estruturados (como `title`, `params.kind`, `draft`, `visibility`, `status` e tags) no front matter de cada arquivo de localidade

### Requirement: Campaign importer detects maps heuristically
O script de importação de campanhas SHALL identificar imagens do 5e.tools que representam mapas de aventura utilizando uma heurística baseada no título da imagem.

#### Scenario: Detecção de imagem de mapa
- **WHEN** uma imagem com tipo `image` possui a palavra "Map" ou "Mapa" (caso insensível) em seu título ou nome
- **THEN** o importador SHALL classificar esta imagem como um mapa para processamento especial

### Requirement: Campaign importer generates map handouts
O importador de campanhas SHALL criar arquivos de handout individuais sob `content/campaigns/<campaign-slug>/handouts/` para cada mapa identificado, definindo a visibilidade de acordo com a heurística de spoiler.

#### Scenario: Mapa do mestre (DM/GM) detectado
- **WHEN** o título do mapa contém "DM", "GM", "Grid", "Numbered" ou não faz menção explícita a "Player"
- **THEN** o handout correspondente SHALL ser criado com `visibility: "gm"`

#### Scenario: Mapa do jogador (Player) detectado
- **WHEN** o título do mapa contém "Player" ou "Player Map" (caso insensível)
- **THEN** o handout correspondente SHALL ser criado com `visibility: "players"`

### Requirement: Campaign importer links locations and scenes to maps
O importador de campanhas SHALL associar o handout de mapa gerado como referência interna no front matter das localidades e cenas relacionadas.

#### Scenario: Associação de mapas a localidades e cenas
- **WHEN** uma localidade ou cena pertence à área descrita pelo mapa importado
- **THEN** o front matter correspondente da localidade e da cena SHALL listar o caminho interno do handout de mapa gerado no campo `handouts`

### Requirement: Import script extracts and translates class and subclass level features
The import script `import_dndbeyond.py` SHALL extract level-specific features for classes and subclasses from 5e.tools JSON files during character import and translate them into Portuguese.

#### Scenario: Character has class and subclass level features
- **WHEN** `import_dndbeyond.py` is run for a character with a subclass or class features defined in 5e.tools
- **THEN** it SHALL extract those features, create translated compendium rules under `content/compendium/rules/`, and reference them in the character's `compendium_refs`

### Requirement: D&D Beyond character importer exports full stats, speeds, saves, senses, languages, size, and alignment
The character import script `import_dndbeyond.py` SHALL parse and calculate size, alignment, speeds, senses, languages, and saving throw modifiers from the D&D Beyond JSON and save them in the character's Markdown under `char_info`.

#### Scenario: Character speed is calculated
- **WHEN** `import_dndbeyond.py` parses a character with multiple movement speeds
- **THEN** it SHALL output walk, fly, swim, climb, and burrow speeds under `char_info.speed` in the front matter

#### Scenario: Character saving throws are calculated
- **WHEN** `import_dndbeyond.py` parses a character
- **THEN** it SHALL calculate modifiers for Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma saving throws (including starting class proficiencies and stat modifiers) and output them under `char_info.saves` in the front matter

#### Scenario: Character size and alignment are resolved
- **WHEN** `import_dndbeyond.py` parses a character
- **THEN** it SHALL map the D&D Beyond sizeId and alignmentId to human-readable strings (e.g. Medium, Lawful Good) and output them under `char_info.size` and `char_info.alignment` in the front matter

#### Scenario: Character senses and languages are resolved
- **WHEN** `import_dndbeyond.py` parses a character
- **THEN** it SHALL extract passive perception, darkvision, and other senses, along with all known languages, and output them under `char_info.senses` and `char_info.languages` in the front matter

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

### Requirement: Character spell flows materialize 5e.tools compendium pages
`create_character.py`, `edit_character.py`, and `import_dndbeyond.py` SHALL use shared 5e.tools spell resolution to create or synchronize a canonical local compendium page before writing a new character spell association. A new canonical association SHALL NOT be emitted when the source spell cannot be resolved unambiguously.

#### Scenario: Character creation selects a supported spell
- **WHEN** the interactive creation flow selects a spell present in the supported 5e.tools data
- **THEN** it SHALL create or synchronize the spell page under `content/compendium/spells/`
- **THEN** it SHALL write the returned internal URL into the character note

#### Scenario: Character editing adds a supported spell
- **WHEN** the interactive editing flow adds a spell present in the supported 5e.tools data
- **THEN** it SHALL use the same canonical materialization helper as character creation
- **THEN** it SHALL avoid adding a duplicate reference already associated with the character

#### Scenario: D&D Beyond import contains a supported spell
- **WHEN** the D&D Beyond payload contains a class, race, background, feat, item, or other granted spell supported by 5e.tools
- **THEN** the importer SHALL materialize the canonical compendium page
- **THEN** it SHALL associate the operational source and availability state with that canonical reference

#### Scenario: Spell cannot be resolved
- **WHEN** a new spell name cannot be resolved unambiguously in the supported 5e.tools source data
- **THEN** the flow SHALL report the unresolved spell
- **THEN** it SHALL NOT silently write a fabricated canonical reference for the new association

### Requirement: Character spell flows emit reference-driven operational entries
New character spell entries SHALL use the canonical `ref` as identity and SHALL include only character-specific state needed to determine readiness, preparation eligibility, source, and usage. Shared spell title, level, description, and roll mechanics SHALL remain in the compendium page. Inline shared fields SHALL remain supported only for legacy fallback.

#### Scenario: Prepared spell is emitted
- **WHEN** an imported or selected spell is prepared for the character
- **THEN** its character entry SHALL contain its canonical `ref` and prepared/availability state
- **THEN** it SHALL NOT duplicate the compendium description or structured roll metadata

#### Scenario: Known spell is emitted
- **WHEN** a known or pact caster has a known spell
- **THEN** the character entry SHALL identify the spell as ready through reference-driven operational state without marking it as requiring preparation

#### Scenario: Spell is always available from another source
- **WHEN** a race, background, feat, class feature, or item grants a spell that is always available
- **THEN** the character entry SHALL preserve its source and always-available or granted state
- **THEN** generic rendering SHALL be able to keep it in the ready list without a preparation checkbox

#### Scenario: Existing legacy character is edited
- **WHEN** the editor encounters spell entries with inline `name` or `level` fields
- **THEN** it SHALL preserve renderability while normalizing successfully resolved entries to canonical refs
- **THEN** it SHALL NOT delete unresolved legacy fallback data

### Requirement: Character spell flows deduplicate references and preserve state
Character spell generation SHALL deduplicate associations by canonical reference across D&D Beyond spell groups, selected spells, class catalogs, and `compendium_refs`. When duplicate source records are merged, the result SHALL preserve the most permissive ready state and all relevant character-specific source/usage information without duplicating shared mechanics.

#### Scenario: D&D Beyond returns the same spell in multiple groups
- **WHEN** one spell appears in class spells and in another spell source group
- **THEN** the generated character spell collection SHALL contain one canonical association
- **THEN** its merged state SHALL preserve preparation or always-available status and source information

#### Scenario: Spell is already in compendium references
- **WHEN** a selected spell's canonical URL already exists in `compendium_refs`
- **THEN** the flow SHALL reuse the URL and SHALL NOT append a duplicate

#### Scenario: Spell synchronization refreshes roll metadata
- **WHEN** canonical 5e.tools spell data includes structured attack, damage, healing, saving throw, or scaling metadata
- **THEN** the compendium synchronization SHALL retain that metadata in `spell_info`
- **THEN** the character entry SHALL continue to reference it without copying it

### Requirement: Spellcasting profiles expose accessible levels and preparation capability
Shared spellcasting inference SHALL expose enough generic profile and per-entry state for the renderer to determine ready spells, management spells, preparation eligibility, positive normal slots, and pact slots without hard-coding a character identity.

#### Scenario: Prepared caster profile is generated
- **WHEN** a supported prepared caster has positive slots and referenced class spells
- **THEN** the generated profile SHALL identify preparation as available
- **THEN** the renderer SHALL be able to derive accessible circles from the positive slot resources

#### Scenario: Known caster profile is generated
- **WHEN** a supported known caster is generated or imported
- **THEN** the profile SHALL identify its associated spells as known and ready
- **THEN** it SHALL NOT grant preparation controls solely because a class catalog exists

#### Scenario: Pact caster profile is generated
- **WHEN** a supported pact caster is generated or imported
- **THEN** the profile SHALL identify pact slot usage, count, and accessible pact slot level

#### Scenario: Hybrid source has explicit preparation behavior
- **WHEN** a character has spells from sources with different preparation rules
- **THEN** entry-specific availability or preparation capability SHALL override the global profile for those entries

#### Scenario: Profile cannot infer a preparation rule
- **WHEN** source metadata is insufficient to establish that a spell is preparable
- **THEN** the generated/rendered entry SHALL degrade to read-only instead of exposing an unsupported preparation action

### Requirement: Spell imports extract structured roll metadata from 5e.tools
Import tools that create or synchronize spell compendium pages SHALL inspect `entries`, `entriesHigherLevel`, `scalingLevelDice`, `spellAttack`, `damageInflict`, `savingThrow`, and `miscTags` and SHALL write normalized mechanical metadata under `spell_info`.

#### Scenario: Import reads nested roll tags
- **WHEN** a roll tag occurs in a nested entries block or higher-level block
- **THEN** the importer SHALL include it in structured extraction rather than requiring it to appear in a top-level string

#### Scenario: Import preserves inline roll markup
- **WHEN** the importer extracts a roll into `spell_info.rolls`
- **THEN** it SHALL continue converting the original body tag into readable dice-friendly markup

#### Scenario: Import reads cantrip scaling table
- **WHEN** a spell contains `scalingLevelDice` as an object or a list of labeled scaling objects
- **THEN** the importer SHALL preserve each character-level threshold and formula in structured metadata

#### Scenario: Import distinguishes continuous and discrete slot scaling
- **WHEN** scaled tags contain `1-9` or `3,5,7,9` progression syntax
- **THEN** the importer SHALL normalize the correct slot thresholds without inventing intermediate increments

#### Scenario: Higher-level effect is prose-only
- **WHEN** entriesHigherLevel describes additional projectiles but provides no scaled tag or structured count field
- **THEN** the importer SHALL preserve the prose and base roll but SHALL NOT infer an aggregate dice formula

### Requirement: Spell metadata synchronization is non-destructive
When a spell page already exists locally, synchronization SHALL update its structured `spell_info` while preserving editorial front matter, translation metadata, title overrides, and Markdown body.

#### Scenario: Translated spell is synchronized
- **WHEN** an existing translated Fireball page is synchronized with current 5e.tools data
- **THEN** its translation metadata and Markdown body SHALL remain unchanged while roll metadata is updated

#### Scenario: Source spell cannot be resolved
- **WHEN** a local spell has no matching source record
- **THEN** synchronization SHALL report the unresolved page and SHALL NOT remove or rewrite its existing metadata

