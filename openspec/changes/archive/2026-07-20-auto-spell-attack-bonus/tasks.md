## 1. Modelo e resolução de conjuração

- [x] 1.1 Identificar o campo de atributo de conjuração nos dados de classe do 5e.tools e criar normalização segura para as chaves de atributo suportadas.
- [x] 1.2 Estender o perfil de conjuração para expor o atributo normalizado apenas quando ele for resolvível para uma ficha de classe única.
- [x] 1.3 Implementar um resolvedor de bônus de ataque mágico que priorize sobrescrita explícita, derive proficiência mais modificador de conjuração quando aplicável e diferencie placeholder legado de valor configurado.
- [x] 1.4 Cobrir o resolvedor com testes para Warlock/Carisma, ausência de dados, sobrescrita excepcional e placeholder legado `0`.

## 2. Fluxos de ficha

- [x] 2.1 Atualizar `create_character.py` para persistir o atributo de conjuração resolvido e não gravar `spell_attack_bonus: 0` como placeholder de novas fichas.
- [x] 2.2 Atualizar `edit_character.py` para manter ou recalcular o atributo de conjuração sem sobrescrever bônus de ataque explicitamente configurados.
- [x] 2.3 Adicionar testes dos fluxos de criação, edição e sincronização para perfil de classe única e caso multiclasse ambíguo.

## 3. Renderização e Dice+

- [x] 3.1 Atualizar `layouts/partials/helpers/spell-rolls.html` para usar o bônus de ataque mágico resolvido em magias com `spell_info.attack_type`.
- [x] 3.2 Omitir somente o controle de ataque quando não houver dado suficiente ou a fonte for multiclasse ambígua, preservando controles de dano, cura e dados.
- [x] 3.3 Estender os testes de renderização Hugo para verificar `Eldritch Blast` com fórmula derivada `1d20+6`, sobrescrita explícita e fallback sem ataque inventado.

## 4. Validação

- [x] 4.1 Executar as suítes Python relevantes para perfil de conjuração, criação/edição de personagem e renderização de rolagens de magia.
- [x] 4.2 Executar `hugo -D --gc --minify` e `hugo --gc --minify`.
- [ ] 4.3 Verificar manualmente, no Owlbear com Dice+ pronto, que o valor derivado continua acionando a mesma ponte de rolagem.
