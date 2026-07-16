## Why

O script de criação de personagens (`create_character.py`) não possui atualmente uma etapa para selecionar o Background do personagem nem para atribuir o equipamento inicial fornecido pelo Background ou pela Classe (Packs). Com a mudança das regras de 2024 (XPHB), o equipamento inicial é diretamente derivado dessas duas fontes. Automatizar essa inserção reduzirá o trabalho manual do usuário e garantirá que os itens (roupas, kits, armas) sejam devidamente resolvidos no compêndio e adicionados ao frontmatter.

## What Changes

- Adição de um fluxo iterativo em `create_character.py` para seleção de Backgrounds a partir da base de dados do 5e.tools (XPHB).
- Inclusão automática dos itens do Background escolhido na lista de equipamentos do personagem (`char_info.equipment`).
- Adição de um fluxo para seleção de Pacote Inicial (Packs) baseados na Classe, extraindo os itens do pacote.
- Geração automática de referências no compêndio para todos os novos itens incluídos na criação do personagem.

## Capabilities

### New Capabilities
- `character-background-equipment`: Permite a seleção de antecedentes (backgrounds) e pacotes de equipamentos (packs), resolvendo automaticamente os itens e gerando as referências no inventário do personagem e no compêndio global.

### Modified Capabilities
- `create-character-interactive`: O fluxo interativo será expandido para solicitar opções de background e pacotes ao usuário durante o ciclo de vida da geração do personagem.

## Impact

- `create_character.py`: Novo menu interativo e processamento de `backgrounds.json` e `items.json`.
- `dnd_utils.py`: Funções para buscar dados de antecedentes e explodir itens contidos em um kit/pacote (ex: Burglar's Pack).
- Frontmatter do personagem gerado: O campo `equipment` passará a conter os itens populados automaticamente.
