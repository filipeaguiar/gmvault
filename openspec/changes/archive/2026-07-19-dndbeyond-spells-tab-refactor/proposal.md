## Why

A aba atual de magias ainda mistura duas responsabilidades: exibição da lista de magias do personagem e estado tático de uso durante o jogo. Para este vault, o estado operacional não precisa ser persistido no Markdown; basta carregar e salvar em `localStorage`, enquanto a lista de magias do personagem deve ser gravada pelos scripts e importadores quando necessário.

Também falta uma forma consistente de adicionar magias manualmente nos fluxos de criação/edição e de organizar visualmente o que está pronto para uso (preparadas ou sempre prontas) versus o que foi aprendido mas ainda não está preparado.

## What Changes

- Persistir a lista de magias do personagem como parte dos dados da ficha.
- Permitir que os scripts adicionem magias automaticamente quando a classe, subclasse, feat, raça ou item concederem magia.
- Permitir entrada manual de magias nos fluxos de criação e edição quando a classe exigir escolha do usuário.
- Manter em `localStorage` apenas o estado visual/operacional da aba de magias, como preparadas, sempre prontas e aprendidas não preparadas.
- Organizar a aba em uma lista escaneável com filtros por nível e separação visual por estado de uso.
- Consultar 5e.tools para determinar como cada classe lida com magias e quais estados devem existir para o personagem.
- Preservar compatibilidade com personagens antigos que ainda usam os campos legados de spells.

## Impact

- `layouts/partials/kinds/character.html`
- `assets/js/spells.js`
- `assets/css/character-sheet.css` e/ou `assets/css/main.css`
- `archetypes/character.md`
- `docs/character-compendium-data.md`
- `create_character.py`
- `edit_character.py`
- `import_dndbeyond.py`
- `dnd_utils.py`
- `tests/test_interactive_character_features.py`
- `tests/test_spell_roll_rendering.py`
- possivelmente novos partials em `layouts/partials/character/`

## Capability Changes

### New Capability
- `generalized-character-spellcasting-ui`: lista persistida de magias do personagem, organização visual por estado de uso e armazenamento operacional em `localStorage`.

### Modified Capabilities
- `interactive-character-sheet-spells`
- `interactive-spell-search`
- `compendium-driven-character-data`

## Risks / Trade-offs

- Personagens antigos podem não ter dados completos para classificar automaticamente o estado de cada magia; nesses casos a UI deve degradar para leitura compatível.
- Multiclasse e fontes múltiplas de magia exigem separar origem, lista persistida e estado operacional.
- O `localStorage` é apenas estado de sessão do navegador; não deve ser tratado como persistência durável da ficha.

## Success Criteria

- A ficha mostra a lista de magias do personagem de forma consistente.
- Magias podem ser adicionadas automaticamente ou manualmente, conforme o fluxo.
- A separação visual entre prontas para uso e aprendidas não preparadas funciona sem depender de regravação do Markdown.
- O estado operacional da aba persiste apenas em `localStorage` e recarrega corretamente.
- A solução continua leve e compatível com personagens legados.
