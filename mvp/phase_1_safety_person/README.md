# MVP Phase 1: Safety Person

This is an isolated MVP sandbox.

It is not the formal `src/` implementation, and it does not define the full
LEDO platform skeleton.

This phase focuses on one person safety lifecycle:

1. A `Person` is located in a `Zone`.
2. A `Hazard` affects that `Zone`.
3. The system creates an `ActionCandidate`.
4. A human approval step creates an `ApprovalDecision`.
5. An approved decision may produce an `ApprovedAction`.
6. Runtime validation checks the current state.
7. The Safety Gate permits or blocks the action.
8. Only a `SafetyGatePass` can produce an `ExecutionRequest`.

The purpose is to validate the smallest ontology-centered safety-gated
lifecycle before promoting any logic into `src/ledo_ontology_core/`.

External physical execution is out of scope. An `ExecutionRequest` is not a
physical command.

## Run the Demo

```bash
python mvp/phase_1_safety_person/run_demo.py
```

## Run the Tests

```bash
python mvp/phase_1_safety_person/test_mvp.py
```

