## 1. Saves and Skills Map Support

- [x] 1.1 Implementar suporte a mapa (dicionário) para o campo `saves` no layout `forge_statblock.html`, garantindo extração direta de valores numéricos e mantendo o fallback de regex.
- [x] 1.2 Implementar suporte a mapa (dicionário) para o campo `skills` no layout `forge_statblock.html`, gerando strings `"Nome +Valor"` e aplicando IDs baseados no hash MD5, mantendo o fallback de split por vírgula.

## 2. Speed and Movement Support

- [x] 2.1 Atualizar a regex de velocidade de caminhada (`walk`) para reconhecer o padrão `"walk [dígitos]"` e evitar valores zerados, mantendo compatibilidade com dígitos isolados.

## 3. Monster Abilities and Actions Parsing

- [x] 3.1 Atualizar a lógica do parser de corpo markdown de monstros em `forge_statblock.html` para dividir inicialmente por cabeçalhos nível 2 (`## `) e, em seguida, identificar as ações e características dividindo os blocos por subcabeçalhos nível 3 (`### `), mantendo o fallback de negritos (`**Nome.**`).

## 4. Verification and Validation

- [x] 4.1 Validar a exportação do JSON do Forge rodando a compilação e verificando o arquivo de saída `public/exports/forge/index.json` (ou o local correspondente no build) e confirmando que salvamentos, perícias, velocidade de caminhada e ações de monstros de exemplo (como o Acolyte e o Adult Blue Dragon) são preenchidos corretamente.
- [x] 4.2 Rodar build do Hugo (`hugo --gc --minify`) para certificar que os templates compilam sem erros.
