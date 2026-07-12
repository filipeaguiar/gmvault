## ADDED Requirements

### Requirement: Carregamento de translation_config.json
O sistema SHALL carregar o arquivo de configuração `translation_config.json` para obter os perfis de tradução e o perfil ativo.

#### Scenario: Carregamento bem-sucedido do perfil ativo
- **WHEN** o script de tradução é inicializado e encontra o arquivo `translation_config.json` contendo um perfil válido
- **THEN** o script extrai as configurações de `engine`, `model`, `base_url`, `api_key_env_var` e `strategy` para aplicar na tradução

#### Scenario: Fallback para CLI padrão
- **WHEN** o script de tradução é inicializado e o arquivo `translation_config.json` não é encontrado
- **THEN** o script emite um aviso silencioso ou informativo e recorre aos valores de fallback definidos via argumentos da CLI

### Requirement: Resolução de segredos via .env
O sistema SHALL ler credenciais confidenciais, como chaves de API, a partir do arquivo `.env` local ou das variáveis de ambiente globais.

#### Scenario: Injeção de chave de API resolvida
- **WHEN** um perfil exige autenticação e define o nome da chave de ambiente no campo `api_key_env_var`
- **THEN** o script lê a chave correspondente a partir do arquivo `.env` ou das variáveis de ambiente e a injeta nas chamadas HTTP para o provedor de tradução

### Requirement: Estratégia de Tradução de Documento Completo (full_document)
O sistema SHALL suportar a tradução do corpo do documento Markdown em uma única chamada de API em vez de segmentar por parágrafos.

#### Scenario: Execução em chamada única
- **WHEN** a estratégia de tradução do perfil ativo estiver configurada como `full_document`
- **THEN** o script envia o corpo de Markdown inteiro de cada arquivo, junto com o glossário estático no prompt de sistema, na mesma requisição para o LLM

### Requirement: Ignorar arquivos confidenciais no Git
O repositório SHALL ignorar arquivos locais contendo configurações personalizadas e credenciais de segurança.

#### Scenario: Ignorar arquivos locais no git
- **WHEN** o arquivo `.gitignore` é analisado pelo Git
- **THEN** os arquivos `.env` e `translation_config.json` devem ser ignorados para evitar commits indesejados
