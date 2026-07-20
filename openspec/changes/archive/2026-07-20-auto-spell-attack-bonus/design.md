## Context

O partial `helpers/spell-rolls.html` renderiza ataques de magias com `char_info.spell_attack_bonus`. A ponte da ficha apenas encaminha a notação HTML final para Dice+, portanto não calcula modificadores. As fichas já armazenam `char_info.proficiency_bonus` e `char_info.mods`, enquanto `char_info.spellcasting.ability` existe no contrato de perfil, mas pode estar vazio nas fichas geradas atualmente.

## Goals / Non-Goals

**Goals:**
- Gerar automaticamente a notação de ataque mágico para conjuradores de classe única quando houver dados suficientes.
- Manter uma sobrescrita explícita para bônus que não possam ou não devam ser inferidos.
- Atualizar criação e edição locais para persistir um atributo de conjuração normalizado.
- Manter a ficha e o Dice+ utilizáveis para conteúdo legado e fora da extensão.

**Non-Goals:**
- Inferir atributos de conjuração por texto da descrição de uma magia.
- Resolver ataque por origem de magia, multiclasse, subclasses excepcionais ou poderes que usam outro atributo.
- Aplicar modificadores de dano, incluindo *Agonizing Blast*.
- Alterar o protocolo, a validação ou a interface do Owlbear/Dice+.

## Decisions

### 1. O perfil de conjuração será a fonte do atributo

`char_info.spellcasting.ability` receberá uma chave normalizada (`str`, `dex`, `con`, `int`, `wis` ou `cha`) derivada de dados estruturados da classe durante criação, edição e sincronização aplicáveis. O cálculo usará `char_info.mods[ability]`, não o valor bruto de atributo.

**Alternativa considerada:** manter uma tabela apenas no layout Hugo. Rejeitada porque esconderia a origem do dado, não ajudaria os fluxos de criação/edição e seria mais frágil para classes futuras.

### 2. A fórmula derivada será proficiência mais modificador de conjuração

Quando o perfil tiver atributo válido e a ficha tiver `proficiency_bonus` e o modificador correspondente, o valor será `proficiency_bonus + mods[ability]`. Para uma magia com `spell_info.attack_type`, o partial emitirá `1d20` mais esse total, preservando os atributos `data-*` existentes.

### 3. Sobrescrita explícita terá precedência sem usar zero como sentinela

Um `spell_attack_bonus` explicitamente configurado continuará sendo a fonte final, pois pode incorporar bônus de itens, talentos ou regras locais. A ausência deverá ser representável de modo distinto de `0`; os fluxos novos não devem gravar `0` meramente como placeholder. Fichas legadas com `0` e atributo resolvível poderão usar o cálculo derivado, pois um ataque mágico de conjurador não tem bônus total zero nas regras usuais.

**Alternativa considerada:** sempre substituir o campo pelo cálculo. Rejeitada porque removeria a capacidade de representar bônus especiais.

### 4. Falha de dados degrada para conteúdo legível

Se não houver sobrescrita válida nem dados completos para derivar, a ficha não inventará um ataque `1d20+0`. A magia e seus controles de dano continuarão renderizáveis; o controle de ataque será omitido até revisão editorial.

### 5. Multiclasse fica fora do resolvedor inicial

O cálculo inicial usará o perfil global somente para fichas de classe única. Futuramente, cada entrada de magia poderá portar `casting_ability` ou uma origem de classe resolvível para calcular ataques distintos. A presente mudança não deve fingir precisão para magias de multiclasses.

## Risks / Trade-offs

- **[Dados de classe podem não expor o atributo de conjuração no mesmo formato]** → Normalizar aliases, testar classes usuais e preservar perfil vazio quando a resolução for incerta.
- **[Fichas legadas usam `spell_attack_bonus: 0` como valor real ou placeholder]** → Documentar a precedência e cobrir ambos os casos com testes; a derivação somente ocorre com perfil válido.
- **[Bônus extraordinários podem divergir da fórmula base]** → Manter sobrescrita explícita como prioridade.
- **[Multiclasse pode usar atributos distintos]** → Limitar o escopo a classe única e omitir cálculo incerto.
- **[Modificadores de atributo de equipamentos são calculados no layout]** → O resolvedor de ataque deve consumir o modificador efetivo já disponível ao template, ou declarar e testar claramente sua ordem de cálculo.

## Migration Plan

1. Passar a gravar atributo de conjuração e ausência de sobrescrita nos novos fluxos locais.
2. Renderizar ataques derivados para fichas com dados completos, sem migrar destrutivamente arquivos existentes.
3. Manter o fallback explícito e omitir controles incertos.
4. Em rollback, restaurar o partial e os fluxos anteriores; os campos aditivos continuam inofensivos para fichas legadas.

## Open Questions

- A sobrescrita explícita deve ser identificada por um novo campo ou a presença de `spell_attack_bonus` não nulo basta para distinguir o valor configurado de placeholders legados?
- O atributo de conjuração deve considerar imediatamente modificadores de atributo vindos de equipamentos equipados, ou isso exige uma regra adicional de ordenação no template?
