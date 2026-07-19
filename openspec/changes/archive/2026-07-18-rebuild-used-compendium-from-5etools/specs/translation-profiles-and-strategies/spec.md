## ADDED Requirements

### Requirement: DeepSeek V4 Pro translation profile is selectable
The translation workflow SHALL expose an OpenAI-compatible DeepSeek profile using model identifier `deepseek-v4-pro` and the official DeepSeek API base URL.

#### Scenario: Operator selects DeepSeek V4 Pro
- **WHEN** the operator chooses the DeepSeek V4 Pro option in the interactive translation flow or by profile
- **THEN** requests SHALL use `deepseek-v4-pro` and credentials resolved from `DEEPSEEK_API_KEY`

#### Scenario: Translation metadata is written
- **WHEN** a document is translated with the DeepSeek V4 Pro profile
- **THEN** `translation.engine` SHALL identify the OpenAI-compatible engine and `translation.model` SHALL equal `deepseek-v4-pro`

### Requirement: Deprecated DeepSeek aliases are not preferred
The project SHALL NOT present `deepseek-chat` as the recommended high-quality DeepSeek translation profile.

#### Scenario: Translation model options are displayed
- **WHEN** the interactive translation menu lists DeepSeek models
- **THEN** it SHALL identify DeepSeek V4 Pro as the high-quality option and SHALL NOT select `deepseek-chat` as the recommended default

### Requirement: Interactive translation allows model selection
The interactive translation flow SHALL allow the operator to choose a configured translation profile or model before execution and SHALL show the choice in its confirmation summary.

#### Scenario: Operator reviews translation operation
- **WHEN** the menu displays the final summary
- **THEN** the selected engine, endpoint profile, and model SHALL be visible before any files are written
