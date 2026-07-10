## ADDED Requirements

### Requirement: Adventure indexes list simplified sessions
Adventure pages SHALL list direct child session pages when using the simplified hierarchy.

#### Scenario: Adventure has direct session children
- **WHEN** an adventure page has direct child branch bundles with `kind: session`
- **THEN** the adventure index navigation SHALL display those sessions as navigable children

#### Scenario: Adventure has legacy sessions section
- **WHEN** an adventure page has legacy sessions under `sessions/<session-slug>/`
- **THEN** the adventure index navigation SHALL continue to display those sessions

### Requirement: Session indexes list simplified scenes
Session pages SHALL list direct child scene pages when using the simplified hierarchy.

#### Scenario: Session has direct scene children
- **WHEN** a session page has direct child pages with `kind: scene`
- **THEN** the session index navigation SHALL display those scenes as navigable children

#### Scenario: Session has legacy scenes section
- **WHEN** a session page has legacy scenes under `scenes/<scene-slug>.md`
- **THEN** the session index navigation SHALL continue to display those scenes
