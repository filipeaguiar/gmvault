## Context

Os jogadores utilizam o vault do GM para hospedar seus personagens (ex: Pinky) usando as opções de compêndio local. Como o vault não utiliza banco de dados dinâmico para os jogadores alterarem suas próprias fichas online via painel, toda edição deve ser feita via Markdown YAML front matter.
Para não forçar que o GM edite o arquivo YAML manualmente (com o risco de errar refs ou a estrutura JSON dos equipamentos), faremos um `edit_character.py`.

## Goals / Non-Goals

**Goals:**
- Prover um script `edit_character.py` que lista todos os arquivos em `content/campaigns/*/characters/*.md`.
- Permitir escolher o personagem a ser editado.
- Reaproveitar a função `search_item_by_name` e o sistema interativo para adicionar equipamentos extras a esse personagem.
- Salvar as adições atualizando as listas `equipment` e `compendium_refs` no arquivo YAML do personagem.

**Non-Goals:**
- Não faremos edição de todos os atributos possíveis (nível, vida) nesta iteração. Focaremos apenas na adição interativa de equipamentos.
- Não faremos exclusão de equipamentos já existentes (apenas adição).

## Decisions

- **Busca de Personagens**: Usaremos `glob` para varrer `content/campaigns/*/characters/*.md`, e faremos o parsing com `python-frontmatter` para extrair nomes e a lista atual de equipamentos.
- **Inserção de Equipamentos**: Utilizaremos a mesma rotina desenvolvida para o script iterativo (perguntar nome do item, buscar no 5e.tools, extrair a referência).
- **Salvamento Parcial**: Usaremos a biblioteca `frontmatter` do python para carregar, alterar o YAML `equipment` e `compendium_refs`, e dar um dump de volta mantendo o body do markdown inalterado.

## Risks / Trade-offs

- **Risk**: A biblioteca `frontmatter` (ou yaml dumpers) pode perder comentários do YAML original.
- **Mitigation**: Como a estrutura de personagem não tem comentários no front matter, e já temos um padrão claro sendo dumpado pelo `create_character.py`, a reconstrução do front matter é segura. Usaremos os mesmos dicionários.
