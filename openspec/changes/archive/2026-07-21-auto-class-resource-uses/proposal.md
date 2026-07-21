## Why

Atualmente, recursos especiais de classes como Pontos de Foco para Monges, Fúria para Bárbaros e Inspiração Bárdica para Bardos são importados ou sincronizados com `max_uses: 0` por padrão. Para acompanhar o uso desses recursos por caixas de seleção na aba de Ações da ficha de personagem, o mestre ou jogador precisa editar manualmente o front matter markdown (`char_info.actions`), definindo `max_uses` e `reset`. 
Esta mudança automatiza o preenchimento dessas propriedades a partir das definições originais das tabelas de classes do 5e.tools presentes no cache local de classes, garantindo também a retrocompatibilidade com fichas existentes que não possuem esses campos declarados.

## What Changes

- **Extração da Tabela de Classes**: Modificação de `create_character.py` e `edit_character.py` para inspecionar `classTableGroups` nos caches JSON de classes e identificar colunas que representem recursos de uso limitado.
- **Sincronização Retroativa (Criação Automática)**: Se o personagem não possuir a ação correspondente ao recurso declarada em `char_info.actions`, o script irá criá-la e inseri-la automaticamente. Se já existir, ele apenas atualizará os valores de `max_uses` e `reset` com base no nível atual.
- **Padronização do Monge (Foco)**: O sistema sempre utilizará a nomenclatura **"Foco"** (ou **"Pontos de Foco"** / **"Focus Points"**) para Monges. Caso o cache JSON legado do 5e.tools mencione "Ki" ou "Ki Points", o script fará a tradução e normalização automática para "Foco".
- **Regras Específicas de Cálculo**: Implementação de heurísticas para tratar recursos com progressão variável ou dependente de atributos (como a Inspiração Bárdica legado, baseada no modificador de Carisma).
- **Mapeamento de Tipo de Recarga (Reset)**: Mapeamento automático de tipos de recarga padrão (ex: Descanso Longo para Fúrias, Descanso Curto ou Longo para Pontos de Foco) ao gerar ou sincronizar as ações.
- **Injeção Automática**: Preenchimento correto dos atributos `max_uses` e `reset` no objeto da respectiva ação sob `char_info.actions` no front matter do personagem markdown.

## Capabilities

### New Capabilities
- `class-resource-auto-extraction`: Extração automatizada e injeção do número de usos máximos e tipo de recarga para habilidades especiais baseadas nas tabelas de classe originais do 5e.tools, com normalização de termos ("Ki" para "Foco").

### Modified Capabilities
*Nenhuma* (a renderização no frontend por meio de caixas de seleção na aba Ações já está implementada e operacional).

## Impact

- Afeta `create_character.py` e `edit_character.py`.
- Sem impacto em layouts de visualização ou esquemas de banco de dados.
- Sem quebras de compatibilidade: fichas existentes sem a definição serão atualizadas automaticamente na próxima sincronização/level up.
