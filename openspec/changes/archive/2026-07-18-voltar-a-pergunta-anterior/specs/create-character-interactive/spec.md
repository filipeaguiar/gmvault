## ADDED Requirements

### Requirement: Navegação regressiva por pergunta
O assistente interativo de criação de personagem SHALL tratar cada pergunta confirmada como uma posição individual de navegação e SHALL interpretar `00` como uma solicitação para retornar exatamente à pergunta confirmada imediatamente anterior.

#### Scenario: Retorno dentro do mesmo passo
- **WHEN** o usuário informa `00` em uma pergunta que possui outra pergunta confirmada antes dela no mesmo passo
- **THEN** o assistente reabre somente a pergunta imediatamente anterior
- **THEN** o assistente não reinicia a primeira pergunta do passo

#### Scenario: Retorno entre passos
- **WHEN** o usuário informa `00` na primeira pergunta de um passo e a pergunta anterior pertence ao passo precedente
- **THEN** o assistente reabre a última pergunta confirmada do passo precedente

#### Scenario: Retornos sucessivos
- **WHEN** o usuário informa `00`, retorna uma pergunta e informa `00` novamente
- **THEN** o assistente retorna mais uma pergunta no histórico a cada solicitação

#### Scenario: Cancelamento na primeira pergunta
- **WHEN** o usuário informa `00` e não existe pergunta anterior no histórico
- **THEN** o assistente cancela a criação de forma controlada
- **THEN** nenhum arquivo de personagem é gerado

### Requirement: Preservação e consistência das respostas durante o retorno
O assistente SHALL preservar respostas confirmadas anteriores à pergunta reaberta e SHALL recalcular ou invalidar respostas posteriores quando a resposta corrigida alterar suas dependências ou opções válidas.

#### Scenario: Correção sem perder respostas anteriores
- **WHEN** o usuário retorna a uma pergunta intermediária e fornece uma nova resposta
- **THEN** as respostas confirmadas antes dessa pergunta permanecem disponíveis sem serem solicitadas novamente
- **THEN** o fluxo prossegue a partir da resposta corrigida

#### Scenario: Resposta posterior continua válida
- **WHEN** uma resposta corrigida não altera as opções ou a validade de uma resposta posterior já confirmada
- **THEN** o assistente preserva a resposta posterior

#### Scenario: Resposta posterior fica incompatível
- **WHEN** uma resposta corrigida altera as opções disponíveis e torna incompatível uma resposta posterior
- **THEN** o assistente descarta a resposta incompatível
- **THEN** o assistente solicita novamente essa resposta quando alcançar a respectiva pergunta

#### Scenario: Entrada inválida não altera o histórico
- **WHEN** o usuário fornece uma entrada inválida em uma pergunta
- **THEN** o assistente repete a pergunta atual
- **THEN** nenhuma posição adicional é criada no histórico de navegação
