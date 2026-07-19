## 1. Controlador de navegação

- [x] 1.1 Adicionar testes unitários para histórico por pergunta, retorno simples, retornos sucessivos, cancelamento inicial e entradas inválidas.
- [x] 1.2 Implementar o controlador de perguntas com chaves estáveis, cursor, respostas confirmadas e sinalização de cancelamento.
- [x] 1.3 Implementar atualização de respostas e invalidação seletiva das respostas posteriores dependentes.

## 2. Integração com a criação de personagem

- [x] 2.1 Adaptar `ask`, `ask_int`, `ask_choice` e seleções múltiplas ao protocolo comum do controlador.
- [x] 2.2 Migrar perguntas básicas, campanha, espécie, classe, nível, subclasse, talentos, background e equipamento inicial para o histórico por pergunta.
- [x] 2.3 Migrar atributos, bônus, perícias, equipamentos extras, magias e escolhas repetíveis para chaves contextuais estáveis.
- [x] 2.4 Recalcular valores derivados após respostas alteradas e preservar somente respostas posteriores ainda válidas.
- [x] 2.5 Garantir que geração de Markdown e criação de referências ocorram somente após a conclusão do fluxo navegável.

## 3. Validação

- [x] 3.1 Adicionar teste integrado com carregadores simulados comprovando retorno dentro de um passo, entre passos e preservação das respostas anteriores.
- [x] 3.2 Executar os testes existentes do criador de personagem e corrigir regressões sem alterar o arquivo gerado.
- [x] 3.3 Executar a suíte Python relevante e validar `openspec validate voltar-a-pergunta-anterior`.
