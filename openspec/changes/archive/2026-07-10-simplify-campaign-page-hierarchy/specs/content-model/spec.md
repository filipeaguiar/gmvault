## MODIFIED Requirements

### Requirement: Campaign hierarchy is campaign adventure session scene
Campaign content SHALL be organized under `content/campaigns/<campaign-slug>/` with adventures, sessions, and scenes forming the operational play hierarchy. The canonical physical structure for new content SHALL place session branch bundles directly under their adventure and scene pages directly under their session, while legacy `sessions/` and `scenes/` collection directories remain supported for existing content.

#### Scenario: Campaign page exists
- **WHEN** a campaign `_index.md` exists
- **THEN** it SHALL act as the campaign landing page and expose campaign overview content plus links or cards for journal, characters, NPCs, locations, factions, handouts, and adventures when present

#### Scenario: Adventure pages exist
- **WHEN** an adventure exists under `adventures/<adventure-slug>/`
- **THEN** it SHALL be represented by an `_index.md` page and may contain direct child session branch bundles

#### Scenario: Simplified session pages exist
- **WHEN** a session exists under `adventures/<adventure-slug>/<session-slug>/_index.md`
- **THEN** it SHALL be treated as a session page and may contain direct child scene pages

#### Scenario: Simplified scene pages exist
- **WHEN** a scene exists under `adventures/<adventure-slug>/<session-slug>/<scene-slug>.md`
- **THEN** it SHALL be treated as a scene page with operational preparation content for play

#### Scenario: Legacy session pages exist
- **WHEN** a session exists under `adventures/<adventure-slug>/sessions/<session-slug>/_index.md`
- **THEN** it SHALL remain supported as a session page

#### Scenario: Legacy scene pages exist
- **WHEN** a scene exists under `adventures/<adventure-slug>/sessions/<session-slug>/scenes/<scene-slug>.md`
- **THEN** it SHALL remain supported as a scene page
