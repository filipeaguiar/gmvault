# owlbear-character-extension Specification

## Purpose
TBD - created by archiving change add-owlbear-character-extension. Update Purpose after archive.
## Requirements
### Requirement: The project SHALL publish an installable Owlbear extension
The Hugo deployment SHALL expose a valid Owlbear Rodeo manifest and static extension shell under the configured `/gmvault/` base path. The manifest SHALL declare `manifest_version: 1`, SHALL declare a valid semantic extension version, and SHALL reference the shell, icon, title, width, and height using URLs that resolve correctly on GitHub Pages.

#### Scenario: Extension manifest is requested
- **WHEN** Owlbear Rodeo loads `/gmvault/owlbear-character-sheet/manifest.json`
- **THEN** it SHALL receive a valid manifest with `manifest_version: 1`, a semantic extension version matching the published release, and an action popover that resolves to the published character extension shell.

#### Scenario: Site is built for production
- **WHEN** `hugo --gc --minify` runs
- **THEN** the manifest, shell, JavaScript, CSS, and icon assets SHALL be included in the generated site without requiring a separate deployment.

### Requirement: The extension SHALL list only player-facing characters
The site SHALL generate a machine-readable character catalog containing built character pages whose visibility is `players` or `public`. Draft pages excluded from the current Hugo build and characters with GM or missing visibility SHALL NOT appear in the catalog.

#### Scenario: Player-visible character exists
- **WHEN** a non-draft character has `visibility: players` or `visibility: public`
- **THEN** the catalog SHALL include its title, canonical URL, summary, and optional campaign and image metadata.

#### Scenario: GM character exists
- **WHEN** a character has `visibility: gm`, `visibility: archived`, or no visibility
- **THEN** the catalog SHALL omit that character.

#### Scenario: Catalog is empty
- **WHEN** no eligible character pages are part of the build
- **THEN** the extension SHALL show an empty state without attempting to load an invalid iframe URL.

### Requirement: Players SHALL be able to select and reopen a character
The extension shell SHALL present the eligible character catalog, allow the current user to select a character, and persist the selected URL locally using a key scoped to the current Owlbear player ID when available.

#### Scenario: Player selects a character
- **WHEN** the player chooses a catalog entry
- **THEN** the extension SHALL load that character in its controlled iframe and save the selection locally.

#### Scenario: Player reopens the extension
- **WHEN** a previously saved character still exists in the current catalog
- **THEN** the extension SHALL reopen that character without requiring another selection.

#### Scenario: Saved character no longer exists
- **WHEN** the persisted URL is absent from the current catalog
- **THEN** the extension SHALL discard the stale selection and return to the selector.

#### Scenario: Player changes character
- **WHEN** the player activates the character selector while a sheet is open
- **THEN** the extension SHALL allow a new selection and update the persisted value and iframe.

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

### Requirement: The extension SHALL initialize the Owlbear SDK safely
The extension shell SHALL import a fixed SDK version, wait for `OBR.onReady`, and obtain player identity from `OBR.player`. Failure to initialize the SDK SHALL produce a visible non-fatal state while preserving access to the character selector and readable sheet. Extension-owned channels and protocol messages SHALL use the namespace `io.github.filipeaguiar.character-sheet` and SHALL NOT use the external extension identifier `gm-vault`.

#### Scenario: Owlbear initializes successfully
- **WHEN** the shell runs as an Owlbear extension with a valid `obrref`
- **THEN** it SHALL obtain the current player ID and name and enable Owlbear-dependent integration.

#### Scenario: Shell opens outside Owlbear
- **WHEN** the shell URL is opened in a normal browser without a valid Owlbear context
- **THEN** it SHALL remain usable for character selection and reference viewing while marking Dice+ integration unavailable.

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

### Requirement: The extension SHALL submit valid Dice+ roll requests
For an accepted iframe roll action, the shell SHALL send one message to `dice-plus/roll-request` containing a unique correlated `rollId`, current Owlbear player ID and name, supported roll target, validated dice notation, popup preference, timestamp, and stable source `io.github.filipeaguiar.character-sheet`.

#### Scenario: Player activates an enhanced value
- **WHEN** the iframe requests a valid roll while Dice+ is ready
- **THEN** the shell SHALL send exactly one Dice+ request with all documented required fields and destination `ALL`.

#### Scenario: Iframe attempts to supply player identity
- **WHEN** a message includes page-provided player ID or name
- **THEN** the shell SHALL ignore those identity values and use `OBR.player` data.

#### Scenario: Roll payload is invalid
- **WHEN** notation, target, version, origin, or message shape fails validation
- **THEN** the shell SHALL reject the request without broadcasting to Dice+ and SHALL return a structured error to the requesting iframe when possible.

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

### Requirement: Cross-frame messages SHALL be validated
The shell SHALL accept bridge messages only from the active character iframe, expected character origin, supported protocol version, known message type, and valid payload. Responses SHALL use the exact expected target origin.

#### Scenario: Message comes from another window
- **WHEN** a sibling extension, stale iframe, or unrelated window sends a matching-looking message
- **THEN** the shell SHALL reject it because `event.source` does not equal the active iframe window.

#### Scenario: Message comes from an unexpected origin
- **WHEN** the message origin differs from the selected character URL origin
- **THEN** the shell SHALL reject it without invoking the Owlbear SDK.

### Requirement: The extension SHALL remain lightweight and accessible
The shell SHALL use semantic HTML, keyboard-accessible controls, visible focus, responsive styling, and vanilla JavaScript without a heavy UI framework. Status messages SHALL be exposed to assistive technology.

#### Scenario: Popover has narrow width
- **WHEN** the extension is opened at its configured Owlbear popover width
- **THEN** the selector, status, and character iframe SHALL remain usable without horizontal overflow.

#### Scenario: Integration state changes
- **WHEN** the shell enters loading, ready, or unavailable state
- **THEN** the state SHALL be conveyed through readable text or an appropriate live region and SHALL NOT depend only on color.

#### Scenario: Dice+ completes or rejects a roll
- **WHEN** a pending roll receives a result or error
- **THEN** the shell SHALL clear the correlated pending state while Dice+ remains responsible for displaying the outcome.

