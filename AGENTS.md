# AGENTS.md — RPG Campaign Vault

## Visão geral do projeto

Este repositório contém um site estático em **Hugo** para organizar campanhas de RPG de mesa em Markdown.

O site deve funcionar como uma wiki leve, navegável e estruturada, com suporte a múltiplas campanhas e a um compêndio global compartilhado entre elas.

O projeto deve priorizar:

* simplicidade;
* arquivos Markdown legíveis;
* estrutura previsível;
* navegação rápida;
* baixo peso no navegador;
* compatibilidade com computadores modestos;
* facilidade de edição manual.

Este projeto **não** deve depender de banco de dados, backend, painel administrativo dinâmico ou frameworks JavaScript pesados.

## Diretrizes de comunicação para agentes

Os agentes de IA que operam neste repositório devem seguir as seguintes regras de comunicação:

*   **Linguagem direta e profissional**: Sempre utilize linguagem direta e profissional.
*   **Explicação clara**: Explique o que precisar, explique o que foi feito.
*   **Sem informalidades**: Sem elogios, sem tom de conversa. Só informação.
*   **Recomendações**: Caso haja recomendação, avise.

## Estrutura conceitual

O site possui duas grandes áreas:

```text
Compêndio Global
→ conteúdo reutilizável entre campanhas

Campanhas
→ conteúdo específico de cada campanha
```

A hierarquia principal das campanhas deve ser:

```text
Campanha
└── Aventuras
    └── Sessões
        └── Cenas
```

## Compêndio global

O compêndio global contém entidades que podem ser compartilhadas entre várias campanhas.

Exemplos:

```text
content/compendium/
├── monsters/
├── items/
├── magic-items/
├── classes/
├── races/
├── feats/
├── spells/
├── backgrounds/
├── conditions/
└── rules/
```

Essas páginas não pertencem a uma campanha específica. Elas podem ser referenciadas por campanhas, aventuras, sessões e cenas.

Tipos esperados no compêndio:

```text
monster
item
magic_item
class
race
feat
spell
background
condition
rule
```

## Campanhas

Cada campanha deve ficar em:

```text
content/campaigns/<campaign-slug>/
```

Estrutura esperada:

```text
content/campaigns/<campaign-slug>/
├── _index.md
├── journal/
├── characters/
├── npcs/
├── locations/
├── factions/
├── handouts/
└── adventures/
```

A página `_index.md` da campanha deve funcionar como página principal da campanha.

Ela deve conter:

* descrição geral;
* pitch;
* tom e temas;
* sistema usado;
* link para “A História Até Aqui”;
* links para personagens;
* links para NPCs;
* links para localidades;
* links para facções;
* links para handouts;
* links para aventuras.

## A História Até Aqui

Toda campanha pode ter uma área chamada:

```text
journal/
```

Essa área representa a narrativa final da campanha, organizada em capítulos ou entradas cronológicas.

Exemplo:

```text
content/campaigns/<campaign-slug>/journal/
├── _index.md
├── 001-chegada.md
├── 002-primeira-missao.md
└── 003-o-mapa-queimado.md
```

O usuário apenas cola ou edita manualmente o texto final em Markdown.

## Aventuras

Cada aventura fica em:

```text
content/campaigns/<campaign-slug>/adventures/<adventure-slug>/
```

Estrutura canônica esperada para novo conteúdo e novas importações:

```text
adventures/<adventure-slug>/
├── _index.md
└── 001-nome-da-sessao/
    ├── _index.md
    ├── cena-1.md
    ├── cena-2.md
    └── cena-3.md
```

Estrutura legada ainda suportada para leitura/renderização:

```text
adventures/<adventure-slug>/
├── _index.md
└── sessions/
    ├── _index.md
    └── 001-nome-da-sessao/
        ├── _index.md
        └── scenes/
            ├── _index.md
            └── cena-1.md
```

Novos scripts e importadores não devem gerar `sessions/` nem `scenes/` como diretórios obrigatórios.

Aventura é um arco, missão, módulo ou bloco jogável dentro da campanha.

A página da aventura deve conter:

* resumo;
* gancho;
* contexto;
* objetivos;
* sessões;
* NPCs envolvidos;
* localidades;
* facções;
* handouts;
* possíveis desfechos.

## Sessões

Uma sessão é um bloco de planejamento dentro de uma aventura.

