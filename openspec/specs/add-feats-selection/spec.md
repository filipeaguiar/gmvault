# add-feats-selection Specification

## Purpose
TBD - created by archiving change add-feats-selection. Update Purpose after archive.
## Requirements
### Requirement: Download and Cache Feats Index
O sistema SHALL baixar sob demanda o arquivo `feats.json` do repositório remoto do 5e.tools e salvá-lo em cache local sob o caminho `content/compendium/feats/.feats_cache.json` para acelerar consultas subsequentes no terminal.

#### Scenario: Download feats when cache is missing
- **WHEN** o criador interativo é executado e o arquivo `.feats_cache.json` não existe localmente
- **THEN** o sistema SHALL efetuar o download via HTTP e criar o arquivo local contendo a lista completa de talentos.

### Requirement: Select Origin Feats at Level 1
O sistema SHALL permitir a seleção de múltiplos Talentos de Origem (*Origin Feats*) se o nível do personagem sendo criado for 1, exibindo o rótulo de suas fontes originais e aceitando múltiplas entradas separadas por vírgula em um único prompt.

#### Scenario: Interactive selection of multiple Origin feats
- **WHEN** o personagem é de nível 1
- **THEN** o sistema SHALL carregar os talentos de categoria \"O\" do cache, exibi-los organizados em colunas exibindo suas fontes (ex: \"Alert (XPHB)\"), e solicitar que o usuário selecione os talentos desejados digitando seus números separados por vírgula.

### Requirement: Select General Feats at Higher Levels
O sistema SHALL permitir a seleção de múltiplos Talentos Gerais ou de Estilo de Combate (*General/Fighting Style Feats*) para personagens de nível superior a 1, exibindo o rótulo de suas fontes originais e aceitando múltiplas entradas separadas por vírgula em um único prompt.

#### Scenario: Choice of General feats at level 4 or higher
- **WHEN** o personagem é de nível maior ou igual a 4
- **THEN** o sistema SHALL listar os talentos qualificados de categoria \"G\", \"FS\", \"FS:P\" e \"FS:R\" contendo suas fontes e permitir a escolha de múltiplos talentos digitando seus números separados por vírgula.

### Requirement: Sync and Download Selected Feat
O sistema SHALL obter a descrição textual detalhada dos talentos escolhidos, gerar os stubs no compêndio local em `content/compendium/feats/<slug>.md` e associar os caminhos correspondentes à lista de `compendium_refs` do personagem.

#### Scenario: Automatically download and sync selected feats
- **WHEN** a criação interativa do personagem é finalizada com talentos selecionados
- **THEN** o sistema SHALL chamar o mecanismo de download para gerar os arquivos Markdown no compêndio (se já não existirem) e registrar os links internos `/compendium/feats/<slug>/` no YAML frontmatter do personagem.

