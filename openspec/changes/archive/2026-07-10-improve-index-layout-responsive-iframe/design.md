## Context

O site é um Hugo estático com layouts próprios e conteúdo Markdown. A navegação principal de páginas de índice é gerada por `layouts/_default/list.html` e `layouts/partials/child_pages.html`, enquanto breadcrumbs e relações são gerados por partials separados.

O uso pretendido dentro de iframe muda a prioridade visual: páginas de índice precisam ser compactas, previsíveis e utilizáveis em larguras reduzidas. Além disso, páginas com `visibility: players` ou `visibility: public` não devem oferecer caminhos gerados automaticamente para conteúdo `gm`, pois isso pode revelar spoilers mesmo sem autenticação real.

Há também inconsistência de metadados: vários arquivos usam `params.kind`, enquanto layouts consultam `.Params.kind`. A mudança deve preservar compatibilidade com o conteúdo existente.

## Goals / Non-Goals

**Goals:**
- Melhorar páginas de índice/lista para navegação ordenada, precisa e responsiva.
- Garantir layout adequado em iframe e em largura baixa.
- Centralizar ou padronizar a resolução de `kind` com fallback para `params.kind`.
- Filtrar navegação gerada em páginas player/public para não apontar para páginas GM.
- Manter implementação leve, sem JavaScript obrigatório e sem tema externo.

**Non-Goals:**
- Implementar autenticação, autorização ou proteção real de conteúdo GM.
- Migrar obrigatoriamente todos os arquivos Markdown existentes.
- Reestruturar toda a árvore de conteúdo.
- Alterar o formato GMVault JSON, exceto se algum helper compartilhado for reutilizado sem mudar contrato.

## Decisions

### 1. Usar helpers/partials pequenos para resolver metadados
Criar partials ou padrões locais reutilizáveis para resolver `kind` e `visibility` efetivos:

```text
kind efetivo       = .Params.kind || .Params.params.kind
visibility efetiva = .Params.visibility, com regras especiais existentes quando necessário
```

Racional: evita migração em massa e corrige todos os layouts que dependem de tipo. Alternativa considerada: migrar todo o conteúdo para `kind` no topo. Isso é mais limpo a longo prazo, mas maior e mais arriscado para esta mudança.

### 2. Filtrar navegação na origem da renderização
As listas automáticas devem decidir se um filho pode ser exibido antes de gerar o link:

```text
Página atual player/public?
├── sim  → mostrar apenas filhos players/public; omitir GM
└── não  → mostrar filhos normalmente
```

Racional: é melhor omitir links perigosos do que renderizá-los desabilitados. Alternativa considerada: mostrar links GM com aviso. Isso ainda expõe títulos e estrutura de spoiler.

### 3. Relações em páginas player/public devem ser seguras por destino
Mesmo para `compendium_refs`, o destino deve ser avaliado. Em páginas player/public, links só devem aparecer quando a página destino também for player/public ou for um tipo explicitamente seguro para jogadores conforme metadados.

Racional: o campo de origem não garante segurança se o destino estiver marcado como GM. Alternativa considerada: confiar no nome do campo `compendium_refs`. Isso pode vazar páginas do compêndio marcadas como GM.

### 4. Índices responsivos com CSS Grid adaptativo
Cards de índice devem usar grid com `auto-fit`/`minmax` em larguras médias e virar coluna única em larguras baixas. Cards devem evitar overflow horizontal, usar títulos quebráveis e metadados compactos.

Racional: funciona dentro de iframe sem JavaScript e preserva desempenho. Alternativa considerada: calcular layout com JS. Isso viola a direção leve do projeto.

### 5. Ordenação determinística
Itens em índices devem ser ordenados por `weight` e título resolvido (`titulo_pt_br` ou `Title`). Quando Hugo não oferecer ordenação composta direta suficiente, usar `ByWeight` e manter títulos consistentes como desempate aceitável, ou aplicar ordenação adicional em grupos específicos.

Racional: a navegação precisa ser previsível durante a sessão. Alternativa considerada: ordem do filesystem. Isso é menos explícito e pode variar conforme criação/importação.

## Risks / Trade-offs

- Filtro por `visibility` pode ocultar páginas sem `visibility` definido → Mitigar tratando ausência como GM por padrão em contexto player/public.
- Compatibilidade com `params.kind` pode espalhar lógica se não centralizada → Mitigar usando helper/partial ou variável local padrão em cada partial alterado.
- Omissão de links GM não é segurança real → Mitigar mantendo documentação/semântica de `visibility` como editorial e não autenticação.
- Melhorias CSS podem afetar páginas específicas com partials customizados → Mitigar com classes específicas para índices e testes visuais em home, campanhas, compêndio e seções de campanha.
