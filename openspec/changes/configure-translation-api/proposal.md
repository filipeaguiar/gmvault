## Why

O processo de tradução atual do script `translate_drafts.py` está acoplado a um fluxo bloco a bloco e configurações fixas de modelo local, o que gera alta latência de rede e perda de contexto global ao utilizar APIs de LLMs mais potentes como o DeepSeek. Além disso, as chaves de API e URLs não estão devidamente isoladas de forma segura em variáveis de ambiente, aumentando o risco de vazamento de credenciais no repositório público do Git.

## What Changes

- **Isolamento de Segredos**: Suporte a variáveis de ambiente locais através de um arquivo `.env` para armazenamento seguro de chaves privadas (ex: `DEEPSEEK_API_KEY`, `OPENAI_API_KEY`).
- **Prevenção de Vazamento**: Atualização do arquivo `.gitignore` para ignorar os arquivos `.env` e `translation_config.json`.
- **Perfis de Tradução Flexíveis**: Introdução de um arquivo `translation_config.json` para definir perfis de tradução estruturados (URL base, modelo, temperatura, timeout, nome da variável de ambiente para a chave de API e estratégia).
- **Controle de Estratégia de Tradução**: Suporte a duas estratégias de tradução no script `translate_drafts.py`:
  - `full_document`: Envio do documento completo em uma única chamada de API (otimizada para LLMs potentes como DeepSeek, reduzindo latência e melhorando a coesão do texto e consistência gramatical).
  - `split_blocks`: Fatiamento bloco a bloco (estratégia legada, mantida para modelos menores e locais sem suporte eficiente a contextos longos ou caching).
- **Template de Exemplo**: Criação de `translation_config.json.example` como modelo de configuração a ser copiado localmente pelo usuário.

## Capabilities

### New Capabilities
- `translation-profiles-and-strategies`: Mapeamento de perfis de tradução externos e locais (DeepSeek API, OpenAI-compatible e locais), permitindo alternar de maneira flexível entre estratégias de tradução (documento completo vs fragmentado) e ler segredos de forma segura.

### Modified Capabilities
<!-- Nenhuma especificação de funcionalidade existente alterada de forma estrutural (apenas implementação) -->

## Impact

- **Segurança**: Prevenção de vazamento de chaves com o `.gitignore` atualizado e uso de `.env`.
- **Desempenho**: Redução drástica da latência de tradução ao processar documentos inteiros em vez de parágrafo por parágrafo com a API do DeepSeek.
- **Arquivos Afetados**:
  - `translate_drafts.py` (lógica principal de tradução e carregamento de configurações)
  - `.gitignore` (inclusão de `.env` e `translation_config.json`)
  - `requirements.txt` (opcional: adição do `python-dotenv` ou parsing manual de `.env`)
  - Criação do template `translation_config.json.example`
