# Recuperação da tradução e publicação da campanha — Plano de implementação

> **Para o Hermes:** executar este plano por etapas, com revisão de fidelidade antes de alterar o estado de publicação. Não criar commit nem enviar alterações sem aprovação explícita do usuário.

**Objetivo:** recuperar uma versão fiel e legível em pt-BR de *Journeys through the Radiant Citadel / Salted Legacy*, impedir nova corrupção automática e fazer a campanha aparecer nas listagens do Hugo.

**Arquitetura:** separar recuperação editorial de publicação. Primeiro, reconstruir os 24 Markdown a partir da versão anterior ao commit `8fc7cac`, preservando apenas metadados e mudanças estruturais legítimas; depois revisar a tradução com verificações automáticas e amostragem humana. Somente quando o conteúdo estiver íntegro, trocar os campos Hugo `draft` necessários para publicação e validar os builds de produção e com rascunhos.

**Stack:** Git, Markdown/YAML, Python 3.11 em `.venv`, Hugo 0.164, pytest.

---

## Diagnóstico confirmado

1. O commit problemático é `8fc7cac` (`campanha`).
2. Ele alterou 24 arquivos Markdown e introduziu erros semânticos, gramaticais e de formatação.
3. O front matter continua sendo YAML válido e o Hugo compila, portanto o build sozinho não detecta a corrupção editorial.
4. A campanha não aparece porque `content/campaigns/journeys-through-the-radiant-citadel/_index.md` contém `draft: true`.
5. As seções filhas também estão como rascunho:
   - `content/campaigns/journeys-through-the-radiant-citadel/adventures/_index.md`
   - `content/campaigns/journeys-through-the-radiant-citadel/adventures/salted-legacy/_index.md`
   - páginas importadas abaixo da aventura.
6. Evidência reproduzida:
   - build normal: **0** arquivos para essa campanha;
   - `hugo --buildDrafts`: **49** arquivos para essa campanha.
7. `layouts/index.html:13-18` lista páginas cujo `kind` é `campaign`, mas `site.Pages` do build normal não contém páginas com `draft: true`.
8. `status: draft` é metadado próprio do projeto; por si só não controla publicação no Hugo. O campo decisivo é `draft`.

---

### Tarefa 1: Criar uma base de recuperação sem apagar o estado atual

**Objetivo:** produzir uma relação exata dos arquivos afetados e separar conteúdo editorial de alterações legítimas em scripts/infraestrutura.

**Arquivos:**
- Inspecionar: os 24 caminhos retornados por `git diff --name-only 8fc7cac^ 8fc7cac -- 'content/**/*.md'`
- Não modificar nesta tarefa.

**Passo 1: registrar os arquivos de conteúdo alterados**

Executar:

```bash
git diff --name-only 8fc7cac^ 8fc7cac -- 'content/**/*.md'
```

Esperado: 24 arquivos Markdown sob `content/campaigns/journeys-through-the-radiant-citadel/`.

**Passo 2: separar as mudanças não editoriais do commit**

Executar:

```bash
git diff --name-status 8fc7cac^ 8fc7cac -- . ':(exclude)content/**/*.md'
```

Esperado: inventário dos scripts/configurações que não devem ser revertidos junto com o conteúdo.

**Passo 3: guardar um patch somente para auditoria**

Executar:

```bash
git diff 8fc7cac^ 8fc7cac -- 'content/**/*.md' > /tmp/gmvault-8fc7cac-content.patch
```

Esperado: patch não vazio em `/tmp`, sem modificar o repositório.

---

### Tarefa 2: Restaurar os 24 Markdown para a base anterior e reaplicar apenas metadados válidos

**Objetivo:** remover a tradução corrompida sem desfazer mudanças legítimas em código.

**Arquivos:**
- Modificar: os 24 Markdown identificados na Tarefa 1.

**Passo 1: extrair cada versão-base do commit pai**

Para cada arquivo da lista, usar o conteúdo de:

```bash
git show 8fc7cac^:<caminho-do-arquivo>
```

Não executar `git revert 8fc7cac`, porque esse commit também contém alterações em scripts e outros arquivos que podem ser legítimas.

