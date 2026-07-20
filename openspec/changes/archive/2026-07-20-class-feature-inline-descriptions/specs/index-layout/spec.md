## ADDED Requirements

### Requirement: Class and subclass layouts resolve related feature pages
Class and subclass layouts SHALL resolve feature URLs from their rendered progression content through `site.GetPage` and use a shared inline-description presentation.

#### Scenario: Layout renders a class progression
- **WHEN** the class layout encounters an internal compendium feature URL in the progression
- **THEN** it SHALL delegate presentation to the shared inline-description partial
