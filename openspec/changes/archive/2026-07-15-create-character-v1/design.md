## Context

A criação de personagens no GM Vault está sendo reformulada para usar um fluxo interativo mais inteligente guiado pelos dados estruturados do 5e.tools (disponíveis em `races.json` e arquivos de classes). Ao mesmo tempo, a terminologia legada "Raça" está sendo atualizada para "Espécie" (alinhando-se à edição D&D 2024).

## Goals / Non-Goals

**Goals:**
- Renomear fisicamente o compêndio `races` para `species` e atualizar os layouts do site Hugo para refletir a terminologia "Espécie".
- Criar a V1 do script interativo `create_character_v1.py` que guiará o usuário, extraindo dados do 5e.tools sobre a Espécie (e subespécie/variante se houver) e Classe principal selecionadas para preencher automaticamente atributos base, velocidade, dados de vida e sentidos.
- Manter compatibilidade legada com fichas antigas usando `or .Params.char_info.species .Params.char_info.race` nos layouts.

**Non-Goals:**
- Não implementar toda a lógica de perícias adicionais, magias detalhadas ou equipamentos na V1. O foco da V1 é a estrutura básica funcional da ficha (Nome, Espécie/Variante, Classe, Nível, Atributos base calculados, HP base, AC base).

## Decisions

- **Estrutura de Pastas:** Renomearemos `content/compendium/races` para `content/compendium/species`. O frontmatter `kind` para esses arquivos será `species` (ajustando o helper de kind do Hugo se aplicável).
- **Termo do frontmatter de personagens:** Em vez de `char_info.race`, usaremos `char_info.species`. Os layouts do Hugo tentarão ler `char_info.species` primeiro e depois `char_info.race` como fallback.
- **5e.tools Offline/Online:** O script tentará ler os arquivos JSON locais se existirem, caso contrário fará o download da URL correspondente do 5e.tools (usando `dnd_utils.py` já refatorado).

## Risks / Trade-offs

- **Risco:** Algumas fichas legadas ou scripts podem referenciar `/compendium/races/`.
- **Mitigação:** Faremos uma varredura geral e substituição sistemática de `/compendium/races/` para `/compendium/species/` nos arquivos Markdown e scripts ativos do projeto, garantindo a integridade dos links.
