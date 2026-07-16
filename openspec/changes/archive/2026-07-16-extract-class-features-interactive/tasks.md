## 1. Mapeamento e Parsing de Características

- [x] 1.1 Implementar lógica para baixar e cachear o arquivo JSON detalhado da classe (ex: `class-fighter.json`) do 5e.tools se não estiver localmente disponível.
- [x] 1.2 Criar rotinas para varrer os arrays `classFeature` e `subclassFeature` e filtrar as características concedidas para o nível atual do personagem.
- [x] 1.3 Desenvolver extrator de fórmulas de dados nas descrições de habilidades (ex: buscar regex `\b\d+d\d+(?:[+-]\d+)?\b` ou usar campos dedicados do 5e.tools).

## 2. Escolhas Interativas e Fallbacks

- [x] 2.1 Detectar características que oferecem escolhas e apresentar prompts de seleção interativa de opções (ex: escolhas de Estilos de Luta, Invocações de Bruxo ou Metamagia).
- [x] 2.2 Adicionar blocos de try-catch para capturar falhas em estruturas JSON não padrão e aplicar fallback de gravação apenas com o título/descrição textual simples.

## 3. Geração no Compêndio e na Ficha

- [x] 3.1 Integrar a criação automática de stubs de compêndio sob `content/compendium/rules/` e vincular os slugs correspondentes no `compendium_refs` do personagem.
- [x] 3.2 Popular automaticamente o campo `char_info.actions` do personagem com a lista de características e habilidades extraídas da progressão da classe, preenchendo o subcampo `roll_formula` quando detectado.
- [x] 3.3 Atualizar o layout do personagem (`layouts/partials/kinds/character.html`) na aba de Ações para exibir e injetar o atributo `data-roll-notation` em ações que possuem `roll_formula`.

## 4. Validação

- [x] 4.1 Criar interativamente um personagem de teste (como um Rogue ou Fighter nível 3) para validar o funcionamento do script, escolhas de habilidades, stubs e fórmulas extraídas (ex: Sneak Attack de Rogue).
- [x] 4.2 Executar a compilação do Hugo (`hugo --gc --minify`) para certificar que a ficha gerada e os stubs do compêndio compilam sem erros de layout ou de referências, e testar a rolagem interativa no VTT.
