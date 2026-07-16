## Context

Atualmente o script `interactive_cli.py` é a porta de entrada para usar as ferramentas de gerenciamento do GM Vault (criação e edição de personagens, traduções, etc.). O usuário deseja poder acessar isso via navegador em sua rede local ou VPN, eliminando a necessidade de logar via SSH ou abrir um terminal nativo.

## Goals / Non-Goals

**Goals:**
- Criar um servidor web local simples (`web_cli.py`).
- O servidor deve renderizar uma interface web utilizando `xterm.js` para simular o terminal no navegador.
- O servidor deve rodar o script `interactive_cli.py` num pseudo-terminal (PTY) em background e encaminhar a entrada/saída para o `xterm.js` via WebSockets.
- Permitir que a interface web seja acessada via rede local/VPN.

**Non-Goals:**
- Não iremos refatorar o `interactive_cli.py` nem reimplementar os menus em HTML nativo. O emulador de terminal web (xterm.js) é suficiente e provê 100% de compatibilidade sem alterar as regras de negócio ou as funções de CLI (`ask_choice`, etc).
- Não haverá sistema de autenticação pesado; o foco é uso em VPN/Localhost seguro.

## Decisions

- **Arquitetura Web**: Usaremos o microframework **Flask** junto com **Flask-SocketIO** para o servidor e gerenciamento de WebSockets.
- **Integração PTY**: Utilizaremos a biblioteca embutida `pty` do Python para spawnar o `interactive_cli.py`. Isso garante que as cores e a detecção de console iterativo do Inquirer/Rich funcionem normalmente, enganando o script para achar que está num terminal real.
- **Frontend**: Usaremos CDN para importar o `xterm.js` e `xterm-addon-fit.js` em um template HTML limpo.

## Risks / Trade-offs

- **Risk**: Suporte a PTY nativo é restrito a sistemas Unix/Linux.
- **Mitigation**: Como o GM Vault e os ambientes alvo (VPN/Localhost do usuário que usa linux) suportam, o `pty` python resolverá o caso de uso.
- **Risk**: As dependências do Flask/SocketIO adicionam peso ao projeto.
- **Mitigation**: Elas podem ser adicionadas num `requirements.txt` ou instaladas no `.venv`.
