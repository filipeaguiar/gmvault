# site-shell Specification

## Purpose
Define the static Hugo shell, build behavior, home page entry points, and lightweight presentation requirements for the RPG Campaign Vault.
## Requirements
### Requirement: Static Hugo site builds without a theme
The vault SHALL be implemented as a Hugo static site using repository-local layouts, partials, assets, and Markdown content rather than an external Hugo theme, backend service, database, or heavy JavaScript framework.

#### Scenario: Production build
- **WHEN** the maintainer runs `hugo --gc --minify`
- **THEN** Hugo SHALL generate the static site successfully from the checked-in content, layouts, and assets

#### Scenario: Local editing server
- **WHEN** the maintainer runs `hugo server -D`
- **THEN** Hugo SHALL be able to serve draft and non-draft Markdown content for local review

### Requirement: Home page exposes primary vault areas
The home page SHALL present Campanhas and Compêndio Global as the primary entry points and SHALL link to their section pages when those pages exist.

#### Scenario: Campaigns exist
- **WHEN** pages with campaign metadata exist in the site
- **THEN** the home page SHALL list them with title, summary, and system metadata when available

#### Scenario: Compendium sections exist
- **WHEN** compendium subsection pages exist
- **THEN** the home page SHALL expose links for monsters, items, magic items, classes, races, feats, spells, backgrounds, conditions, and rules

### Requirement: Lightweight visual shell
The site SHALL provide readable wiki-style pages with a simple header, footer, content width, cards, badges, metadata blocks, responsive iframe-friendly layouts, and CSS-only styling suitable for modest computers.

#### Scenario: Page renders
- **WHEN** any content page is opened
- **THEN** the page SHALL render through the common base layout and shared CSS without requiring application JavaScript

#### Scenario: Page renders inside narrow iframe
- **WHEN** any content or index page is displayed inside an iframe with limited width
- **THEN** the visual shell SHALL avoid horizontal overflow and preserve readable content, visible navigation, and usable tap/click targets

