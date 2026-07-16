## 1. Scaffold e Menu

- [x] 1.1 Criar o script `edit_character.py` com o boilerplate da CLI e imports padrão (import `dnd_utils`, `glob`, `python-frontmatter`).
- [x] 1.2 Implementar a busca de personagens lendo todos arquivos `.md` de `content/campaigns/*/characters/*.md` e listando no console via `ask_choice` pelo nome.

## 2. Parsing e Modificação do YAML

- [x] 2.1 Abrir o arquivo escolhido via `frontmatter.load()`.
- [x] 2.2 Reutilizar a lógica de busca do 5e.tools (usando `dnd_utils.search_item_by_name`) num loop onde o usuário digita nomes de itens para adicionar na ficha.
- [x] 2.3 Para cada item escolhido, perguntar a quantidade e fazer o append na lista do post (`post['equipment']`) e chamar `fetch_from_5etools` para popular o compêndio, guardando as referências em `post['compendium_refs']`.

## 3. Salvamento Seguro

- [x] 3.1 Garantir que o dump preserve o conteúdo Markdown abaixo do yaml e salve devolta no arquivo `.md`.
- [x] 3.2 Testar a execução do script com o personagem recém-criado Pinky e verificar se a ficha ganha os itens novos, rodando o `hugo server -D` para validação visual.
