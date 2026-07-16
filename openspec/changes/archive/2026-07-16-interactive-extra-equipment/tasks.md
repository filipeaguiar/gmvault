## 1. Funções de Busca (dnd_utils.py)

- [x] 1.1 Criar uma função `search_item_by_name(query, item_data)` que retorne uma lista de itens que contenham `query` (case-insensitive) no nome.
- [x] 1.2 Garantir que a função retorne apenas nomes de itens distintos (ou referências a eles) adequados para o menu.

## 2. Etapa Interativa (create_character.py)

- [x] 2.1 Adicionar um loop antes da consolidação de equipamentos (passo 8.2), perguntando `ask("Deseja adicionar um item extra? (Deixe em branco para pular/finalizar)")`.
- [x] 2.2 Ao receber uma resposta não vazia, usar `search_item_by_name` para buscar as opções em `item_data`.
- [x] 2.3 Se 0 resultados, exibir aviso e voltar ao início do loop.
- [x] 2.4 Se 1 resultado, assumir o item, exibir o nome encontrado e perguntar a quantidade via `ask_int`.
- [x] 2.5 Se múltiplos resultados, exibir um `ask_choice` para desambiguação e em seguida perguntar a quantidade.
- [x] 2.6 Adicionar o item escolhido à lista temporária `extra_items` e continuar no loop.

## 3. Consolidação e Testes

- [x] 3.1 Somar a lista `extra_items` à variável `combined_items` que já recebe os itens de background e do pacote.
- [x] 3.2 Garantir que o script executa do início ao fim com sucesso.
- [x] 3.3 Executar `pytest` para verificar se nenhuma mudança quebrou a suíte de testes.
