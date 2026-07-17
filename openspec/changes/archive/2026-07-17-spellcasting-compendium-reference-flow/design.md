## Context

A ficha renderiza hoje `char_info.spells` como lista superior e `char_info.class_spells` como catálogo inferior. As duas estruturas repetem parcialmente identidade e nível, enquanto o conteúdo detalhado já é resolvido por `site.GetPage`. O JavaScript clona cards completos para simular preparo em `localStorage`, troca o controle por um badge “Preparada” e filtra dez níveis fixos. Os importadores, por sua vez, nem sempre garantem que toda entrada possua `ref`, calculam slots por uma classe principal e podem manter duplicatas oriundas de várias fontes.

O repositório já possui o caminho adequado para conteúdo compartilhado: `dnd_utils.fetch_from_5etools("spell", name)` cria ou sincroniza uma página em `content/compendium/spells/` com `spell_info`, incluindo metadados estruturados de rolagem. A mudança deve consolidar esse contrato sem adicionar backend, framework JavaScript ou persistência editorial no navegador, e deve continuar renderizando fichas legadas.

## Goals / Non-Goals

**Goals:**

- Garantir que toda magia produzida pelos fluxos de personagem tenha uma página canônica resolvível no compêndio, alimentada pelo 5e.tools.
- Manter na ficha somente referências e estado operacional específico do personagem.
- Construir uma visão normalizada e deduplicada para renderização a partir das referências atuais e legadas.
- Separar visualmente magias prontas para uso, no topo, das demais magias referenciadas, em uma lista inferior de gerenciamento.
- Expor preparo somente onde o perfil ou a entrada permitir e manter os demais perfis em leitura.
- Renderizar somente níveis e trackers acessíveis ao personagem.
- Preservar integralmente `spell_info` e os controles/atributos usados pela integração Dice+ durante filtros e mudanças locais de preparo.

**Non-Goals:**

- Implementar edição persistente do Markdown pelo navegador ou tratar `localStorage` como fonte canônica.
- Baixar toda a coleção de magias do 5e.tools sem que ela seja referenciada por um personagem ou catálogo selecionado.
- Reimplementar todas as regras de multiclass spell slots ou validar integralmente regras de preparação do sistema.
- Alterar o protocolo da extensão Owlbear/Dice+ ou inferir rolagens a partir de prosa.
- Remover imediatamente os campos legados `name`, `level`, `prepared`, `class_spells` ou seus fallbacks.

## Decisions

### 1. O compêndio será a fonte canônica de identidade, nível, conteúdo e mecânica

Cada magia nova selecionada ou importada será primeiro resolvida por `fetch_from_5etools("spell", name)`. Somente uma referência retornada e uma página local existente serão consideradas uma associação canônica. `spell_info` fornecerá nível, escola, casting time, alcance, duração e rolagens; a ficha manterá apenas `ref` e atributos operacionais como `prepared`, `availability`, `source` e `usage` quando aplicáveis.

A sincronização deve ser não destrutiva e preservar tradução, corpo revisado e metadados editoriais locais, conforme o comportamento já esperado do fetch/sync de magias.

**Alternativa considerada:** copiar os dados do 5e.tools para cada entrada de `char_info.spells`. Rejeitada porque duplica regras, diverge após sincronizações e enfraquece o compêndio como fonte compartilhada.

### 2. A renderização usará uma coleção normalizada derivada, sem exigir migração imediata

Um partial/helper de Hugo deverá montar um conjunto deduplicado por `ref` usando, nesta ordem:

1. entradas operacionais de `char_info.spells`;
2. referências de catálogo em `char_info.class_spells`;
3. referências de magia presentes em `compendium_refs`.

Somente páginas resolvidas cujo `kind`/`params.kind` seja `spell` participarão da coleção canônica. Entradas operacionais manterão precedência sobre referências de catálogo. Nome e nível serão lidos da página; campos inline serão usados apenas para fallback legado quando a referência estiver ausente ou não resolver.

A coleção será classificada em:

- **ready**: cantrips e magias conhecidas para perfis `known`/`pact`; magias `prepared`, `always` ou `granted`; e entradas explicitamente prontas por sua fonte;
- **management**: demais referências deduplicadas que não estão em `ready`.

Para perfil `hybrid`, uma propriedade por entrada (`availability` e/ou `can_prepare`) terá precedência sobre a regra global. Sem metadado suficiente, a entrada degrada para leitura em vez de oferecer uma ação potencialmente inválida.

**Alternativa considerada:** migrar todas as fichas para um novo bloco único antes de alterar o layout. Rejeitada porque seria destrutiva, aumentaria o risco editorial e impediria implantação incremental.

### 3. O contrato operacional será ampliado de forma compatível

Novos geradores poderão emitir entradas mínimas como:

```yaml
char_info:
  spells:
    - ref: "/compendium/spells/bless/"
      prepared: true
      availability: "prepared"
      source: "cleric"
      usage: "1 action"
```

`availability` aceitará estados operacionais como `prepared`, `known`, `always` e `granted`. `can_prepare` na entrada poderá sobrescrever o perfil global para fontes híbridas. Os campos inline `name` e `level` deixam de ser necessários em conteúdo novo, mas seguem suportados como fallback.

`char_info.class_spells` permanece temporariamente como lista de referências de catálogo para compatibilidade. Ele não contém descrição nem mecânica e não é fonte de verdade; pode futuramente ser renomeado por mudança separada.

### 4. Níveis acessíveis serão derivados dos recursos reais do personagem