Ela pode corresponder a uma sessão real de jogo ou a uma unidade planejada de preparação.

Cada nova sessão fica em:

```text
adventures/<adventure-slug>/<session-slug>/_index.md
```

Sessões legadas em `adventures/<adventure-slug>/sessions/<session-slug>/_index.md` continuam suportadas para conteúdo antigo.

A sessão deve conter:

* objetivo da sessão;
* estado inicial;
* resumo para o mestre;
* cenas;
* NPCs importantes;
* localidades importantes;
* ganchos;
* pistas;
* testes importantes;
* handouts;
* possíveis conflitos;
* possíveis desfechos;
* transição para a próxima sessão;
* pendências.

## Cenas

Cena é uma unidade operacional de preparação e condução da sessão.

O termo “cena” é usado de forma livre. Uma cena pode ser:

* chegada a uma vila;
* praça central;
* loja;
* taverna;
* conversa com NPC;
* investigação;
* mapa específico;
* trecho de viagem;
* sala de dungeon;
* combate;
* armadilha;
* encontro social;
* situação aberta com ganchos.

Cada nova cena fica em:

```text
adventures/<adventure-slug>/<session-slug>/<scene-slug>.md
```

Cenas legadas em `adventures/<adventure-slug>/sessions/<session-slug>/scenes/<scene-slug>.md` continuam suportadas para conteúdo antigo.

A cena deve conter:

* uso na sessão;
* descrição;
* elementos importantes;
* NPCs;
* localidades e pontos de interesse;
* ganchos;
* pistas;
* testes;
* mapas e handouts;
* possíveis conflitos;
* transições;
* notas do mestre.

## Front matter padrão

Todo conteúdo deve usar YAML front matter.

Campos comuns:

```yaml
---
title: "Título da Página"
kind: "scene"
draft: false
weight: 10
summary: "Resumo curto da página."

tags:
  - exemplo

visibility: "gm"
status: "draft"

related:
  - "/caminho/para/outra/pagina/"
---
```

## Campo `kind`

Cada página deve ter um campo `kind`.

Valores principais:

```text
campaign
journal_index
journal_entry
character
npc
location
faction
handout
adventure
session
scene
monster
item
magic_item
class
race
feat
spell
background
condition
rule
```

Não usar `section` como entidade estrutural principal. A hierarquia correta é:

```text
adventure
└── session
    └── scene
```

## Campo `visibility`

O campo `visibility` é um metadado editorial, não autenticação.

Valores aceitos:

```text
gm
players
public
archived
```

Significado:

```text
gm
→ conteúdo do mestre.

players
→ conteúdo pensado para jogadores da campanha.

public
→ conteúdo seguro para publicação aberta.

archived
→ conteúdo antigo ou fora de uso.
```

Não tratar `visibility` como segurança real. Páginas publicadas em site público podem ser acessadas por URL.

## Campo `status`

Valores sugeridos:

```text
draft
ready
active
completed
archived
```

Uso:

```text
draft
→ ainda em preparação.

ready
→ pronto para uso.

active
→ atualmente em uso na campanha.

completed
→ concluído.

archived
→ antigo ou fora de uso.
```

## Relacionamentos

Relacionamentos entre páginas devem ser representados como listas de URLs internas no front matter.

Exemplo:

```yaml
npcs:
  - "/campaigns/exemplo-campanha/npcs/nara/"

locations:
  - "/campaigns/exemplo-campanha/locations/vila-exemplo/"

handouts:
  - "/campaigns/exemplo-campanha/handouts/carta-exemplo/"

compendium_refs:
  - "/compendium/monsters/goblin/"
  - "/compendium/items/corda/"
```

Os layouts devem tentar resolver essas URLs internas com `site.GetPage` e exibir o título da página relacionada. Se não for possível resolver, exibir o caminho bruto como fallback.

## Navegação esperada

O site deve ter:

* página inicial com links para Campanhas e Compêndio;
* índice de campanhas;
* índice do compêndio;
* breadcrumbs em todas as páginas;
* listas automáticas de páginas filhas;
* cards ou listas para conteúdo relacionado;
* metadados visíveis;
* navegação simples e leve.

O índice `content/campaigns/_index.md` é uma página de navegação do mestre e deve usar `visibility: "gm"` quando listar campanhas com conteúdo GM. Páginas públicas ou de jogadores continuam impedidas de gerar navegação automática para filhos `gm`.