**Passo 2: comparar front matter antigo e atual**

Preservar apenas campos estruturais que tenham sido deliberadamente adicionados e que não sejam produto da tradução, por exemplo:

- `params.kind`
- `visibility`
- relações `npcs`, `locations` e `handouts`
- bloco `translation`, após corrigir seu estado

Não preservar alterações linguísticas do corpo feitas pelo commit problemático.

**Passo 3: marcar honestamente o estado da tradução**

Enquanto a revisão não estiver concluída, usar no bloco `translation`:

```yaml
translation:
  source_language: en
  target_language: pt-BR
  engine: argos
  status: needs_review
```

O campo `engine` deve refletir o mecanismo realmente usado; trocar por outro valor se a reconstrução não usar Argos.

**Passo 4: revisar o diff de recuperação**

Executar:

```bash
git diff --stat -- 'content/**/*.md'
git diff --check
```

Esperado: apenas os 24 conteúdos planejados; nenhum erro de whitespace reportado por `git diff --check`.

---

### Tarefa 3: Refazer a tradução por unidade semântica e preservar Markdown

**Objetivo:** obter pt-BR natural e fiel, sem traduzir identificadores, URLs ou estruturas Markdown.

**Arquivos prioritários:**
- `content/campaigns/journeys-through-the-radiant-citadel/adventures/salted-legacy/001-inicio/02-background.md`
- `.../03-welcome-to-the-market.md`
- `.../04-market-investigations.md`
- `.../05-market-games.md`
- `.../06-what-vendors-know.md`
- `.../07-revealing-the-plot.md`
- `.../09-siabsungkoh-gazetteer.md`
- demais índices, handouts, NPCs e localizações da lista da Tarefa 1.

**Passo 1: definir regras de preservação**

Para cada arquivo:

- traduzir títulos e prosa, não slugs nem URLs;
- manter nomes próprios quando não houver tradução oficial;
- manter `CD`, atributos e termos de regras de D&D de forma consistente;
- preservar links, imagens, tabelas, blockquotes, listas e marcadores `ZXQ...` byte a byte quando forem identificadores;
- não traduzir chaves YAML;
- não converter `![alt](url)` em `[alt](url)`;
- não remover aspas de diálogos;
- não alterar números, CDs, dados, alcance, pontos de vida e quantidades sem justificativa no original.

**Passo 2: traduzir em lotes pequenos**

Trabalhar em uma seção ou arquivo por vez. Após cada lote, comparar original e tradução lado a lado. Não fazer nova tradução automática massiva sobre texto que já esteja em português.

**Passo 3: adotar glossário mínimo consistente**

Criar durante a implementação um glossário revisável para termos recorrentes, por exemplo:

| Original | pt-BR sugerido |
|---|---|
| vendor | vendedor/comerciante |
| saving throw | teste de resistência |
| ability check | teste de atributo |
| Armor Class | Classe de Armadura (CA) |
| hit points | pontos de vida (PV) |
| player version | versão para os jogadores |
| Market Games | Jogos do Mercado |
| Market Mischief | Travessuras no Mercado |

Confirmar terminologia oficial de D&D 5e antes da revisão final; não inventar traduções para nomes próprios.

**Passo 4: revisar cada arquivo antes de avançar**

Critérios mínimos:

- nenhuma frase sem sentido;
- concordância e regência naturais em pt-BR;
- regras mecanicamente equivalentes ao original;
- cabeçalhos e referências internas coerentes;
- imagens e tabelas renderizáveis.

---

### Tarefa 4: Criar validações automáticas contra regressão editorial

**Objetivo:** detectar corrupção estrutural que o Hugo não acusa.

**Arquivos:**
- Criar: `tests/test_campaign_content.py`
- Possivelmente modificar: `translate_drafts.py`, somente depois de reproduzir a causa da corrupção.

**Passo 1: escrever testes inicialmente falhos para integridade Markdown**

O teste deve percorrer os Markdown da campanha e falhar quando encontrar:

