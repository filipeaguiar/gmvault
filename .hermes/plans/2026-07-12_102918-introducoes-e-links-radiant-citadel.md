# Introduções editoriais e correção de links da Cidadela Radiante — Plano de Implementação

> **Para o Hermes:** executar este plano tarefa por tarefa com TDD estrito (RED → GREEN → REFACTOR). Não fazer commit nem push sem aprovação explícita do usuário.

**Objetivo:** representar introduções de campanha e de aventura como conteúdo editorial incorporado às respectivas páginas principais, sem duplicá-las nas grades de navegação, e eliminar links quebrados na versão GitHub Pages do GMvault.

**Arquitetura:** adicionar um papel editorial explícito e reutilizável no front matter (`params.content_role: introduction`) e fazer os templates Hugo agregarem os filhos introdutórios por `weight`. Links internos devem ser resolvidos pelo Hugo (`ref`, `relref`, `.RelPermalink` ou `relURL`) em vez de URLs raiz literais, preservando o subcaminho `/gmvault/`. O importador registra classificação e ordem; a tradução não pode alterar destinos estruturais.

**Stack:** Python 3.11, `unittest`, PyYAML, Hugo, Go templates, HTML/link crawler local, GitHub Pages.

---

## Diagnóstico confirmado antes da execução

1. A página publicada contém dois links rápidos sem o prefixo `/gmvault/`:
   - `https://filipeaguiar.github.io/campaigns/.../journal/`
   - `https://filipeaguiar.github.io/campaigns/.../adventures/`
2. A origem está em `content/campaigns/journeys-through-the-radiant-citadel/_index.md`, que usa links Markdown absolutos iniciados em `/campaigns/...`.
3. `hugo.yaml` define `baseURL: https://filipeaguiar.github.io/gmvault/`; portanto links iniciados em `/` ignoram o subcaminho. Essa falha específica não parece ter sido causada pela tradução.
4. Os links produzidos pelos templates com `.RelPermalink` incluem `/gmvault/` corretamente.
5. O diretório de trabalho já contém alterações não commitadas, um checkpoint `*.translation.partial`, conteúdo de compêndio e imagens não rastreadas. A implementação deve preservar tudo e limitar cada alteração aos arquivos aprovados.

---

## Critérios de aceitação

- [ ] A introdução geral do livro aparece na página principal da campanha.
- [ ] A introdução não aparece novamente como card de aventura.
- [ ] A introdução de cada aventura aparece antes das sessões/cenas da própria aventura.
- [ ] Páginas introdutórias não aparecem novamente como cards de sessão/cena.
- [ ] Introduções e conteúdo normal respeitam `weight`, com título como desempate determinístico.
- [ ] O importador grava `params.content_role: introduction` sem depender do título depois da importação.
- [ ] Tradução preserva slugs, `ref`/`relref`, destinos Markdown, URLs e campos estruturais de front matter.
- [ ] Todos os `href` e `src` internos do build público resolvem para um arquivo/âncora existente ou são explicitamente classificados como indisponíveis/draft.
- [ ] Nenhum link interno publicado escapa de `/gmvault/` por erro de URL raiz.
- [ ] Build Hugo normal passa sem `--buildDrafts`.
- [ ] O checkpoint parcial da tradução permanece preservado até uma tarefa específica de retomada.

---

### Tarefa 1: Congelar e inventariar o estado atual

**Objetivo:** separar alterações existentes das que serão feitas por este trabalho.

**Arquivos:** nenhum arquivo de produto deve ser alterado.

**Passos:**

1. Registrar `git status --short --branch`, `git diff --stat` e a lista de não rastreados relevantes.
2. Salvar, fora do Git ou em relatório temporário, os hashes SHA-256 dos arquivos já modificados que serão tocados.
3. Localizar todos os `*.translation.partial`; confirmar especialmente:
   `content/campaigns/journeys-through-the-radiant-citadel/adventures/welcome-to-the-radiant-citadel/001-inicio/02-using-the-adventures.md.translation.partial`.
