## MODIFIED Requirements

### Requirement: Adventure indexes list simplified sessions
Adventure pages SHALL list direct child and nested session child scene pages.

#### Scenario: Adventure has direct session children
- **WHEN** an adventure page has direct child branch bundles with `kind: session`
- **THEN** the adventure index navigation SHALL collect scenes and display them directly in the scene timeline

#### Scenario: Adventure has legacy sessions section
- **WHEN** an adventure page has legacy sessions under `sessions/<session-slug>/`
- **THEN** the adventure index navigation SHALL collect and display all their scenes directly in the scene timeline
