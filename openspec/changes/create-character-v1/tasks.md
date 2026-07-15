## 1. Directory and Path Migration (Species)

- [x] 1.1 Rename directory `content/compendium/races` to `content/compendium/species`.
- [x] 1.2 Update all layouts (`layouts/index.html`, `layouts/partials/kinds/character.html`) to use "Espécie" and fallback logic for `.Params.char_info.race`/`.Params.char_info.species`.
- [x] 1.3 Rename `layouts/partials/kinds/race.html` to `layouts/partials/kinds/species.html` and update its labels/content.
- [x] 1.4 Update all existing character sheets frontmatter to replace `race` with `species` and update references inside `/compendium/races/` to `/compendium/species/`.

## 2. Helper functions in dnd_utils.py

- [x] 2.1 Update `dnd_utils.py` and `import_dndbeyond.py` to support `species` kind instead of `race` (mapping `/compendium/species/` paths).
- [x] 2.2 Add local caching check in `dnd_utils.py` to search locally under `/content/compendium/` before downloading from 5e.tools.

## 3. Implement V1 CLI Script (create_character_v1.py)

- [x] 3.1 Create `create_character_v1.py` with CLI boilerplate and argparse support.
- [x] 3.2 Add species selection: fetch `races.json` from 5e.tools, list available species, let user select one, and list/select subraces/variants.
- [x] 3.3 Add class/level selection: fetch class index and class json from 5e.tools, list classes, resolve Hit Dice.
- [x] 3.4 Add stats entry: prompt for attributes, apply species/variant ability score bonuses automatically.
- [x] 3.5 Calculate derived values: HP (based on class HD + level + CON mod), speed, senses (darkvision, etc.).

## 4. File Generation and Testing

- [x] 4.1 Implement frontmatter generation for `create_character_v1.py` using `dump_yaml_indented` with the new `species` key.
- [x] 4.2 Generate the Markdown file `content/campaigns/<campaign>/characters/<slug>.md`.
- [x] 4.3 Run a test creation and verify the build with `hugo --gc --minify`.
