## 1. Refatoração do Template HTML (layouts/partials/kinds/character.html)

- [ ] 1.1 Mover a seção de "Espaços de Magia" (Spell Slots Tracker) para o início/meio da aba "Ações e Recursos" (`tab-actions`), logo abaixo dos Recursos de Classe.
- [ ] 1.2 Mover a seção de renderização de "Armas" (Weapons grid) da aba "Equipamentos" (`tab-equip`) para a aba "Ações e Recursos", abaixo dos Espaços de Magia.
- [ ] 1.3 Mover a renderização da lista de "Magias" (Grimoire) da aba "Grimório" (`tab-grimoire`) para o final da aba "Ações e Recursos".

## 2. Ajustes de CSS (assets/css/character-sheet.css)

- [ ] 2.1 Adicionar regras responsivas (`@media`) se necessário, para garantir que os grids de armas (`.weapon-grid`) se adaptem para `flex-direction: column` em larguras pequenas (como 400px ou menos).
- [ ] 2.2 Ajustar margens e paddings dos blocos inseridos na aba de Ações para criar uma separação visual clara entre Recursos de Classe, Armas e Magias.

## 3. Validação e Teste Local

- [ ] 3.1 Executar `hugo server -D` e verificar se a aba "Ações" (`tab-actions`) exibe todos os 4 blocos sem quebrar o layout.
- [ ] 3.2 Simular a visualização em resoluções mobile (via DevTools ou iframe) garantindo que os checkboxes (slots, ações) e botões de rolagem funcionam e estão visíveis.