4. Não restaurar, mover, substituir nem incluir automaticamente os arquivos não rastreados.
5. Criar uma lista de escopo permitida para a execução: importador, tradutor, templates, testes e front matters da campanha.

**Verificação:** repetir os hashes antes de cada fase destrutiva e confirmar que alterações preexistentes fora do escopo continuam intactas.

---

### Tarefa 2: Criar auditor determinístico de links do build

**Objetivo:** produzir uma lista completa e reproduzível de links quebrados, em vez de corrigir apenas os exemplos visíveis.

**Arquivos:**
- Criar: `tests/test_internal_links.py`
- Criar: `scripts/check_internal_links.py` (ou helper equivalente dentro de `tests/`, se não houver convenção de scripts)

**Ciclo TDD:**

1. Criar fixture HTML com:
   - link válido sob `/gmvault/`;
   - link raiz incorreto `/campaigns/...`;
   - arquivo de imagem ausente;
   - fragmento `#ancora` ausente;
   - URL externa, que deve ser ignorada ou auditada separadamente.
2. Executar `python -m unittest tests.test_internal_links -v` e registrar RED.
3. Implementar o crawler mínimo com `html.parser` da biblioteca padrão:
   - coletar `href`, `src` e fragmentos;
   - normalizar `baseURL` e percent-encoding;
   - mapear URLs para arquivos do diretório publicado;
   - distinguir `missing-file`, `missing-anchor`, `outside-base-path` e `external`.
4. Executar novamente e registrar GREEN.
5. Gerar build local:
   ```bash
   hugo --destination /tmp/gmvault-link-audit
   .venv/bin/python scripts/check_internal_links.py \
     --public /tmp/gmvault-link-audit \
     --base-url https://filipeaguiar.github.io/gmvault/ \
     --scope campaigns/journeys-through-the-radiant-citadel/
   ```
6. Salvar relatório com URL de origem, destino, tipo do erro e arquivo fonte provável.

**Verificação:** o relatório deve capturar os dois links rápidos já confirmados e não marcar os cards gerados por `.RelPermalink` como quebrados.

---

### Tarefa 3: Definir o contrato de front matter para papel editorial

**Objetivo:** formalizar um único metadado para introduções em qualquer nível.

**Arquivos:**
- Criar ou modificar teste: `tests/test_content_roles.py`
- Modificar documentação existente apropriada; se não houver, criar `docs/content-roles.md`

**Contrato proposto:**

```yaml
params:
  kind: adventure
  content_role: introduction
weight: 10
```

Para filhos de aventura:

```yaml
params:
  kind: scene
  content_role: introduction
weight: 10
```

Ausência de `content_role` significa conteúdo normal. Nesta fase, implementar apenas `introduction`; não criar papéis futuros sem necessidade.

**Ciclo TDD:**

1. Criar testes de leitura/classificação para `introduction`, conteúdo normal e valor desconhecido.
2. Registrar RED.
3. Implementar helper único de classificação, evitando lógica duplicada no importador e testes.
4. Registrar GREEN.

**Decisão importante:** títulos como `Introduction`, `Adventure Background` e `Running the Adventure` são apenas heurísticas de importação; templates nunca devem classificar por título.

---

### Tarefa 4: Marcar introduções durante a importação do 5e.tools

**Objetivo:** preservar ordem e função editorial já no momento da importação.

**Arquivos:**
- Modificar: `import_campaign.py`
- Criar: `tests/test_import_campaign_content_roles.py`
- Possivelmente modificar: `interactive_cli.py` e `tests/test_interactive_cli.py`

**Ciclo TDD:**

1. Criar fixture mínima semelhante a `adv_data["data"]` com:
   - capítulo introdutório geral;
   - primeira aventura real;
   - seções introdutórias dentro da aventura;
   - primeira cena jogável.
