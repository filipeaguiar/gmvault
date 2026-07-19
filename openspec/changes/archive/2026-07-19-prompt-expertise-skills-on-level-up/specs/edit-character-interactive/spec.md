## MODIFIED Requirements

### Requirement: Editor exposes local level-up operation
The interactive character editor SHALL offer a level-up operation for a selected local character whose class progression can be resolved, collect every required deterministic player choice including Expertise skill selections, and present the completed plan before modifying the file.

#### Scenario: Eligible character is selected
- **WHEN** the editor loads a character with a valid class and current level
- **THEN** the editor SHALL offer the level-up operation alongside existing editing operations

#### Scenario: Editor presents plan before writing
- **WHEN** the user selects level-up
- **THEN** the editor SHALL display the target level, automatic changes, new features, and required choices before modifying the file

#### Scenario: Expertise requires skill selections
- **WHEN** the target-level features include `Expertise`
- **THEN** the editor SHALL prompt the user to select two distinct eligible skills before presenting the confirmation prompt
