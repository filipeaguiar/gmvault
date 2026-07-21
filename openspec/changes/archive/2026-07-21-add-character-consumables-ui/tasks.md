## 1. Markdown Schema & Character Updates

- [x] 1.1 Adicionar estrutura de Fúria (`consumables`) na ficha de Einvor (`content/campaigns/journeys-through-the-radiant-citadel/characters/einvor.md`).
- [x] 1.2 Adicionar estrutura de Pontos de Foco (`consumables`) na ficha de Durin (`content/campaigns/journeys-through-the-radiant-citadel/characters/durin.md`).
- [x] 1.3 Adicionar estrutura de Pontos de Feitiçaria (`consumables`) na ficha de Violeta (`content/campaigns/journeys-through-the-radiant-citadel/characters/violeta.md`).

## 2. HTML Layout & CSS Styling

- [x] 2.1 Criar classes CSS em `assets/css/` para estilização dos contadores (`consumable-badge`, `badge-rage`, `badge-focus`, `badge-sorcery`).
- [x] 2.2 Alterar o layout/partial de estatísticas superiores do personagem para exibir a lista de `consumables` (com condicional `with` para segurança).
- [x] 2.3 Executar build de teste local do Hugo (`hugo --gc --minify`) para garantir estabilidade e renderização corretas dos badges.
