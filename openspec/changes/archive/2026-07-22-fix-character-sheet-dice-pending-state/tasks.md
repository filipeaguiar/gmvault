## 1. Remove competing roll enhancement paths

- [x] 1.1 Stop loading the generic `roll-engine.js` on character-sheet pages used by the Owlbear flow.
- [x] 1.2 Verify that character pages outside a validated Owlbear bridge remain readable reference content without local roll activation.

## 2. Harden Dice+ pending-state ownership

- [x] 2.1 Update the sheet client so only one pending request can exist per control and stale completions after timeout or teardown are ignored.
- [x] 2.2 Update the Owlbear bridge lifecycle so iframe unbind/rebind clears ownership safely and late Dice+ responses become no-ops.
- [x] 2.3 Preserve readiness retry behavior so a sheet can transition from reference-only mode to interactive mode after Dice+ becomes available.

## 3. Add regression coverage and diagnostics

- [x] 3.1 Extend extension runtime and sheet-client tests for duplicate activation, unbind during pending roll, delayed result/error after timeout, and successful retry.
- [x] 3.2 Validate the production Hugo build for both browser reference mode and Owlbear interactive mode after the single-controller change.
