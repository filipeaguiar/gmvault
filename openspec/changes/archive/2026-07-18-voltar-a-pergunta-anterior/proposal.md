## Why

No fluxo interativo de `create_character.py`, digitar `00` lança uma exceção tratada apenas no laço dos passos principais. Como resultado, o usuário perde todas as respostas dadas dentro do passo atual e retorna ao começo dele, em vez de corrigir somente a resposta imediatamente anterior.

## What Changes

- Fazer `00` retornar à pergunta imediatamente anterior do fluxo de criação de personagem.
- Preservar as respostas já confirmadas antes da pergunta de destino, evitando repetir todo o passo atual.
- Permitir retornos sucessivos, uma pergunta por vez, inclusive entre os limites dos passos principais.
- Manter o cancelamento da operação quando `00` for informado na primeira pergunta disponível.
- Adicionar testes automatizados para navegação regressiva e preservação das respostas anteriores.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `create-character-interactive`: alterar o contrato de navegação do assistente para que `00` retorne exatamente uma pergunta, sem reiniciar o passo atual.

## Impact

- Fluxo e gerenciamento de estado em `create_character.py`.
- Funções de prompt `ask`, `ask_int`, `ask_choice` e seleções compostas que propagam a solicitação de retorno.
- Testes do criador interativo em `tests/`.
- Sem novas dependências e sem alteração no formato Markdown gerado.
