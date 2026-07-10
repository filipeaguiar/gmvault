# campaign-hierarchy-simplification Specification

## Purpose
TBD - created by archiving change simplify-campaign-page-hierarchy. Update Purpose after archive.
## Requirements
### Requirement: Simplified campaign hierarchy is canonical
New campaign adventure content SHALL use a simplified physical hierarchy that preserves `adventure → session → scene` semantics without mandatory `sessions/` and `scenes/` collection directories.

#### Scenario: New adventure has sessions
- **WHEN** a new adventure is created under `content/campaigns/<campaign-slug>/adventures/<adventure-slug>/`
- **THEN** session pages SHALL be created as direct child branch bundles under the adventure directory

#### Scenario: New session has scenes
- **WHEN** a new session is created as `adventures/<adventure-slug>/<session-slug>/_index.md`
- **THEN** scene pages SHALL be created directly inside that session directory

### Requirement: Legacy campaign hierarchy remains readable
The site SHALL continue to render and export content that uses the legacy `sessions/<session>/scenes/<scene>.md` structure.

#### Scenario: Legacy session exists
- **WHEN** an adventure contains `sessions/<session-slug>/_index.md` with session metadata
- **THEN** layouts and exports SHALL still treat that page as a session

#### Scenario: Legacy scene exists
- **WHEN** a session contains `scenes/<scene-slug>.md` with scene metadata
- **THEN** layouts and exports SHALL still treat that page as a scene

### Requirement: Kind metadata drives hierarchy semantics
Campaign hierarchy detection SHALL prefer page `kind` metadata over directory names when identifying adventures, sessions, and scenes.

#### Scenario: Direct child session exists
- **WHEN** an adventure has a direct child branch bundle with `kind: session`
- **THEN** that child SHALL be treated as a session even without a `sessions/` parent directory

#### Scenario: Direct child scene exists
- **WHEN** a session has a direct child page with `kind: scene`
- **THEN** that child SHALL be treated as a scene even without a `scenes/` parent directory

### Requirement: Collection index pages are optional in simplified hierarchy
The simplified hierarchy SHALL NOT require `sessions/_index.md` or `scenes/_index.md` for new content.

#### Scenario: Adventure has no sessions index
- **WHEN** an adventure uses direct child session bundles and has no `sessions/_index.md`
- **THEN** the adventure page SHALL still list or expose its sessions

#### Scenario: Session has no scenes index
- **WHEN** a session uses direct child scene pages and has no `scenes/_index.md`
- **THEN** the session page SHALL still list or expose its scenes