2. Testar que a ordem de entrada vira `weight` explícito (`10`, `20`, ...).
3. Testar que o capítulo geral recebe `content_role: introduction`.
4. Testar que antecedentes/ganchos/preparação da aventura recebem o mesmo papel no nível da aventura.
5. Testar que uma cena jogável não recebe o papel.
6. Registrar RED.
7. Extrair uma função pura de classificação; usar heurísticas conservadoras e permitir confirmação numerada no modo interativo quando houver ambiguidade.
8. Persistir a decisão no front matter.
9. Registrar GREEN.

**Proteção:** reimportações devem ser idempotentes e não apagar uma classificação corrigida manualmente sem confirmação.

---

### Tarefa 5: Renderizar a introdução da campanha e removê-la da grade

**Objetivo:** incorporar `Welcome to the Radiant Citadel` à página da campanha.

**Arquivos:**
- Modificar: `layouts/partials/kinds/campaign.html`
- Criar: `layouts/partials/editorial_introduction.html`
- Criar: `tests/test_campaign_introduction_rendering.py`
- Modificar front matter: `content/campaigns/journeys-through-the-radiant-citadel/adventures/welcome-to-the-radiant-citadel/_index.md`

**Ciclo TDD:**

1. Montar site Hugo temporário com campanha, uma introdução e uma aventura normal.
2. Testar que o HTML da campanha contém o conteúdo introdutório antes da grade.
3. Testar que a introdução não gera card em “Aventuras / Arcos de Jogo”.
4. Testar que a aventura normal continua na grade.
5. Testar ordenação dos fragmentos introdutórios por `weight` e título.
6. Registrar RED.
7. Implementar partial reutilizável que selecione filhos com `.Params.content_role == "introduction"`.
8. Filtrar esses filhos da grade de aventuras.
9. Registrar GREEN.

**Limite:** não copiar o texto para o `_index.md` da campanha. O conteúdo deve continuar com uma única fonte e ser agregado pelo Hugo.

---

### Tarefa 6: Renderizar introduções das aventuras e removê-las das cenas

**Objetivo:** usar o mesmo mecanismo na página principal de cada aventura.

**Arquivos:**
- Modificar: template de aventura identificado pela resolução de `params.kind` (provável `layouts/partials/kinds/adventure.html`)
- Modificar: `layouts/partials/kinds/session.html` quando a introdução estiver modelada abaixo de sessão
- Reutilizar: `layouts/partials/editorial_introduction.html`
- Criar: `tests/test_adventure_introduction_rendering.py`

**Ciclo TDD:**

1. Criar fixture Hugo com aventura contendo duas seções introdutórias e duas cenas.
2. Testar que introduções aparecem antes da navegação jogável.
3. Testar que não são repetidas como cards.
4. Testar que cenas normais permanecem navegáveis.
5. Testar `weight` e fallback por título.
6. Registrar RED.
7. Implementar usando o mesmo partial da campanha, sem duplicar seleção/ordenação.
8. Registrar GREEN.

**Regra editorial:** introdução pode abranger mais de um arquivo — antecedentes, ganchos, sinopse e orientação ao Mestre — e não apenas o primeiro arquivo.

---

### Tarefa 7: Corrigir geração de links internos e tornar o importador independente do subcaminho

**Objetivo:** impedir URLs que funcionam em domínio raiz, mas quebram em GitHub Pages sob `/gmvault/`.

**Arquivos:**
- Modificar: `import_campaign.py` nas linhas que geram “Links Rápidos”
- Modificar: `content/campaigns/journeys-through-the-radiant-citadel/_index.md`
- Criar ou ampliar: `tests/test_internal_links.py`

**Abordagem:**

1. Preferir links resolvidos pelo Hugo:
   ```markdown
   [Aventuras Ativas]({{< relref "adventures" >}})
   ```
   ou eliminar links manuais redundantes quando o painel já usa `.GetPage` + `.RelPermalink`.
2. Não substituir por `/gmvault/...` literal, pois isso acoplaria conteúdo ao ambiente de publicação.
3. Criar teste que constrói o mesmo site com dois `baseURL` diferentes — raiz e subdiretório — e exige links válidos nos dois.
4. Registrar RED com o conteúdo atual.
5. Corrigir gerador e página existente.
6. Registrar GREEN.

