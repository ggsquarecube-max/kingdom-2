# Kingdom-2 P0 core specification

This is the minimum viable implementation target for the first milestone.

## Goals

The P0 core should produce a reproducible and reviewable foundation for Kingdom-2 before Android interface work expands.

## In scope

### 1. Evidence and provenance

- store evidence records
- record source metadata and assumptions
- track confidence and uncertainty
- maintain provenance lineage

### 2. Dependency graph

- model data and computation dependencies
- identify missing or stale dependencies
- expose validation status
- flag dependency failures that affect results

### 3. Run manifests

- launch metadata and configuration capture
- input and output tracking
- environment capture
- reproducibility hash generation

### 4. Verification engine

- create verification entries
- record pass/fail/inconclusive outcomes
- attach evidence references
- distinguish independent checks from routine tests

### 5. Test pipeline

- unit tests for core entities
- integration tests for the API contract
- regression tests for verification logic
- reproducibility checks for manifest handling

## Out of scope for P0

- full Android UI polish
- broad external integrations
- advanced analytics dashboards
- operational automation beyond the core verification flow

## Definition of done

P0 is complete when:

- a run can be created and tracked with a manifest
- all evidence records include provenance
- dependency freshness can be queried
- verification status can be attached to results
- test reports are stored and reviewable
- unknown and conflicting evidence remain visible
- a deterministic example workflow can be executed and re-run

## Required example workflow

The project should include one bounded, real example that demonstrates the system end-to-end. It should include:

- an input dataset or fixture
- a reproducible manifest
- a run execution result
- a dependency graph
- verification result
- a stored test report

This is the first concrete proof that Kingdom-2 is not just a conceptual design but a working system model.

## Acceptance gates

Every change in P0 should pass:

- unit tests covering core models
- integration tests for API endpoints
- regression tests for verification behavior
- reproducibility checks for the example workflow

## Immediate next step

The next implementation step is to create the core domain model and a minimal service scaffold that supports the EvidenceRecord, DependencyNode, RunManifest, VerificationResult, and TestReport contracts.
