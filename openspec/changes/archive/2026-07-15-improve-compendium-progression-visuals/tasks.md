## 1. Estrutura semântica da página

- [x] 1.1 Atualizar `layouts/partials/kinds/class.html` para adicionar classes semânticas ao cabeçalho, metadados, corpo de progressão e seção de subclasses.
- [x] 1.2 Adicionar ícones RuneScape nos títulos de progressão, níveis e subclasses sem inserir caracteres Unicode ou emojis.
- [x] 1.3 Preservar links, conteúdo Markdown e summaries existentes durante a alteração do template.
- [x] 1.4 Inserir headings `Nível X` ao gerar novas progressões e migrar as páginas de classe existentes para agrupar entradas consecutivas pelo nível.
- [x] 1.5 Garantir que o gerador/importador crie páginas de regra com o texto das características ausentes antes de gerar os links da progressão.
- [x] 1.6 Remover headings redundantes de progressão das páginas existentes e do gerador, mantendo o nome resolvido da classe como título principal.

## 2. Estilo da progressão

- [x] 2.1 Criar estilos para o título da classe e o bloco de metadados com tipografia, cores e hierarquia visual próprias.
- [x] 2.2 Transformar headings e listas de progressão em uma apresentação organizada por nível, com cards/linhas, bordas, espaçamento e destaque para o nível.
- [x] 2.3 Estilizar links internos da progressão com cores do compêndio, estados hover/focus e quebra segura de URLs longas.
- [x] 2.4 Estilizar a seção de subclasses com cards, ícones, summaries e links internos sem estilo padrão do navegador.
- [x] 2.5 Estilizar headings de nível como divisores de grupo e garantir que as entradas permaneçam separadas quando reutilizadas na ficha do personagem.
- [x] 2.6 Substituir os cards individuais da progressão por listas simples separadas por headings e linhas horizontais.
- [x] 2.7 Criar render hook para links Markdown internos respeitarem o `baseURL` configurado e não gerarem 404.
- [x] 2.8 Ajustar o template para exibir somente o nome da classe, priorizando `titulo_pt_br` sobre `title`.

## 3. Responsividade e acessibilidade

- [x] 3.1 Ajustar a progressão para uma coluna em telas estreitas e impedir overflow horizontal em iframes.
- [x] 3.2 Garantir contraste, foco visível, títulos semânticos e ícones complementares ao texto.
- [x] 3.3 Confirmar que nenhum caractere Unicode decorativo ou emoji foi adicionado ao template/CSS.

## 4. Validação

- [x] 4.1 Criar teste de renderização para uma classe com progressão longa e subclasses, verificando títulos, níveis, summaries, agrupamento por nível e links.
- [x] 4.2 Executar `hugo --gc --minify` e revisar o HTML gerado para confirmar ausência de links com estilo padrão e ausência de overflow estrutural.
- [x] 4.3 Executar os testes relacionados a layouts e links internos.
- [x] 4.4 Testar links de características com e sem página pré-existente e verificar que o conteúdo é renderizado na classe e na ficha do personagem.
