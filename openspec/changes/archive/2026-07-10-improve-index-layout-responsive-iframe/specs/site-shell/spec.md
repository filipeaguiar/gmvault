## MODIFIED Requirements

### Requirement: Lightweight visual shell
The site SHALL provide readable wiki-style pages with a simple header, footer, content width, cards, badges, metadata blocks, responsive iframe-friendly layouts, and CSS-only styling suitable for modest computers.

#### Scenario: Page renders
- **WHEN** any content page is opened
- **THEN** the page SHALL render through the common base layout and shared CSS without requiring application JavaScript

#### Scenario: Page renders inside narrow iframe
- **WHEN** any content or index page is displayed inside an iframe with limited width
- **THEN** the visual shell SHALL avoid horizontal overflow and preserve readable content, visible navigation, and usable tap/click targets
