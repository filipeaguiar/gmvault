# forge-statblock-export-fixes Specification

## Purpose
TBD - created by archiving change fix-forge-monster-export. Update Purpose after archive.
## Requirements
### Requirement: Support structured saves (maps) in export
O layout de exportação do Forge SHALL verificar dinamicamente se o campo `saves` no front matter é um dicionário/mapa. Se for, ele SHALL extrair os valores numéricos associados a cada atributo (Str, Dex, Con, Int, Wis, Cha) de forma direta. Se for uma string, ele SHALL aplicar o fallback de expressão regular legado.

#### Scenario: Parsing saves from map
- **WHEN** a propriedade `saves` for um mapa do tipo `{"con": "+11", "dex": "+5"}`
- **THEN** o layout SHALL extrair os valores numéricos de salvamento correspondentes como `conSave = 11` e `dexSave = 5`

---

### Requirement: Support structured skills (maps) in export
O layout de exportação do Forge SHALL verificar dinamicamente se o campo `skills` no front matter é um dicionário/mapa. Se for, ele SHALL iterar pelos pares chave-valor e criar a lista de perícias estruturadas. Se for uma string, ele SHALL aplicar o fallback de divisão de string legado.

#### Scenario: Parsing skills from map
- **WHEN** a propriedade `skills` for um mapa do tipo `{"perception": "+12", "stealth": "+5"}`
- **THEN** o layout SHALL extrair a lista de perícias com cada item no formato `"Nome +Valor"`, gerando IDs únicos via hash MD5

---

### Requirement: Robust walk speed extraction
O layout de exportação do Forge SHALL suportar a extração da velocidade de caminhada mesmo quando a string começar ou contiver a palavra `"walk "`. Ele SHALL casar a expressão `"walk [digitos]"` para ler o valor numérico. Se a correspondência falhar, ele SHALL ler os dígitos do início da string como fallback.

#### Scenario: Extracting walk speed from complex speed text
- **WHEN** a string de velocidade for `"walk 40 ft., fly 80 ft."`
- **THEN** o layout SHALL extrair com sucesso o valor numérico `40` como a velocidade de caminhada (`walkSpeed`)

---

### Requirement: Hierarchical parsing of actions and features from body
O layout de exportação do Forge SHALL dividir o corpo do markdown em blocos de cabeçalhos de nível 2 (`## `) para isolar seções como `"Ações"`, `"Características"`, etc. Dentro de cada seção maior, ele SHALL dividir os sub-blocos por cabeçalhos de nível 3 (`### `) para extrair o nome e a descrição de cada item individual de forma limpa, mantendo o fallback para itens delimitados por negritos (`**Nome.**`).

#### Scenario: Extracting actions from markdown body headers
- **WHEN** o corpo do Markdown do monstro contiver a seção `## Ações` e a subseção `### Mordida` seguida por texto de descrição
- **THEN** o layout SHALL extrair a ação `"Mordida"` com sua respectiva descrição e adicioná-la à lista de ações exportadas

