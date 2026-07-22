## MODIFIED Requirements

### Requirement: Character roll values support progressive enhancement
The character sheet SHALL render eligible saving throw bonuses, skill bonuses, attack formulas, damage formulas, and explicitly configured action formulas as readable text with structured roll metadata. The values SHALL remain non-interactive reference content by default and SHALL become controls only after a validated Owlbear extension bridge confirms Dice+ availability. Character sheet pages SHALL use exactly one enhancement path for those values in Owlbear-supported sheets and SHALL NOT activate a second generic roll controller over the same metadata.

#### Scenario: Character sheet opens in a normal browser
- **WHEN** no compatible Owlbear character extension bridge is available
- **THEN** roll bonuses and formulas SHALL remain readable text and SHALL NOT display a separate roll button or unavailable interactive control

#### Scenario: Character sheet opens with Dice+ ready
- **WHEN** the controlled extension completes a valid bridge handshake and confirms Dice+ readiness
- **THEN** eligible values SHALL become keyboard-accessible controls while preserving the same visible number or formula as their label

#### Scenario: Generic site roll enhancement is also present on the page shell
- **WHEN** a character page is rendered for the Owlbear-supported sheet flow
- **THEN** the page SHALL ensure that only the validated Owlbear enhancement path can activate roll interaction for its structured roll metadata

#### Scenario: Action has no structured formula
- **WHEN** an action contains descriptive rules but no explicit valid dice notation
- **THEN** the sheet SHALL keep that action as reference content and SHALL NOT infer a roll from prose

### Requirement: Character bridge messages are versioned and correlated
The character client SHALL communicate with the parent extension using a versioned message envelope and unique request and roll identifiers. It SHALL accept responses only from the parent window, expected origin, supported protocol version, and matching pending identifier, and SHALL discard stale completions after a timeout or teardown.

#### Scenario: Matching result arrives
- **WHEN** the parent sends a valid result for a pending request and roll ID
- **THEN** the sheet SHALL clear the pending state only from the action that originated that request

#### Scenario: Unrelated message arrives
- **WHEN** the sheet receives a message from another origin, another window, an unsupported version, or an unknown identifier
- **THEN** it SHALL ignore the message without changing any roll state

#### Scenario: Stale result arrives after timeout
- **WHEN** the sheet has already cleared a pending request because of timeout and later receives a result or error for that stale request
- **THEN** it SHALL ignore the message without reviving pending state or altering the current control state

#### Scenario: Sheet unloads
- **WHEN** the character page is unloaded or its controller is destroyed
- **THEN** it SHALL remove message listeners, clear timers, and reject or discard pending requests safely