**Verificação imediata:** os dois links rápidos publicados devem passar a conter `/gmvault/campaigns/...` no build de produção.

---

### Tarefa 8: Impedir que a tradução altere destinos estruturais

**Objetivo:** evitar futuras quebras de URL/slug durante tradução, mesmo que a causa atual principal seja o `baseURL`.

**Arquivos:**
- Modificar: `translate_drafts.py`
- Modificar: `tests/test_lmstudio_translation.py`
- Possivelmente modificar: `tests/test_translation_glossary.py`

**Ciclo TDD:**

1. Criar documento contendo:
   - link Markdown com texto traduzível e destino interno;
   - imagem;
   - shortcode `ref`/`relref`;
   - URL externa;
   - campos estruturais (`slug`, `url`, `aliases`, `locations`, IDs e referências).
2. Usar tradutor fake agressivo que tentaria traduzir tudo.
3. Exigir que somente texto visível seja alterado; todos os destinos devem permanecer byte a byte iguais.
4. Registrar RED para qualquer proteção ausente.
5. Proteger/restaurar tokens estruturais antes/depois da chamada ao modelo.
6. Registrar GREEN.
7. Adicionar teste de checkpoint para garantir que o parcial preserve os mesmos destinos.

**Observação:** essa tarefa deve ser integrada com a futura retomada verdadeira de `*.translation.partial`, mas não deve consumir nem apagar o checkpoint existente.

---

### Tarefa 9: Corrigir links quebrados encontrados pelo inventário

**Objetivo:** tratar cada classe de erro com a correção certa, sem publicar conteúdo incompleto apenas para eliminar 404.

**Arquivos:** definidos pelo relatório da Tarefa 2.

**Tratamento por classe:**

| Classe | Correção |
|---|---|
| `outside-base-path` | `relref`, `.RelPermalink` ou `relURL`; nunca prefixo literal de produção |
| destino draft | ocultar/desabilitar link ou publicar somente se o conteúdo estiver completo |
| slug inexistente | corrigir referência para slug canônico; não traduzir slug |
| imagem ausente | adicionar o asset realmente referenciado ou remover referência inválida |
| âncora ausente | corrigir o fragmento com base no ID gerado pelo Hugo |
| referência de compêndio ausente | resolver para entrada canônica ou renderizar indicação não clicável |

**Ciclo por correção:** para cada classe, adicionar caso RED no teste de links, fazer correção mínima e registrar GREEN.

**Cuidado especial:** os muitos `.webp` e arquivos de compêndio não rastreados devem ser auditados; não adicioná-los em massa sem comprovar que são usados por páginas publicadas e sem aprovação.

---

### Tarefa 10: Migrar o conteúdo atual da Cidadela Radiante

**Objetivo:** aplicar o contrato às páginas já importadas sem retraduzir conteúdo.

**Arquivos:**
- `content/campaigns/journeys-through-the-radiant-citadel/adventures/welcome-to-the-radiant-citadel/_index.md`
- Filhos introdutórios dentro de `welcome-to-the-radiant-citadel/`
- Seções introdutórias de `salted-legacy/`
- Outras aventuras somente após classificação confirmada

**Passos:**

1. Gerar dry-run listando página, título, `weight` e classificação proposta.
2. Revisar falsos positivos antes de escrever.
3. Marcar `Welcome to the Radiant Citadel` como introdução da campanha.
4. Marcar antecedentes/ganchos/preparação de `Salted Legacy` como introdução da aventura.
5. Não remover `draft` de conteúdo incompleto.
6. Não modificar o checkpoint parcial.
7. Construir página da campanha e da aventura e comparar a ordem visual.

**Verificação:** conteúdo introdutório deve aparecer uma única vez; *Legado Salgado* deve continuar publicada e navegável.

---

### Tarefa 11: Validação completa local

