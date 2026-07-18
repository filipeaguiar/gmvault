## Context

O 5e.tools não fornece uma única propriedade `rolls` para magias. As fórmulas aparecem em tags embutidas em `entries` e `entriesHigherLevel`:

- `{@damage 8d6}` e `{@dice 5d8}` para rolagens base;
- `{@scaledamage 8d6|3-9|1d6}` e `{@scaledice 1d8|1-9|1d8}` para progressão por nível do slot;
- `scalingLevelDice` para patamares explícitos por nível de personagem, principalmente em truques (`1`, `5`, `11`, `17`);
- `spellAttack` para ataques mágicos corpo a corpo ou à distância;
- `damageInflict`, `savingThrow` e `miscTags` para semântica adicional, incluindo cura (`HL`).

Hoje `clean_5etools_tags` transforma parte dessas tags em elementos `data-roll-notation` no corpo, mas o front matter de magia não mantém as fórmulas. A ficha precisa abrir o acordeão para expor a rolagem e não consegue montar uma linha mecânica consistente junto ao nome.

## Goals / Non-Goals

**Goals:**

- Definir um formato canônico, legível e editável para rolagens em `spell_info`.
- Extrair fórmulas sem depender de texto traduzido ou de parsing no template Hugo.
- Exibir rolagens estáticas de dano, cura e dados genéricos ao lado do nome da magia.
- Exibir ataques mágicos usando o bônus atual do personagem.
- Preservar os controles de rolagem existentes no corpo da magia.
- Atualizar magias existentes sem apagar tradução ou conteúdo editorial.

**Non-Goals:**

- Calcular automaticamente todos os efeitos variáveis descritos em prosa.
- Resolver decisões do jogador, como tipo de dano escolhido por `Chromatic Orb`, distribuição de alvos ou agregação dos dardos de `Magic Missile`.
- Inferir escalonamento descrito somente em prosa, como quantidade de raios de Eldritch Blast.
- Escolher automaticamente qual slot o jogador pretende gastar ao conjurar.
- Substituir o bridge progressivo já usado pela integração Dice+.

## Decisions

### 1. Metadados canônicos sob `spell_info`

A página de compêndio usará campos estáveis e independentes do idioma:

```yaml
spell_info:
  level: "3rd level"
  level_number: 3
  attack_type: null
  damage_types:
    - fire
  saving_throws:
    - dexterity
  rolls:
    - kind: damage
      notation: "8d6"
      label: "Dano"
      damage_type: fire
      scaling:
        mode: spell_slot
        thresholds:
          "3": "8d6"
          "4": "9d6"
          "5": "10d6"
```

`kind` aceita inicialmente `damage`, `healing` e `dice`. `attack_type` aceita `melee`, `ranged` ou `null`; a jogada de ataque não é salva como fórmula porque depende de `char_info.spell_attack_bonus`.

Alternativa considerada: armazenar somente HTML pronto. Foi rejeitada porque dificultaria autoria manual, tradução, testes e uso dos mesmos dados em outros layouts.

### 2. Extração orientada às tags do 5e.tools

A extração percorrerá recursivamente `entries` e `entriesHigherLevel`, incluindo strings dentro de estruturas `entries`, listas e tabelas quando aplicável. Tags `damage` geram `kind: damage`; tags `dice` geram `healing` quando `miscTags` contém `HL`, caso contrário `dice`. Tags escaladas enriquecem uma rolagem base equivalente com `scaling` e não criam botões duplicados.

`scalingLevelDice` será normalizado como `mode: character_level`, preservando todos os patamares explícitos. `scaledamage` e `scaledice` serão normalizados como `mode: spell_slot`; intervalos contínuos (`3-9`) e listas de degraus (`3,5,7,9`) serão expandidos em um mapa de patamares e fórmulas. Para níveis entre degraus, vale o maior patamar menor ou igual ao slot usado.

As rolagens serão deduplicadas por semântica e notação normalizada. Espaços em expressões como `1d4 + 1` serão normalizados para `1d4+1`, compatível com Dice+. O cálculo das fórmulas escaladas ocorrerá no importador, não no template Hugo, para manter a apresentação simples e testável.

Alternativa considerada: extrair por regex apenas do Markdown já renderizado. Foi rejeitada porque a tradução ou limpeza do texto pode alterar tags e contexto semântico.

### 3. Partial reutilizável para a linha de rolagens

Um partial Hugo receberá a página da magia e, opcionalmente, o contexto do personagem. Ele renderizará:

- ataque mágico `1d20±N` quando houver `attack_type` e bônus do personagem;
- para `character_level`, somente a fórmula do maior patamar que não exceda `char_info.level`;
- para `spell_slot`, somente fórmulas de níveis presentes em `char_info.spell_slots` com quantidade maior que zero e compatíveis com o nível base da magia;
- a fórmula base para rolagens sem escalonamento;
- nenhum bloco quando a magia não possuir rolagem nem ataque utilizável.

Quando mais de um nível de slot estiver disponível, o partial exibirá controles compactos identificados pelo nível do slot, sem mostrar patamares futuros. Isso inclui a fórmula base no menor slot permitido e as variações estruturadas para slots superiores disponíveis. Fórmulas idênticas resultantes de slots distintos poderão ser agrupadas visualmente, desde que o nível utilizável permaneça claro.

Magic Missile é uma exceção importante: o 5e.tools registra `1d4+1` por dardo e descreve somente em prosa que slots superiores criam mais dardos. Como os dardos podem ter alvos diferentes, o sistema manterá o controle de `1d4+1` por dardo e não inventará `3d4+3`, `4d4+4` ou uma contagem estruturada ausente na fonte. A descrição de nível superior continuará acessível no acordeão. Uma página manual poderá declarar patamares adicionais quando houver revisão editorial explícita.

O partial será usado nas magias preparadas, na lista completa da classe e na página individual da magia. A clonagem já realizada por `spells.js` manterá os controles porque eles estarão dentro do card clonado.

Alternativa considerada: duplicar a lógica nos dois loops da ficha. Foi rejeitada para evitar divergências entre lista preparada, lista de classe e página do compêndio.

### 4. Sincronização não destrutiva

Ao reencontrar uma magia local, o importador atualizará apenas `spell_info` a partir da fonte. Título traduzido, campos editoriais, metadados de tradução e corpo Markdown serão preservados. O archetype documentará os mesmos campos com listas vazias e exemplos seguros.

A migração poderá percorrer magias existentes e executar a mesma sincronização. Falhas de correspondência serão relatadas sem remover arquivos nem dados anteriores.

### 5. Valores canônicos e tradução na apresentação

`kind`, `attack_type`, tipos de dano e resistências permanecem em identificadores canônicos em inglês. Os layouts convertem esses valores para rótulos em português. Isso mantém o front matter previsível para Dice+, scripts e futuras exportações.

## Risks / Trade-offs

- **[Tags complexas ou aninhadas não reconhecidas]** → Usar percurso recursivo e fixtures reais de Fireball, Cure Wounds, Magic Missile, Eldritch Blast e Sleep.
- **[Fórmulas repetidas no corpo e no cabeçalho]** → A repetição é intencional: o cabeçalho oferece acesso rápido e o corpo mantém o contexto da regra.
- **[Cura inferida incorretamente de `dice`]** → Classificar como cura somente quando `miscTags` contém `HL`; manter os demais casos como `dice`.
- **[Muitos níveis de slot podem poluir a linha]** → Renderizar somente slots disponíveis e usar rótulos compactos por nível; nunca mostrar patamares futuros.
- **[Escalonamento existe apenas em prosa]** → Manter a rolagem base por instância, conservar a descrição de nível superior e não inventar multiplicadores, projéteis ou quantidade de ataques.
- **[Sincronização sobrescreve revisão humana]** → Alterar somente `spell_info`, preservando o restante do arquivo e cobrindo o comportamento com teste de regressão.
- **[Magia de ataque sem contexto de personagem]** → Na página do compêndio, mostrar apenas o tipo de ataque; a fórmula dinâmica aparece somente na ficha.

## Migration Plan

1. Implementar e testar a extração estruturada com fixtures do 5e.tools.
2. Atualizar o archetype e os layouts com fallback para magias antigas sem `rolls`.
3. Sincronizar um conjunto pequeno de magias representativas e validar Dice+.
4. Executar a migração sobre `content/compendium/spells/`, mantendo relatório de itens não encontrados.
5. Executar testes Python, build Hugo com drafts e testes do bridge Dice+.

Rollback: reverter os layouts e remover os novos campos de `spell_info` não afeta o corpo Markdown nem as referências existentes.

## Open Questions

- Fórmulas de ataque e dano que criam múltiplos projéteis continuarão representando uma única instância da rolagem base nesta mudança.
- Uma mudança futura poderá permitir escolher interativamente o slot no momento da rolagem em vez de exibir os níveis atualmente disponíveis.