- YAML inválido;
- imagem transformada em link comum quando o mesmo URL era imagem na base;
- links com espaço indevido entre `]` e `(`;
- aspas de diálogos obviamente desequilibradas;
- palavras aglutinadas extensas como `Logotipodepoisdedeixaratenda`;
- placeholders `ZXQ...` alterados ou removidos;
- títulos de tabela substituídos por rótulos genéricos como `Tradução:`.

**Passo 2: executar o teste e comprovar que ele detecta a versão corrompida**

Executar contra `8fc7cac` em worktree temporária ou fixture derivada do patch:

```bash
.venv/bin/python -m pytest tests/test_campaign_content.py -v
```

Esperado: falhas específicas para os defeitos conhecidos.

**Passo 3: validar o conteúdo recuperado**

Executar novamente na árvore corrigida.

Esperado: todos os testes de integridade passam.

**Passo 4: testar o tradutor antes de reutilizá-lo**

Adicionar testes unitários para `translate_drafts.py` garantindo que:

- front matter é preservado;
- blocos de código, URLs, imagens e placeholders não são traduzidos;
- texto já em pt-BR não recebe uma segunda tradução destrutiva;
- erro parcial não sobrescreve o arquivo original;
- a escrita usa arquivo temporário e substituição atômica somente após validação.

Executar:

```bash
.venv/bin/python -m pytest -v
```

Esperado: suíte completa aprovada.

---

### Tarefa 5: Revisar fidelidade mecânica e editorial

**Objetivo:** garantir que a aventura continue jogável e equivalente ao texto-fonte.

**Arquivos:** todos os arquivos narrativos da aventura.

**Passo 1: comparar elementos mecânicos**

Produzir e comparar, por arquivo, contagens/listas de:

- `CD` e respectivos valores;
- dados (`d4`, `d6`, `d8`, etc.);
- CA, PV, rodadas, níveis e recompensas;
- nomes de NPCs e locais;
- referências `ZXQ...`;
- links e URLs de imagens.

Esperado: nenhuma divergência não justificada entre fonte e tradução.

**Passo 2: procurar resíduos em inglês**

Executar uma busca orientativa, excluindo URLs, slugs e nomes próprios. Revisar manualmente cada ocorrência; não substituir automaticamente.

Termos prioritários: `check`, `saving throw`, `player`, `Market Games`, `Market Mischief`, `Welcome to the Market`, `Hide-and-Seek`.

**Passo 3: revisar amostras obrigatórias**

Ler integralmente ao menos:

1. introdução e background;
2. chegada ao mercado e diálogo da rivalidade;
3. regras dos três Jogos do Mercado;
4. revelação da trama;
5. gazetteer;
6. conclusão e avanço de personagens.

**Passo 4: atualizar o estado editorial**

Somente depois da revisão completa, trocar:

```yaml
translation:
  status: reviewed
```

Não confundir esse estado editorial com publicação Hugo.

---

### Tarefa 6: Publicar a campanha no Hugo

**Objetivo:** fazer a campanha e suas páginas aparecerem no build normal.

**Arquivos:**
- Modificar: `content/campaigns/journeys-through-the-radiant-citadel/_index.md`
- Modificar: `content/campaigns/journeys-through-the-radiant-citadel/adventures/_index.md`
- Modificar: `content/campaigns/journeys-through-the-radiant-citadel/adventures/salted-legacy/_index.md`
- Modificar: páginas descendentes que ainda tenham `draft: true` e devam ser publicadas.

**Passo 1: listar todos os rascunhos da campanha**

Executar:

```bash
grep -RIl '^draft: true$' content/campaigns/journeys-through-the-radiant-citadel
```

Esperado: lista explícita de tudo que continuará invisível no build normal.

**Passo 2: alterar apenas conteúdo aprovado**

Para a campanha, índices e páginas revisadas, definir:

```yaml
draft: false
status: active
```

`status: active` mantém coerência editorial do projeto, mas é `draft: false` que efetivamente publica no Hugo.

Se algumas páginas não estiverem prontas, mantê-las em `draft: true`; não é necessário bloquear toda a campanha por causa delas, desde que os templates lidem bem com referências ausentes.

**Passo 3: adicionar teste de visibilidade**

