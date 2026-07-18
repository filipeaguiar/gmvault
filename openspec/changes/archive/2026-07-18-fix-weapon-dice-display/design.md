## Context

Armas no compêndio continham abreviações cruas do 5e.tools em vez de valores mapeados. Isso impedía que o layout `character.html` reconhecesse armas (verificação `eq $itemInfo.type "Weapon"`) e traduzisse tipos de dano e propriedades.

O `compendium_rebuild.py` já possui `item_info()` com mapeamentos corretos:
- `type_map`: M→Weapon, R→Weapon, LA→Armor, etc.
- `damage_map`: P→piercing, S→slashing, B→bludgeoning, etc.
- `prop_map`: F→finesse, L→light, T→thrown, etc.

## Goals / Non-Goals

**Goals:**
- Regenerar todos os arquivos do compêndio com valores mapeados
- Verificar que armas exibem rolagens de dados corretamente
- Manter traduções e metadados existentes

**Non-Goals:**
- Alterar o layout `character.html` (já funciona com valores mapeados)
- Modificar scripts de importação (já usam `compendium_rebuild.py`)
- Alterar a estrutura de dados do YAML

## Decisions

**Usar `compendium_rebuild.py rebuild --apply`**
- O script já resolve entidades 5e.tools e aplica mapeamentos via `item_info()`
- Alternativa considerada: corrigir manualmente cada arquivo → rejeitada por ser propensa a erros e não escalável
- Alternativa considerada: adicionar mapeamento no `import_campaign.py` → rejeitada porque o fluxo já passa por `compendium_rebuild.py`

**Preservar traduções existentes**
- O `compendium_rebuild.py` preserva `translation` e `titulo_pt_br` quando existem
- Garante que trabalhos de tradução manual não são perdidos

## Risks / Trade-offs

- **Tradução automática anterior pode ter gerado textos inconsistentes** → Revisão manual continua necessária para conteúdo publicável
- **Arquivos com `draft: true` serão atualizados** → Testar com `hugo server -D` e `hugo -D --gc --minify` antes de publicar
