# Character Level Up Specification

## Purpose
Define deterministic local character advancement for XPHB classes while preserving canonical compendium references and explicit player choices.

## Requirements
### Requirement: Local character level-up plan
The system SHALL build a level-up plan for a local character using the selected XPHB class, subclass, current class level, and target next level before changing the character file.

#### Scenario: Plan identifies new class features
- **WHEN** a character advances from level N to N+1 in an XPHB class
- **THEN** the plan SHALL identify class features whose acquisition level is N+1 and reference their canonical local rule pages

#### Scenario: Plan identifies subclass features
- **WHEN** the character has an XPHB-compatible subclass with a feature at the target level
- **THEN** the plan SHALL include that subclass feature without including unrelated subclasses

### Requirement: Level-up applies deterministic character state
The system SHALL update deterministic character state only after the user confirms the level-up plan.

#### Scenario: Confirmed level-up updates core state
- **WHEN** the user confirms a valid plan
- **THEN** the system SHALL update the class level, total level, proficiency bonus when applicable, hit points according to the selected hit-point result, and derived spell-slot state

#### Scenario: Confirmed level-up adds feature references without duplicates
- **WHEN** a target-level feature resolves to a local compendium rule
- **THEN** the system SHALL add its reference and operational action entry when applicable without duplicating an existing entry

### Requirement: Level-up requires explicit player choices
The system SHALL not invent choices that are not deterministically represented by the class data.

#### Scenario: Target level grants an optional choice
- **WHEN** the target level grants a feat, spell, invocation, maneuver, attribute increase, or comparable selectable option
- **THEN** the system SHALL prompt for a choice or report a pending choice before confirmation

#### Scenario: User cancels a pending choice
- **WHEN** the user cancels level-up before confirming all required choices
- **THEN** the character Markdown file SHALL remain unchanged

### Requirement: Level-up applies Expertise choices
The system SHALL require the user to select two distinct eligible skills when the target level grants the class feature `Expertise`.

#### Scenario: Target level grants Expertise
- **WHEN** the level-up plan includes the `Expertise` class feature
- **THEN** the system SHALL present only proficient skills that do not already have Expertise as eligible options
- **THEN** the system SHALL require two distinct selections before level-up confirmation

#### Scenario: Expertise choices are confirmed
- **WHEN** the user confirms a valid level-up with two Expertise selections
- **THEN** the system SHALL mark both selected skills with `expertise: true`
- **THEN** the system SHALL recalculate each selected skill bonus using twice the current proficiency bonus

#### Scenario: Expertise cannot be selected
- **WHEN** fewer than two eligible proficient skills are available or the user cancels the required selection
- **THEN** the system SHALL report that Expertise remains pending
- **THEN** the character Markdown file SHALL remain unchanged

### Requirement: Level-up preserves legacy and editorial state
The system SHALL preserve existing manual fields, unresolved references, and Markdown body content during level-up.

#### Scenario: Legacy character has unrelated operational fields
- **WHEN** a valid legacy character is leveled up
- **THEN** fields unrelated to the level-up plan and the Markdown body SHALL remain unchanged
