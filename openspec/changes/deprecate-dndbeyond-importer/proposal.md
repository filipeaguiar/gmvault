## Why

A criação e a edição locais de personagens não cobrem toda a sincronização de referências que hoje está concentrada em `import_dndbeyond.py`. A importação pela API do D&D Beyond deve ser descontinuada, sem perder a capacidade de materializar no compêndio as regras necessárias às fichas criadas ou mantidas localmente.

## What Changes

- **BREAKING** Remover o fluxo suportado de importação de personagens pela API do D&D Beyond e depreciar `import_dndbeyond.py`.
- Transferir a resolução de conteúdo 5e.tools usada pelo importador para os fluxos de criação e edição de personagens.
- Garantir que criação e edição sincronizem classes, espécies, subclasses, talentos, itens, itens mágicos, magias, ações padrão e regras/características de classe necessárias antes de gravar referências na ficha.
- Preservar conteúdo e fichas já gerados pelo importador, incluindo referências e dados operacionais legados.

## Capabilities

### New Capabilities
- `local-character-compendium-sync`: Sincronização completa de entradas do compêndio exigidas por fluxos locais de criação e edição de personagem.

### Modified Capabilities
- `create-character-interactive`: A criação passa a materializar todas as referências compartilhadas necessárias à ficha.
- `edit-character-interactive`: A edição passa a materializar as referências compartilhadas introduzidas ou mantidas pela ficha.
- `import-tools`: O importador de D&D Beyond deixa de ser um fluxo suportado; requisitos de compêndio e ficha passam para ferramentas locais.

## Impact

Afeta `import_dndbeyond.py`, `create_character.py`, `edit_character.py`, `dnd_utils.py`, testes associados e a documentação de comandos. Não adiciona dependências de execução além das fontes 5e.tools já utilizadas.