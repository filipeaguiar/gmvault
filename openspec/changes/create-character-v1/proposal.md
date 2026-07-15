## Why

Para implementar a criação de personagem guiada por dados do 5e.tools e substituir a terminologia antiga "Raça" por "Espécie" (alinhando com a nova edição D&D 2024), precisamos de uma base estrutural limpa e incremental. A V1 do script focará no fluxo básico guiado por dados para coletar o nome, escolher a espécie (com suas variantes/subespécies), a classe principal, nível e atributos, gerando um Markdown com frontmatter YAML 100% correto e sem a necessidade de o usuário digitar manualmente todas as informações derivadas.

## What Changes

- **Renomeação Estrutural (Espécie)**: Renomear a pasta `content/compendium/races` para `content/compendium/species` e alterar as chaves de frontmatter `.Params.char_info.race` para `.Params.char_info.species` (mantendo fallback nos layouts).
- **Geração Guiada (V1)**: Criação de um novo script `create_character_v1.py` que solicita nome do personagem, lê as espécies disponíveis em `races.json` (ou online via 5e.tools), lista as opções de subespécies/variantes, lê a classe selecionada em `classes.json`, e guia o usuário na definição dos atributos (com bônus de espécie aplicados).
- **Atualização de Layouts**: Atualizar os layouts Hugo (`layouts/index.html`, `layouts/partials/kinds/character.html` e readequar `layouts/partials/kinds/race.html` para `species.html`) para renderizar "Espécie" em vez de "Raça".

## Capabilities

### New Capabilities
- `create-character-v1`: Novo script de CLI interativo que coleta informações básicas de espécie/classe diretamente dos arquivos ou URLs do 5e.tools e gera uma ficha funcional minimalista com a nova terminologia.

### Modified Capabilities

## Impact

- Renomeação de pasta: `content/compendium/races` -> `content/compendium/species`.
- Novo script `create_character_v1.py` (ou substituição definitiva do anterior).
- Atualização em `layouts/partials/kinds/character.html` e `layouts/index.html`.
- Renomeação do partial de kind `race.html` -> `species.html`.
