## Why

Atualmente, a importação de personagens depende exclusivamente do D&D Beyond via API. No entanto, é necessário permitir a criação interativa e manual de personagens locais através de um script de linha de comando que conduza o usuário por perguntas. Isso resolve o problema de dependência de ferramentas externas (D&D Beyond) para personagens criados puramente no GM Vault, permitindo construir o frontmatter corretamente a partir das informações baixadas para o compêndio e dos cálculos estruturais da ficha (bônus, hp, etc).

## What Changes

- Criação de um novo script interativo em Python (`create_character.py`) que faz perguntas ao usuário no terminal para preencher os dados do personagem (nome, raça, classe, atributos, magias, itens, etc.).
- Uso da lógica de download de informações do 5e.tools (semelhante ao já presente em `import_dndbeyond.py`) para popular o compêndio.
- Adição de lógicas de cálculo de bônus de atributos e demais estatísticas derivadas.
- Geração final do arquivo markdown do personagem na pasta da campanha escolhida, com o frontmatter (`char_info` e outras) populado e devidamente formatado usando PyYAML.

## Capabilities

### New Capabilities
- `create-character-interactive`: Novo fluxo de CLI interativo (usando Rich, por exemplo) que coleta dados, extrai entidades requeridas do compêndio, faz cálculos base e gera a ficha final.

### Modified Capabilities

## Impact

- Novo script `create_character.py`.
- Facilitação da criação de personagens independentes da API do D&D Beyond.
- Poderá haver a necessidade de compartilhar código (importando funções de `import_dndbeyond.py` ou movendo para um arquivo utilitário) para reaproveitar a geração de YAML e buscas no 5e.tools.
