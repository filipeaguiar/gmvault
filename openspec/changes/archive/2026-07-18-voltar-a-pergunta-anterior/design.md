## Context

`create_character.py` organiza a coleta em dez passos grandes e usa `GoBackException` para sair de qualquer prompt. A exceção é capturada somente pelo laço dos passos, portanto uma solicitação de retorno reinicia o passo inteiro. Alguns passos contêm várias perguntas, laços de seleção e perguntas condicionais, o que torna insuficiente apenas diminuir o número do passo.

A mudança deve preservar respostas válidas, cálculos dependentes e o comportamento de `ask`, `ask_int`, `ask_choice` e seleções compostas, sem alterar o arquivo de personagem produzido.

## Goals / Non-Goals

**Goals:**

- Tratar cada prompt confirmado como uma unidade navegável do assistente.
- Fazer `00` reabrir somente o prompt confirmado imediatamente anterior.
- Atualizar ou invalidar apenas o estado que depende da resposta alterada.
- Suportar retornos sucessivos e travessia entre passos.
- Manter o cancelamento quando não houver pergunta anterior.
- Cobrir a navegação com testes determinísticos, sem acesso à rede.

**Non-Goals:**

- Alterar regras de criação, cálculos de personagem ou formato do front matter.
- Modificar `edit_character.py`, o menu web ou importadores.
- Persistir uma sessão incompleta entre execuções do processo.
- Introduzir biblioteca externa de interface ou framework de formulários.

## Decisions

### Usar um controlador de navegação com histórico de perguntas

A coleta interativa será mediada por um controlador que registra, para cada pergunta, uma chave estável, a resposta confirmada e a função responsável por aplicar essa resposta ao estado da criação. Ao receber `00`, o controlador move o cursor exatamente uma posição para trás e reabre a pergunta correspondente. A resposta substituída atualiza o estado antes de o fluxo avançar novamente.

Essa abordagem é preferível a decrementar `step`, porque o passo não representa a granularidade pedida. Também é preferível a uma cadeia de blocos `try/except` específicos, que duplicaria lógica e seria frágil diante de novas perguntas.

### Manter o estado coletado separado de valores derivados

Respostas serão mantidas em um estado explícito do assistente. Valores derivados — opções condicionais, bônus, modificadores e listas calculadas — serão recalculados a partir do ponto alterado. Respostas posteriores incompatíveis com as novas opções serão descartadas; respostas anteriores e ainda válidas serão preservadas.

Isso evita estado local obsoleto quando, por exemplo, classe, nível ou espécie forem alterados. Preservar cegamente todas as respostas posteriores foi descartado porque poderia produzir combinações inválidas.

### Adaptar todos os tipos de prompt ao mesmo protocolo de retorno

`ask`, `ask_int`, `ask_choice`, seleções múltiplas e perguntas dentro de laços usarão o mesmo sinal de retorno e serão registradas individualmente. Entradas inválidas continuam repetindo a pergunta atual e não entram no histórico. Perguntas condicionais só entram na sequência quando sua condição estiver ativa.

A primeira pergunta navegável não tem antecessora: `00` nela mantém o comportamento atual de cancelar a operação de forma controlada.

### Isolar efeitos colaterais da fase navegável

Downloads/cache e preparação de catálogos podem ocorrer durante a coleta, mas geração de Markdown e publicação de stubs permanecem após a confirmação final. Ao voltar, o controlador não deve duplicar gravações nem tratar mensagens de cabeçalho como perguntas.

### Testar o controlador e um fluxo integrado representativo

Testes unitários verificarão cursor, substituição de resposta, retorno sucessivo, cancelamento inicial e invalidação de respostas dependentes. Um teste integrado com prompts e carregadores simulados verificará que `00` em uma pergunta intermediária reabre apenas a anterior e que o fluxo conclui com os valores corrigidos.

## Risks / Trade-offs

- [Refatoração do fluxo extenso pode introduzir regressões em ramificações condicionais] → Migrar os prompts para o controlador por grupos e manter testes existentes, acrescentando cenários para espécie, classe, atributos e listas repetíveis.
- [Alterar uma resposta pode invalidar opções posteriores] → Recalcular dependências e descartar somente respostas posteriores que não pertençam mais ao conjunto válido.
- [Chaves de perguntas repetidas podem colidir em laços] → Compor chaves estáveis com contexto e índice, como perícia adicional ou posição de metamagia.
- [Carregamentos podem ser repetidos ao recalcular opções] → Reutilizar os caches e objetos de catálogo já carregados durante a mesma execução.
