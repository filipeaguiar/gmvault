## Why

Atualmente, o script `create_character.py` permite gerar novos personagens de forma interativa, mas não temos uma maneira simples de *editar* um personagem já criado, como adicionar mais equipamentos depois da sessão (ex: quando os jogadores compram itens novos). A criação de um script de edição (ou adicionar um modo de edição) resolve o problema de manutenção da ficha usando as mesmas ferramentas validadas de importação do 5e.tools.

## What Changes

- Criação de um novo script `edit_character.py` (ou expansão da CLI iterativa para incluir modo edição) que lista os personagens locais e permite selecionar um.
- O script fará o parse do front matter YAML do personagem existente.
- Uma vez carregado, o script exibirá um menu com opções do que editar. Inicialmente, o foco será "Adicionar Equipamentos".
- A opção de adicionar equipamentos reaproveitará a lógica já estabelecida de busca interativa, adição ao array de equipamentos, consolidação e atualização das referências (`compendium_refs`).
- Salva o arquivo de volta preservando os dados anteriores, atualizando apenas a seção modificada.

## Capabilities

### New Capabilities
- `edit-character-interactive`: Menu iterativo que lê um arquivo markdown de personagem local, permite alteração de dados específicos (como equipamentos) e reescreve o YAML front matter preservando o conteúdo principal.

### Modified Capabilities
- Nenhuma alteração direta em capacidades existentes.

## Impact

- Novos scripts interativos de CLI.
- Possível extração de lógica de salvamento e manipulação de YAML para `dnd_utils.py` se necessário reaproveitar entre `create_character` e `edit_character`.
