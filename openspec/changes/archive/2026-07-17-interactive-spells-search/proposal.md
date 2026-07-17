## Why

Personagens conjuradores precisam de uma forma fácil de gerenciar suas magias. Atualmente, magias teriam que ser inseridas manualmente no markdown. Uma busca iterativa no backend (via CLI) resolve parte do problema. No entanto, para conjuradores que *preparam* magias (ex: Clérigo, Paladino), é necessário também haver uma interface no Frontend (página gerada pelo Hugo) que mostre toda a lista de magias da classe para que o próprio jogador faça o "toggle" (marcar/desmarcar) das magias que preparou no dia. Além disso, precisamos calcular e injetar o número de Spell Slots (Espaços de Magia) que o personagem possui para exibirmos as checkboxes.

## What Changes

- **Backend (CLI)**: Adaptação das funções no `dnd_utils.py` para carregar `spells-*.json` do 5e.tools, permitindo busca iterativa (`search_spell_by_name`) para registrar magias conhecidas. 
- **Backend (Slots)**: Cálculo do número de Spell Slots com base na classe e nível fornecidos no script, injetando uma chave `spell_slots` com o total por nível no YAML da ficha.
- **Frontend (Hugo)**: Refatoração do layout da ficha do personagem (`layouts/characters/single.html`):
  - Renderizar magias usando *accordions* (tags `<details>` e `<summary>`).
  - Adicionar trackers/checkboxes visuais lendo as variáveis `spell_slots` geradas.
  - Criar duas seções de magias separadas: "Magias Preparadas/Conhecidas" e "Lista Completa da Classe".
- **Frontend (JS)**: Criação de um pequeno script JavaScript na página da ficha para permitir marcar/desmarcar magias da Lista Completa, enviando-as visualmente para a seção "Magias Preparadas".
- **Integração Owlbear**: Identificar magias que tenham rolagens de dano/cura e adicionar o atributo HTML `data-roll-notation`.

## Capabilities

### New Capabilities
- `interactive-spell-search`: Busca e injeção interativa de magias e slots via CLI no backend.
- `interactive-character-sheet-spells`: Interface web (frontend) reativa para ficha com accordions, seleção de magias, controle de Spell Slots, e integração de rolagens com Owlbear Rodeo.

## Impact

- `create_character.py` e `dnd_utils.py` receberão lógica para magias e cálculo de Spell Slots segundo as tabelas oficiais.
- O tema do Hugo receberá atualizações visuais para magias e VTT.
