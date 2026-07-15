## 1. Importer Updates

- [x] 1.1 Extract size and alignment from D&D Beyond API and map sizeId/alignmentId to strings.
- [x] 1.2 Extract and compute character movement speeds (walk, swim, climb, fly, burrow) including custom overrides.
- [x] 1.3 Extract and calculate saving throw proficiencies and final modifiers.
- [x] 1.4 Extract senses (passive perception, darkvision) and known languages.
- [x] 1.5 Update Markdown templates in `import_dndbeyond.py` to output the new attributes under `char_info`.

## 2. Layout Refactoring

- [x] 2.1 Update `forge_statblock.html` to read movement speed directly from `char_info.speed`.
- [x] 2.2 Update `forge_statblock.html` to read saving throw modifiers and text directly from `char_info.saves` and `char_info.saves_summary`.

## 3. Migration and Verification

- [x] 3.1 Re-import all campaign characters using the updated script to refresh their front matter metadata.
- [x] 3.2 Run Hugo build to verify that the statblocks JSON export compiles correctly.
- [x] 3.3 Run Python tests to ensure no regressions are introduced.
