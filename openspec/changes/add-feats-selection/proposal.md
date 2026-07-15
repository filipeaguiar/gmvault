## Why

Os personagens de D&D ganham talentos (feats) no nível 1 (geralmente concedidos pelo Background nas regras modernas do D&D 2024 / Tasha) e em níveis subsequentes através de características de classe. Atualmente, o criador interativo de personagens (`create_character.py`) não permite a escolha e associação de talentos à ficha de personagem, o que resulta em fichas incompletas que precisam ser editadas manualmente.

## What Changes

- **Seleção Interativa de Talentos**: Adicionar uma etapa no script `create_character.py` para escolher talentos de forma interativa.
  - **Nível 1 (Talento de Origem)**: Permitir escolher exatamente 1 Talento de Origem (*Origin Feat*), exibindo no menu em colunas os talentos de categoria "O" (Origin) oriundos da fonte `XPHB` (D&D 2024).
  - **Níveis 4+ (Talentos Gerais/Combate)**: Oferecer a opção de escolher talentos adicionais (categoria "G" ou "FS" da fonte `XPHB`) correspondentes aos aumentos de nível de classe.
- **Sincronização com o Compêndio**: Integrar o fluxo de talentos selecionados para baixar automaticamente os arquivos do 5e.tools salvando-os em `content/compendium/feats/` e vinculá-los à lista de `compendium_refs` no frontmatter do personagem.
- **Ajustes de Atributos**: Os talentos do D&D 2024 oferecem pequenos aumentos de atributos (+1). O criador deve alertar o usuário para selecionar esses aumentos de atributos em conjunto com os bônus do Background.

## Capabilities

### New Capabilities

- `add-feats-selection`: Regula a inclusão da seleção interativa de talentos na interface de criação e o download dos stubs correspondentes para o compêndio local.

### Modified Capabilities

- `rpg-character-sheet`: A visualização HTML da ficha do personagem precisa renderizar adequadamente a lista de `feats` e resolver referências internas no compêndio sem erros ou quebras de layout.

## Impact

- `create_character.py`: Implementação do fluxo de prompt de escolha de talentos e chamada para `fetch_from_5etools`.
- `dnd_utils.py`: Validação de que a extração de talentos do arquivo `feats.json` remoto do 5e.tools é realizada sem erros de parsing ou codificação.
- `layouts/partials/kinds/character.html`: Validação de que a renderização de múltiplos talentos em lista (campo `char_info.feats`) é amigável e limpa.
