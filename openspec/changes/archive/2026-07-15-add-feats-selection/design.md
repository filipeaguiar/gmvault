## Context

O script de criação de personagens `create_character.py` é uma ferramenta CLI que auxilia na montagem do YAML de frontmatter das fichas de RPG. Atualmente, ele suporta a seleção e integração de espécie, classe, atributos, salvaguardas, perícias e especializações.

Para completar a criação de personagem de forma aderente às regras modernas (D&D 2024 / Tasha), falta a capacidade de escolher e associar **Talentos (Feats)**, salvando-os de forma estruturada no campo `char_info.feats` e registrando as referências no `compendium_refs` da ficha.

## Goals / Non-Goals

**Goals:**
- Baixar e fazer cache local do arquivo `feats.json` do espelho do 5e.tools em `content/compendium/feats/.feats_cache.json`.
- Filtrar talentos por fonte `XPHB` (D&D 2024) para priorizar a nova edição das regras, mas permitindo exibir talentos de outras fontes (ex: `TCE`, `XGE`, `PHB`) caso o jogador prefira.
- Implementar prompt de seleção para Talentos de Origem (*Origin Feats*, categoria `O`) no nível 1, exibindo suas fontes de origem e permitindo ao usuário digitar múltiplos números separados por vírgula em um único prompt.
- Implementar prompt de seleção para múltiplos Talentos Gerais ou de Estilo de Combate (*General Feats* / *Fighting Style*, categorias `G` e `FS`), exibindo suas fontes e permitindo a seleção múltipla por vírgula.
- Fazer download automático das descrições dos talentos selecionados para `content/compendium/feats/` e vinculá-las no compêndio da ficha.

**Non-Goals:**
- Ajustar atributos base automaticamente baseando-se em talentos ("half-feats"). Como a interface de atributos já permite bônus customizados livremente, o jogador ajusta seus atributos base de acordo com o talento escolhido diretamente no passo de atributos.
- Tradução automática dos talentos durante o fluxo de criação. A tradução deve ocorrer no script `translate_drafts.py` como em outros fluxos de pós-processamento.

## Decisions

### Decisão 1: Cache Local de Talentos
Usar o mesmo padrão das espécies para armazenar o arquivo bruto `feats.json` localmente em `content/compendium/feats/.feats_cache.json`. Isso evita lentidão no terminal CLI ao abrir o menu de escolhas.

### Decisão 2: Filtragem por Categoria e Exibição de Fonte
Utilizar a taxonomia nativa do 5e.tools:
- **Origem (Origin Feats)**: Filtrar por categoria `O`.
- **Gerais/Combate (General Feats)**: Filtrar por categoria igual a `"G"`, `"FS"`, `"FS:P"` ou `"FS:R"`.

Os talentos exibidos serão etiquetados com sua fonte oficial (ex: `Alert (XPHB)`, `Elven Accuracy (XGE)`) para que o usuário identifique facilmente as regras modernas de 2024 vs legadas de 2014.

### Decisão 3: Digitação Múltipla Separada por Vírgula
Substituir a escolha de "um por um" pela digitação de múltiplos números separados por vírgula (idêntico ao fluxo de Perícias). O usuário poderá digitar `1, 4` para selecionar os talentos desejados de uma única vez. Se não quiser nenhum talento, basta apertar Enter (vazio).

## Risks / Trade-offs

- **[Risco]** Falha de conexão com os espelhos do 5e.tools ou ausência do arquivo remoto.
  - **Mitigação**: O script captura exceções de rede ou parsing e oferece um prompt de texto simples para o usuário digitar o nome do talento que ele deseja adicionar.
