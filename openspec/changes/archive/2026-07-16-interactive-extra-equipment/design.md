## Context

Atualmente o script `create_character.py` preenche os itens iniciais (background e pack) mas não permite que o usuário digite o nome de itens avulsos que ele também possua no inventário no momento da criação.

## Goals / Non-Goals

**Goals:**
- Permitir uma etapa interativa via CLI onde o usuário digita nomes de itens para buscar no 5e.tools.
- Desambiguar múltiplos itens usando um menu de escolha caso o nome procurado resulte em múltiplas correspondências (ex: "Shield" tem vários tipos).
- Adicionar o item escolhido à lista de equipamentos finais com `quantity` configurado por input, assim como sua referência ao compêndio.

**Non-Goals:**
- Não iremos refatorar o parser completo de JSONs no 5e.tools, usaremos funções simplificadas iterando na lista de `items.json`.
- Não será possível alterar itens já inseridos nessa etapa; a etapa é append-only.

## Decisions

- **Busca via Substring Case Insensitive**: Na etapa de loop, vamos varrer a lista de nomes nos dados parseados de `items.json` e `items-base.json`. Qualquer nome que contenha a substring procurada será retornado.
- **Menu de Desambiguação**: Utilizaremos `ask_choice` passando a lista das opções encontradas. Caso retorne 0 itens, avisa e volta; se retornar 1, confirma; se retornar mais de 1, exibe opções.
- **Pergunta de Quantidade**: Sempre perguntar "Qual a quantidade de [Nome]?" usando `ask_int()` (default 1).
- **Encerramento da etapa**: A condição de saída do loop é o usuário enviar um campo de texto vazio (apertar Enter sem digitar nada) na pergunta "Deseja adicionar um item individual?".

## Risks / Trade-offs

- **Risk**: Itens muito genéricos podem retornar listas enormes que poluem o menu interativo (ex: buscar por "sword").
- **Mitigation**: Limitar a exibição ou orientar o usuário a ser mais específico via prompt de ajuda, além de ordernar por tamanho da string para que correspondências exatas fiquem no topo.
