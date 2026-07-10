## ADDED Requirements

### Requirement: Campaign importer generates simplified adventure hierarchy
`import_campaign.py` SHALL generate new campaign adventure content using the simplified physical hierarchy for sessions and scenes.

#### Scenario: Import creates adventure session
- **WHEN** `import_campaign.py` creates a session for an imported adventure
- **THEN** it SHALL write the session as `content/campaigns/<campaign-slug>/adventures/<adventure-slug>/<session-slug>/_index.md`

#### Scenario: Import creates session scene
- **WHEN** `import_campaign.py` creates a scene for an imported session
- **THEN** it SHALL write the scene directly under the session directory as `<scene-slug>.md`

#### Scenario: Import creates adventure support indexes
- **WHEN** `import_campaign.py` imports a new adventure
- **THEN** it SHALL NOT create mandatory `sessions/_index.md` or `scenes/_index.md` pages for the simplified hierarchy
