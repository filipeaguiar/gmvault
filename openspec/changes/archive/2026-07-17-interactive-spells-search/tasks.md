## 1. DND Utils & CLI Modificações (Backend)

- [x] 1.1 Em `dnd_utils.py`, adicionar download automático de `spells-phb.json`.
- [x] 1.2 Criar `search_spell_by_name(spell_name, source)` usando desambiguação interativa.
- [x] 1.3 Adicionar chamada de `search_spell_by_name` em `create_character.py` (e `edit_character.py` se pronto).
- [x] 1.4 Criar a função `calculate_spell_slots(class_name, level)` usando a tabela base do 5e.
- [x] 1.5 Injetar o dicionário de slots no YAML (chave `spell_slots`) durante a criação do personagem na CLI.
- [x] 1.6 Adicionar lógica para baixar todas as magias da classe de uma vez no compêndio caso o personagem seja do tipo que prepara magias (ex: Clérigo).

## 2. Hugo Layout: Estrutura Visual de Magias (Frontend)

- [x] 2.1 Em `layouts/characters/single.html`, criar iteradores para acessar magias resolvidas da página (usando `site.GetPage` sobre `compendium_refs` e filtrando magias da classe).
- [x] 2.2 Estruturar a renderização em `details` / `summary` para cada magia.
- [x] 2.3 Criar divs distintas para `#prepared-spells` e `#class-spells`.
- [x] 2.4 Adicionar o campo de input `<input type="text" id="spell-search">` acima da lista completa.
- [x] 2.5 Ler a chave `spell_slots` do YAML e gerar checkboxes dinamicamente para cada nível de magia que o jogador tem (ex: Nível 1: [ ] [ ] [ ] [ ]).

## 3. UI Interativa (Frontend JS)

- [x] 3.1 Adicionar caixas de seleção (checkboxes) visuais ao lado de cada magia em `#class-spells`.
- [x] 3.2 Criar um script Javascript (`assets/js/spells.js`) que escuta mudanças nos checkboxes e clona/move o `<details>` correspondente para `#prepared-spells`.
- [x] 3.3 Adicionar o ouvinte de eventos no `id="spell-search"` para filtrar os elementos da lista via Javascript (escondendo os que não dão match via CSS `display: none`).
- [x] 3.4 Garantir que os checkboxes dos "Spell Slots" não conflitem com os checkboxes de preparo.

## 4. Integração VTT (Owlbear Dice+)

- [x] 4.1 Modificar o importador (ou o layout Hugo) para extrair arrays de dano da magia no JSON do 5e.tools.
- [x] 4.2 Injetar o span `<span class="dice+" data-roll-notation="X">X</span>` na descrição das magias que possuem dano/cura, integrando ao Owlbear Rodeo.
