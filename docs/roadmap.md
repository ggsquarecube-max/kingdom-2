# Kingdom-2 roadmap

## Immediate milestone

The first implementation package should establish the P0 core without a large UI surface.

### Deliverables

1. Core domain model
   - evidence
   - dependency graph
   - run manifests
   - verification state

2. Verification engine
   - reproducibility checks
   - comparison logic
   - contradiction and unknown handling

3. CI gating
   - unit and integration tests
   - regression checks
   - reproducibility coverage

4. Bounded demonstration workflow
   - a small but meaningful real execution path
   - independent validation
   - clear provenance capture

## After the core stabilizes

- build Android around the API
- add review and approval interfaces
- expose evidence and audit history
- integrate with selected external services

## Final recommendation

Kingdom-2 should be designed around a single governing rule:

> No result is trusted merely because the system produced it.

Results must carry evidence, reproducible execution history, test results, and an appropriate level of independent verification.
