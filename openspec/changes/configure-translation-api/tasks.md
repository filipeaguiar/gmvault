## 1. Configuração e Segurança

- [x] 1.1 Atualizar o arquivo `.gitignore` para ignorar `.env` e `translation_config.json`
- [x] 1.2 Criar o template `translation_config.json.example` contendo perfis de exemplo para `deepseek-api` e `gemma-local`
- [x] 1.3 Criar o template `.env.example` contendo as variáveis de ambiente necessárias (`DEEPSEEK_API_KEY`, `OPENAI_API_KEY`)

## 2. Leitura de Configurações no Script de Tradução

- [x] 2.1 Implementar a função `load_env` em `translate_drafts.py` para realizar o parseamento manual do arquivo `.env`
- [x] 2.2 Implementar a função `load_translation_config` para carregar as definições estruturadas do arquivo `translation_config.json`
- [x] 2.3 Atualizar os argumentos de CLI (função `parse_args`) para aceitar a flag `--profile` e ler os parâmetros a partir do arquivo JSON carregado

## 3. Implementação das Estratégias de Tradução

- [x] 3.1 Adaptar a função `translate_text` para aceitar a estratégia de tradução selecionada (`full_document` ou `split_blocks`)
- [x] 3.2 Implementar o fluxo de chamada de API única na estratégia `full_document` enviando o Markdown e glossário integral no prompt de sistema
- [x] 3.3 Implementar limitador de segurança e fallback automático para `split_blocks` se o corpo do arquivo for excessivamente longo
- [x] 3.4 Garantir que o glossário estático fixo no prompt de sistema aproveite a otimização de Prompt Caching da API do DeepSeek

## 4. Validação e Testes

- [x] 4.1 Validar a inicialização do script sem arquivo de configuração (fallback CLI)
- [x] 4.2 Testar a execução do script com `--profile` e `--dry-run` usando chaves fictícias no `.env`
- [x] 4.3 Executar uma verificação de linting e validação de build de produção do Hugo com `hugo --gc --minify`
