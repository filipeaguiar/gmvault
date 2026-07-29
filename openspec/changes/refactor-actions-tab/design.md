## Context

A ficha de personagem atualmente (Hugo templates + CSS em `character-sheet.css`) possui abas separadas para "Ações e Recursos" (`tab-actions`), "Equipamentos" (`tab-equip`), e "Grimório" (`tab-grimoire`). No entanto, durante o jogo e particularmente em dispositivos móveis ou VTTs, a necessidade de trocar de aba constantemente para ver recursos de classe, ataques de armas, magias e espaços de magia retarda a fluidez do jogo. 

## Goals / Non-Goals

**Goals:**
- Consolidar as seções de Recursos de Classe, Espaços de Magia, Ataques (Armas) e Magias Conhecidas em uma única aba de Combate/Ações (`tab-actions`).
- Garantir que essa nova aba seja perfeitamente responsiva para mobile/iframes.
- Manter a funcionalidade dos dados interativos (rolagens de dados e checkboxes consumíveis).

**Non-Goals:**
- Refatorar a lógica de cálculo dos bônus de magias ou armas.
- Excluir completamente a aba de Equipamentos ou a Aba Grimório inteira (elas podem continuar existindo como visualizações completas e detalhadas).
- Mudar o CSS global do projeto fora do escopo da ficha de personagem.

## Decisions

- **Inclusão Dinâmica na Aba de Ações:** O template `layouts/partials/kinds/character.html` será modificado. A seção `<div id="tab-actions">` passará a importar, além dos Recursos de Classe (já presentes), uma renderização compacta de "Espaços de Magia" (Spell Slots Tracker), a seção de "Ataques de Armas" (weapons do `tab-equip`) e, por fim, a lista "Magias Preparadas/Conhecidas" (do `tab-grimoire`).
- **Reuso de Parciais (Partials):** As magias podem continuar usando a `helpers/character-spells.html` parcial, e os ataques de armas serão extraídos de `tab-equip` para que possam ser iterados dentro da aba de ações, ou a lógica da aba `tab-equip` para armas será copiada e isolada em um partial `helpers/character-weapons.html`.
- **Estilos CSS:** O arquivo `assets/css/character-sheet.css` precisará de regras adicionais de `@media (max-width: 600px)` ou ajustes de `display: flex` para empilhar itens que atualmente ocupam muito espaço horizontal nas seções de magias e armas, caso já não sejam totalmente responsivos.

## Risks / Trade-offs

- **[Risco] Poluição Visual e Excesso de Scroll Vertical:** Juntar tudo em uma só aba pode criar um scroll longo para classes como Bardo ou Mago.
  - **Mitigação:** Agrupar bem visualmente (cards bem definidos e margin compacta) e permitir fechar/ocultar (details/summary) ou simplesmente depender do scroll nativo que é rápido no mobile.
- **[Risco] Duplicação de IDs no DOM:** Mover checkboxes de spell slots ou inputs para duas abas simultâneas (se a aba original do grimório for mantida) vai quebrar a associação no VTT.
  - **Mitigação:** Em vez de duplicar, as armas de ataque e a seção de "Magias/Slots" serão *movidas* para a aba Ações e removidas da aba Equipamentos e Grimório para fins de combate imediato, ou usaremos classes em vez de IDs (já que muitos trackers do owlbear rely on classes). O design prevê mover os elementos para a aba de combate prioritariamente.
