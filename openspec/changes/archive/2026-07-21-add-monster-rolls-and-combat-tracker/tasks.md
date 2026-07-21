## 1. Monster Statblock & CSS Updates

- [x] 1.1 Adicionar atributos `data-roll-notation` e `class="roll-ready"` nos modificadores de atributos no `layouts/partials/statblock.html`.
- [x] 1.2 Adicionar `data-roll-notation` e `class="roll-ready"` nos campos de testes de resistência e perícias em `layouts/partials/statblock.html`.
- [x] 1.3 Inserir estilos CSS globais no final de `assets/css/main.css` para toasts de notificação de rolagem e elementos `.roll-ready`.

## 2. JavaScript Roll Engine & Auto-Rolling

- [x] 2.1 Criar o arquivo `assets/js/roll-engine.js` contendo o interceptador de cliques e a lógica de rolagem local (toasts) / VTT postMessage.
- [x] 2.2 Implementar no `roll-engine.js` o parser de nós de texto que detecta fórmulas de dados (ex: `1d6+2`) e bônus de ataque (ex: `+5 para acertar`) e as envelopa em spans interativos.
- [x] 2.3 Incluir a chamada do script `assets/js/roll-engine.js` de forma global em `layouts/_default/baseof.html`.

## 3. Combat Tracker & Verification

- [x] 3.1 Criar a página Markdown `content/combat.md` com `layout: combat` e `visibility: gm`.
- [x] 3.2 Desenvolver o layout `layouts/page/combat.html` com a caixa de texto de notas, o motor de busca/filtro de monstros, e renderização dinâmica dos statblocks lado a lado com controle de HP individual.
- [x] 3.3 Rodar a validação local com `./pre-push-check.sh` para garantir o sucesso do build do site estático e do pacote compactado ZIP.
