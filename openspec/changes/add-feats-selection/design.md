## Context

O script de criação de personagens `create_character.py` é uma ferramenta CLI que auxilia na montagem do YAML de frontmatter das fichas de RPG. Atualmente, ele suporta a seleção e integração de espécie, classe, atributos, salvaguardas, perícias e especializações.

Para completar a criação de personagem de forma aderente às regras modernas (D&D 2024 / Tasha), falta a capacidade de escolher e associar **Talentos (Feats)**, salvando-os de forma estruturada no campo `char_info.feats` e registrando as referências no `compendium_refs` da ficha.

## Goals / Non-Goals

**Goals:**
- Baixar e fazer cache local do arquivo `feats.json` do espelho do 5e.tools em `content/compendium/feats/.feats_cache.json`.
- Filtrar talentos por fonte `XPHB` (D&D 2024) para priorizar a nova edição das regras.
- Implementar prompt de seleção para exatamente 1 Talento de Origem (*Origin Feat*, categoria `O`) no nível 1.
- Implementar prompt de seleção opcional para múltiplos Talentos Gerais ou de Estilo de Combate (*General Feats* / *Fighting Style*, categorias `G` e `FS`) para personagens de nível superior.
- Fazer download automático das descrições dos talentos selecionados para `content/compendium/feats/` e vinculá-las no compêndio da ficha.

**Non-Goals:**
- Ajustar atributos base automaticamente baseando-se em talentos ("half-feats"). Como a interface de atributos já permite bônus customizados livremente, o jogador ajusta seus atributos base de acordo com o talento escolhido diretamente no passo de atributos.
- Tradução automática dos talentos durante o fluxo de criação. A tradução deve ocorrer no script `translate_drafts.py` como em outros fluxos de pós-processamento.

## Decisions

### Decisão 1: Cache Local de Talentos
Usar o mesmo padrão das espécies para armazenar o arquivo bruto `feats.json` localmente em `content/compendium/feats/.feats_cache.json`. Isso evita lentidão no terminal CLI ao abrir o menu de escolhas.

### Decisão 2: Filtragem por Categoria
Utilizar a taxonomia nativa do 5e.tools:
- **Origem (Origin Feats)**: Filtrar por `source: "XPHB"` e `category: "O"`.
- **Gerais/Combate (General Feats)**: Filtrar por `source: "XPHB"` e `category` igual a `"G"`, `"FS"`, `"FS:P"` ou `"FS:R"`.

Se o download ou parsing falhar, o script deve permitir que o usuário digite o nome do talento manualmente como fallback.

### Decisão 3: Exibição no Terminal
Usar a biblioteca `Rich` para exibir a lista de talentos organizada em 4 colunas horizontais sem borda, garantindo legibilidade e rapidez de seleção.

## Risks / Trade-offs

- **[Risco]** Falha de conexão com os espelhos do 5e.tools ou ausência do arquivo remoto.
  - **Mitigação**: O script captura exceções de rede ou parsing e oferece um prompt de texto simples para o usuário digitar o nome do talento que ele deseja adicionar.
