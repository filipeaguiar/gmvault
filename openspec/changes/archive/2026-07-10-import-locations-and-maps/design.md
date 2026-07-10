## Context

Atualmente, `import_campaign.py` cria apenas stubs de localidade vazios no início do fluxo e não realiza nenhuma amarração com os mapas contidos nas campanhas importadas do 5e.tools. O objetivo deste design é definir a arquitetura para enriquecer as localidades, detectar mapas de forma heurística, gerar handouts para esses mapas e estabelecer as devidas amarrações nos arquivos de conteúdo Hugo.

## Goals / Non-Goals

**Goals:**
- Identificar de forma heurística as imagens que representam mapas nas aventuras importadas.
- Criar arquivos de handout dedicados para esses mapas com a visibilidade correta (baseada na presença de spoilers ou grades).
- Enriquecer as páginas de localidade (`locations/*.md`) com a lista de cenas vinculadas a ela e o link/visualização do mapa da localidade.
- Associar os mapas aos campos `handouts` nas frentes YAML de localidades e cenas relacionadas.

**Non-Goals:**
- Implementar corte ou edição de imagens de mapa automaticamente.
- Forçar modificações em campanhas que não utilizam o script de importação.
- Integrar com ferramentas dinâmicas de visualização de mapas (VTT).

## Decisions

### 1. Coleta e Processamento Sequencial de Localidades
Em vez de gravar o arquivo de localidade imediatamente ao encontrar seu nome (`write_location_stub`), o script irá acumular as informações de localidade em memória durante a execução da importação.
- **Estrutura de dados em memória**:
  `locations_registry = { loc_slug: { "name": loc_name, "maps": set(), "scenes": [] } }`
- **Registro no loop**:
  - Quando uma nova localidade principal é ativada (`current_loc_slug = slugify(s_title)`), ela é adicionada ao `locations_registry` se não existir.
  - Cada cena processada registra-se na lista de `"scenes"` da localidade ativa atual no `locations_registry`.
  - No final de toda a importação (ao fim de `choice == "1"` ou `choice in ["2", "3"]`), o script percorre `locations_registry` e grava/atualiza os arquivos markdown enriquecidos em `locations/`.

### 2. Heurística de Detecção de Imagens de Mapa
Durante o processamento das imagens em `parse_entry(entry_type == "image")`:
- Se o título da imagem contiver as palavras chaves `map` ou `mapa` (caso insensível), a imagem será considerada um mapa.
- **Ação**:
  - A imagem será baixada e salva no diretório de static.
  - O script criará um arquivo de handout de mapa em `content/campaigns/<campaign-slug>/handouts/map-<slug_filename>.md`.
  - A visibilidade do handout será `"gm"` por padrão. Se o título contiver a palavra `"player"` (caso insensível), a visibilidade será `"players"`.
  - O handout de mapa gerado será registrado no contexto da cena atual (`ctx["handouts"]`) e associado à localidade ativa atual no `locations_registry`.

### 3. Layout Enriquecido no Markdown de Localidades
O arquivo markdown de cada localidade gerado conterá:
- YAML Front Matter completo:
  - `title` com o nome amigável da localidade.
  - `params.kind: "location"`.
  - `visibility: "gm"`.
  - `status: "ready"`.
  - `handouts` contendo a lista de referências internas para os handouts de mapa gerados.
- Corpo Markdown rico:
  - Uma seção listando as cenas/sub-áreas que pertencem a esta localidade.
  - Uma seção exibindo os mapas relacionados (com markdown de imagem normal) para visualização direta do mestre de jogo.

## Risks / Trade-offs

- **[Risco] Mapa associado à localidade errada** → Mitigação: O script mantém um rastreamento rigoroso da localidade ativa atual (`current_loc_slug`). Se uma imagem de mapa for processada dentro de uma cena ou quarto numerado, ela será associada à localidade principal ativa do momento. Isso reflete precisamente a estrutura hierárquica do 5e.tools.
- **[Risco] Imagens normais de lore contendo a palavra "map" no título sendo identificadas como mapas** → Mitigação: A heurística baseada na palavra chave "map/mapa" é muito precisa para o ecossistema do 5e.tools. Casos raros de falsos positivos resultarão apenas em handouts adicionais, sem quebra de comportamento.
