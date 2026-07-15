## Why

Os jogadores e mestres do gmvault desejam utilizar o arquivo Hugo Markdown do personagem como a fonte da verdade para a evolução de suas fichas de RPG (subir nível de classe, adicionar novos equipamentos e magias) por meio de edições manuais locais. Atualmente, o compêndio local só é populado pelo importador do D&D Beyond, o que forçaria reimportar e sobrescrever edições manuais; logo, faz-se necessário um utilitário para varrer alterações locais na ficha e sincronizar o compêndio local buscando dados ausentes no 5e.tools de forma independente.

## What Changes

- **Sincronização de Ficha Local com 5e.tools**: Desenvolvimento de um comando/script Python que aceita o caminho de um arquivo Markdown de personagem e executa o parsing de seu YAML frontmatter.
- **Detecção de Elementos Não Mapeados**: O utilitário varre as listas de magias, equipamentos, classes e talentos na ficha e verifica quais delas não possuem caminhos correspondentes cadastrados na propriedade `compendium_refs` do personagem.
- **Resolução Remota e Criação no Compêndio**: Para cada item não mapeado (ou arquivo de compêndio local inexistente), o script consulta remotamente o mirror do 5e.tools, baixa os dados canônicos em inglês e gera o stub do compêndio correspondente como rascunho (`draft: true`, `status: "draft"`).
- **Escrita Cirúrgica de Referências**: O script atualiza o campo `compendium_refs` no frontmatter do personagem e grava as mudanças de volta de forma a preservar os demais atributos editados manualmente e a biografia em prosa da ficha.

## Capabilities

### New Capabilities
- `local-character-sync-tools`: Script utilitário e CLI para atualizar e sincronizar arquivos de personagens modificados manualmente, populando o compêndio local de RPG de forma autônoma a partir de fontes do 5e.tools.

### Modified Capabilities
Nenhuma.

## Impact

- **Scripts de Infraestrutura**: Criação do arquivo de script utilitário `scripts/sync_character.py` (ou nos diretórios equivalentes da CLI do gmvault).
- **Manipulação de Markdown**: Implementação de leitura e escrita isolada de YAML delimitado por `---`, garantindo que comentários, estrutura YAML e a biografia original abaixo não sejam corrompidos ou apagados na ficha.
