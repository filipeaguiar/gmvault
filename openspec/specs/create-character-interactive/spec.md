# create-character-interactive Specification

## Purpose
TBD - created by archiving change create-character-interactive-script. Update Purpose after archive.
## Requirements
### Requirement: Interactive Character Creation
The script SHALL prompt the user to input character details such as name, race, class, level, stats, spells, background, starting packs, and equipment via terminal interface.

#### Scenario: User provides character details
- **WHEN** the script is executed
- **THEN** it asks for basic information (name, campaign) and step-by-step asks for race, class, level, background, starting packs, ability scores, proficiencies, etc.

### Requirement: Compendium Population
The script SHALL query the `5etools` mirrors for every supported shared entity represented by the locally created character, including classes, subclasses, species, feats, standard actions, class and subclass features, spells, items, and magic items, and SHALL materialize missing canonical compendium pages before writing their references into the character note.

#### Scenario: Character has a new species
- **WHEN** the user selects a species that is not in the compendium
- **THEN** the script SHALL download and save its canonical page from 5e.tools before writing the character

#### Scenario: Character has supported missing shared content
- **WHEN** the completed creation data includes a supported missing feat, spell, item, magic item, action, or class feature
- **THEN** the script SHALL synchronize the canonical compendium page and record its returned internal URL without duplicate references

#### Scenario: Content cannot be resolved
- **WHEN** a supported selected entity cannot be resolved unambiguously from 5e.tools
- **THEN** the script SHALL report it and SHALL NOT write a fabricated canonical reference

### Requirement: Stat Calculation
The script SHALL automatically calculate modifiers, AC, max HP, and proficiency bonus based on level, stats, and class/race info.

#### Scenario: Calculating modifiers
- **WHEN** the user inputs a Strength score of 16
- **THEN** the script calculates the STR modifier as +3.

### Requirement: Frontmatter Generation
The script SHALL generate the Markdown file for the character in the selected campaign using `PyYAML` to correctly format `char_info` with lists and dictionaries.

#### Scenario: File creation
- **WHEN** the interactive flow is completed
- **THEN** the script creates `content/campaigns/<campaign>/characters/<slug>.md` with properly formatted YAML frontmatter and no inline single-line JSON blocks.

### Requirement: Navegação regressiva por pergunta
O assistente interativo de criação de personagem SHALL tratar cada pergunta confirmada como uma posição individual de navegação e SHALL interpretar `00` como uma solicitação para retornar exatamente à pergunta confirmada imediatamente anterior.

#### Scenario: Retorno dentro do mesmo passo
- **WHEN** o usuário informa `00` em uma pergunta que possui outra pergunta confirmada antes dela no mesmo passo
- **THEN** o assistente reabre somente a pergunta imediatamente anterior
- **THEN** o assistente não reinicia a primeira pergunta do passo

#### Scenario: Retorno entre passos
- **WHEN** o usuário informa `00` na primeira pergunta de um passo e a pergunta anterior pertence ao passo precedente
- **THEN** o assistente reabre a última pergunta confirmada do passo precedente

#### Scenario: Retornos sucessivos
- **WHEN** o usuário informa `00`, retorna uma pergunta e informa `00` novamente
- **THEN** o assistente retorna mais uma pergunta no histórico a cada solicitação

#### Scenario: Cancelamento na primeira pergunta
- **WHEN** o usuário informa `00` e não existe pergunta anterior no histórico
- **THEN** o assistente cancela a criação de forma controlada
- **THEN** nenhum arquivo de personagem é gerado

### Requirement: Preservação e consistência das respostas durante o retorno
O assistente SHALL preservar respostas confirmadas anteriores à pergunta reaberta e SHALL recalcular ou invalidar respostas posteriores quando a resposta corrigida alterar suas dependências ou opções válidas.

#### Scenario: Correção sem perder respostas anteriores
- **WHEN** o usuário retorna a uma pergunta intermediária e fornece uma nova resposta
- **THEN** as respostas confirmadas antes dessa pergunta permanecem disponíveis sem serem solicitadas novamente
- **THEN** o fluxo prossegue a partir da resposta corrigida

#### Scenario: Resposta posterior continua válida
- **WHEN** uma resposta corrigida não altera as opções ou a validade de uma resposta posterior já confirmada
- **THEN** o assistente preserva a resposta posterior

#### Scenario: Resposta posterior fica incompatível
- **WHEN** uma resposta corrigida altera as opções disponíveis e torna incompatível uma resposta posterior
- **THEN** o assistente descarta a resposta incompatível
- **THEN** o assistente solicita novamente essa resposta quando alcançar a respectiva pergunta

#### Scenario: Entrada inválida não altera o histórico
- **WHEN** o usuário fornece uma entrada inválida em uma pergunta
- **THEN** o assistente repete a pergunta atual
- **THEN** nenhuma posição adicional é criada no histórico de navegação

### Requirement: Compendium Population
The script SHALL query the `5etools` mirrors for every supported shared entity represented by the locally created character, including classes, subclasses, species, feats, standard actions, class and subclass features, spells, items, and magic items, and SHALL materialize missing canonical compendium pages before writing their references into the character note.

#### Scenario: Character has a new species
- **WHEN** the user selects a species that is not in the compendium
- **THEN** the script SHALL download and save its canonical page from 5e.tools before writing the character

#### Scenario: Character has supported missing shared content
- **WHEN** the completed creation data includes a supported missing feat, spell, item, magic item, action, or class feature
- **THEN** the script SHALL synchronize the canonical compendium page and record its returned internal URL without duplicate references

#### Scenario: Content cannot be resolved
- **WHEN** a supported selected entity cannot be resolved unambiguously from 5e.tools
- **THEN** the script SHALL report it and SHALL NOT write a fabricated canonical reference

### Requirement: New spellcaster profiles persist a normalized casting ability
The interactive character creation flow SHALL determine and persist `char_info.spellcasting.ability` as a normalized ability key for a selected single-class spellcaster when the class data resolves that ability. It SHALL leave the field empty rather than guessing when the ability cannot be resolved.

#### Scenario: Creating a Warlock
- **WHEN** the user creates a single-class Warlock and the resolved class data identifies Charisma as its spellcasting ability
- **THEN** the generated character front matter SHALL contain `char_info.spellcasting.ability: cha`

#### Scenario: Class ability cannot be resolved
- **WHEN** the selected class data does not provide an unambiguous spellcasting ability
- **THEN** the generated profile SHALL leave `spellcasting.ability` empty
- **THEN** the creation flow SHALL NOT assign an ability based only on class-name heuristics

### Requirement: New character creation distinguishes absent spell attack overrides
The interactive character creation flow SHALL not write `spell_attack_bonus: 0` merely as a placeholder for a character whose spell attack bonus is intended to be derived.

#### Scenario: Creating a spellcaster with a resolved ability
- **WHEN** the user creates a single-class spellcaster with a resolvable casting ability and no exceptional attack bonus
- **THEN** the generated front matter SHALL leave the explicit spell attack override absent or mark it as absent distinctly from zero

