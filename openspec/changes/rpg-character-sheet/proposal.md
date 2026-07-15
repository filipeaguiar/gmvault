## Why

As fichas de personagem atuais no site estático do gmvault são renderizadas de forma puramente textual e linear, o que não remete à imersão visual de uma sessão de RPG de mesa tradicional. O gmvault precisa de uma interface visual dedicada, organizada e interativa que permita aos jogadores e ao mestre consultarem rapidamente atributos, perícias, inventário e magias de forma estruturada.

## What Changes

- **Layout de Ficha de RPG**: Substituição da renderização linear textual por um layout estilizado semelhante a uma ficha de personagem clássica de papel.
- **Atributos em Quadrados**: Cada atributo (Força, Destreza, Constituição, Inteligência, Sabedoria, Carisma) será exibido em um quadrado dedicado, com destaque visual maior para o modificador e o valor base associado.
- **Navegação por Abas (Tabs)**: Introdução de uma navegação por abas interativas no topo da ficha usando CSS/JS leve:
  1. **Atributos e Estatísticas**: Atributos e modificadores, Pontos de Vida (Atuais/Máximos), Classe de Armadura, Deslocamento (Speed), Bônus de Proficiência, Salvaguardas (Saving Throws) e Sentidos Passivos (como Percepção Passiva). Todos os termos traduzidos para o português brasileiro oficial de D&D 5e, além do Ouro acumulado.
  2. **Perícias (Perícias)**: Exibição em duas colunas ordenadas com marcadores visuais discretos para indicar proficiência e um marcador diferenciado para especialização (expertise), tudo em pt_br.
  3. **Ações (Ações)**: Exibição de ações padrão de combate e exploração (Ataque, Esconder, Desengajar, Disparar, Ajudar, Esquivar, etc.) e ações especiais de classe/subclasse. Ações com usos limitados (ex: Fúria, Inspiração Bárdica) exibirão checkboxes correspondentes aos usos máximos para rastreamento em jogo.
  4. **Equipamentos (Equipamentos)**: Seções dedicadas para Armas, Armaduras, Consumíveis (dados dinâmicos do compêndio) e Outros Itens.
  5. **Grimório (Grimório)**: Exibição de magias conhecidas agrupadas por círculo com cards interativos detalhados (ativo apenas para conjuradores).
  6. **Classe & Subclasse**: Detalhes e descrição da classe e subclasse do personagem, exibindo o que ele recebe em cada nível de sua progressão.
  7. **Características & Traços (Talentos/Traços)**: Lista completa de características de classe, raça e talentos (Features & Traits) do personagem, traduzidos para pt_br.
  8. **Imagem (Retrato)**: A última aba será dedicada à exibição da ilustração oficial ou retrato do personagem em tamanho destacado para imersão visual.
- **Sincronização de Ficha Local com 5e.tools**: Desenvolvimento de uma ferramenta que permite aos usuários evoluírem e atualizarem suas fichas editando diretamente o arquivo Markdown do personagem. Ao adicionar novas magias, itens, classes ou talentos no YAML frontmatter do Markdown, um script varre essas chaves, busca quaisquer novos stubs inexistentes no compêndio a partir do 5e.tools e atualiza a lista de referências do compêndio (`compendium_refs`) no próprio Markdown, sem sobrescrever edições manuais de atributos, vida ou nome.

## Capabilities

### New Capabilities
- `rpg-character-sheet`: Sistema visual de renderização de ficha de personagem de RPG no gmvault com suporte a abas, estilização de atributos e integração com dados do compêndio.
- `character-sync-tools`: Script utilitário para sincronização e enriquecimento de fichas Markdown editadas manualmente por meio do download automático de dados de apoio a partir do 5e.tools para o compêndio local.

### Modified Capabilities
Nenhuma.

## Impact

- **Layouts do Hugo**: Criação de layouts específicos em `layouts/characters/single.html` ou similares.
- **Estilos Globais**: Atualização das folhas de estilo CSS (`assets/css/`) para comportar a visualização em quadrados, tabelas de 2 colunas e cards de magia.
- **Assets e Scripts**: Scripts mínimos de Vanilla JS (ou técnicas CSS puras com inputs de rádio) para a comutação de abas interativas sem depender de frameworks JavaScript.
- **Leitura do Compêndio**: O layout fará chamadas a `site.GetPage` para obter informações complementares de magias e itens do compêndio baseando-se nas referências internas cadastradas no Markdown do personagem.
- **Integração VTT (Virtual Tabletop)**: O design da página e dos estilos deve prever a exibição em `iframes` de VTT. Os estilos de layout devem ser compactos, com padding reduzido no container externo, elementos interativos altamente responsivos em painéis reduzidos, e rolagem interna de conteúdo bem implementada para evitar barras de rolagem dupla indesejadas no navegador do VTT.
