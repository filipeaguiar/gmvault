## 1. CSS & Assets Setup

- [ ] 1.1 Criar a folha de estilos `assets/css/character-sheet.css` contendo as regras visuais de abas, grid quadrado de atributos, colunas de perícias, cards de grimório de magias e inventário responsivo.
- [ ] 1.2 Importar a nova folha de estilos no layout do cabeçalho ou layout de página dos personagens do Hugo.
- [ ] 1.3 Definir as classes de utilidade CSS `.tab-content` (com `display: none` por padrão) e `.active` (com `display: block` ou `grid`) para a alternância dinâmica.

## 2. Layout Character Template Creation

- [ ] 2.1 Criar o template de layout exclusivo do Hugo em `layouts/characters/single.html` para renderização de fichas de personagens.
- [ ] 2.2 Estruturar a seção de cabeçalho do personagem exibindo o nome, raça, classe, nível, alinhamento e imagem (caso disponível).
- [ ] 2.3 Implementar a navegação de abas no topo da ficha usando uma lista de botões estilizados de comutação.
- [ ] 2.4 Inserir o script Vanilla JS nativo inline (leve e compacto) que escuta cliques nos botões de abas e altera a classe `.active` para alternar a exibição sem recarga de tela.
- [ ] 2.5 Configurar verificação condicional no Hugo para exibir a aba de "Grimório" apenas se o personagem possuir magias cadastradas na ficha.

## 3. Tab 1 & Tab 2 Implementation (Stats & Skills)

- [ ] 3.1 Implementar a Aba 1 (Estatísticas) com um grid CSS de 6 colunas responsivo, exibindo Força, Destreza, Constituição, Inteligência, Sabedoria e Carisma em caixas quadradas estilizadas, com o modificador destacado no centro e valor base no canto.
- [ ] 3.2 Renderizar na Aba 1 os pontos de vida (HP), classe de armadura (AC), bônus de proficiência, DC de magias (se conjurador) e ouro acumulado de forma visível e destacada.
- [ ] 3.3 Implementar a Aba 2 (Perícias) renderizando todas as perícias de D&D 5e em duas colunas ordenadas alfabeticamente.
- [ ] 3.4 Inserir indicadores visuais distintos na lista de perícias: um marcador preenchido (círculo ou ícone) para proficiência simples e um ícone duplicado ou estrela para indicar especialização (expertise).

## 4. Tab 3 & Tab 4 Implementation (Inventory & Grimoire)

- [ ] 4.1 Implementar a Aba 3 (Equipamentos) dividida de forma estruturada em três seções: Armas e Armaduras, Itens Consumíveis e Itens Gerais.
- [ ] 4.2 Estilizar cada arma e armadura com ícones de categorias, exibindo os metadados de rolagens de ataque/dano se estiverem presentes no Markdown.
- [ ] 4.3 Implementar a Aba 4 (Grimório), agrupando as magias por nível em cards individuais estruturados.
- [ ] 4.4 Integrar o layout com o compêndio global via `site.GetPage` para puxar e preencher dados dos cards de itens consumíveis e magias se a página correspondente existir no diretório `compendium/`.
- [ ] 4.5 Implementar a Aba 5 (Imagem) como a última aba fixa da ficha de RPG, renderizando a ilustração a partir do frontmatter do personagem (campo `image` ou `avatar`) com uma imagem de silhueta/heráldica medieval como fallback de segurança caso o campo esteja ausente.

## 5. Responsiveness & Validation

- [ ] 5.1 Adicionar Media Queries no arquivo CSS para colapsar o grid horizontal de atributos em visualização mobile (abaixo de 768px), ajustando-o para 3 ou 2 colunas, e alinhar a tabela de perícias e magias em uma única coluna vertical.
- [ ] 5.2 Executar o build estático local (`hugo --gc --minify`) para validar a compilação sem erros.
- [ ] 5.3 Validar visualmente a ficha interativa em navegadores testando a responsividade e o funcionamento das abas em múltiplos personagens de exemplo.
