# extract-class-features Specification

## Purpose
TBD - created by archiving change extract-class-features-interactive. Update Purpose after archive.
## Requirements
### Requirement: O script SHALL baixar e parsear características detalhadas da classe e subclasse
O script de criação de personagem SHALL baixar sob demanda as informações detalhadas da classe e subclasse do 5e.tools e carregar as características correspondentes ao nível selecionado do personagem.

#### Scenario: Parse de características para classe no nível 3
- **WHEN** o usuário seleciona uma classe no nível 3
- **THEN** o script SHALL parsear a progressão e extrair todas as características correspondentes aos níveis 1, 2 e 3 da classe.

### Requirement: O script SHALL solicitar escolhas interativas para características com opções
Quando uma característica possuir opções de escolha estruturadas ou for identificada como uma escolha de classe (ex: Estilo de Luta, Invocações de Bruxo, Metamagia), o script SHALL listar as opções e solicitar ao usuário que faça a seleção.

#### Scenario: Usuário escolhe um Estilo de Luta
- **WHEN** a característica "Fighting Style" é processada
- **THEN** o script SHALL ler as opções válidas de Estilo de Luta e solicitar a seleção no terminal interativo.

### Requirement: O script SHALL gerar stubs no compêndio para cada característica extraída
Para cada característica identificada, o script SHALL verificar se existe o stub correspondente em `content/compendium/rules/` e gerá-lo automaticamente caso esteja ausente.

#### Scenario: Geração de stub de regra ausente
- **WHEN** uma característica não possui um arquivo correspondente no compêndio local
- **THEN** o script SHALL criar um arquivo Markdown válido com frontmatter em `content/compendium/rules/<slug>.md`.

### Requirement: O script SHALL extrair fórmulas de rolagem de características e mapeá-las em ações
Para características que possuem fórmulas de rolagem associadas (ex: dano de Sneak Attack, cura de Second Wind), o script SHALL identificar essa fórmula nos dados do 5e.tools e preencher o campo `roll_formula` da respectiva ação.

#### Scenario: Extração de Sneak Attack no nível 3
- **WHEN** a característica "Sneak Attack" é processada para um Rogue de nível 3
- **THEN** o script SHALL definir a fórmula "2d6" no campo `roll_formula` da ação correspondente.

### Requirement: O layout da ficha SHALL expor e aprimorar progressivamente fórmulas de ações
O layout da ficha do personagem SHALL exibir a fórmula de rolagem configurada em uma ação (`char_info.actions`) como texto com metadados `data-roll-notation`, tornando-a interativa apenas após a ponte Dice+ confirmar readiness.

#### Scenario: Exibição de ação com rolagem Dice+
- **WHEN** a ficha do personagem é carregada sob a extensão com Dice+ ativo e possui uma ação com `roll_formula` definida
- **THEN** a fórmula de rolagem SHALL ser exibida e aprimorada progressivamente para controle de clique/foco.

### Requirement: O script SHALL associar características a ações e referências do personagem
O script SHALL preencher automaticamente a lista de ações (`char_info.actions`) e os links do compêndio (`compendium_refs`) no frontmatter do personagem criado com as características extraídas.

#### Scenario: Gravação final da ficha do personagem
- **WHEN** a ficha do personagem é salva no formato Markdown
- **THEN** o arquivo gerado SHALL conter as características extraídas inseridas em `char_info.actions` e seus caminhos de regra em `compendium_refs`.

