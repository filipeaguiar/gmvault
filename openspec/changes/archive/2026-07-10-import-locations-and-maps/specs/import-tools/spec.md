## ADDED Requirements

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