Campanhas importadas por scripts podem permanecer com `draft: true` até revisão editorial. Elas aparecem durante desenvolvimento com `hugo server -D` ou `hugo -D --gc --minify`, mas ficam fora de builds de produção com `hugo --gc --minify` até serem publicadas manualmente com `draft: false`.

Exemplo de breadcrumb:

```text
Campanhas > Cidadela Radiante > Aventuras > Mercado Noturno > Sessões > Sessão 01 > Cenas > Praça Central

O breadcrumb deve ser oculto em páginas que podem ser visualizadas pelos jogadores, uma vez que publicaremos como p[agina pública no github. Páginas de handout não devem ter breadcrumbs, nem páginas de personagem, nem páginas de itens, magias, etc. Deve ser possível acessar essas páginas pelo slug delas, sem navegaćão externa. Dessa forma um jogador pode ver a página de seu personagem, ver os itens que ele tem, magias e aćões, feats, etc, sem conseguir navegar para a parte que possa ter spoilers.
```

## Aparência esperada

O site deve parecer uma wiki de campanha limpa e leve.

Direção visual:

* layout simples;
* leitura confortável;
* largura máxima para texto;
* cards discretos;
* menu superior simples;
* breadcrumbs;
* metadados em bloco destacado;
* modo claro/escuro via CSS simples, se possível;
* sem dependência de tema pesado;
* sem framework JavaScript.

O site deve ser confortável para consulta durante uma sessão de RPG, inclusive em tela pequena ou notebook fraco.

Se possível, usar uma fonte adequada. A tipografia vai vender o conteúdo.

## Tema

Não usar tema externo no MVP.

Criar layouts próprios mínimos em:

```text
layouts/_default/
layouts/partials/
assets/css/
```

A estrutura do projeto é específica demais para depender inicialmente de um tema de documentação pronto.

## Diretórios reservados para integrações futuras

Reservar estes diretórios, mas não implementar geração automática agora:

```text
static/exports/gm-vault/
static/exports/forge/
```

Esses diretórios poderão ser usados futuramente para arquivos JSON consumidos por ferramentas externas.

No MVP, esses diretórios podem existir vazios ou com arquivos de exemplo simples.

## Requisitos técnicos

O projeto deve:

* usar Hugo;
* usar Markdown;
* usar YAML front matter;
* ter layouts próprios simples;
* funcionar com `hugo server -D`;
* funcionar com `hugo --gc --minify`;
* evitar dependências pesadas;
* manter estrutura clara de conteúdo;
* incluir archetypes para os principais tipos de página.

## Archetypes

Archetypes são templates para criar novos arquivos Markdown.

Criar archetypes para:

```text
campaign
journal-entry
character
npc
location
faction
handout
adventure
session
scene
monster
item
magic-item
class
race
feat
spell
background
condition
rule
```

Mudanças em archetypes afetam apenas novos arquivos criados depois. Arquivos antigos não são atualizados automaticamente.

## Conteúdo de exemplo

O projeto deve conter conteúdo fictício de exemplo para validar a estrutura:

```text
1 campanha
1 entrada de journal
1 personagem
1 NPC
1 localidade
1 facção
1 handout
1 aventura
2 sessões
3 cenas
1 monstro
1 item
1 item mágico
1 classe
1 raça
1 feat
1 magia
1 background
1 condição
1 regra
```

O conteúdo de exemplo deve ser genérico e não deve copiar texto de livros publicados.

## Comandos esperados

Rodar localmente:

```bash
hugo server -D
```

Gerar build:

```bash
hugo --gc --minify
```

## Critérios de aceite

O projeto está correto quando:

* a página inicial lista Campanhas e Compêndio;
* a página de campanha mostra “A História Até Aqui”;
* campanhas possuem aventuras;
* aventuras possuem sessões;
* sessões possuem cenas;
* cenas exibem metadados e conteúdo operacional;
* o compêndio existe separado das campanhas;
* páginas do compêndio podem ser referenciadas por páginas de campanha;
* os layouts são leves e legíveis;
* os archetypes existem;
* `hugo server -D` funciona;
* `hugo --gc --minify` funciona;

## Scripts de importação

