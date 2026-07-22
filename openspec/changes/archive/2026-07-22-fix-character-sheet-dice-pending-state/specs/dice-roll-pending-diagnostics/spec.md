## ADDED Requirements

### Requirement: Pending-roll regressions SHALL be covered by automated diagnostics
The project SHALL provide automated coverage for the pending-roll lifecycle in the Owlbear character flow, including duplicate activation prevention, iframe teardown during pending rolls, late Dice+ responses, and successful recovery after retry. The diagnostics SHALL exercise the published extension bridge and sheet client contracts rather than relying only on manual reproduction.

#### Scenario: Duplicate activation is attempted on one control
- **WHEN** the same enhanced roll value is activated again while its request is still pending
- **THEN** the diagnostics SHALL verify that no second Dice+ request is emitted for that same control until the first request resolves, errors, or times out

#### Scenario: Iframe is unbound before Dice+ responds
- **WHEN** a pending roll exists and the active character iframe is replaced or unbound before the Dice+ response arrives
- **THEN** the diagnostics SHALL verify that pending state is cleared safely and any late result or error is ignored without mutating the new iframe state

#### Scenario: Dice+ responds after a client timeout
- **WHEN** a roll request times out in the bridge and a delayed Dice+ result or error later arrives for that roll ID
- **THEN** the diagnostics SHALL verify that the delayed response is treated as an orphaned no-op and does not restore or corrupt any visible pending state

#### Scenario: A later retry succeeds after a prior failure
- **WHEN** a player retries a previously failed or timed-out roll from the same sheet control
- **THEN** the diagnostics SHALL verify that the new request receives a fresh correlation ID and can complete successfully without interference from the earlier failed request
