## Context

A ficha de personagem e o importador precisam evoluir para suportar modificadores semânticos de equipamentos equipados (ex: itens mágicos que alteram atributos ou CA) e exibir metadados avançados (como alcance, tipo de dano e propriedades de armas) na aba de Equipamentos. Como o Hugo é um gerador de sites estáticos, os cálculos semânticos baseados nas propriedades `equipped` do frontmatter devem ser resolvidos em tempo de build nos templates Hugo, enquanto o importador `import_dndbeyond.py` deve estruturar essas propriedades no YAML de saída.

## Goals / Non-Goals

**Goals:**
- Extrair propriedades avançadas de itens (alcance, propriedades, tipo de dano, modificadores) no importador.
- Calcular dinamicamente em tempo de build (no template Hugo) a Classe de Armadura (CA) e Atributos de acordo com os itens ativos (`equipped: true`).
- Propagar as alterações de atributos para os modificadores correspondentes, testes de resistência e perícias.
- Melhorar a interface da aba de equipamentos para exibir visualmente essas propriedades de forma clara e profissional.

**Non-Goals:**
- Implementar troca dinâmica de equipamentos via JavaScript interativo na ficha pública (a ficha é estática e lê o estado configurado no frontmatter Markdown).
- Modificar sistemas de regras externos que não sejam do D&D 5e.

## Decisions

### 1. Estruturação do Frontmatter de Equipamentos
O frontmatter dos personagens passará a ter entradas ricas sob `.Params.char_info.equipment`.
```yaml
equipment:
  - name: "Espada Longa"
    quantity: 1
    equipped: true
    filter_type: "Weapon"
    ref: "/compendium/items/espada-longa/"
    properties: ["versatile"]
    range: null
    damage_formula: "1d8 + 3"
    damage_type: "slashing"
    category: "martial"
  - name: "Luvas de Força de Gigante do Pântano"
    quantity: 1
    equipped: true
    filter_type: "Wondrous item"
    ref: "/compendium/magic-items/luvas-de-forca-de-gigante/"
    modifiers:
      stat_override:
        str: 21
  - name: "Escudo"
    quantity: 1
    equipped: true
    filter_type: "Armor"
    ref: "/compendium/items/escudo/"
    armor_class: 2
    armor_type: 4 # Shield
```

### 2. Algoritmo de Cálculo Dinâmico no Template Hugo
No início do template `character.html`, utilizaremos o `newScratch` do Hugo para calcular dinamicamente os atributos reais a partir dos valores base de `.Params.char_info.stats`, aplicando:
1. **Stat Overrides**: Modificadores do tipo `stat_override` (ex: `str: 21` das Luvas de Força). Se o valor do item for maior que o valor base, substitui.
2. **Stat Bonuses**: Modificadores do tipo `stat_bonus` (ex: `dex: 1`). Adiciona ao valor base.
3. **Cálculo de Modificadores**: `math.Floor((score - 10) / 2)` para obter os novos modificadores.
4. **Propagação para Salvaguardas e Perícias**: Calcular o delta entre o novo modificador e o modificador base do personagem, adicionando esse delta aos bônus salvos no arquivo Markdown.
5. **Cálculo da CA**:
   - Identificar a armadura equipada (Leve, Média, Pesada ou Sem Armadura) e escudo equipado.
   - Aplicar a fórmula de CA correta com base na Destreza calculada (limitar a +2 para armaduras médias, desconsiderar para armaduras pesadas).
   - Somar os bônus de CA (`modifiers.ac_bonus`) de todos os itens mágicos equipados.

### 3. Melhorias Visuais na Interface
- **Armas**: Exibir tipo de dano, propriedades e alcance usando badges ou texto compacto ao lado dos botões de rolagem de ataque/dano.
- **Opacidade para Não Equipados**: Itens com `equipped: false` serão renderizados com opacidade `0.5` e exibirão um badge discreto "Não Equipado", diferenciando claramente o inventário ativo do passivo.

## Risks / Trade-offs

- **[Risco] Double-counting de modificadores mágicos de CA ou Atributos**  
  → *Mitigação*: O importador `import_dndbeyond.py` deve gravar apenas os modificadores individuais de cada item em sua respectiva entrada de equipamento, e não deve somar previamente esses modificadores mágicos nos atributos base ou CA base salvos nos campos de topo (`char_info.stats` ou `char_info.ac`). Esses campos de topo representarão apenas o estado natural e básico do personagem, deixando toda a lógica cumulativa para o template Hugo resolver em tempo de build.