Em `tests/test_campaign_content.py`, verificar que a raiz da campanha publicada contém:

```yaml
params:
  kind: campaign
draft: false
```

E que páginas obrigatórias da aventura também não estão como rascunho.

**Passo 4: validar o build de produção**

Executar:

```bash
rm -rf /tmp/gmvault-prod
hugo --destination /tmp/gmvault-prod --cleanDestinationDir --gc --minify
```

Esperado: build com código de saída 0 e arquivos sob:

```text
/tmp/gmvault-prod/campaigns/journeys-through-the-radiant-citadel/
```

**Passo 5: validar a listagem da home**

Confirmar no HTML gerado:

```bash
grep -n "Viagens pela Cidadela Radiante" /tmp/gmvault-prod/index.html
```

Esperado: pelo menos uma ocorrência dentro de `campaign-list`.

**Passo 6: validar a listagem de campanhas**

Confirmar que a página `/campaigns/` contém a campanha e que o link gerado resolve para um arquivo existente no destino.

---

### Tarefa 7: Validação visual final

**Objetivo:** verificar o que testes textuais não cobrem.

**Passo 1: iniciar Hugo localmente sem `-D`**

Executar:

```bash
hugo server --disableFastRender
```

Não usar `-D`, pois isso mascararia novamente o problema de publicação.

**Passo 2: conferir no navegador**

Validar:

- campanha aparece na home;
- campanha aparece em `/campaigns/`;
- título pt-BR está correto;
- aventura aparece dentro da campanha;
- imagens são renderizadas como imagens;
- tabelas e blockquotes mantêm formatação;
- links para NPCs, locais, handouts e mapas funcionam;
- nenhuma página aprovada retorna 404.

**Passo 3: executar a suíte final**

```bash
.venv/bin/python -m pytest -v
hugo --destination /tmp/gmvault-final --cleanDestinationDir --gc --minify
```

Esperado: testes aprovados e build Hugo com saída 0.

---

## Arquivos provavelmente alterados

- 24 Markdown do commit `8fc7cac` sob `content/campaigns/journeys-through-the-radiant-citadel/`.
- `tests/test_campaign_content.py` (novo).
- `translate_drafts.py` (somente se os testes confirmarem que ele causou ou permite a corrupção).
- Nenhum template precisa ser alterado para a causa atual: `layouts/index.html` já seleciona corretamente páginas com `kind: campaign`; o Hugo apenas exclui rascunhos de `site.Pages`.

## Critérios de aceite

- [ ] Os 24 arquivos não contêm os erros semânticos identificados.
- [ ] A tradução está em pt-BR natural e fiel ao texto-fonte.
- [ ] Valores mecânicos de D&D permanecem equivalentes ao original.
- [ ] Markdown, imagens, links, tabelas, blockquotes e placeholders estão preservados.
- [ ] A suíte automatizada detecta as regressões observadas no commit problemático.
- [ ] `hugo` sem `-D` gera a campanha.
- [ ] A home e `/campaigns/` listam “Viagens pela Cidadela Radiante”.
- [ ] O build final e o pytest passam.
- [ ] Diff final revisado pelo usuário antes de qualquer commit.

## Riscos e decisões

- **Risco de reverter demais:** evitar `git revert` integral; restaurar apenas os 24 Markdown.
- **Risco de nova tradução destrutiva:** não reaplicar tradução automática em massa e proteger estruturas Markdown antes de qualquer chamada ao tradutor.
- **Risco de publicar conteúdo incompleto:** separar `translation.status` de `draft`; só publicar páginas revisadas.
- **Risco de referências para rascunhos:** validar links/404 após publicar parcialmente.
- **Decisão pendente:** confirmar se a intenção é publicar toda a campanha imediatamente após a revisão ou publicar primeiro apenas a raiz e a aventura *Legado Salgado*.

## Estratégia de commits

Não criar commits sem autorização explícita. Quando autorizado, preferir dois commits independentes para facilitar auditoria e rollback:

1. `fix(content): recover and review Radiant Citadel translation`
2. `fix(content): publish Radiant Citadel campaign`
