## Why

As fichas de personagem atuais no site estático do gmvault são renderizadas de forma puramente textual e linear, o que não remete à imersão visual de uma sessão de RPG de mesa tradicional. O gmvault precisa de uma interface visual dedicada, organizada e interativa que permita aos jogadores e ao mestre consultarem rapidamente atributos, perícias, inventário e magias de forma estruturada.

## What Changes

- **Layout de Ficha de RPG**: Substituição da renderização linear textual por um layout estilizado semelhante a uma ficha de personagem clássica de papel.
- **Atributos em Quadrados**: Cada atributo (Força, Destreza, Constituição, Inteligência, Sabedoria, Carisma) será exibido em um quadrado dedicado, com destaque visual maior para o modificador e o valor base associado.
- **Navegação por Abas (Tabs)**: Introdução de uma navegação por 4 abas interativas no topo da ficha usando CSS/JS leve:
  1. **Atributos e Estatísticas**: Atributos/modificadores, pontos de vida (HP), classe de armadura (AC), bônus de proficiência, classe de dificuldade (DC) de magias e ouro acumulado.
  2. **Perícias (Skills)**: Exibição em duas colunas ordenadas com marcadores visuais discretos para indicar proficiência e um marcador diferenciado para especialização (expertise).
  3. **Equipamentos e Itens**: Seções dedicadas para Armas, Armaduras (com ícones dedicados e rolagens correspondentes), Itens Consumíveis (dados dinâmicos do compêndio) e Outros Itens.
  4. **Grimório (Grimoire)**: Exibição de magias conhecidas agrupadas por nível com cards interativos detalhados (puxando informações adicionais do compêndio).

## Capabilities

### New Capabilities
- `rpg-character-sheet`: Sistema visual de renderização de ficha de personagem de RPG no gmvault com suporte a abas, estilização de atributos e integração com dados do compêndio.

### Modified Capabilities
Nenhuma.

## Impact

- **Layouts do Hugo**: Criação de layouts específicos em `layouts/characters/single.html` ou similares.
- **Estilos Globais**: Atualização das folhas de estilo CSS (`assets/css/`) para comportar a visualização em quadrados, tabelas de 2 colunas e cards de magia.
- **Assets e Scripts**: Scripts mínimos de Vanilla JS (ou técnicas CSS puras com inputs de rádio) para a comutação de abas interativas sem depender de frameworks JavaScript.
- **Leitura do Compêndio**: O layout fará chamadas a `site.GetPage` para obter informações complementares de magias e itens do compêndio baseando-se nas referências internas cadastradas no Markdown do personagem.
