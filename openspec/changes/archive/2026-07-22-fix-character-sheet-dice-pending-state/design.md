## Context

The player-facing character sheet currently has two separate roll-enhancement paths in the published site: the generic site `roll-engine.js` and the Owlbear-specific `sheet-client.js`. The Owlbear extension already provides a validated bridge, per-iframe correlation, and Dice+ readiness negotiation, but the generic engine still runs on the same character pages because it is loaded from the shared site shell. This creates an ambiguous authority over `[data-roll-notation]` elements and makes it difficult to distinguish true Dice+ delays from local duplicate activation or stale pending state.

The fix also touches iframe lifecycle ownership. The extension binds a specific iframe window, clears pending rolls on unbind, and retries Dice+ readiness while the popover remains open. That is the right architectural direction, but it needs clearer ownership boundaries and regression coverage around late responses, rebinding, and repeated user actions.

## Goals / Non-Goals

**Goals:**
- Ensure character sheets inside Owlbear have exactly one authoritative interactive roll controller.
- Preserve the existing Dice+ bridge contract based on validated readiness, request correlation, and result/error routing.
- Make pending state cleanup deterministic when the iframe changes, Dice+ responds late, or the user retries.
- Keep normal browser viewing readable and non-interactive unless the validated Owlbear bridge enables enhancement.
- Add diagnostics and automated coverage for the known failure modes.

**Non-Goals:**
- Reintroduce generic auto-roll parsing for monsters or arbitrary site pages.
- Change the Dice+ protocol namespace, payload shape, or result rendering model.
- Add persistent roll history inside the character sheet.
- Introduce a new frontend framework or heavy client-side state library.

## Decisions

### 1. The Owlbear character iframe will use a single enhancement path
Character pages used by the Owlbear extension will rely only on `sheet-client.js` for roll interaction. The shared `roll-engine.js` will no longer be allowed to enhance those same values.

**Rationale:** The pending-roll bug is most plausibly caused by two controllers acting on the same DOM contract. A single controller makes ownership, testing, and diagnostics tractable.

**Alternatives considered:**
- Keep both engines and gate them with runtime flags. Rejected because it preserves hidden coupling and raises regression risk.
- Replace the Owlbear client with the generic engine. Rejected because the generic engine does not participate in the full readiness/correlation contract.

### 2. The bridge remains the only authority for Dice+ request correlation
`bridge.js` remains responsible for readiness negotiation, request validation, pending roll tracking, timeouts, and forwarding only correlated results/errors back to the originating iframe.

**Rationale:** Correlation already belongs at the extension shell because it has Owlbear identity, Dice+ channel access, and iframe ownership.

**Alternatives considered:**
- Move correlation into the page iframe. Rejected because the iframe should not know Owlbear player state or direct Dice+ channels.
- Let Dice+ state drive the sheet directly. Rejected because it would couple the sheet to extension-only APIs.

### 3. Character pages outside Owlbear remain reference-only by default
Without a validated bridge handshake, character pages will show roll metadata as readable text only.

**Rationale:** This aligns the runtime behavior with the intended progressive-enhancement contract and removes confusing half-interactive states in ordinary browsers.

**Alternatives considered:**
- Preserve local browser rolling as a fallback. Rejected because it reintroduces a second authority and diverges from the extension behavior players actually use.

### 4. Diagnostics and tests will target lifecycle failure modes explicitly
Automated coverage will exercise duplicate activation prevention, late Dice+ results, iframe rebinding/unload, and concurrent valid requests from separate actions.

**Rationale:** The bug is intermittent, so confidence must come from lifecycle-focused regression tests rather than only manual validation.

**Alternatives considered:**
- Rely on manual Owlbear testing only. Rejected because the failure is timing-sensitive and hard to reproduce consistently.

## Risks / Trade-offs

- **[Loss of generic site-side rolling]** → Mitigation: keep roll values readable and limit the change to character-sheet interaction, not the underlying metadata.
- **[Late Dice+ responses after iframe teardown]** → Mitigation: define and test orphaned-response handling as a safe no-op in the bridge.
- **[Behavior differences between local browser and Owlbear]** → Mitigation: make the difference explicit in the spec and diagnostics, with reference-only behavior outside Owlbear.
- **[Hidden dependency on `roll-engine.js` elsewhere]** → Mitigation: scope the change carefully and validate affected pages/tests before removing or excluding the generic engine.

## Migration Plan

1. Remove or exclude the generic roll engine from character-sheet pages used by the Owlbear extension.
2. Keep `sheet-client.js` as the sole interactive layer and verify it only activates after `DICE_READY(true)`.
3. Tighten bridge handling around unbind/rebind and orphaned results without changing the public Dice+ protocol.
4. Add or update automated tests for the extension runtime, sheet client, and character page rendering.
5. Validate production build behavior in both normal browser mode and Owlbear extension mode.

Rollback is straightforward: restore the previous asset inclusion and bridge behavior if the new single-controller path reveals an unexpected regression.

## Open Questions

- Should the generic `roll-engine.js` be removed entirely from the project or only excluded from character-sheet pages?
- Do we want lightweight operator diagnostics for orphaned/late results in production logs, or only test coverage?
- Is there any remaining supported non-Owlbear use case that still depends on local browser rolling for character pages?
