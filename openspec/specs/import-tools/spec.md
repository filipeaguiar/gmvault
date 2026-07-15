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

