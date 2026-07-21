## Why

O mestre precisa de rolagens ágeis de monstros no site do GM Vault, dada a instabilidade da conexão do Forge com o Dice+. Além disso, abrir várias abas de monstros durante combates complexos polui o navegador, sendo necessária uma tela única de rastreamento de combates (Combat Tracker) para carregar múltiplos monstros de uma nota do GM em uma única tela.

## What Changes

* **Mecanismo de Rolagens em Monstros:** Adicionar atributos e estilos de rolagens (`data-roll-notation`) nas jogadas de atributos, resistências, perícias e ações dos monstros do compêndio.
* **Auto-Rolador JavaScript Global (`roll-engine.js`):** Script global para interceptar rolagens, executar no VTT quando em iframe, ou disparar um toast estático com o resultado em tela cheia no navegador normal.
* **Tela Única de Combate (Combat Tracker):** Página `/combat/` contendo um interpretador de nota simples do GM para instanciar múltiplos statblocks de monstros na mesma tela.

## Capabilities

### New Capabilities
- `monster-rolls-and-combat-tracker`: Mecanismo de rolagens automáticas em monstros e tela de combate integrada baseada em notas.

### Modified Capabilities
<!-- Nenhuma -->

## Impact

* **Layouts:** `layouts/partials/statblock.html` e `layouts/_default/baseof.html`.
* **Novas Páginas:** `content/combat.md` e `layouts/shortcodes/` ou templates para renderizar a interface de combate.
* **Assets:** Novo script JS `assets/js/roll-engine.js` e novas regras CSS em `assets/css/main.css`.
