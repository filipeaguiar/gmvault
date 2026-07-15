## 1. Script Setup & Parsing

- [x] 1.1 Criar o script utilitário em `scripts/sync_character.py` para processar fichas Markdown editadas manualmente.
- [x] 1.2 Implementar no script a leitura do YAML frontmatter e a extração estruturada de magias (`spells`), equipamentos (`equipment`), classes (`classes_progression`) e talentos (`feats`).

## 2. Compendium Sourcing & 5e.tools Integration

- [x] 2.1 Integrar o script com a lógica do 5e.tools para buscar e baixar no compêndio local quaisquer itens de apoio cujos caminhos de referência não constem no campo `compendium_refs` do personagem.

## 3. Markdown Writing & Verification

- [x] 3.1 Implementar a escrita cirúrgica de volta no arquivo Markdown do personagem, atualizando o campo `compendium_refs` com os novos stubs e preservando a integridade da biografia e prosa do arquivo.
- [x] 3.2 Criar testes unitários para validar que as alterações manuais em chaves de atributos e a seção da biografia de personagens não são modificadas ou danificadas pelo script.
