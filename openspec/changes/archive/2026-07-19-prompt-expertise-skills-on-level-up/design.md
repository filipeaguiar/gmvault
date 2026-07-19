## Context

O fluxo de `edit_character.py` monta a lista de características do nível de destino, atualiza uma cópia de `char_info` e só a persiste após confirmação. A ficha já representa cada perícia como um dicionário com `proficient`, `expertise` e `bonus`, e o recálculo existente já dobra a proficiência quando `expertise` é verdadeiro.

## Goals / Non-Goals

**Goals:**
- Converter a aquisição de uma característica `Expertise` em uma escolha obrigatória e persistente no fluxo de subida de nível.
- Limitar as opções às perícias proficientes sem Expertise e aplicar o dobro da proficiência às duas escolhidas.
- Preservar a garantia atual de não alterar a ficha antes da confirmação.

**Non-Goals:**
- Não implementar Expertise para ferramentas, nem outras características que concedam escolhas de perícia.
- Não inferir escolhas retroativamente em fichas existentes.
- Não alterar o fluxo de criação inicial de personagem.

## Decisions

- Detectar Expertise pela lista de características do plano do nível, comparando o nome de forma normalizada. Isso usa a mesma fonte canônica já usada para adicionar características e evita manter uma tabela paralela por classe e nível.
- Oferecer somente entradas de `char_info.skills` que tenham `proficient: true` e não tenham `expertise: true`; Expertise exige proficiência e não pode ser aplicada duas vezes à mesma perícia.
- Coletar duas escolhas distintas antes da prévia e da confirmação. A cópia profunda já utilizada pelo fluxo garante que cancelar ou falhar na escolha não modifique o front matter.
- Reusar o recálculo de bônus existente após marcar as escolhas, em vez de gravar valores calculados especificamente para Expertise.

Alternativa descartada: deduzir as escolhas por ordem das perícias ou escolher automaticamente. Isso produziria decisões de jogador que o sistema não pode determinar.

## Risks / Trade-offs

- [Dados de classe nomeiam a característica de modo inesperado] → normalizar o nome e cobrir a detecção com testes usando a entrada canônica `Expertise`.
- [Ficha legada não possui duas perícias elegíveis] → informar a pendência e não confirmar nem salvar a subida de nível.
- [A característica aparece mais de uma vez na lista] → solicitar somente uma seleção de duas perícias por avanço.