O repositório possui scripts Python de importação que fazem parte do sistema operacional do vault. Eles não são apenas utilitários descartáveis; agentes devem considerá-los ao alterar modelo de conteúdo, front matter, layouts ou regras de visibilidade.

### `import_campaign.py`

Importador de campanhas/aventuras a partir de dados do 5e.tools.

Entrada esperada:

```bash
python3 import_campaign.py <slug-da-aventura-5etools>
```

Exemplos de slug esperados pelo script incluem identificadores como `jttrc` ou `lmop`, desde que existam no índice remoto do 5e.tools.

Fluxo conceitual:

```text
5e.tools adventures.json
        ↓
adventure/adventure-<slug>.json
        ↓
bestiary/fluff opcionais
        ↓
content/campaigns/<campaign-slug>/
├── _index.md
├── adventures/
│   └── <adventure-slug>/
│       └── sessions/
│           └── <session-slug>/
│               └── scenes/
├── npcs/
├── locations/
├── handouts/
└── ...

content/compendium/
├── monsters/
└── magic-items/

static/images/campaigns/<campaign-slug>/
```

Comportamentos importantes:

* baixa dados remotos de `https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/`;
* baixa imagens de `https://raw.githubusercontent.com/5etools-mirror-3/5etools-img/master/` quando há arte/fluff;
* cria a estrutura base da campanha caso não exista;
* oferece três modos interativos:
  * livro inteiro como uma aventura;
  * antologia, com cada capítulo como aventura;
  * um capítulo específico como aventura isolada;
* transforma capítulos, seções e entradas do 5e.tools em sessões e cenas;
* novas importações devem usar a estrutura simplificada `adventures/<adventure>/<session>/<scene>.md`, sem gerar `sessions/_index.md` ou `scenes/_index.md` como diretórios obrigatórios;
* converte tags do 5e.tools como monstros, criaturas, itens, magias, áreas, CD e dados para texto Markdown ou referências internas;
* cria stubs de NPCs, monstros, itens mágicos, localidades e handouts de arte;
* classifica criaturas específicas da campanha entre NPCs e monstros usando metadados do bestiário (`isNpc`, `isNamedCreature`) quando disponíveis;
* adiciona imagens de NPCs/monstros como handouts visíveis para jogadores (`visibility: "players"`), enquanto a maior parte do conteúdo importado permanece `visibility: "gm"`;
* usa `params.kind` em vez de `kind` no topo em vários arquivos gerados. Os layouts devem manter compatibilidade com esse formato legado ou o script deve ser migrado em mudança planejada.

Cuidados:

* o script sobrescreve algumas páginas de aventura durante a consolidação de relações; revisar diffs depois de importar;
* o conteúdo importado pode derivar de material publicado. Não tratar como conteúdo fictício livre;
* a importação depende de rede e de mirrors comunitários, portanto pode falhar por indisponibilidade ou mudança de schema remoto;
* muitos arquivos são criados como `draft: true`; testar com `hugo server -D` e também com build final sem drafts quando relevante;
* relações geradas usam URLs internas no front matter. Layouts devem continuar resolvendo essas URLs com `site.GetPage` e fallback seguro;
* qualquer mudança em `visibility` deve considerar que páginas player-facing não devem criar navegação para páginas GM.

### `import_dndbeyond.py`

Importador de personagem a partir da API pública de personagem do D&D Beyond.

Entrada esperada:

```bash
python3 import_dndbeyond.py <character-id> --campaign <campaign-slug>
```

Se `--campaign` não for informado, o padrão atual é `cidadela-radiante`.

Fluxo conceitual:

```text
D&D Beyond character API
        ↓
cálculo local de atributos, CA, HP, classe, raça, talentos, magias
        ↓
verificação/criação de referências no compêndio via 5e.tools
        ↓
content/campaigns/<campaign-slug>/characters/<personagem>.md
        ↓
content/compendium/{classes,races,feats,spells,items,magic-items,rules}/
```

Comportamentos importantes:

