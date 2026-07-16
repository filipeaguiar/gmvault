## 1. Buscar Dados do 5e.tools

- [x] 1.1 Adicionar função em `dnd_utils.py` para carregar dados de `backgrounds.json`.
- [x] 1.2 Adicionar função em `dnd_utils.py` para carregar dados de `items.json` e preparar uma função auxiliar para recuperar e catalogar itens no compêndio global.
- [x] 1.3 Adicionar lógica em `dnd_utils.py` para buscar os itens (ou "explodir" kits em múltiplos itens) e resolver suas referências formatadas em YAML (ex: `ref: "/compendium/items/<slug>/"`).

## 2. Menu Interativo de Criação de Personagem

- [x] 2.1 Modificar `create_character.py` para exibir um menu com os Backgrounds disponíveis do XPHB e processar a escolha do usuário.
- [x] 2.2 Modificar `create_character.py` para consultar os Pacotes (Packs) Iniciais disponíveis (ex: Burglar's Pack, Explorer's Pack, etc.) para a Classe escolhida e perguntar ao usuário qual pacote ele deseja.
- [x] 2.3 Após as escolhas, consolidar todos os itens ganhos (roupas do Background, ouro, ferramentas e os itens dentro do Pack escolhido) e preencher a lista de inventário do personagem.

## 3. Integração na Build (Hugo e Testes)

- [x] 3.1 Gravar o personagem gerado com o novo inventário e checar se `char_info.equipment` contém a lista de itens.
- [x] 3.2 Executar `hugo server -D` e `pytest` localmente, bem como garantir que as dependências de compêndio para esses itens sejam acionadas pela lógica.
