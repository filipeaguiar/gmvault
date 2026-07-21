## Context

Os personagens jogadores (Durin, Einvor e Violeta) dependem de recursos consumíveis limitados de suas classes. Para facilitar a visualização desses recursos durante as sessões de RPG no site estático do Hugo, precisamos mapear e estilizar estes dados no topo da ficha, facilitando o controle visual do mestre.

## Goals / Non-Goals

**Goals:**
* Definir uma propriedade estruturada `consumables` dentro de `char_info` nos arquivos markdown dos personagens jogadores.
* Criar contadores visuais no topo da ficha do site estático (layouts do Hugo) integrando o valor atual e máximo do recurso.
* Adicionar regras CSS dedicadas para estilizar os contadores com as cores temáticas apropriadas de cada classe.

**Non-Goals:**
* Criar componentes interativos complexos baseados em Javascript ou banco de dados (o consumo continuará sendo alterado manualmente direto nos markdowns).

## Decisions

### Decisão 1: Schema de Dados no Markdown
Mapear os recursos sob `char_info.consumables` como uma lista de dicionários no front matter:
```yaml
char_info:
  consumables:
    - name: "Pontos de Foco"
      current: 3
      max: 3
      type: "focus"
```
*Racional:* Oferece flexibilidade máxima para adicionar múltiplos consumíveis por personagem futuramente (ex: Foco e também Ki, ou Fúria e Infusões).

### Decisão 2: Onde renderizar no Layout HTML
Injetar os contadores na seção superior de metadados da ficha de personagem (onde são exibidos os slots de magia, classe, raça, HP e CA).
*Racional:* O topo da página é a área de maior visibilidade durante a consulta rápida do mestre na sessão.

### Decisão 3: Cores e Classes CSS Customizadas
Adicionar as seguintes classes de estilo no arquivo de estilos principal do site:
* `.consumable-badge`: estilo geral do badge (margens, bordas, padding, sombra leve, fonte destacada).
* `.badge-rage` (Bárbaro): Vermelho profundo/Alaranjado.
* `.badge-focus` (Monge): Azul-celeste/Elétrico.
* `.badge-sorcery` (Feiticeiro): Roxo/Violeta místico.

## Risks / Trade-offs

* **[Risco]** Fichas de outros personagens sem a chave `consumables` quebrando a compilação do Hugo.
  * **Mitigação:** Utilizar condicionais do Hugo Go-templates (`{{ with .Params.char_info.consumables }}`) para renderizar a seção apenas se a chave estiver definida e populada.