O layout calculará níveis acessíveis pela união de:

- nível `0` quando houver cantrip referenciado pronto ou gerenciável;
- chaves de `char_info.spell_slots` com quantidade maior que zero;
- nível de pact slot exposto pelo perfil/dados existentes;
- níveis de magias `always`/`granted` prontas que não consumam slots normais.

Os botões de filtro e cabeçalhos serão gerados apenas para essa união. O tracker continuará usando exclusivamente grupos de slots com quantidade positiva. Uma magia de catálogo acima do maior círculo acessível não será exibida na lista de gerenciamento, ainda que a lista completa da classe a referencie.

**Alternativa considerada:** continuar renderizando níveis 0–9 fixos e apenas ocultar cards. Rejeitada porque comunica acesso inexistente e piora a consulta em telas pequenas.

### 5. A lista superior será operacional e não repetirá o badge de preparo

O título e a descrição da seção superior indicarão que as magias estão prontas para uso. Cards dessa seção não exibirão badge “Preparada” individual. Badges que representem informações não redundantes, como fonte concedida ou estado conhecido quando necessário para um perfil híbrido, podem permanecer.

A lista inferior conterá somente referências não presentes na lista superior. Checkboxes serão renderizados apenas para entradas preparáveis; perfis conhecidos, pact, espontâneos ou concedidos permanecem em leitura. A busca e o filtro de nível atuarão nas duas listas sem duplicar uma magia.

### 6. A interação moverá nós preservando controles Dice+

Os cards serão renderizados uma vez com o partial de `helpers/spell-rolls.html` e terão um identificador estável por `ref`. Ao preparar/despreparar, o JavaScript moverá o mesmo nó entre as listas, ou reconstruirá a partir de um `<template>` canônico que preserve todos os atributos e descendentes. Não substituirá o HTML do controle de rolagem nem removerá `data-roll-notation` e metadados correlatos.

O estado local continuará separado por pathname e armazenará apenas refs preparadas e slots consumidos. Refs desconhecidas, inacessíveis ou não preparáveis serão descartadas ao restaurar estado antigo. Sem JavaScript ou `localStorage`, a lista inicial gerada pelo Hugo continuará funcional e legível.

**Alternativa considerada:** clonar cards e reescrever o badge como hoje. Rejeitada porque cria cópias divergentes, pode duplicar IDs/listeners e ameaça os metadados Dice+.

### 7. Os fluxos Python compartilharão normalização e deduplicação

`dnd_utils.py` concentrará helpers para:

- materializar uma magia pelo nome no compêndio;
- construir a entrada operacional mínima com `ref`;
- deduplicar magias por referência, mesclando estado sem perder `prepared`, fonte ou uso;
- inferir perfil e níveis acessíveis a partir das entradas normalizadas.

`create_character.py`, `edit_character.py` e `import_dndbeyond.py` usarão esses helpers em vez de construir refs condicionais de forma independente. Uma magia que não puder ser resolvida no 5e.tools não será adicionada como nova entrada canônica; o fluxo informará a falha. Dados legados já presentes continuarão renderizáveis pelo fallback.

## Risks / Trade-offs

- **[Catálogos de classe podem ser grandes e gerar muitas páginas draft]** → importar somente referências exigidas pelo fluxo escolhido, deduplicar antes do fetch e documentar o custo quando o usuário solicitar a lista completa da classe.
- **[Dados de D&D Beyond e 5e.tools podem usar nomes/fontes diferentes]** → centralizar aliases e resolução, registrar falhas claramente e nunca substituir silenciosamente uma magia por correspondência ambígua.
- **[Multiclasse possui slots e regras de preparo mais complexos que a inferência atual]** → permitir metadado por entrada e degradar ações incertas para leitura; cobrir cálculo completo em mudança separada.
- **[Estado local pode divergir do front matter]** → tratar `localStorage` apenas como estado temporário da sessão e validar refs/permissões ao restaurá-lo.
- **[Páginas de magia draft podem não existir em build de produção]** → manter fallback não fatal na ficha e testes com `hugo -D` e sem drafts; a publicação continua uma decisão editorial.
- **[Mover cards pode interferir na inicialização Dice+]** → preservar os mesmos nós/atributos, evitar HTML reconstruído e incluir testes de renderização e runtime da extensão.

## Migration Plan

1. Adicionar helpers e testes de normalização/materialização sem alterar fichas existentes.
2. Atualizar os três fluxos de personagem para produzir refs deduplicadas e estado operacional mínimo.
3. Introduzir a coleção normalizada e o novo layout com fallback para o modelo atual.
4. Atualizar JavaScript/CSS e validar filtros, preparo local, slots e Dice+.
5. Atualizar archetype e documentação do contrato.
6. Validar fichas preparadas, conhecidas, pact e híbridas, seguidas de builds Hugo com e sem drafts.

Rollback: restaurar o layout e JavaScript anteriores. Como os novos campos são aditivos e `ref` já é suportado, o conteúdo gerado continuará legível pelo fallback; nenhuma migração destrutiva deverá ser necessária.

## Open Questions

- Para perfis híbridos importados do D&D Beyond, quais identificadores de origem são suficientemente estáveis para definir `can_prepare` sem uma tabela manual extensa?
- O conjunto completo de classe deve continuar em `char_info.class_spells` ou migrar futuramente para um nome neutro como `spell_catalog_refs`?
- Magias concedidas acima do círculo normal devem aparecer também no filtro do nível próprio ou em um filtro separado de fonte? Este design adota o nível próprio inicialmente.
