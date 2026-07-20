## ADDED Requirements

### Requirement: Editorial translation can cover published player-facing class content
The vault SHALL permit manually reviewed translations of player-facing class, feature, and subclass pages regardless of their `draft` value, without invoking the automatic draft translator.

#### Scenario: Published class page is translated manually
- **WHEN** an editor translates a player-facing class, feature, or subclass page with `draft: false`
- **THEN** the translation SHALL be preserved as editorial content and SHALL NOT require `translate_drafts.py` execution

#### Scenario: Manual translation records localized title
- **WHEN** an editor localizes a canonical imported class, feature, or subclass page
- **THEN** the page MAY retain its canonical `title` and SHALL use `titulo_pt_br` for its Portuguese display title when a localized title is available
