## Context

Atualmente, o script [translate_drafts.py](file:///home/filipe/Documentos/Projetos/gmvault/translate_drafts.py) realiza traduções fragmentadas (bloco a bloco), forçando dezenas de conexões HTTPS e chamadas de API consecutivas por arquivo Markdown. Embora isso atenda a modelos locais menores (com janelas de contexto limitadas), gera alta latência de rede e impede que LLMs robustos (como DeepSeek ou Gemini) enxerguem o fluxo textual de forma integral, o que prejudica a concordância gramatical e a consistência tonal do RPG.

Ademais, segredos e configurações de tradução (URLs e modelos) estão acoplados e expostos no código, dificultando alterações rápidas de perfis.

## Goals / Non-Goals

**Goals:**
- **Isolar Credenciais**: Mover segredos como chaves de API para um arquivo `.env` ignorado pelo Git.
- **Perfis Estruturados**: Configurar múltiplos endpoints de API (como DeepSeek API, LM Studio local, OpenAI) usando um arquivo centralizado `translation_config.json`.
- **Estratégias Flexíveis**: Implementar suporte para traduzir o arquivo Markdown completo em uma única chamada de API (`full_document`), mantendo a compatibilidade com a tradução fatiada (`split_blocks`) para modelos locais.
- **Minimizar Dependências**: Manter a independência do script sem forçar novas bibliotecas pesadas de terceiros.

**Non-Goals:**
- Criar interface visual de usuário (GUI) ou painel administrativo para as configurações.
- Substituir o funcionamento ou as configurações da biblioteca Argos Translate (motor local).
- Implementar mecanismos de rotação automática ou teste dinâmico de chaves de API.

## Decisions

### Decisão 1: Parser manual simplificado de `.env` em Python
- **Abordagem escolhida**: Implementar uma função interna simples em [translate_drafts.py](file:///home/filipe/Documentos/Projetos/gmvault/translate_drafts.py) de aproximadamente 10 a 15 linhas para ler e analisar o arquivo `.env` de forma direta (buscando linhas no formato `KEY=VALUE`).
- **Alternativas consideradas**: Inclusão de `python-dotenv` no `requirements.txt`.
- **Justificativa**: Evita a necessidade de gerenciar downloads adicionais de pacotes e instalação de dependências em ambientes mínimos de produção, reduzindo atritos no pipeline de build.

### Decisão 2: Formato e Mapeamento de Credenciais em `translation_config.json`
- **Abordagem escolhida**: O JSON de configuração mapeará perfis com o campo `api_key_env_var` (especificando a chave de ambiente que guarda o segredo) ao invés de salvar a API Key diretamente no JSON.
- **Alternativas consideradas**: Salvar a chave de API diretamente no JSON de configuração.
- **Justificativa**: O arquivo `translation_config.json` pode conter dados que o usuário queira versionar/compartilhar (perfis de prompts, URLs, modelos), enquanto as variáveis de ambiente em `.env` permanecem estritamente privadas e seguras.

### Decisão 3: Integração do Glossário na Estratégia `full_document`
- **Abordagem escolhida**: No modo `full_document`, o script injetará a totalidade dos termos do glossário de forma fixa e direta no prompt de sistema de cada requisição. O script não rodará a limpeza dinâmica `select_glossary_config` por arquivo neste modo.
- **Alternativas consideradas**: Manter a filtragem dinâmica de termos de glossário antes de enviar para o DeepSeek.
- **Justificativa**: Passar um glossário estático fixo ativa a otimização de **Prompt Caching** (cache de prompt) na API do DeepSeek ou do Gemini. O provedor processa os tokens de entrada repetidos uma vez e aplica descontos de até 90% nas chamadas subsequentes, além de acelerar o processamento.

## Risks / Trade-offs

- **[Risco]** Vazamento acidental de chaves de API se o `.env` for forçado ao Git.
  - **Mitigação**: Inclusão explícita imediata de `.env` e `translation_config.json` no arquivo [.gitignore](file:///home/filipe/Documentos/Projetos/gmvault/.gitignore).
- **[Risco]** Estouro de contexto ou limite de tokens de saída da API ao traduzir um arquivo Markdown muito extenso em chamada única.
  - **Mitigação**: O script limitará o uso do modo `full_document` por arquivo e disparará avisos claros, permitindo o fallback automático para a estratégia `split_blocks` caso o tamanho do texto do corpo ultrapasse um limite operacional de segurança (ex: 30.000 caracteres ou ~8.000 tokens).
