## Why

Armas no compêndio estavam exibindo abreviações cruas do 5e.tools (`type: M|XPHB`, `damage_type: P`, `properties: [F|XPHB]`) em vez de valores mapeados (`type: Weapon`, `damage_type: piercing`, `properties: [finesse]`). Isso causava:

1. Cards de armas não eram reconhecidos como armas (layout verifica `eq $itemInfo.type "Weapon"`)
2. Tipo de dano não era traduzido nos labels
3. Propriedades não eram traduzidas nos badges

O `compendium_rebuild.py` já possui o mapeamento correto, mas os arquivos no repositório não tinham sido regenerados com ele.

## What Changes

- Executar `compendium_rebuild.py rebuild --apply` para regenerar todos os arquivos do compêndio com mapeamentos corretos
- Verificar que armas agora exibem `type: Weapon`, `damage_type: piercing/slashing/bludgeoning`, e propriedades mapeadas
- Garantir que o layout `character.html` renderiza corretamente os dados mapeados

## Capabilities

### New Capabilities

### Modified Capabilities

- `compendium-structure`: Itens do compêndio agora usam valores mapeados em vez de abreviações cruas

## Impact

- Arquivos em `content/compendium/items/` e `content/compendium/magic-items/` serão regenerados
- Layout `layouts/partials/kinds/character.html` não precisa de alterações (já espera valores mapeados)
- Scripts de importação (`import_campaign.py`, `import_dndbeyond.py`) usam `compendium_rebuild.py` para resolver entidades, então estão alinhados
