## Why

A aba atual de magias na ficha do personagem ainda reflete uma solução centrada em um único fluxo: uma lista de magias preparadas/ativas, uma lista completa da classe e um tracker genérico de slots. Isso funciona parcialmente para bardos e outros conjuradores preparados, mas não cobre bem conjuradores conhecidos, espontâneos, híbridos ou com mecânicas especiais (warlock/pact magic, always-prepared, spellbook, lista fixa, listas por fonte).

As screenshots de referência do D&D Beyond mostram um modelo mais robusto: uma visão resumida com contadores no topo, busca rápida, filtros por nível, lista escaneável com colunas/metadata e uma tela de gerenciamento com ações explícitas de preparar/despreparar. A experiência é mais universal porque separa estado operacional da magia do modo como cada classe conjura.

## What Changes

- Redesenhar a aba de spells como uma interface orientada a **perfil de conjuração**, não a uma classe específica.
- Introduzir um modelo de dados de spellcasting na ficha que represente, de forma explícita:
  - tipo de conjuração (`prepared`, `known`, `spontaneous`, `hybrid`, `pact`, `feature-granted`);
  - habilidade de conjuração (INT/WIS/CHA);
  - cantrips conhecidos, magias conhecidas, magias preparadas, magias sempre preparadas;
  - slots normais, pact slots e eventuais recursos especiais;
  - fontes das magias por classe/subclasse/feat/raça/item.
- Separar a UI em blocos reutilizáveis:
  - cabeçalho com contadores e métricas principais;
  - busca global por nome;
  - filtros/tabs por nível (Cantrips, 1º–9º, e eventualmente “Todas”);
  - lista principal escaneável;
  - ações contextuais por tipo de conjurador.
- Ajustar a interação para suportar:
  - preparar/despreparar quando a classe permitir;
  - marcar como conhecida quando o personagem for caster conhecido;
  - exibir apenas leitura quando o sistema não permitir alterar a seleção;
  - manter listas separadas quando uma ficha tiver magia de múltiplas fontes.
- Atualizar frontmatter, scripts de importação/edição e helpers para que a mesma interface funcione para bardos, clérigos, druidas, paladinos, rangers, artificers, sorcerers, warlocks, wizards e híbridos/multiclasse.

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
- `generalized-character-spellcasting-ui`: renderização universal da aba de magias com contadores, filtros, ações e degradação por tipo de conjurador.

### Modified Capabilities
- `interactive-character-sheet-spells`
- `interactive-spell-search`
- `compendium-driven-character-data`

## Risks / Trade-offs

- Fichas antigas podem não ter dados suficientes para classificar corretamente o caster; nesse caso, a UI deve degradar para uma lista somente leitura com os contadores disponíveis.
- Multiclasse e casters híbridos exigem separar a origem da magia do seu estado operacional; sem isso, a UI tende a misturar slots, fontes e preparo.
- Parte da UI será estática em build Hugo e parte será interativa via JS leve; o estado interativo não deve ser tratado como persistência durável.

## Success Criteria

- A mesma aba consegue representar pelo menos:
  - preparadores com limite de magias preparadas;
  - conhecidos sem preparo;
  - warlocks com pact magic;
  - casters híbridos/multiclasse;
  - fichas sem magia sem quebrar a navegação.
- A visualização fica escaneável como nas screenshots: contadores no topo, busca, tabs por nível, lista consistente e ações claras.
- A arquitetura permite adicionar regras específicas de classe sem reescrever a UI inteira.
