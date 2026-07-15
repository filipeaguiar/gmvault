## ADDED Requirements

### Requirement: A ficha SHALL expose a versioned iframe bridge
A ficha renderizada pelo Hugo SHALL communicate with the parent `gm-vault` extension through a versioned bridge contract instead of importing the Owlbear Rodeo SDK directly. The contract SHALL support requesting a roll and reporting availability, completion, and failure through validated `postMessage` events. The parent extension SHALL be the component that accesses the Owlbear SDK and Dice+ broadcast channels.

#### Scenario: Ficha runs inside the gm-vault iframe
- **WHEN** `gm-vault` loads a character sheet in its iframe
- **THEN** the sheet SHALL send a versioned request to the parent window and SHALL be able to request a roll without importing `@owlbear-rodeo/sdk`.

#### Scenario: Ficha runs outside Owlbear Rodeo
- **WHEN** a character sheet is opened without a `gm-vault` bridge
- **THEN** the sheet SHALL remain readable and SHALL show roll actions as unavailable without throwing an uncaught integration error.

### Requirement: The host SHALL verify Dice+ availability
The `gm-vault` host SHALL check Dice+ availability through the `dice-plus/isReady` broadcast channel before sending roll requests. Each check SHALL include a unique `requestId` and SHALL stop waiting after a bounded timeout.

#### Scenario: Dice+ responds to the readiness check
- **WHEN** the host sends a readiness request with a unique `requestId`
- **THEN** it SHALL mark Dice+ available only after receiving a response on `dice-plus/isReady` containing the same `requestId` and a positive readiness value.

#### Scenario: Dice+ does not respond
- **WHEN** no matching readiness response arrives before the timeout
- **THEN** the host SHALL report Dice+ unavailable and SHALL not send a roll request.

### Requirement: The host SHALL send validated roll requests through Dice+
For an enabled sheet action, the host SHALL send a message to `dice-plus/roll-request` with a unique `rollId`, the Owlbear player identity obtained by the host, a player name, a supported `rollTarget`, a validated `diceNotation`, a boolean `showResults`, a timestamp, and the stable `gm-vault` extension identifier as `source`. The message SHALL be sent with the Owlbear broadcast destination required for the selected roll target, using the Dice+ documented channel contract.

#### Scenario: Character action requests a roll
- **WHEN** a player activates an action with a valid structured dice notation and Dice+ is available
- **THEN** the host SHALL send exactly one correlated request containing all required Dice+ fields and SHALL expose the generated `rollId` to the sheet controller.

#### Scenario: Action has no valid notation
- **WHEN** a character action has missing, malformed, or unsupported dice notation
- **THEN** the sheet SHALL not send a Dice+ request and SHALL present the action as unavailable or invalid.

#### Scenario: Request contains page-provided identity
- **WHEN** the sheet asks the host to roll
- **THEN** the host SHALL use the current Owlbear player ID and name rather than trusting a player identity supplied by the static page.

### Requirement: Results and errors SHALL be correlated with the originating action
The host SHALL listen on the source-specific `{source}/roll-result` and `{source}/roll-error` channels documented by Dice+. It SHALL match messages by `rollId`, deliver only the matching event to the requesting sheet context, and ignore unknown or already completed identifiers.

#### Scenario: Dice+ returns a result
- **WHEN** a result arrives with a pending `rollId`
- **THEN** the sheet SHALL receive the total value and SHALL be able to display the documented roll summary and grouped dice results.

#### Scenario: Dice+ returns an error
- **WHEN** an error arrives with a pending `rollId`
- **THEN** the sheet SHALL leave the rolling state, display a recoverable error state, and retain the action for another attempt.

#### Scenario: Result belongs to another request
- **WHEN** a result or error arrives with an unknown `rollId`
- **THEN** the host SHALL ignore it and SHALL not update any visible action.

### Requirement: Roll actions SHALL expose accessible progressive states
The sheet SHALL render controls only for actions with structured roll metadata and SHALL expose at least unavailable, ready, rolling, completed, and error states. It SHALL update the action without blocking access to the rest of the character sheet, and result values SHALL be inserted as text rather than interpreted as HTML.

#### Scenario: Roll is in progress
- **WHEN** a valid action is activated
- **THEN** the control SHALL indicate that the roll is in progress and SHALL prevent duplicate activation for the same action until completion, timeout, or error.

#### Scenario: Roll completes
- **WHEN** a matching Dice+ result is delivered
- **THEN** the control SHALL show the final total and a readable summary while preserving the action label and its original character-sheet context.

#### Scenario: Roll times out
- **WHEN** a pending roll exceeds the configured response timeout
- **THEN** the control SHALL return to a retryable state and SHALL show that no result was received.

### Requirement: The bridge SHALL validate iframe messages and clean up resources
The `gm-vault` parent SHALL validate the iframe message origin, `event.source`, version, type, payload shape, and allowed action fields before forwarding it to Dice+. Responses to the iframe SHALL use the exact configured target origin. The host SHALL remove broadcast listeners, message listeners, pending timers, and completed roll entries when the extension surface is disposed.

#### Scenario: Invalid iframe message arrives
- **WHEN** a message has an untrusted origin, unexpected source window, unsupported version, unknown type, or invalid payload
- **THEN** the host SHALL reject it without sending a Dice+ broadcast message.

#### Scenario: Extension surface is disposed
- **WHEN** the relevant `gm-vault` surface closes or is reloaded
- **THEN** the host SHALL unsubscribe from the Dice+ channels and clear pending requests and timers.

### Requirement: The integration SHALL remain optional for static builds
The Hugo build SHALL not require the Owlbear SDK or Dice+ to generate or render character sheets. The integration assets SHALL degrade safely when the host bridge is unavailable, and existing non-roll character content SHALL remain usable.

#### Scenario: Hugo production build runs without SDK dependencies
- **WHEN** the project runs its normal Hugo build outside an Owlbear environment
- **THEN** the build SHALL complete without resolving `@owlbear-rodeo/sdk` and SHALL render character sheets without integration runtime errors.

#### Scenario: Dice+ is not installed in the room
- **WHEN** a sheet is opened in Owlbear but the readiness check fails
- **THEN** the sheet SHALL retain all character information and SHALL mark Dice+ actions unavailable rather than blocking the page.
