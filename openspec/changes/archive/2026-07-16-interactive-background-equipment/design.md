## Context

O script de criação de personagens precisa de acesso aos arquivos de equipamentos, kits e backgrounds do 5e.tools. Como o script já busca os dados iniciais do 5e.tools e permite escolha de raça e classe, é natural que a seleção de backgrounds (que define boa parte do equipamento inicial no D&D 2024) também ocorra aqui.

## Goals / Non-Goals

**Goals:**
- Prover seleções interativas durante a criação da ficha.
- Adicionar equipamentos base do Background ao inventário.
- Adicionar pacotes/kits iniciais escolhidos pela classe e "explodir" seu conteúdo em itens separados no inventário, para que tudo possa ser devidamente importado e renderizado pela interface de compêndio.
- Garantir que cada item inicial seja importado para o compêndio.

**Non-Goals:**
- Interface de inventário ou "loja" durante o script de criação.
- Importar todo o equipamento do D&D Beyond automaticamente, isso já existe no `import_dndbeyond.py`. O objetivo aqui é o `create_character.py`.

## Decisions

- **Busca de Backgrounds**: Iremos baixar e ler o `backgrounds.json` do 5e.tools.
- **Explosão de Packs (Kit de Assaltante, etc)**: Iremos criar um dicionário fixo (ou buscar da base) contendo o nome do Pack e os seus itens para que, ao invés do usuário ganhar "Burglar's Pack" na ficha, ele ganhe os itens que compõem esse pacote (mochila, velhas, corda, pé de cabra).
- **Referências**: A inserção no frontmatter usará a mesma estrutura `ref: "/compendium/items/<slug-do-item>/"`.

## Risks / Trade-offs

- **Risk:** Os nomes dos itens podem não bater com o importador local, gerando links quebrados.
- **Mitigation:** Utilizar os utilitários de `dnd_utils.py` para slugificar os nomes do inglês e invocar (ou simular) o processo de importação para as pastas do compêndio quando o item for adicionado à ficha.
