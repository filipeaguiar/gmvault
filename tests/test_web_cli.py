import unittest
from unittest.mock import call, patch

import web_cli


class WebCliTests(unittest.TestCase):
    def tearDown(self):
        web_cli.sessions.clear()

    def test_modified_enter_sequences_are_normalized(self):
        self.assertEqual(web_cli.normalize_terminal_input("\x1b[27;5;106~"), "\n")
        self.assertEqual(web_cli.normalize_terminal_input("[27;5;106~"), "\n")
        self.assertEqual(web_cli.normalize_terminal_input("\x1b[106;5u"), "\n")
        self.assertEqual(web_cli.normalize_terminal_input("[106;5u"), "\n")
        self.assertEqual(web_cli.normalize_terminal_input("\x1b[A"), "\x1b[A")

    def test_index_serves_xterm_and_socketio_client(self):
        response = web_cli.app.test_client().get("/")

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("@xterm/xterm", html)
        self.assertIn("cdn.socket.io/4.8.1/socket.io.min.js", html)
        self.assertIn('terminal.onData((data) => socket.emit("pty_input"', html)
        self.assertIn('socket.on("pty_output"', html)

    @patch("web_cli.pty.fork", return_value=(1234, 42))
    def test_start_pty_session_registers_parent_process(self, fork):
        session = web_cli.start_pty_session("client-1")

        self.assertEqual(session, web_cli.PtySession(pid=1234, fd=42))
        self.assertIs(web_cli.sessions["client-1"], session)
        fork.assert_called_once_with()

    @patch("web_cli.stop_pty_session")
    @patch("web_cli.socketio.emit")
    @patch("web_cli.os.read", side_effect=[b"Ol\xc3", b"\xa1", b""])
    def test_reader_decodes_split_utf8_and_emits_to_own_client(
        self, _read, emit, stop
    ):
        session = web_cli.PtySession(pid=1234, fd=42)

        web_cli.read_pty_output("client-1", session)

        output = "".join(
            event.args[1]["output"]
            for event in emit.call_args_list
            if event.args and event.args[0] == "pty_output"
        )
        self.assertEqual(output, "Olá")
        self.assertIn(call("pty_exit", to="client-1"), emit.call_args_list)
        stop.assert_called_once_with("client-1")

    @patch("web_cli.os.waitpid")
    @patch("web_cli.os.kill")
    @patch("web_cli.os.close")
    @patch("web_cli.socketio.start_background_task")
    @patch("web_cli.pty.fork", return_value=(1234, 42))
    def test_socket_forwards_arrow_key_and_resize_to_pty(
        self, _fork, _background, close, kill, waitpid
    ):
        with patch("web_cli.os.write", return_value=3) as write, patch(
            "web_cli.fcntl.ioctl"
        ) as ioctl:
            client = web_cli.socketio.test_client(web_cli.app)
            self.assertTrue(client.is_connected())

            client.emit("pty_input", {"input": "\x1b[A"})
            client.emit("pty_resize", {"cols": 120, "rows": 40})

            write.assert_called_once()
            self.assertEqual(bytes(write.call_args.args[1]), b"\x1b[A")
            ioctl.assert_called_once()
            client.disconnect()

        close.assert_called_once_with(42)
        kill.assert_called_once_with(1234, web_cli.signal.SIGHUP)
        waitpid.assert_called_once_with(1234, web_cli.os.WNOHANG)


if __name__ == "__main__":
    unittest.main()