**Objetivo:** provar que código, conteúdo e site estão consistentes.

**Comandos:**

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m py_compile import_campaign.py translate_drafts.py interactive_cli.py
git diff --check
hugo --destination /tmp/gmvault-radiant-final
.venv/bin/python scripts/check_internal_links.py \
  --public /tmp/gmvault-radiant-final \
  --base-url https://filipeaguiar.github.io/gmvault/ \
  --scope campaigns/journeys-through-the-radiant-citadel/
```

**Resultados esperados:**

- todos os testes passam;
- compilação Python passa;
- `git diff --check` não encontra whitespace inválido;
- Hugo normal termina com código 0;
- auditor retorna zero links internos quebrados no escopo publicado;
- nenhuma introdução aparece duplicada;
- nenhuma página incompleta foi publicada por efeito colateral.

Executar também um build com `baseURL` temporário em raiz para provar portabilidade.

---

### Tarefa 12: Revisão e publicação controlada

**Objetivo:** apresentar mudanças para aprovação antes de registrar/publicar.

**Passos:**

1. Mostrar `git diff --stat` e diff apenas dos arquivos do escopo.
2. Mostrar relatório “antes/depois” dos links quebrados.
3. Mostrar URLs locais das páginas da campanha e de *Legado Salgado*.
4. Confirmar que o checkpoint parcial continua presente.
5. Solicitar aprovação explícita para commit.
6. Após aprovação, criar commits pequenos e temáticos, por exemplo:
   - `test: add Hugo internal link audit`
   - `feat: model editorial introductions`
   - `fix: resolve campaign links under base URL`
   - `content: classify Radiant Citadel introductions`
7. Solicitar aprovação explícita separada antes de push/deploy, se não estiver incluída na aprovação anterior.
8. Após deploy, executar auditoria HTTP da URL pública e comparar com o build local.

---

## Arquivos provavelmente alterados

- `import_campaign.py`
- `translate_drafts.py`
- `interactive_cli.py` (somente se houver confirmação interativa)
- `layouts/partials/kinds/campaign.html`
- `layouts/partials/kinds/adventure.html`
- `layouts/partials/kinds/session.html`
- `layouts/partials/editorial_introduction.html`
- `content/campaigns/journeys-through-the-radiant-citadel/_index.md`
- front matters de introdução sob `content/campaigns/journeys-through-the-radiant-citadel/adventures/`
- `tests/test_internal_links.py`
- `tests/test_content_roles.py`
- `tests/test_import_campaign_content_roles.py`
- `tests/test_campaign_introduction_rendering.py`
- `tests/test_adventure_introduction_rendering.py`
- `tests/test_lmstudio_translation.py`
- `scripts/check_internal_links.py`
- `docs/content-roles.md`

## Riscos e mitigação

1. **Working tree já alterada:** inventário e hashes antes de editar; nunca usar reset/checkout destrutivo.
2. **Introdução formada por árvore profunda:** partial deve ter recursão controlada e testes; não renderizar toda a subárvore indiscriminadamente.
3. **Conteúdo draft:** não publicar somente para satisfazer o crawler; esconder link ou apresentar estado indisponível.
4. **Heurísticas de título:** usar apenas na importação e persistir decisão explícita.
5. **Tradução de estruturas:** proteger destinos por tokens e testar com tradutor fake agressivo.
6. **GitHub Pages em subdiretório:** testar com mais de um `baseURL`.
7. **Assets não rastreados:** adicionar apenas os efetivamente referenciados e aprovados.
8. **Checkpoint incompleto:** não consumir nem apagar até existir retomada verdadeira testada.
9. **Compatibilidade com campanhas antigas:** ausência de `content_role` mantém comportamento atual.

## Fora do escopo desta execução

- Completar a tradução de todas as aventuras.
- Publicar aventuras ainda incompletas.
- Traduzir slugs ou renomear diretórios.
- Adicionar em massa todo o compêndio e todas as imagens não rastreadas.
- Commit, push ou deploy sem aprovação explícita.
