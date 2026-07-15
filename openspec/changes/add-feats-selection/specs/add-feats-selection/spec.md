## ADDED Requirements

### Requirement: Download and Cache Feats Index
O sistema SHALL baixar sob demanda o arquivo `feats.json` do repositório remoto do 5e.tools e salvá-lo em cache local sob o caminho `content/compendium/feats/.feats_cache.json` para acelerar consultas subsequentes no terminal.

#### Scenario: Download feats when cache is missing
- **WHEN** o criador interativo é executado e o arquivo `.feats_cache.json` não existe localmente
- **THEN** o sistema SHALL efetuar o download via HTTP e criar o arquivo local contendo a lista completa de talentos.

### Requirement: Select Origin Feat at Level 1
O sistema SHALL permitir a seleção de Talentos de Origem (*Origin Feats*) se o nível do personagem sendo criado for 1, permitindo especificar a quantidade a ser escolhida.

#### Scenario: Interactive selection of Origin feats
- **WHEN** o personagem é de nível 1
- **THEN** o sistema SHALL perguntar a quantidade de talentos de Origem desejada (padrão `1`), obter os talentos de categoria \"O\" e fonte \"XPHB\" do cache, exibi-los organizados em colunas no terminal e solicitar que o usuário selecione a quantidade informada.

### Requirement: Select General Feats at Higher Levels
O sistema SHALL permitir a seleção de múltiplos Talentos Gerais ou de Estilo de Combate (*General/Fighting Style Feats*) para personagens de nível superior a 1.

#### Scenario: Choice of General feats at level 4 or higher
- **WHEN** o personagem é de nível maior ou igual a 4
- **THEN** o sistema SHALL perguntar quantos talentos adicionais o usuário deseja selecionar, listar os talentos qualificados de categoria "G", "FS", "FS:P" e "FS:R" (fonte "XPHB") e solicitar as escolhas por numeração separada por vírgula.

### Requirement: Sync and Download Selected Feat
O sistema SHALL obter a descrição textual detalhada dos talentos escolhidos, gerar os stubs no compêndio local em `content/compendium/feats/<slug>.md` e associar os caminhos correspondentes à lista de `compendium_refs` do personagem.

#### Scenario: Automatically download and sync selected feats
- **WHEN** a criação interativa do personagem é finalizada com talentos selecionados
- **THEN** o sistema SHALL chamar o mecanismo de download para gerar os arquivos Markdown no compêndio (se já não existirem) e registrar os links internos `/compendium/feats/<slug>/` no YAML frontmatter do personagem.
