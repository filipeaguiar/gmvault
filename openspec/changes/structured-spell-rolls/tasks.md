## 1. Extração e modelo estruturado

- [x] 1.1 Implementar em `dnd_utils.py` um extrator recursivo para `scalingLevelDice` e tags `damage`, `dice`, `scaledamage` e `scaledice` presentes em `entries` e `entriesHigherLevel`.
- [x] 1.2 Normalizar e deduplicar fórmulas, classificando-as como `damage`, `healing` ou `dice`, gerando patamares `character_level` ou `spell_slot` para progressões contínuas e discretas e evitando inferências a partir de prosa.
- [x] 1.3 Mapear `spellAttack`, `damageInflict`, `savingThrow`, `miscTags` e nível numérico para os campos canônicos de `spell_info`.
- [x] 1.4 Integrar o novo `spell_info` à criação e sincronização de páginas de magia, preservando o markup Dice+ já gerado no corpo.
- [x] 1.5 Implementar atualização não destrutiva de `spell_info` para magias existentes, preservando tradução, campos editoriais e corpo Markdown.

## 2. Archetype e autoria manual

- [x] 2.1 Atualizar `archetypes/spell.md` com `level_number`, `attack_type`, `damage_types`, `saving_throws` e `rolls`, incluindo um exemplo comentado de escalonamento.

## 3. Renderização das rolagens

- [x] 3.1 Criar um partial reutilizável que resolva patamares pelo `char_info.level` e pelos `spell_slots` disponíveis e renderize somente ataques e fórmulas utilizáveis com `roll-ready`, `data-roll-notation` e rótulos acessíveis.
- [x] 3.2 Integrar o partial à linha do nome das magias preparadas em `layouts/partials/kinds/character.html`.
- [x] 3.3 Integrar o partial à linha do nome na lista completa da classe e verificar que `assets/js/spells.js` preserva os controles ao clonar uma magia preparada.
- [x] 3.4 Integrar os metadados estruturados à página individual de magia sem criar fórmula de ataque quando não houver contexto de personagem.
- [x] 3.5 Adicionar estilos compactos e responsivos para a linha de rolagens, distinguindo ataque, dano, cura e dados genéricos sem adicionar um botão textual separado.

## 4. Migração e validação

- [x] 4.1 Adicionar testes unitários com fixtures de Fireball, Cure Wounds, Magic Missile, Eldritch Blast, Sleep, Fire Bolt, Spirit Shroud e uma magia sem rolagens, validando que Magic Missile permanece `1d4+1` por dardo sem agregação inferida.
- [x] 4.2 Adicionar teste de regressão que confirme sincronização de `spell_info` sem alteração do corpo e dos metadados de tradução.
- [x] 4.3 Adicionar teste de renderização Hugo para rolagens ao lado do nome, ataque com `spell_attack_bonus`, seleção do patamar atual de truques, filtragem por slots disponíveis, ausência segura de controles e clonagem de cards preparados.
- [x] 4.4 Sincronizar magias representativas, revisar o diff e então migrar as páginas resolvíveis em `content/compendium/spells/`, relatando as não encontradas sem modificá-las.
- [ ] 4.5 Executar os testes Python e JavaScript relacionados ao Dice+, `hugo -D --gc --minify` e `hugo --gc --minify`.
