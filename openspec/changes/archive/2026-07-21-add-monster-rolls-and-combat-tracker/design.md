## Context

Os mestres usam o GM Vault como ferramenta de suporte na mesa de RPG. Para evitar dependências instáveis de extensões externas durante os combates e visualizações de monstros, precisamos de um mecanismo de rolagem nativo rápido e uma tela unificada para consolidar combates.

## Goals / Non-Goals

**Goals:**
* Integrar atributos `data-roll-notation` e classes CSS no `statblock.html` para habilitar rolagens de atributos, testes e resistências.
* Desenvolver um script JS global `roll-engine.js` que detecta e substitui fórmulas de dados textuais por elementos interativos em monstros.
* Implementar um sistema de rolagem client-side local com exibição de toasts de resultado caso esteja fora de um iframe de VTT.
* Criar a página `/combat/` que lê o `statblocks.json` compilado e permite gerenciar múltiplos monstros e suas rolagens em uma tela única.

**Non-Goals:**
* Persistência em banco de dados ou sincronização multiplayer. O estado do combate será mantido apenas em memória na sessão atual do navegador.

## Decisions

### Decisão 1: Injeção do `roll-engine.js` e CSS
Carregar o script global em `layouts/_default/baseof.html` para todas as páginas. As regras do toast de rolagem serão inseridas em `assets/css/main.css`.
*Racional:* Permite que qualquer página do site estático (incluindo monstros do compêndio, fichas de personagens ou anotações do GM) ganhe suporte a rolagens nativas.

### Decisão 2: Regex do Auto-Rolador de Ações
O script JS deve percorrer os nós de texto dentro das ações dos monstros e converter os padrões:
1. `\+(\d+)\s*(?:para acertar|to hit)` -> Rolagem de Ataque (`1d20+X`).
2. `(\d+d\d+(?:\s*[+-]\s*\d+)?)` -> Rolagem de Dano/Efeito (ex: `2d6+5`).
*Racional:* Automatiza as rolagens nas ações dos monstros importados do 5e.tools sem necessidade de editar manualmente as centenas de arquivos Markdown do compêndio.

### Decisão 3: Interface do Combat Tracker (`/combat/`)
Criar o arquivo `content/combat.md` apontando para um layout dedicado `layouts/page/combat.html`. A interface fará um fetch assíncrono em `/exports/forge/statblocks.json` e renderizará caixas colaterais com inputs de HP para os monstros listados na nota do GM.

## Risks / Trade-offs

* **[Risco]** Regex corromper tags HTML ao re-escrever o conteúdo.
  * **Mitigação:** O algoritmo percorrerá recursivamente apenas nós do tipo `Node.TEXT_NODE` (evitando nós de elemento) ao fazer a substituição por elementos HTML clicáveis de dados.
