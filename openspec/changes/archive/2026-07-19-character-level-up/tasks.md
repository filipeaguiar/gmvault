## 1. XPHB progression resolution

- [x] 1.1 Add pure helpers that load the selected XPHB class/subclass progression and return target-level features without duplicates.
- [x] 1.2 Add validation for eligible character state and a serializable level-up plan containing deterministic changes and pending choices.
- [x] 1.3 Add fixtures covering a base class gain, subclass gain, repeated feature, unresolved reference, and source-priority fallback.

## 2. Character state application

- [x] 2.1 Implement confirmed application of class level, total level, proficiency bonus, selected hit-point gain, spell slots, feature actions, and compendium references.
- [x] 2.2 Implement interactive prompts for hit points and required choices, with cancellation leaving the file untouched.
- [x] 2.3 Preserve manual fields, unresolved legacy values, existing action state, and Markdown body while deduplicating new references.

## 3. Editor and rendering integration

- [x] 3.1 Add the level-up operation and plan preview to `edit_character.py`.
- [x] 3.2 Ensure the Class tab renders target-level features from canonical references and does not expose future levels.
- [x] 3.3 Add integration tests for editor level-up, character-sheet rendering, and cancellation behavior.

## 4. Validation

- [x] 4.1 Run focused Python tests, full Python tests, Hugo draft and production builds, and OpenSpec validation.
- [x] 4.2 Document the local level-up workflow and its supported XPHB scope.
