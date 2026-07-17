## Why

As magias importadas já preservam algumas tags de dados no corpo Markdown, mas a ficha não possui uma representação estruturada e confiável das rolagens para exibi-las junto ao nome da magia. Isso limita a integração com Dice+, dificulta distinguir dano, cura e ataques mágicos e deixa o comportamento dependente da descrição textual.

## What Changes

- Extrair do schema do 5e.tools `scalingLevelDice`, as tags `damage`, `dice`, `scaledamage` e `scaledice`, além de `spellAttack`, `damageInflict`, `savingThrow` e `miscTags`.
- Gravar no `spell_info` uma lista canônica e deduplicada de rolagens, com notação, tipo e rótulo, mantendo separadamente metadados de ataque, dano, cura e resistência.
- Preservar no corpo Markdown os controles de rolagem que já existem; os novos metadados complementam, e não substituem, a descrição da magia.
- Exibir controles Dice+ compactos na mesma linha do nome da magia nas listas de magias preparadas e de classe.
- Resolver escalonamento no contexto da ficha: truques usam o maior patamar permitido pelo nível atual do personagem, e magias de slot exibem apenas fórmulas correspondentes a slots que o personagem realmente possui.
- Permitir que ataques mágicos usem dinamicamente `char_info.spell_attack_bonus`, enquanto dano e cura usam as fórmulas estáticas do compêndio.
- Atualizar o archetype de magia para documentar o formato estruturado esperado.
- Sincronizar metadados estruturados de magias já existentes sem apagar tradução, front matter editorial ou corpo Markdown revisado.

## Capabilities

### New Capabilities
- `structured-spell-rolls`: formato canônico para rolagens e metadados mecânicos de magias armazenados no compêndio.

### Modified Capabilities
- `interactive-character-sheet-spells`: exibir rolagens Dice+ ao lado do nome das magias nas listas preparadas e completas.
- `import-tools`: extrair e sincronizar dados estruturados de rolagem a partir do schema de magias do 5e.tools.

## Impact

- `dnd_utils.py`: extração, normalização, deduplicação e sincronização de `spell_info`.
- `archetypes/spell.md`: novos campos estruturados para autoria manual.
- `layouts/partials/kinds/character.html`: linha de título das magias com controles Dice+.
- `layouts/partials/kinds/spell.html`: apresentação dos metadados e rolagens na página da magia.
- `assets/css/character-sheet.css` e possivelmente `assets/js/spells.js`: layout compacto e clonagem consistente dos controles.
- Conteúdo existente em `content/compendium/spells/`: migração não destrutiva de metadados.
- Testes Python, Hugo e Dice+ para fórmulas de dano, cura, ataque e magias sem rolagem.
