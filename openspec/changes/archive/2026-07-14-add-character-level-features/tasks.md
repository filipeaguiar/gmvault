## 1. Class and Subclass Feature Extraction from 5e.tools

- [x] 1.1 Update `import_dndbeyond.py` to support fetching class and subclass feature entries by level from 5e.tools JSON files.
- [x] 1.2 Implement the helper function in `import_dndbeyond.py` to write these features as compendium rule pages under `content/compendium/rules/` with `draft: true` and `status: "draft"`.
- [x] 1.3 Update the character importer in `import_dndbeyond.py` to automatically add references to these features under `compendium_refs` in character Markdown files.

## 2. Forge Export Integration

- [x] 2.1 Update `layouts/partials/helpers/forge_statblock.html` to process `compendium_refs` and extract rules/feats to include them in the Forge `abilities` array (`Z034`) for characters.
- [x] 2.2 Re-import character data for campaigns and verify that their features are correctly generated and exported in the Forge JSON statblock.
