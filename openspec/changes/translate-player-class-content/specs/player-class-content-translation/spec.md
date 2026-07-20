## ADDED Requirements

### Requirement: Player-selectable class content is available in Portuguese
The vault SHALL provide manually reviewed pt-BR content for the Barbarian, Bard, Monk, and Rogue class pages, their directly referenced class features, and their selectable subclasses and subclass features from XPHB, TCE, and XGE.

#### Scenario: Player opens a class page
- **WHEN** a player opens the Barbarian, Bard, Monk, or Rogue page
- **THEN** the class progression and its feature link labels SHALL be presented in pt-BR

#### Scenario: Player opens a subclass choice
- **WHEN** a player opens a subclass page associated with Barbarian, Bard, Monk, or Rogue
- **THEN** its title, descriptive content, and referenced subclass features SHALL be presented in pt-BR

### Requirement: Manual translations preserve vault structure
Manual class-content translation SHALL preserve YAML front matter, canonical internal URLs, Markdown structure, HTML, and mechanical notation.

#### Scenario: Translated page contains structured content
- **WHEN** a translated class, feature, or subclass page includes front matter, internal links, HTML, dice notation, or structured metadata
- **THEN** those structures SHALL remain valid and semantically unchanged except for localized display text

#### Scenario: Translated class content is built
- **WHEN** Hugo builds the vault with drafts enabled
- **THEN** the translated class, feature, and subclass pages SHALL render without build errors
