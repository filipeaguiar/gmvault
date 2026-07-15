## 1. Setup e Processamento de Dados

- [ ] 1.1 Implementar no script `create_character.py` o download sob demanda do arquivo `feats.json` salvando-o localmente em `content/compendium/feats/.feats_cache.json`.
- [ ] 1.2 Adicionar lógica para carregar, decodificar e filtrar os talentos a partir do cache, separando-os por Talentos de Origem (fonte `XPHB` e categoria `O`) e Talentos Gerais/Estilos de Combate (fonte `XPHB` e categorias `G` ou `FS`).

## 2. Prompts Interativos de Seleção

- [ ] 2.1 Adicionar etapa de seleção no fluxo de criação para nível 1 perguntando a quantidade e permitindo a seleção de múltiplos Talentos de Origem, exibindo a lista em 4 colunas usando Rich.
- [ ] 2.2 Adicionar etapa opcional de seleção para nível >= 4 perguntando a quantidade de talentos adicionais e permitindo a seleção a partir dos Talentos Gerais/Combate.
- [ ] 2.3 Implementar comportamento de fallback com entrada textual manual caso ocorra erro ao carregar ou processar o JSON de talentos.

## 3. Integração e Geração do Compêndio

- [ ] 3.1 Integrar a função de download `fetch_from_5etools` no fluxo de finalização do script para gerar stubs de talentos em `content/compendium/feats/<slug>.md`.
- [ ] 3.2 Atualizar a gravação da ficha do personagem (bloco YAML de frontmatter) salvando a lista de talentos escolhidos em `char_info.feats` e registrando os caminhos correspondentes em `compendium_refs`.

## 4. Validação

- [ ] 4.1 Criar um personagem de teste interativamente escolhendo talentos para validar o terminal e a ficha YAML gerada.
- [ ] 4.2 Executar o build do Hugo (`hugo --gc --minify`) para garantir que os layouts da ficha renderizam e linkam os novos talentos corretamente.
