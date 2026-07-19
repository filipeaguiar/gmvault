## 1. Shared synchronization

- [x] 1.1 Inventory the 5e.tools-only character resolution in `import_dndbeyond.py` and extract reusable, defensive character-reference synchronization helpers into `dnd_utils.py`.
- [x] 1.2 Resolve and deduplicate supported local character entities while preserving existing operational data and reporting unresolved entities.
- [x] 1.3 Add focused tests or fixtures for complete and unresolved local character synchronization.

## 2. Local character workflows

- [x] 2.1 Integrate complete compendium synchronization into `create_character.py` before it writes a new character.
- [x] 2.2 Integrate synchronization after editor operations that add shared content and add an explicit full synchronization action to `edit_character.py`.
- [x] 2.3 Verify local creation and editing preserve legacy front matter and do not create duplicate references.

## 3. Deprecation and validation

- [x] 3.1 Remove `import_dndbeyond.py` and references that present it as a supported command.
- [x] 3.2 Update tests and documentation for the local-only workflow and compatibility of existing imported notes.
- [ ] 3.3 Run Python tests, Hugo draft and production builds, and OpenSpec validation.
