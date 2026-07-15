## 1. CSS & Assets Setup

- [ ] 1.1 Criar a folha de estilos `assets/css/character-sheet.css` contendo as regras visuais de abas, grid quadrado de atributos, colunas de perícias, cards de grimório de magias, seções de inventário e estilização compacta de VTT.
- [ ] 1.2 Importar a nova folha de estilos no layout do cabeçalho ou layout de página dos personagens do Hugo.
- [ ] 1.3 Definir as classes de utilidade CSS `.tab-content` (com `display: none` por padrão) e `.active` (com `display: block` ou `grid`) para a alternância de exibição.
- [ ] 1.4 Adicionar a classe `.vtt-iframe` no CSS para remover margens externas, esconder cabeçalho global e aplicar `overflow: hidden` na página, com rolagem apenas no container interno da aba ativa.

## 2. Layout Character Template Creation

- [ ] 2.1 Criar o template de layout exclusivo do Hugo em `layouts/characters/single.html` para renderização de fichas de personagens.
- [ ] 2.2 Estruturar a seção de cabeçalho do personagem exibindo o nome, raça, classe, nível, alinhamento e imagem (caso disponível).
- [ ] 2.3 Implementar a detecção dinâmica de iframe em JavaScript (`if (window.self !== window.top) document.documentElement.classList.add('vtt-iframe');`).
- [ ] 2.4 Implementar a navegação de abas no topo da ficha usando uma lista de botões compactos e clicáveis de comutação para as 8 abas.
- [ ] 2.5 Inserir o script Vanilla JS nativo inline que escuta cliques nos botões de abas e altera a classe `.active` para alternar a exibição sem recarga de tela.
- [ ] 2.6 Configurar verificação condicional no Hugo para exibir a aba de "Grimório" (Aba 5) apenas se o personagem possuir magias cadastradas na ficha.

## 3. Tab 1 & Tab 2 Implementation (Stats & Skills)

- [ ] 3.1 Implementar a Aba 1 (Estatísticas) com um grid CSS de 6 colunas responsivo, exibindo Força, Destreza, Constituição, Inteligência, Sabedoria e Carisma em caixas quadradas estilizadas, com o modificador destacado no centro e valor base no canto.
- [ ] 3.2 Renderizar na Aba 1 de forma proeminente e traduzida para pt_br: Classe de Armadura, Pontos de Vida (HP Atuais e Máximos), Deslocamento (Speed), Bônus de Proficiência, Salvaguardas (Saving Throws) de todos os atributos, Sentidos Passivos (como Percepção Passiva e outros) e Ouro.
- [ ] 3.3 Implementar a Aba 2 (Perícias) renderizando todas as perícias de D&D 5e em duas colunas ordenadas alfabeticamente.
- [ ] 3.4 Inserir indicadores visuais distintos na lista de perícias: um marcador preenchido para proficiência simples e um ícone duplicado ou estrela para indicar especialização (expertise), tudo em pt_br.

## 4. Tabs 3, 4 & 5 Implementation (Actions, Inventory & Grimoire)

- [ ] 4.1 Implementar a Aba 3 (Ações) listando as ações padrão de combate e exploração (Ataque, Esquivar, Disparar, Desengajar, Ajudar, Esconder, etc.) e as ações de classe/subclasse do personagem.
- [ ] 4.2 Adicionar na Aba 3 fileiras de checkboxes clicáveis representando a quantidade máxima de usos de recursos de uso limitado (ex: Fúria, Inspiração Bárdica) cadastrados no personagem.
- [ ] 4.3 Implementar a Aba 4 (Equipamentos) dividida em seções para Armas e Armaduras, Itens Consumíveis e Itens Gerais, contendo ícones estilizados.
- [ ] 4.4 Implementar a Aba 5 (Grimório) agrupando magias por nível em cards individuais estruturados, exibindo metadados como escola, tempo de conjuração e alcance.
- [ ] 4.5 Integrar as Abas 4 e 5 com o compêndio global via `site.GetPage` para buscar e enriquecer dados adicionais (descrição e tempo de conjuração de itens consumíveis e magias).

## 5. Tabs 6, 7 & 8 Implementation (Class, Features & Portrait)

- [ ] 5.1 Implementar a Aba 6 (Classe) exibindo a descrição da classe e subclasse do personagem e uma lista cronológica contendo os recursos e benefícios ganhos em cada nível da progressão.
- [ ] 5.2 Implementar a Aba 7 (Características) exibindo todas as habilidades de classe, traços raciais e talentos (Features & Traits) do personagem, traduzidos para o português brasileiro.
- [ ] 5.3 Implementar a Aba 8 (Imagem) como a aba final fixa da ficha de RPG, renderizando a ilustração a partir do frontmatter (campo `image` ou `avatar`) com uma imagem de silhueta/heráldica medieval como fallback de segurança caso o campo esteja ausente.

## 6. Responsiveness, VTT & Validation

- [ ] 6.1 Adicionar Media Queries no CSS para colapsar o grid de atributos e as colunas de perícias e magias em telas pequenas (mobile abaixo de 768px).
- [ ] 6.2 Validar a compatibilidade com iframe de VTT, garantindo que paddings externos sejam anulados, o cabeçalho global seja ocultado e a rolagem interna do contêiner da aba seja fluida e sem dupla barra de rolagem.
- [ ] 6.3 Executar o build estático local (`hugo --gc --minify`) para validar a compilação sem erros.
- [ ] 6.4 Validar visualmente a ficha interativa e a comutação de abas em múltiplos navegadores e em tamanho de iframe.
