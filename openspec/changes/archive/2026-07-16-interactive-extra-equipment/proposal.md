## Why

O script de criação de personagem atualmente adiciona automaticamente os itens provenientes do background e do pacote inicial escolhido (ex: Burglar's Pack). No entanto, algumas classes ou builds exigem a escolha de armas extras, armaduras ou escudos que não estão inclusos nesses pacotes. Os jogadores hoje precisam adicionar esses itens manualmente na ficha Markdown. Essa mudança permitirá que os jogadores busquem e adicionem itens individuais de forma interativa diretamente no final da criação do personagem.

## What Changes

- O script `create_character.py` ganhará uma nova etapa ao final do processo chamada "EQUIPAMENTOS EXTRAS".
- O usuário poderá buscar itens por nome (ex: "Longsword", "Shield", "Leather Armor").
- O script fará uma busca no banco de dados local do 5e.tools (via `items.json` e `items-base.json`).
- Os itens selecionados serão adicionados à lista `char_info.equipment` e as referências ao compêndio serão atualizadas, gerando os arquivos locais no compêndio quando necessário.
- A etapa continuará em loop perguntando se o usuário quer adicionar mais itens até que ele responda negativamente ou em branco.

## Capabilities

### New Capabilities
- `interactive-item-search`: Capacidade de buscar, desambiguar e extrair itens individuais do 5e.tools no script iterativo e adicioná-los diretamente no equipamento e compêndio.

### Modified Capabilities

## Impact

- `create_character.py`: Uma nova etapa será inserida antes da gravação do arquivo final, para popular a lista `equipment_data`.
- `dnd_utils.py`: Funções utilitárias como `fetch_from_5etools` e `load_item_data` já suportam grande parte dessa mecânica. Podemos apenas precisar expor uma busca por nome para listar opções caso haja desambiguação ou utilizar uma string genérica.
- Sem impacto em quebras de código (`BREAKING`). Apenas expansão da lista de equipamentos e referências do yaml gerado.
