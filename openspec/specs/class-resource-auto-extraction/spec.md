# class-resource-auto-extraction Specification

## Purpose
TBD - created by archiving change auto-class-resource-uses. Update Purpose after archive.
## Requirements
### Requirement: Extraction of class table group resource columns
O script de criação ou modificação de personagem SHALL carregar o cache JSON da classe do personagem e analisar `classTableGroups` para identificar colunas associadas a recursos limitados (especificamente `"Ki Points"`, `"Focus Points"`, `"Rages"`, e `"Bardic Inspiration"`).

#### Scenario: Identifying Monk Focus column
- **WHEN** o script carrega o arquivo de cache JSON do Monge (`.class-monk.json_cache.json`)
- **THEN** ele SHALL identificar a coluna `"Focus Points"` no índice correto do `colLabels`

---

### Requirement: Setting max uses based on level
O script SHALL extrair o valor da linha da tabela de classe correspondente ao nível atual do personagem na coluna de recursos identificada e atribuir esse valor ao campo `max_uses` da respectiva ação do personagem.

#### Scenario: Monk level 5 focus points
- **WHEN** o personagem é um Monge de nível 5
- **THEN** o script SHALL ler o valor da linha 5 da tabela de classe (`rows[4]`), obter o número de Focus Points (valor `5`) e gravar no `max_uses` da ação de Foco

---

### Requirement: Normalizing Monk resource naming to Focus
O script SHALL normalizar qualquer referência legado ao recurso do Monge (como `"Ki Points"` ou `"Ki"`) para o termo padrão de regras novas **"Pontos de Foco"** ou **"Foco"** (ou `"Focus Points"` em contextos de importação em inglês).

#### Scenario: Normalising Ki to Focus
- **WHEN** o script encontra a coluna `"Ki Points"` na tabela de classe de um Monge clássico
- **THEN** ele SHALL mapear esse recurso para o nome da ação `"Pontos de Foco"` em português

---

### Requirement: Auto-creating missing action in character sheet
Se a ação que representa o recurso especial de classe (Foco, Fúria, Inspiração Bárdica) estiver ausente do array `char_info.actions` do personagem markdown, o script SHALL criá-la e inseri-la automaticamente.

#### Scenario: Retroactive addition of Focus action
- **WHEN** o script sincroniza uma ficha de Monge de nível 2 que não possui a ação `"Pontos de Foco"` em seu front matter
- **THEN** o script SHALL adicionar o dicionário `{"name": "Pontos de Foco", "ref": "/compendium/rules/ki/", "max_uses": 2, "reset": "Descanso Curto ou Longo", "source": "class"}` ao array `char_info.actions`

