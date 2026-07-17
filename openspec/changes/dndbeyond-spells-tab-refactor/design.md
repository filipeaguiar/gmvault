## Contexto e leitura das referências

As screenshots mostram duas camadas de UX:

1. **Visão resumida da ficha**
   - counters principais no topo;
   - área de spells com busca;
   - filtro rápido por nível;
   - colunas para leitura rápida (tempo, alcance, ataque/CD, efeito);
   - botão de gerenciamento de magias;
   - slots exibidos como blocos/tokens.

2. **Tela de gerenciamento**
   - abas entre “Add Spells” e “Prepared Spells”;
   - contadores claros (“Cantrips”, “Prepared Spells 4/5”);
   - busca por nome;
   - filtros por nível;
   - lista de magias com ações explícitas (“Prepare”, “Unprepare”);
   - badges que indicam origem/regras (ex.: ritual, regras expandidas, classe).

A leitura crítica é: o baseline não é só “listar magias”; é **resumir estado, permitir triagem e expor uma ação simples por linha**. Isso deve ser generalizado para múltiplos modelos de conjuração.

## Proposta de modelagem

### 1. Introduzir um objeto canônico de conjuração

Adicionar, no frontmatter do personagem, um bloco derivado ou explícito como `spellcasting` (nome pode variar, mas deve ser único e documental) com a seguinte intenção:

- `mode`: `prepared | known | spontaneous | pact | hybrid | feature_granted`
- `ability`: `int | wis | cha`
- `save_dc`, `attack_bonus`
- `cantrips_known`
- `spells_known_max`
- `spells_prepared_max`
- `prepared_spell_refs`
- `known_spell_refs`
- `always_prepared_spell_refs`
- `class_spell_refs`
- `bonus_spell_refs` (raça/feat/item/background)
- `slot_progression`
- `pact_slots`
- `ritual_casting` / flags específicos quando necessário
- `sources` com a origem de cada grupo (classe, subclasse, feat, item etc.)

A UI não deve depender de `char_info.spells` e `char_info.class_spells` como conceitos finais; esses campos podem continuar como compatibilidade, mas a camada de renderização deve usar uma visão consolidada.

### 2. Separar estado operacional de catálogo

O catálogo de magias possíveis vem do compêndio e das fontes permitidas. O estado operacional da ficha deve guardar apenas:

- quais magias são conhecidas;
- quais estão preparadas;
- quais são sempre preparadas;
- quais pertencem a fontes adicionais;
- quantos slots/recursos estão disponíveis e quais já foram gastos na sessão.

Isso reduz ambiguidade para classes híbridas e evita tratar “lista completa da classe” como se fosse sempre equivalente a “lista de magias preparáveis”.

## Proposta de UI

### Layout sugerido

1. **Header de spells**
   - contador de cantrips;
   - contador de magias preparadas/known;
   - contador de slots por nível;
   - eventual contador de spellbook/pact slots;
   - botão de ação principal: “Gerenciar Magias”.

2. **Barra de triagem**
   - input de busca por nome;
   - filtros por nível (chips/tabs);
   - filtros opcionais por fonte, estado (prepared/known/always-prepared/ritual) e por tipo (attack, save, utility).

3. **Lista escaneável**
   - cada linha/card deve conter:
     - nome;
     - nível;
     - badges de origem e estado;
     - tempo de conjuração;
     - alcance;
     - ataque/CD;
     - efeito/resumo curto;
     - ação contextual.
   - a apresentação deve poder alternar entre tabela compacta e card condensado no mobile.

4. **Seções por nível**
   - `Cantrips`;
   - `1st Level` até `9th Level`;
   - omitir níveis vazios por padrão ou mantê-los recolhidos, dependendo do tipo de conjurador.

### Ações por tipo de conjurador

- **Prepared casters**: mostrar `Prepare` / `Unprepare`.
- **Known casters**: mostrar `Known` / `Swap` apenas se a classe permitir troca; caso contrário, apenas badge de leitura.
- **Spontaneous casters**: mostrar somente leitura; a seleção é feita fora da aba ou em uma aba de level-up/edit.
- **Hybrid casters**: separar o que é prepared do que é known por origem, evitando um único botão genérico para tudo.
- **Warlock/pact magic**: slots e magias conhecidas devem ser exibidos como grupo próprio, não como “slots normais”.

## Degradação esperada

- **Casters sem preparo**: a UI vira catálogo + rastreador de recursos, sem botão de preparar/despreparar.
- **Casters conhecidos**: a UI mostra limite de magias conhecidas e estado atual, mas não ação de preparo.
- **Casters híbridos**: a UI divide a origem por blocos, com rótulos explícitos; a ação só aparece onde existe regra para isso.
- **Fichas sem spellcasting**: ocultar a aba ou mostrar um estado vazio útil (“este personagem não possui conjuração”).

## Arquivos prováveis a tocar

- `layouts/partials/kinds/character.html`
- `layouts/partials/character/spells/*.html` ou novo conjunto de partials por bloco
- `assets/js/spells.js`
- `assets/css/character-sheet.css`
- `assets/css/main.css` se badges/contadores forem compartilhados
- `archetypes/character.md`
- `docs/character-compendium-data.md`
- `create_character.py`
- `edit_character.py`
- `import_dndbeyond.py`
- `dnd_utils.py`
- testes de ficha e rolagem

## Critérios de aceite

1. A aba mostra contadores no topo e busca funcional.
2. Há filtragem por nível e a lista permanece escaneável.
3. A mesma base suporta bardos, magos, clérigos, druidas, paladinos, patrulheiros, artífices, feiticeiros, bruxos e híbridos.
4. Não existe dependência de uma única lista `class_spells` para todos os casos.
5. A interface não quebra quando campos antigos estiverem ausentes.
6. O layout e a interação ficam próximos da referência D&D Beyond, mas preservam o padrão leve do gmvault.

## Questões em aberto

- O estado de preparo/gasto deve permanecer apenas em memória da página, em localStorage, ou ser salvo no frontmatter?
- O modelo final deve distinguir explicitamente spellbook, list known, list prepared e always-prepared, ou deve derivar isso por regras de classe?
- Fichas multiclasse devem exibir uma aba única com blocos por origem ou abas separadas por classe?
