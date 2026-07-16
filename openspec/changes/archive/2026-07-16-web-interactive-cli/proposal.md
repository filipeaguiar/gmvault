## Why

O script `interactive_cli.py` e suas dependências (como `create_character.py` e `edit_character.py`) funcionam muito bem via terminal, mas a usabilidade ficaria muito mais amigável e acessível se houvesse uma interface Web simples. Rodar localmente ou via VPN permite que usuários acessem os fluxos interativos de qualquer dispositivo na rede sem precisar acessar o terminal via SSH.

## What Changes

- Criação de uma interface web simples utilizando um microframework web para Python (ex: Flask ou FastAPI, ou o recurso `http.server` adaptado).
- Como as perguntas da CLI (ex: `ask_choice`, `ask`, `ask_int`) são fortemente síncronas e bloqueantes, a adaptação web precisará interceptar as requisições de entrada/saída (I/O).
- Vamos introduzir um novo script de servidor web (`web_cli.py` ou similar) ou uma ponte WebSocket/HTTP que consiga renderizar o terminal no navegador (ex: usando `xterm.js` via WebSockets) ou transformar os prompts em formulários.
- A opção mais fiel e de menor esforço estrutural é utilizar uma biblioteca que expõe uma aplicação de console no navegador (como WebSockets + xterm.js) ou refatorar o I/O do interactive_cli para ser agnóstico e suportar um front-end web.

## Capabilities

### New Capabilities
- `web-cli-server`: Serviço web para acesso remoto local/VPN às funções da CLI do GM Vault.

### Modified Capabilities
- `interactive-cli`: Possível refatoração para permitir injeção de dependência de `I/O` (Input/Output), separando a lógica de exibição/pergunta do uso estrito de `sys.stdin`/`print`.

## Impact

- Scripts de interação como `create_character.py`, `edit_character.py`, `interactive_cli.py`.
- Adição de possíveis novas dependências no ambiente virtual (ex: `flask`, `fastapi`, `websockets`, ou similar).
