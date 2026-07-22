## MODIFIED Requirements

### Requirement: The extension SHALL control the character iframe lifecycle
The shell SHALL create or reuse one iframe for the selected Hugo character URL, calculate the expected origin, and bind the Dice+ bridge to that exact iframe window. It SHALL remove listeners and pending operations before replacing the selected page or unloading, and SHALL treat any result or error that arrives after unbind as an orphaned no-op instead of applying it to a new sheet state.

#### Scenario: Character iframe loads
- **WHEN** a selected character page finishes loading
- **THEN** the shell SHALL register a versioned message listener associated with that iframe window and origin

#### Scenario: Character changes
- **WHEN** the selected character URL changes
- **THEN** the shell SHALL destroy the previous bridge state before binding the new iframe document

#### Scenario: Late result arrives after iframe replacement
- **WHEN** Dice+ returns a result or error for a roll whose iframe binding was already removed
- **THEN** the shell SHALL ignore that message without mutating the newly bound iframe state or reviving any prior pending state

#### Scenario: Extension closes
- **WHEN** the Owlbear popover unloads
- **THEN** the shell SHALL unsubscribe from Dice+ channels and clear message listeners, timers, and pending roll correlations

### Requirement: The extension SHALL verify Dice+ readiness
Before enabling roll interactions, the shell SHALL send a request with a unique `requestId` and timestamp to `dice-plus/isReady`, listen for a matching response with `ready: true`, and stop waiting after a bounded timeout. While the active iframe remains open, the shell SHALL retry readiness checks after timeout and SHALL notify the iframe whenever readiness transitions between unavailable and available.

#### Scenario: Dice+ responds ready
- **WHEN** a matching `ready: true` response arrives before timeout
- **THEN** the shell SHALL notify the character iframe that roll enhancement is available

#### Scenario: Dice+ request is echoed without readiness
- **WHEN** the shell receives its own readiness request or another message lacking `ready: true`
- **THEN** it SHALL ignore that message and continue waiting for a valid response

#### Scenario: Dice+ is absent temporarily
- **WHEN** no matching ready response arrives before timeout but the iframe remains active
- **THEN** the shell SHALL keep the sheet in reference-only mode and schedule another readiness probe without blocking the content

#### Scenario: Dice+ becomes available after a retry
- **WHEN** a later readiness probe receives a valid `ready: true` response for the active iframe
- **THEN** the shell SHALL transition the sheet from reference-only mode to interactive mode without requiring a character reselection

### Requirement: Dice+ results SHALL return to the correct sheet action
The shell SHALL subscribe once to `io.github.filipeaguiar.character-sheet/roll-result` and `io.github.filipeaguiar.character-sheet/roll-error`, correlate messages by `rollId`, and send the result or error only to the iframe request that created the pending roll. A completed, timed-out, or discarded roll ID SHALL NOT be applied again if Dice+ later emits another message for that ID.

#### Scenario: Dice+ completes a roll
- **WHEN** a result arrives for a pending `rollId`
- **THEN** the shell SHALL return total, summary, and grouped dice data to the originating iframe request and remove the pending correlation

#### Scenario: Dice+ reports an error
- **WHEN** an error arrives for a pending `rollId`
- **THEN** the shell SHALL return a retryable error to the originating sheet action and remove the pending correlation

#### Scenario: Unknown result arrives
- **WHEN** a result or error contains an unknown or completed `rollId`
- **THEN** the shell SHALL ignore it without modifying the visible sheet

#### Scenario: Roll response times out
- **WHEN** Dice+ does not answer a submitted roll within the configured timeout
- **THEN** the shell SHALL remove the pending entry and notify the sheet that the action may be retried

#### Scenario: Delayed duplicate response arrives after timeout
- **WHEN** Dice+ later emits a result or error for the same timed-out `rollId`
- **THEN** the shell SHALL ignore the delayed message and SHALL NOT change the ready state of any current sheet control
