## 1. Implementar Heurística de Mapas e Geração de Handouts

- [x] 1.1 Criar a função auxiliar `write_map_handout` para gerar o arquivo markdown do handout de mapa com visibilidade correta (`players` para mapas de jogador, `gm` para mapas de mestre/outros) e tags apropriadas.
- [x] 1.2 Modificar o tratamento de `entry_type == "image"` na função `parse_entry` para identificar heuristicamente imagens de mapas (presença de "map" ou "mapa" no título).
- [x] 1.3 Fazer com que `parse_entry` chame a geração de handout de mapa quando um mapa for detectado e adicione a referência do handout à lista de handouts da localidade ativa.

## 2. Registro e Acúmulo de Localidades em Memória

- [x] 2.1 Declarar e gerenciar a estrutura `locations_registry` em `main()` para acumular as localidades ativas, seus mapas e as cenas pertencentes a cada uma.
- [x] 2.2 Atualizar o processamento de cenas em `main()` (nas opções de importação) para associar as cenas e sub-seções à localidade ativa correspondente no `locations_registry`.
- [x] 2.3 Passar a localidade ativa para as funções de análise de entrada ou registrá-las de forma que `parse_entry` consiga associar mapas à localidade correspondente.

## 3. Escrita Consolidada e Enriquecida de Localidades

- [x] 3.1 Criar a função `write_enriched_locations` para iterar sobre `locations_registry` no fim da importação e gerar os arquivos markdown em `content/campaigns/<campaign-slug>/locations/`.
- [x] 3.2 Implementar a geração de front matter rico (com o campo `handouts` apontando para os handouts de mapa gerados) e corpo markdown contendo a lista de cenas vinculadas e exibição de imagens dos mapas.


## 4. Validação e Teste do Fluxo de Importação

- [x] 4.1 Executar a importação de uma campanha de teste (ex: `lmop` ou `jttrc`) e verificar a correta criação dos diretórios e arquivos em `locations/` e `handouts/`.
- [x] 4.2 Rodar `hugo server -D` para checar se a estrutura de links e metadados renderiza sem falhas no servidor local.
- [x] 4.3 Rodar `hugo --gc --minify` para validar o build estático completo.