* busca `https://character-service.dndbeyond.com/character/v5/character/<id>`;
* exige que a ficha esteja acessível pela API; fichas privadas ou respostas inválidas encerram com erro;
* calcula atributos finais a partir de `stats` e modificadores;
* calcula CA considerando armadura, escudo, defesa sem armadura de monge/bárbaro e bônus mágicos;
* calcula HP a partir de HP base, modificador de Constituição por nível e bônus adicionais;
* coleta classe, raça, talentos, equipamentos equipados e magias conhecidas;
* monta `compendium_refs` para classe, raça, talentos, itens, itens mágicos e magias;
* se uma referência do compêndio não existir localmente, tenta criá-la via dados do 5e.tools;
* cria regras de compêndio para habilidades de classe, opções de classe, pactos, invocações e recursos similares;
* grava personagem em `content/campaigns/<campaign-slug>/characters/<slug>.md` com `visibility: "players"` e `status: "ready"`;
* usa `params.kind: "character"`; layouts devem manter fallback para `params.kind`.

Cuidados:

* o script pode atualizar/criar muitos arquivos no compêndio como `draft: true`;
* parte do texto de regras vem de snippets/descrições externas e pode exigir revisão, tradução e adequação editorial;
* as referências de compêndio em páginas de personagem só devem renderizar links seguros para jogadores; destinos GM devem ser omitidos em contexto player-facing;
* o cálculo de ficha é pragmático, não substitui validação manual completa da ficha no D&D Beyond;
* equipamentos não equipados geralmente não entram na lista de referências;
* subclasses, opções e features são filtradas por blacklist simples, sujeita a falsos positivos ou lacunas.

### `translate_drafts.py`

Script opcional de pós-processamento para traduzir arquivos Markdown em draft usando Argos Translate e glossário controlado.

Entrada esperada para compêndio:

```bash
source .venv/bin/activate
python3 translate_drafts.py --scope compendium --dry-run
python3 translate_drafts.py --scope compendium --path content/compendium/spells --apply
```

Entrada esperada para campanha:

```bash
source .venv/bin/activate
python3 translate_drafts.py --scope campaign --campaign <campaign-slug> --dry-run
python3 translate_drafts.py --scope campaign --campaign <campaign-slug> --apply
```

Fluxo conceitual:

```text
Markdown draft em inglês
        ↓
proteção de YAML, links, código, paths internos, imagens e dados
        ↓
tokenização de termos do glossário D&D/RPG
        ↓
Argos Translate en → pt
        ↓
restauração de tokens e estruturas protegidas
        ↓
Markdown ainda em draft, marcado como machine_translated
```

Comportamentos importantes:

* processa apenas arquivos com `draft: true` por padrão;
* usa `--scope compendium` para limitar a tradução a `content/compendium/`;
* usa `--scope campaign --campaign <slug>` para limitar a tradução a `content/campaigns/<slug>/`;
* aceita `--path` apenas dentro do escopo selecionado;
* rejeita caminhos que escapem do escopo;
* executa em dry-run por padrão e só grava com `--apply`;
* mantém `draft: true` após tradução;
* adiciona metadados `translation` indicando tradução automática por Argos;
* usa `translation_glossary.json` para controlar termos como `Armor Class`, `Hit Points`, atributos, condições, ações e escolas de magia;
* protege estruturas Markdown sensíveis antes de traduzir.

Cuidados:

* `argostranslate` deve ser instalado no ambiente virtual local `.venv`; Hugo não deve depender dessa biblioteca;
* o modelo Argos `en → pt` deve estar instalado no ambiente antes de usar `--apply`;
* tradução automática não torna o conteúdo pronto para publicação. Revisão humana continua obrigatória;
* o glossário é um controle editorial do projeto e pode ser expandido manualmente;
* não usar `--include-non-draft` sem revisão explícita, pois pode alterar conteúdo já pronto;
* após traduções aplicadas, rodar `hugo -D --gc --minify` e revisar diffs.

### Diretrizes para agentes ao alterar importadores

* Não alterar scripts de importação/tradução sem proposta ou solicitação explícita.
* Preservar compatibilidade com conteúdo já gerado por importações anteriores.
* Se normalizar front matter para `kind` no topo, atualizar os importadores e validar conteúdo legado com fallback.
* Após mudanças em importadores, testar pelo menos:
  * geração de campanha com `import_campaign.py` usando um slug pequeno ou fixture;
  * geração de personagem com `import_dndbeyond.py` quando houver ID acessível;
  * `hugo server -D`;
  * `hugo -D --gc --minify`;
  * `hugo --gc --minify`.
* Revisar manualmente visibilidade de handouts, personagens e compêndio depois de importações.
* Não assumir que `visibility` é segurança real; ela apenas controla apresentação e navegação gerada.
