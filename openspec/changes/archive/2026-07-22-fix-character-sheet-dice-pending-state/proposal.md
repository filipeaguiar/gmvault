## Why

Character sheet rolls in Owlbear sometimes remain stuck in a pending state in Dice+, which makes the sheet feel unreliable during play. Investigation suggests the current page can load more than one roll controller and can lose pending-roll ownership during iframe lifecycle changes, so the fix is needed now to restore predictable player-facing behavior.

## What Changes

- Remove the generic site roll engine from character-sheet pages used by the Owlbear extension so the iframe has a single authoritative roll client.
- Harden the Owlbear Dice+ bridge and sheet client against stale iframe bindings, delayed responses, and orphaned pending rolls.
- Add diagnostic and automated coverage for repeated roll requests, iframe rebinding, and late Dice+ responses.
- Preserve non-Owlbear browsing as readable reference content without interactive roll controls.

## Capabilities

### New Capabilities
- `dice-roll-pending-diagnostics`: Defines observability and regression coverage for pending-roll lifecycle failures in the Owlbear character flow.

### Modified Capabilities
- `owlbear-character-extension`: Tighten roll ownership, pending correlation, and iframe lifecycle handling so one character sheet action maps to one Dice+ request and pending state clears safely.
- `rpg-character-sheet`: Clarify that character sheets rendered for the Owlbear extension must rely on a single validated enhancement path for interactive rolls and remain reference-only otherwise.

## Impact

- Affected code: `layouts/_default/baseof.html`, `layouts/partials/kinds/character.html`, `assets/js/roll-engine.js`, `static/owlbear-character-sheet/sheet-client.js`, `static/owlbear-character-sheet/bridge.js`, `static/owlbear-character-sheet/main.js`.
- Affected behavior: player roll activation inside the Owlbear character iframe, pending-state cleanup, and non-extension browsing of character pages.
- Affected tests: Owlbear extension runtime tests, sheet client tests, and character sheet rendering coverage.
