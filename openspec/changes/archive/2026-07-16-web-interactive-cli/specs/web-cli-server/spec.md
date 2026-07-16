## ADDED Requirements

### Requirement: Web CLI Server Launcher
The system SHALL provide a web server script (`web_cli.py`) that serves an HTML interface representing a terminal.

#### Scenario: User visits the server URL
- **WHEN** the user navigates to `http://localhost:5000` (ou porta configurada)
- **THEN** the system serves an HTML page containing an `xterm.js` terminal window
- **THEN** a WebSocket connection is established with the server

### Requirement: PTY Session Management
The system SHALL spawn an instance of `interactive_cli.py` inside a pseudo-terminal (PTY) when a WebSocket client connects.

#### Scenario: Client connects via WebSocket
- **WHEN** the WebSocket connection is opened
- **THEN** the server spawns `python3 interactive_cli.py` in a PTY
- **THEN** the server pipes the PTY standard output to the WebSocket

### Requirement: Bidirectional Communication
The system SHALL forward user keystrokes from the web terminal to the PTY and vice-versa.

#### Scenario: User interacts with the terminal
- **WHEN** the user types characters into the `xterm.js` interface
- **THEN** the WebSocket sends the keystrokes to the server
- **THEN** the server writes the keystrokes to the PTY's file descriptor
- **THEN** the PTY output updates the `xterm.js` display in real-time
