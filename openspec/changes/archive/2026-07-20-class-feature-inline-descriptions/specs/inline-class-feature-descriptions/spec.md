## ADDED Requirements

### Requirement: Class progression includes feature descriptions
The class page SHALL render the canonical descriptive content of each resolvable feature referenced under a class level.

#### Scenario: Referenced feature is available
- **WHEN** a class level contains a link to a readable feature page
- **THEN** the class page SHALL display the localized feature title and rendered feature description beneath that level

#### Scenario: Referenced feature is unavailable
- **WHEN** a class level contains a link that cannot be resolved to a readable page
- **THEN** the class page SHALL render a safe fallback with the feature link label or internal path and SHALL complete the build

### Requirement: Subclass pages include subclass feature descriptions
The subclass page SHALL render descriptive content for its referenced subclass features using the same presentation model as class pages.

#### Scenario: Player compares subclass features
- **WHEN** a player opens a subclass page
- **THEN** each referenced subclass feature SHALL be visible in its level context without requiring navigation to the feature page

### Requirement: Inline descriptions preserve visibility boundaries
The layout SHALL not embed or link a GM-visible feature in a player-visible or public class or subclass page.

#### Scenario: Feature has GM visibility
- **WHEN** a player-visible class page references a GM-visible feature
- **THEN** the feature SHALL be omitted from the inline description and generated navigation
