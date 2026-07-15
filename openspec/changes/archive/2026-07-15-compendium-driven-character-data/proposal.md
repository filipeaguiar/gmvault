## Why

As fichas de personagem armazenam no frontmatter descrições extensas de ações, traços raciais, talentos e características de classe. Em Pinky, por exemplo, várias descrições estão em inglês e duplicam conteúdo já disponível no compêndio, dificultando tradução, manutenção e correções centralizadas. O problema precisa ser corrigido tanto nas fichas atuais quanto no fluxo de criação de novas fichas. O compêndio deve ser a fonte de verdade: a ficha deve manter apenas dados específicos do personagem e referências internas, enquanto o Hugo resolve e renderiza o conteúdo relacionado durante o build.

## What Changes

- Analisar e refatorar a ficha de Pinky como caso de migração, preservando no frontmatter apenas dados específicos da personagem e metadados operacionais, como usos, recarga, preparo, quantidade e fórmulas.
- Substituir descrições duplicadas de ações, traços raciais, talentos, características de classe, propriedades de armas e detalhes de itens por referências internas ao compêndio.
- Atualizar o layout de personagem para resolver referências com `site.GetPage`, renderizar o conteúdo da nota correspondente e usar fallback explícito quando uma referência não puder ser resolvida.
- Ajustar o importador de personagens para gerar novas fichas no formato referencial, sem reintroduzir descrições textuais duplicadas no frontmatter.
- Estender a sincronização local de personagens para descobrir, validar e manter referências de ações e características além de magias, equipamentos, classes, raças e talentos.
- Criar ou completar notas do compêndio para conteúdos reutilizáveis identificados durante a análise de Pinky, mantendo tradução e revisão editorial nas notas compartilhadas.
- Atualizar o archetype `archetypes/character.md` para que novas fichas já nasçam com o formato referencial e sem campos de descrição duplicada.
- Auditar scripts auxiliares relacionados, incluindo `translate_drafts.py`, para preservar e processar corretamente referências sem transformar URLs e metadados em texto duplicado.
- Documentar quais dados continuam específicos da ficha e quais devem obrigatoriamente ser obtidos do compêndio.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `rpg-character-sheet`: fichas devem resolver e renderizar ações, traços, talentos, características e itens referenciados no compêndio durante o build, sem depender de descrições duplicadas no frontmatter.
- `local-character-sync-tools`: a sincronização deve manter referências de conteúdo reutilizável e identificar referências ausentes para ações e características do personagem.
- `import-tools`: os importadores e processadores auxiliares devem produzir frontmatter referencial, preservar referências e manter no personagem somente dados específicos e operacionais.
- `content-model`: o archetype de personagem deve gerar a estrutura referencial usada por fichas atuais e futuras.

## Impact

- `content/campaigns/journeys-through-the-radiant-citadel/characters/pinky.md`, demais fichas e notas relacionadas em `content/compendium/`.
- `layouts/partials/kinds/character.html` e possivelmente parciais auxiliares de resolução de relações.
- `scripts/sync_character.py`, `import_dndbeyond.py`, `translate_drafts.py` e testes relacionados.
- `archetypes/character.md`, que define a estrutura inicial de novas fichas.
- Especificações do modelo de ficha, sincronização local, archetypes e ferramentas de importação.
- O conteúdo publicado poderá mudar de idioma e de origem de renderização, mas referências internas e fallback devem manter o build funcional durante a migração.
