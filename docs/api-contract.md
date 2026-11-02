# Kingdom-2 core data model

This document defines the first core contracts needed before UI or Android work begins.

## Core entities

### EvidenceRecord

Represents a single piece of evidence or fact source.

Required fields:

- id: string
- source: string
- source_type: enum {dataset, model, observation, external_api, human_input, run_output}
- timestamp: ISO-8601 datetime
- version: string
- hash: string
- confidence: float between 0 and 1
- uncertainty: string
- assumptions: string[]
- status: enum {supported, refuted, conflicting, unknown}
- provenance: ProvenanceMetadata

### ProvenanceMetadata

- record_id: string
- parent_ids: string[]
- created_by: string
- created_at: ISO-8601 datetime
- collection_method: string
- environment: string
- transformation_steps: string[]

### DependencyNode

Represents a dependency or required upstream element in the execution graph.

Required fields:

- id: string
- name: string
- type: enum {dataset, model, external_service, configuration, run_output, assumption}
- version: string
- freshness_status: enum {fresh, stale, missing, unknown}
- last_verified_at: ISO-8601 datetime | null
- requires: string[]
- provides: string[]
- validation_state: enum {valid, invalid, unknown}

### RunManifest

Records the complete runtime context of a given computation or research run.

Required fields:

- id: string
- started_at: ISO-8601 datetime
- ended_at: ISO-8601 datetime
- inputs: string[]
- parameters: object
- environment: object
- execution_steps: string[]
- outputs: string[]
- status: enum {running, succeeded, failed, canceled, partial}
- canonical_result_id: string | null
- reproducibility_hash: string

### VerificationResult

The outcome of a verification, comparison, or independent check.

Required fields:

- id: string
- target_id: string
- method: string
- verifier: string
- status: enum {pass, fail, inconclusive, unknown}
- evidence_refs: string[]
- notes: string
- timestamp: ISO-8601 datetime

### TestReport

Summarizes a test run and its acceptance outcome.

Required fields:

- id: string
- suite_name: string
- started_at: ISO-8601 datetime
- ended_at: ISO-8601 datetime
- passed: number
- failed: number
- skipped: number
- coverage: number
- status: enum {pass, fail, partial}
- failing_tests: string[]

### ImprovementProposal

Describes a change under evaluation.

Required fields:

- id: string
- title: string
- problem_statement: string
- baseline_reference: string
- hypothesis: string
- expected_effect: string
- validation_plan: string
- status: enum {proposed, testing, accepted, rejected}

## Notes on semantics

- Evidence is not automatically true just because it appears in the system.
- Dependencies should be explicitly declared and monitored for freshness.
- Run manifests should enable reproducibility by another agent or process.
- Verification results must distinguish test evidence from unverified claims.
- Contradictions and unknowns must remain visible rather than being folded away.

## Recommended storage model

Use a normalized model with:

- evidence table / collection
- dependency graph table
- run manifest table
- verification result table
- test report table
- improvement proposal table

Relationships:

- EvidenceRecord -> many VerificationResult records
- RunManifest -> many outputs and dependency records
- DependencyNode -> many run and evidence relationships
- ImprovementProposal -> baseline and post-change test reports

## Acceptance criteria

A core implementation is considered complete when:

- every run has a manifest
- every evidence item has provenance
- every dependency can be checked for freshness
- every critical claim has verification metadata
- contradictions remain visible
- reproducibility can be independently reconstructed
