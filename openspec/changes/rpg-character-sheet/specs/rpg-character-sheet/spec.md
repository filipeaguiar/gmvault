## ADDED Requirements

### Requirement: Tab Navigation Interface
O sistema SHALL disponibilizar uma barra de abas interativas no topo da visualização da ficha do personagem ("Atributos", "Perícias", "Equipamentos" e, opcionalmente para conjuradores, "Grimório") para comutação de conteúdo.

#### Scenario: Tab switching activation
- **WHEN** o usuário clica em uma aba na barra de navegação da ficha
- **THEN** o sistema SHALL alternar a visualização ocultando as demais áreas e exibindo apenas a correspondente à aba selecionada, sem realizar recarga de página (através de CSS puro com inputs de rádio ou Vanilla JS leve).

### Requirement: Square Attribute and Highlight Modifiers
O sistema SHALL exibir cada um dos 6 atributos principais do personagem em um elemento visual quadrado, com destaque visual maior para o modificador calculado e menor para o valor base associado.

#### Scenario: Render attributes visual boxes
- **WHEN** a ficha do personagem é renderizada no Hugo
- **THEN** o sistema SHALL desenhar Força, Destreza, Constituição, Inteligência, Sabedoria e Carisma em caixas quadradas destacando o modificador (ex: +3) de forma proeminente e exibindo também o valor base (ex: 16), o bônus de proficiência, classe de armadura, pontos de vida, bônus de CD de magia (se aplicável) e ouro acumulado.

### Requirement: Column Skills and Expertise Highlights
O sistema SHALL exibir a lista de perícias do personagem dividida em duas colunas ordenadas alfabeticamente na aba de Perícias, com marcadores visuais diferenciados para indicar proficiência simples ou especialização (expertise).

#### Scenario: Render skills list
- **WHEN** a aba de Perícias é exibida
- **THEN** o sistema SHALL renderizar a lista de todas as perícias (Skills) em 2 colunas, exibindo o bônus total de cada perícia, um indicador visual preenchido se o personagem for proficiente, e um indicador com símbolo alternativo (como uma estrela ou marcação em dobro) caso ele possua especialização (expertise).

### Requirement: Categorized Equipment List
O sistema SHALL exibir o inventário do personagem sob a aba de Equipamentos, dividido de forma estruturada em Armas e Armaduras, Itens Consumíveis e Outros Itens, com ícones dedicados e metadados operacionais.

#### Scenario: Render categorized inventory
- **WHEN** a aba de Equipamentos é exibida
- **THEN** o sistema SHALL listar os itens do personagem em três seções separadas: Armas e Armaduras (com ícones dedicados e fórmulas de rolagem de ataque/dano baseadas nos metadados), Itens Consumíveis (como poções e pergaminhos cujas informações podem ser puxadas e completadas a partir do compêndio correspondente) e Outros Itens (itens gerais de aventura).

### Requirement: Caster Grimoire by Level
O sistema SHALL renderizar a aba de Grimório exclusivamente para personagens capazes de conjurar magias, agrupando suas magias conhecidas por nível.

#### Scenario: Render grimoire cards
- **WHEN** o personagem possuir magias cadastradas em sua ficha e a aba de Grimório for acessada
- **THEN** o sistema SHALL listar todas as magias divididas por nível de círculo (truques, 1º nível, 2º nível, etc.), exibindo cada magia em um card individual com metadados cruciais (tempo de conjuração, alcance, duração, escola e link direto para os detalhes da magia no compêndio).
