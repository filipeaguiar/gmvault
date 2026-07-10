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

Estrutura esperada:

```text
adventures/<adventure-slug>/
├── _index.md
└── sessions/
    ├── _index.md
    └── 001-nome-da-sessao/
        ├── _index.md
        └── scenes/
            ├── _index.md
            ├── cena-1.md
            ├── cena-2.md
            └── cena-3.md
```

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

Cada sessão fica em:

```text
adventures/<adventure-slug>/sessions/<session-slug>/_index.md
```

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

Cada cena fica em:

```text
adventures/<adventure-slug>/sessions/<session-slug>/scenes/<scene-slug>.md
```

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
