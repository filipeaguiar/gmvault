## Context

A ficha de personagem e o importador precisam evoluir para suportar modificadores semânticos de equipamentos de forma totalmente orientada ao compêndio. As propriedades de itens (tipo, dano, propriedades de combate, classe de armadura, peso, modificadores mágicos) devem residir nas páginas do compêndio correspondente (`content/compendium/items/` ou `content/compendium/magic-items/`). A ficha do personagem no Markdown frontmatter apenas listará referências (`ref`) a esses itens com estado operacional (`equipped`, `quantity`). O template Hugo `character.html` resolverá essas notas em tempo de build para calcular atributos, CA e renderizar os detalhes.

## Goals / Non-Goals

**Goals:**
- Desacoplar a ficha do personagem das propriedades estáticas dos itens, centralizando os metadados no compêndio global.
- Atualizar o importador `import_dndbeyond.py` para gravar metadados de itens e modificadores mágicos no compêndio, e apenas criar referências leves na ficha do personagem.
- Resolver e acumular dinamicamente modificadores de atributos (sobreposição e bônus), salvaguardas e CA baseados nos itens equipados ativos no template do Hugo.

**Non-Goals:**
- Modificar o fluxo de jogo com scripts de backend (os cálculos ocorrem estaticamente durante o build do Hugo).

## Decisions

### 1. Estrutura do Compêndio (Itens)
As páginas dos itens no compêndio conterão dados sob `item_info`:
```yaml
title: "Adaga"
params:
  kind: "item"
item_info:
  type: "Weapon"
  cost: "2.0 gp"
  weight: "1 lb"
  properties: ["finesse", "light", "thrown"]
  range: "20/60"
  damage: "1d4"
  damage_type: "piercing"
```
Para itens mágicos com modificadores:
```yaml
title: "Luvas de Força de Gigante do Pântano"
params:
  kind: "magic_item"
item_info:
  type: "Wondrous item"
  weight: "1 lb"
  modifiers:
    stat_override:
      str: 21
```

### 2. Estrutura da Ficha de Personagem (Frontmatter)
Apenas dados operacionais leves:
```yaml
char_info:
  equipment:
    - name: "Adaga"
      quantity: 1
      equipped: true
      ref: "/compendium/items/dagger/"
    - name: "Luvas de Força de Gigante do Pântano"
      quantity: 1
      equipped: true
      ref: "/compendium/magic-items/luvas-de-forca-de-gigante/"
```

### 3. Resolução no Template Hugo `character.html`
1. Inicializar atributos finais do scratch Hugo com os atributos base da ficha.
2. Iterar sobre `char_info.equipment` e resolver o item com `site.GetPage .ref`.
3. Se o item estiver equipado (`equipped: true`), ler `item_info.modifiers`:
   - `stat_override`: se o valor sobrescrito for maior que o valor corrente no scratch, atualiza.
   - `stat_bonus`: soma o bônus no valor corrente do scratch.
4. Calcular modificadores e o delta (diferença) em relação aos modificadores base originais.
5. Aplicar o delta no bônus de perícias e salvaguardas durante suas renderizações.
6. Resolver o cálculo de CA considerando o tipo de armadura equipada, escudo equipado (lido da nota do compêndio resolvida com `item_info.type = "Shield"` ou `item_info.armor_class`) e bônus de CA (`ac_bonus` em `modifiers` do item mágico).

## Risks / Trade-offs

- **[Risco] Item sem referência ou referência quebrada no compêndio**  
  → *Mitigação*: O template Hugo deve validar se a página resolvida com `site.GetPage` não é nula (`if $itemPage`) antes de acessar suas propriedades. Caso seja nula, o layout deve usar os dados inline ou fallback padrão da ficha de personagem sem quebrar o build do Hugo.
