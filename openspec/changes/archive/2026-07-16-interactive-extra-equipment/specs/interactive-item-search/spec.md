## ADDED Requirements

### Requirement: Interactive Item Search Prompt
The system SHALL prompt the user to add extra items at the end of the character creation process, looping until the user submits an empty response.

#### Scenario: User provides empty input
- **WHEN** the system asks "Deseja adicionar um item individual? (Deixe em branco para finalizar):"
- **WHEN** the user provides an empty string
- **THEN** the system proceeds to the next step (generating the file) without adding extra items

### Requirement: Case-insensitive Substring Search
The system SHALL search `items.json` and `items-base.json` using a case-insensitive substring match of the user's input against the item names.

#### Scenario: User searches for an item
- **WHEN** the user types "Longsword"
- **THEN** the system finds "Longsword" and any other item containing "longsword"

### Requirement: Disambiguation Menu
The system SHALL present a disambiguation menu if the search returns multiple items.

#### Scenario: Search returns multiple items
- **WHEN** the user types "Sword"
- **THEN** the system finds "Shortsword", "Longsword", "Greatsword"
- **THEN** the system presents an `ask_choice` menu for the user to select the correct item

#### Scenario: Search returns one item
- **WHEN** the user types "Burglar's Pack"
- **THEN** the system finds exactly 1 item
- **THEN** the system automatically selects it without prompting

### Requirement: Quantity Selection
The system SHALL ask for the quantity of the selected item before adding it.

#### Scenario: Item is selected
- **WHEN** an item is selected from search
- **THEN** the system asks "Quantidade de [ItemName]:" using `ask_int` (default 1)
- **THEN** the system appends it to the `pack_items` or a dedicated extra items list to be processed.
