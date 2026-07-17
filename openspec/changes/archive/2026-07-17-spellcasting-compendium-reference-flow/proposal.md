## Why

A ficha ainda mantém dois conjuntos parcialmente redundantes de magias (`spells` e `class_spells`) e apresenta o estado de preparo repetidamente em cada card, o que mistura catálogo, conteúdo canônico e estado operacional. O fluxo deve usar os dados de magias do 5e.tools para materializar páginas canônicas no compêndio, deixando a ficha apenas com referências e estado específico do personagem, sem perder a experiência genérica entre tipos de conjurador nem os metadados de rolagem Dice+.

## What Changes

- Tornar as páginas em `content/compendium/spells/`, geradas ou sincronizadas a partir do 5e.tools, a fonte canônica de descrição e metadados compartilhados das magias usadas pela ficha.
- Fazer os fluxos de criação, edição e importação materializarem no compêndio cada magia referenciada e gravarem na ficha somente referências e estado operacional, com fallback seguro para conteúdo legado.
- Manter no topo do Grimório somente as magias prontas para uso conforme o perfil de conjuração do personagem (preparadas, conhecidas, sempre disponíveis ou concedidas por outra fonte).
- Remover o badge repetido de “Preparada” dos cards da lista operacional; o contexto da seção e os controles de gerenciamento comunicarão esse estado.
- Exibir filtros, grupos e trackers somente para círculos e slots aos quais o personagem possui acesso, incluindo cantrips e pact slots quando aplicáveis.
- Adicionar abaixo da lista operacional uma lista de gerenciamento com as demais magias referenciadas, oferecendo checkboxes de preparo apenas quando o perfil/fonte permitir essa ação.
- Preservar comportamento somente leitura para conjuradores conhecidos, espontâneos, concedidos por feature e outros perfis sem preparo, além de suportar perfis híbridos sem regras específicas por personagem.
- Preservar a resolução de `spell_info`, os controles de rolagem estruturada e os atributos `data-*` usados pela integração Dice+ ao alternar o estado de preparo.
- Manter compatibilidade de renderização com fichas legadas durante a migração, sem tratar o estado em `localStorage` como alteração do conteúdo canônico.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `interactive-character-sheet-spells`: reorganizar a lista operacional e a lista de gerenciamento, limitar níveis/slots acessíveis e condicionar os controles de preparo ao perfil de conjuração.
- `compendium`: exigir que magias exibidas pela ficha sejam resolvidas de páginas canônicas do compêndio, mantendo na ficha somente referências e estado operacional.
- `import-tools`: materializar/sincronizar magias via dados do 5e.tools e gerar referências canônicas e deduplicadas para o estado de conjuração do personagem.

## Impact

- Renderização e interação: `layouts/partials/kinds/character.html`, possíveis novos partials de personagem, `assets/js/spells.js` e `assets/css/character-sheet.css`.
- Modelo e documentação: `archetypes/character.md` e `docs/character-compendium-data.md`.
- Fluxos de personagem e integração 5e.tools: `dnd_utils.py`, `create_character.py`, `edit_character.py` e `import_dndbeyond.py`.
- Testes de perfil de conjuração, importação, renderização Hugo, persistência local e metadados/execução de rolagens Dice+.
- Conteúdo legado continua renderizável; a normalização pode alterar o front matter produzido por novas importações e edições, mas não exige migração destrutiva imediata.
