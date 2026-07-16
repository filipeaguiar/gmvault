## ADDED Requirements

### Requirement: Character roll values support progressive enhancement
The character sheet SHALL render eligible saving throw bonuses, skill bonuses, attack formulas, damage formulas, and explicitly configured action formulas as readable text with structured roll metadata. The values SHALL remain non-interactive reference content by default and SHALL become controls only after a validated extension bridge confirms Dice+ availability.

#### Scenario: Character sheet opens in a normal browser
- **WHEN** no compatible Owlbear character extension bridge is available
- **THEN** roll bonuses and formulas SHALL remain readable text and SHALL NOT display a separate roll button or unavailable interactive control.

#### Scenario: Character sheet opens with Dice+ ready
- **WHEN** the controlled extension completes a valid bridge handshake and confirms Dice+ readiness
- **THEN** eligible values SHALL become keyboard-accessible controls while preserving the same visible number or formula as their label.

#### Scenario: Action has no structured formula
- **WHEN** an action contains descriptive rules but no explicit valid dice notation
- **THEN** the sheet SHALL keep that action as reference content and SHALL NOT infer a roll from prose.

### Requirement: Enhanced roll controls use the visible value as the action
The sheet SHALL use the displayed bonus or dice formula itself as the enhanced roll control and SHALL NOT add a separate textual button labelled “Rolar”. Each enhanced control SHALL expose an accessible label describing the associated skill, save, attack, damage, or action.

#### Scenario: Skill bonus is enhanced
- **WHEN** a skill with bonus `+7` is enabled by the extension bridge
- **THEN** the visible `+7` SHALL be the clickable and keyboard-focusable control with an accessible name identifying the skill test.

#### Scenario: Weapon formulas are enhanced
- **WHEN** a weapon has explicit attack and damage formulas and Dice+ is available
- **THEN** each displayed formula SHALL independently trigger its corresponding attack or damage roll without adding a separate roll button.

### Requirement: Character roll actions expose progressive states
An enhanced roll value SHALL expose ready, rolling, completed, error, and timeout behavior without blocking navigation or reference content. Result and error messages SHALL be inserted as text and associated with the originating value.

#### Scenario: Roll starts
- **WHEN** the player activates an enhanced value
- **THEN** that value SHALL indicate a pending roll and SHALL prevent duplicate activation until result, error, or timeout.

#### Scenario: Roll succeeds
- **WHEN** a matching Dice+ result returns through the extension bridge
- **THEN** the sheet SHALL show the total and readable summary near the originating value and SHALL permit a later reroll.

#### Scenario: Roll fails or times out
- **WHEN** a matching error returns or the request exceeds its timeout
- **THEN** the sheet SHALL show a retryable error near the originating value while keeping the rest of the sheet usable.

### Requirement: Character bridge messages are versioned and correlated
The character client SHALL communicate with the parent extension using a versioned message envelope and unique request and roll identifiers. It SHALL accept responses only from the parent window, expected origin, supported protocol version, and matching pending identifier.

#### Scenario: Matching result arrives
- **WHEN** the parent sends a valid result for a pending request and roll ID
- **THEN** the sheet SHALL update only the action that originated that request.

#### Scenario: Unrelated message arrives
- **WHEN** the sheet receives a message from another origin, another window, an unsupported version, or an unknown identifier
- **THEN** it SHALL ignore the message without changing any roll state.

#### Scenario: Sheet unloads
- **WHEN** the character page is unloaded or its controller is destroyed
- **THEN** it SHALL remove message listeners, clear timers, and reject or discard pending requests safely.
