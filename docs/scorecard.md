# Kingdom-2 engineering scorecard and roadmap

## Scorecard

| Measurement | Desired direction |
| --- | --- |
| Reproducible runs | Increase |
| Undetected regressions | Decrease |
| Independent verification coverage | Increase |
| Unresolved critical failures | Decrease |
| Provenance completeness | Approach 100% |
| Dependency freshness | Improve |
| False-positive scientific claims | Minimize |
| Resource efficiency | Improve without sacrificing correctness |

## Improvement priorities

| Priority | Deliverable | Acceptance condition |
| --- | --- | --- |
| P0 | Evidence, provenance, manifests, dependency tracking, verification | Core correctness tests pass |
| P1 | One bounded scientific demonstration | Results independently reviewed; unknowns preserved |
| P2 | Selective external integrations | Compatibility and provenance verified |
| P3 | Resilience, observability, performance | Failure and regression tests pass |
| P4 | Android interface and ecosystem maturity | End-to-end workflows and security checks pass |

## Immediate roadmap

### Phase 1: core contracts

- EvidenceRecord
- DependencyNode
- RunManifest
- VerificationResult
- TestReport
- ImprovementProposal

### Phase 2: reproducibility and evidence

- explicit provenance handling
- dependency freshness tracking
- deterministic execution metadata
- fail-safe behavior for conflicting evidence

### Phase 3: verification and review

- independent verification checks
- regression pipelines
- reproducibility passes across runs
- explicit unknown/contradiction states

### Phase 4: interface integration

- Android dashboard for monitoring and review
- control and evidence screens
- role-aware operations
- signed workflow and audit visibility

## Critical rule

Do not use a single composite score to hide important failures.

A critical correctness or security defect must remain visible even if a broader score appears healthy.
