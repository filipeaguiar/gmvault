## Why

Atualmente as abas "Ações e Recursos" e "Grimório" (ou a aba de equipamentos) dividem ações importantes em várias partes, dificultando a rápida tomada de decisão durante o jogo. Os usuários (especialmente via mobile no Owlbear Rodeo) precisam de uma visualização unificada que priorize Recursos de Classe, Espaços de Magia, Ataques Físicos e Magias em uma única tela, com design responsivo, para uma navegação ágil.

## What Changes

- Unificação das seções vitais de combate na aba de "Ações e Recursos" (`tab-actions`).
- Adição da exibição de Espaços de Magia (Spell Slots) ao lado/abaixo dos Recursos de Classe.
- Reordenação da exibição: (1) Recursos de Classe, (2) Espaços de Magia, (3) Ataques Físicos, e (4) Magias.
- Otimização de UI/UX para garantir que a aba de Ações responda bem em dispositivos móveis (iframes dentro do Owlbear Rodeo), evitando rolagem horizontal desnecessária.

## Capabilities

### New Capabilities
- `unified-combat-tab`: Consolidação de ataques físicos, magias, espaços de magia e recursos de classe em uma única visualização focada em combate para mobile.

### Modified Capabilities
- 

## Impact

- **Código afetado:** `layouts/partials/kinds/character.html` e `assets/css/character-sheet.css`.
- **Sistemas afetados:** Visualização da ficha no VTT via iframe e também no modo standalone.
- As abas antigas (como Grimório e Equipamentos) podem ser mantidas como referência completa ou ser reorganizadas com base nesta mudança.
