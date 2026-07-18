## 1. Regenerar compêndio

- [x] 1.1 Executar `python3 compendium_rebuild.py rebuild --staging /tmp/compendium-fix` para gerar staging com mapeamentos corretos
- [x] 1.2 Verificar que arquivos de armas no staging têm `type: Weapon`, `damage_type: piercing/slashing/bludgeoning`, e propriedades mapeadas
- [x] 1.3 Executar `python3 compendium_rebuild.py promote --staging /tmp/compendium-fix --apply` para promover staging para o compêndio

## 2. Validação

- [x] 2.1 Verificar que `content/compendium/items/dagger.md` tem `type: Weapon` e `damage_type: piercing`
- [x] 2.2 Verificar que `content/compendium/items/shortsword.md` tem `type: Weapon` e `damage_type: piercing`
- [x] 2.3 Executar `hugo server -D` e verificar que armas aparecem na seção de equipamentos do personagem
- [x] 2.4 Executar `hugo -D --gc --minify` para verificar build completo
