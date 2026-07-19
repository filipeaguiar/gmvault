## ADDED Requirements

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
