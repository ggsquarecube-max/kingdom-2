# Kingdom-2 architecture

## Purpose

Kingdom-2 is a reproducible, adaptive computational and research system.

Its purpose is to unify information, computational methods, models, and evidence in a system that is:

- explicit about uncertainty
- transparent about provenance
- testable under independent verification
- capable of detecting contradictions and missed dependencies
- structured for improvement based on measured results

## Architectural direction

Android is an optional interface for Kingdom-2, not the computational foundation.

The core system should remain platform-independent and versioned so it can support multiple interfaces without embedding business logic in any one UI.

## Layered architecture

### 1. Android interface

The Android layer should handle:

- monitoring system state
- starting, pausing, and canceling permitted tasks
- presenting evidence, findings, and alerts
- enabling review and approval flows
- exposing run manifests and audit history

The Android interface should not silently convert unknown or conflicting evidence into trusted results.

### 2. Versioned API / communication layer

A stable contract should sit between the Android client and the core engine.

This layer should define:

- request and response schemas
- authentication and authorization boundaries
- permission scopes
- versioning strategy
- error and status handling

### 3. Kingdom-2 core engine

The core engine owns the truth model.

It is responsible for:

- evidence records
- provenance and lineage
- state transitions
- dependency tracking
- run execution and manifests
- verification logic
- reproducibility checks
- audit and review trails

### 4. Data and computation layer

This layer contains the system’s computational and scientific capabilities:

- models
- external integrations
- repositories and execution artifacts
- historical and current data
- test fixtures and reference data

## Design principles

### Keep the core independent of Android

The system should operate without relying on a specific mobile platform.

### Make contracts explicit

Stable API boundaries prevent incorrect assumptions between clients and engine logic.

### Preserve provenance

Every result must record where it came from, how it was generated, and what assumptions were in force.

### Prefer verification over confidence

Evidence should be classified as supported, refuted, conflicting, or unknown.

### Support offline-safe interface behavior

Android should be able to display relevant information when connectivity is limited, while preserving safe synchronization rules.

### Require permissions for actions

Sensitive operations must be gated by role-based or capability-based authorization.

## Recommended development order

1. Define the domain model
2. Define the API contracts
3. Implement the core engine
4. Add verification, provenance, tests, and reproducibility checks
5. Build Android against the stable API
6. Add integration and end-to-end validation

## Priority order

### P0

- evidence and provenance records
- dependency tracking
- run manifests
- verification results
- core correctness tests

### P1

- bounded scientific demonstration
- independent validation of selected workflows
- uncertainty and contradiction handling

### P2

- selective external integrations
- compatibility and provenance validation

### P3

- resilience, observability, performance
- regression and failure injection coverage

### P4

- Android maturity and ecosystem polish
- end-to-end UI workflows
- security and audit checks

## Final rule

Android is an interface for Kingdom-2, not the authority behind its results.
The engine remains the source of truth, and all outputs must be verifiable, reproducible, and explainable.
