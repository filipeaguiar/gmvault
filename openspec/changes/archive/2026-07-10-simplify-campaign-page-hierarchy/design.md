## Context

A estrutura atual cumpre a hierarquia conceitual, mas faz isso com muitos diretórios intermediários:

```text
content/campaigns/<campaign>/adventures/<adventure>/
├── _index.md
└── sessions/
    ├── _index.md
    └── <session>/
        ├── _index.md
        └── scenes/
            ├── _index.md
            └── <scene>.md
```

Na prática, `sessions/` e `scenes/` funcionam principalmente como contêineres/indexadores. Para campanhas importadas, isso gera centenas de `_index.md`, URLs longas e uma estrutura difícil de editar manualmente.

O objetivo é manter a semântica de `Aventura → Sessão → Cena`, mas simplificar a árvore física:

```text
content/campaigns/<campaign>/adventures/<adventure>/
├── _index.md                 # kind: adventure
└── <session>/
    ├── _index.md             # kind: session
    └── <scene>.md            # kind: scene
```

## Goals / Non-Goals

**Goals:**
- Remover `sessions/` e `scenes/` como diretórios obrigatórios para novo conteúdo.
- Manter `adventure`, `session` e `scene` como entidades de conteúdo distintas.
- Manter compatibilidade de renderização/exportação com a estrutura legada.
- Atualizar importadores para gerar a estrutura simplificada.
- Atualizar navegação automática e GMVault JSON para detectar os dois formatos durante transição.
- Reduzir profundidade de URL e número de `_index.md` gerados.

**Non-Goals:**
- Remover o conceito de sessões.
- Remover o conceito de cenas.
- Migrar obrigatoriamente todo conteúdo existente em uma única etapa destrutiva.
- Criar banco de dados, aliases complexos ou roteamento dinâmico.
- Resolver tradução ou revisão editorial de conteúdo importado.

## Decisions

### 1. Novo modelo canônico sem diretórios indexadores `sessions` e `scenes`
Modelo canônico para novas aventuras:

```text
adventures/<adventure-slug>/
├── _index.md
└── <session-slug>/
    ├── _index.md
    ├── <scene-1>.md
    ├── <scene-2>.md
    └── <scene-3>.md
```

Racional: preserva a árvore Hugo de páginas pai/filho, reduz dois níveis de diretório por cena e elimina `_index.md` que existem apenas para listar coleções técnicas.

Alternativa considerada:

```text
adventures/<adventure>/sessions/<session>/<scene>.md
```

Essa opção removeria apenas `scenes/`, mas ainda manteria um diretório `sessions/` com pouco valor editorial.

### 2. Compatibilidade legada por detecção flexível
Layouts, partials e exportadores devem procurar sessões e cenas nos dois formatos:

```text
Novo:
adventures/<adv>/<session>/_index.md
adventures/<adv>/<session>/<scene>.md

Legado:
adventures/<adv>/sessions/<session>/_index.md
adventures/<adv>/sessions/<session>/scenes/<scene>.md
```

Racional: evita migração obrigatória e permite que conteúdo antigo continue navegável.

### 3. `kind` determina semântica, não o nome do diretório
A detecção deve priorizar `kind: session` e `kind: scene` em vez de depender exclusivamente de caminhos contendo `sessions` ou `scenes`.

Racional: permite estrutura física mais simples sem perder semântica.

### 4. O importador de campanha é o ponto principal da mudança
O nesting excessivo é gerado principalmente por `import_campaign.py`. A implementação deve começar por ele, não por migração manual.

`import_campaign.py` deve criar sessões diretamente sob a aventura e cenas diretamente dentro da sessão:

```text
adv_dir/<session-slug>/_index.md
adv_dir/<session-slug>/<scene-slug>.md
```

Racional: importações são a maior fonte de nesting excessivo. Corrigir a origem impede que novas campanhas importadas continuem criando a estrutura longa.

### 5. Migração opcional, não obrigatória
Pode haver script ou tarefa manual de migração depois, mas esta mudança deve priorizar:

- importações futuras no formato simplificado;
- novo conteúdo manual no formato simplificado;
- leitura do formato legado;
- documentação do formato canônico.

Racional: mover centenas de arquivos pode quebrar URLs e diffs em massa. A migração pode ser feita quando houver decisão explícita sobre aliases/redirects.

## Risks / Trade-offs

- URLs antigas e novas podem coexistir → Mitigar documentando formato canônico e mantendo compatibilidade de leitura.
- Listagens podem duplicar sessões se uma aventura tiver ambos os formatos → Mitigar filtrando por `kind` e evitando contar diretórios indexadores técnicos como sessões reais.
- Export GMVault pode perder cenas se assumir paths antigos → Mitigar criando helpers de descoberta por `kind`.
- Importador pode gerar nomes que colidem com arquivos de suporte no diretório da aventura → Mitigar prefixando sessões importadas com `001-`, `002-`, etc.
- Sem `sessions/_index.md`, perde-se página agregadora intermediária → Mitigar listando sessões diretamente na página da aventura.
- Sem `scenes/_index.md`, perde-se página agregadora intermediária → Mitigar listando cenas diretamente na página da sessão.
