## 1. Configuração e Dependências

- [x] 1.1 Adicionar dependências no ambiente virtual (Flask, Flask-SocketIO)
- [x] 1.2 Criar um arquivo requirements extra caso necessário ou documentar as dependências (ex: `requirements-web.txt`).

## 2. Servidor Base e Frontend

- [x] 2.1 Criar o arquivo `web_cli.py` configurando a aplicação Flask e inicializando SocketIO.
- [x] 2.2 Criar o template HTML (ex: `templates/index.html`) importando a CDN do `xterm.js` e inicializando o terminal no frontend.
- [x] 2.3 Implementar o websocket do lado do cliente para enviar input e receber a resposta do PTY.

## 3. Lógica de PTY Backend

- [x] 3.1 Implementar a conexão SocketIO no `web_cli.py`.
- [x] 3.2 Usar o módulo `pty` e `os.forkpty` (ou `subprocess` adaptado) para inicializar `python3 interactive_cli.py`.
- [x] 3.3 Criar uma thread que lê do file descriptor do PTY e faz broadcast via socketIO para o frontend.
- [x] 3.4 Conectar o canal de recebimento do socketIO para escrever no file descriptor do PTY, lidando adequadamente com encoding (UTF-8).

## 4. Testes Locais

- [x] 4.1 Executar o servidor e testar se a formatação (Inquirer/Rich) renderiza corretamente no xterm.
- [x] 4.2 Validar o encaminhamento das setas pelo terminal web; manter a seleção numérica dos menus existentes, sem navegação por setas, conforme decisão de escopo.
