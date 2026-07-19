# Baseline de implementação

Data: 2026-07-17

## Inventário

- 455 arquivos Markdown no compêndio: 454 entidades e um `_index.md` reservado.
- 171 referências diretas a partir de campanhas/personagens.
- 20 dependências transitivas de regras.
- 191 páginas selecionadas.
- 263 páginas de entidade sem uso.

## Testes antes das alterações

- `hugo -D --gc --minify`: sucesso, 940 páginas; somente avisos de depreciação de `languageCode`/`.Site.LanguageCode`.
- `hugo --gc --minify`: sucesso, 603 páginas; mesmos avisos de depreciação.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: não concluiu em 180 segundos. A suíte efetuou chamadas de rede repetidas e produziu grande volume de avisos `Nenhum item encontrado`; registrado como comportamento preexistente. Testes focados e a suíte final com timeout controlado serão usados durante a implementação.
