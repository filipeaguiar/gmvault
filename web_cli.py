#!/usr/bin/env python3
"""Expõe a CLI interativa do GM Vault em um terminal web local."""

from __future__ import annotations

import argparse
import codecs
import fcntl
import os
import pty
import re
import signal
import struct
import sys
import termios
import threading
from dataclasses import dataclass, field
from pathlib import Path

from flask import Flask, render_template, request
from flask_socketio import SocketIO


PROJECT_ROOT = Path(__file__).resolve().parent
CLI_SCRIPT = PROJECT_ROOT / "interactive_cli.py"
MODIFY_OTHER_KEYS_PATTERN = re.compile(r"(?:\x1b)?\[27;(\d+);(\d+)~")
CSI_U_PATTERN = re.compile(r"(?:\x1b)?\[(\d+);(\d+)u")


@dataclass
class PtySession:
    """Processo e descritor PTY pertencentes a um cliente Socket.IO."""

    pid: int
    fd: int
    write_lock: threading.Lock = field(
        default_factory=threading.Lock, repr=False, compare=False
    )


sessions: dict[str, PtySession] = {}
sessions_lock = threading.RLock()

app = Flask(__name__, template_folder=str(PROJECT_ROOT / "templates"))
app.config["SECRET_KEY"] = "gmvault-local-web-cli"
socketio = SocketIO(app, async_mode="threading")


@app.get("/")
def index():
    """Renderiza o terminal web."""
    return render_template("web_cli.html")


def start_pty_session(sid: str) -> PtySession:
    """Inicia ``interactive_cli.py`` em um pseudo-terminal Unix."""
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(PROJECT_ROOT)
        environment = os.environ.copy()
        environment.setdefault("TERM", "xterm-256color")
        environment["PYTHONUNBUFFERED"] = "1"
        os.execvpe(
            sys.executable,
            [sys.executable, str(CLI_SCRIPT)],
            environment,
        )

    session = PtySession(pid=pid, fd=fd)
    with sessions_lock:
        sessions[sid] = session
    return session


def read_pty_output(sid: str, session: PtySession) -> None:
    """Encaminha continuamente a saída UTF-8 do PTY para seu cliente."""
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
    try:
        while True:
            try:
                chunk = os.read(session.fd, 4096)
            except OSError:
                break
            if not chunk:
                break
            output = decoder.decode(chunk)
            if output:
                socketio.emit("pty_output", {"output": output}, to=sid)
        remaining = decoder.decode(b"", final=True)
        if remaining:
            socketio.emit("pty_output", {"output": remaining}, to=sid)
    finally:
        socketio.emit("pty_exit", to=sid)
        stop_pty_session(sid)


def stop_pty_session(sid: str) -> None:
    """Fecha o PTY e solicita o encerramento do processo filho."""
    with sessions_lock:
        session = sessions.pop(sid, None)
    if session is None:
        return
    try:
        os.close(session.fd)
    except OSError:
        pass
    try:
        os.kill(session.pid, signal.SIGHUP)
    except ProcessLookupError:
        pass
    try:
        os.waitpid(session.pid, os.WNOHANG)
    except ChildProcessError:
        pass


@socketio.on("connect")
def handle_connect(_auth=None):
    """Cria uma sessão PTY exclusiva para o cliente conectado."""
    sid = request.sid
    socketio.emit("pty_output", {"output": "Iniciando sessão…\r\n"}, to=sid)
    session = start_pty_session(sid)
    socketio.start_background_task(read_pty_output, sid, session)


@socketio.on("disconnect")
def handle_disconnect(reason=None):
    """Finaliza os recursos associados ao cliente desconectado."""
    del reason
    stop_pty_session(request.sid)


def decode_modified_key(match: re.Match[str]) -> str:
    """Converte modifyOtherKeys/CSI-u para o caractere de controle original."""
    modifier = int(match.group(1)) - 1
    codepoint = int(match.group(2))
    try:
        character = chr(codepoint)
    except ValueError:
        return match.group(0)

    if modifier & 4:  # Ctrl
        upper = character.upper()
        if "@" <= upper <= "_":
            character = chr(ord(upper) & 0x1F)
        elif upper == "?":
            character = "\x7f"
    if modifier & 2:  # Alt
        character = "\x1b" + character
    return character


def normalize_terminal_input(value: str) -> str:
    """Normaliza protocolos de teclado habilitados por terminais avançados."""
    value = MODIFY_OTHER_KEYS_PATTERN.sub(decode_modified_key, value)

    def decode_csi_u(match: re.Match[str]) -> str:
        reordered = f"\x1b[27;{match.group(2)};{match.group(1)}~"
        nested = MODIFY_OTHER_KEYS_PATTERN.fullmatch(reordered)
        return decode_modified_key(nested) if nested else match.group(0)

    return CSI_U_PATTERN.sub(decode_csi_u, value)


@socketio.on("pty_input")
def handle_pty_input(payload):
    """Escreve teclas UTF-8, inclusive sequências ANSI, no PTY do cliente."""
    value = payload.get("input") if isinstance(payload, dict) else payload
    if not isinstance(value, str) or not value:
        return
    value = normalize_terminal_input(value)
    encoded = value.encode("utf-8")
    if len(encoded) > 65536:
        return
    with sessions_lock:
        session = sessions.get(request.sid)
    if session is None:
        return
    try:
        with session.write_lock:
            view = memoryview(encoded)
            while view:
                written = os.write(session.fd, view)
                view = view[written:]
    except OSError:
        stop_pty_session(request.sid)


@socketio.on("pty_resize")
def handle_pty_resize(payload):
    """Mantém as dimensões do PTY sincronizadas com o xterm.js."""
    if not isinstance(payload, dict):
        return
    try:
        cols = max(2, min(500, int(payload.get("cols", 80))))
        rows = max(2, min(300, int(payload.get("rows", 24))))
    except (TypeError, ValueError):
        return
    with sessions_lock:
        session = sessions.get(request.sid)
    if session is None:
        return
    try:
        size = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(session.fd, termios.TIOCSWINSZ, size)
    except OSError:
        stop_pty_session(request.sid)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Terminal web para a CLI do GM Vault.")
    parser.add_argument("--host", default="127.0.0.1", help="Endereço de escuta.")
    parser.add_argument("--port", type=int, default=5000, help="Porta HTTP.")
    parser.add_argument("--debug", action="store_true", help="Ativa o modo de depuração.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    socketio.run(
        app,
        host=args.host,
        port=args.port,
        debug=args.debug,
        allow_unsafe_werkzeug=True,
    )


if __name__ == "__main__":
    main()
