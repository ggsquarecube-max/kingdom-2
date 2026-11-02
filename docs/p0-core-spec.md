# Kingdom-2 API contract

This document defines the minimum API boundary between the Android interface and the Kingdom-2 core engine.

## Design goals

- keep Android as a client
- preserve engine ownership of correctness
- allow versioned evolution without breaking the interface
- require permission-aware operations
- expose evidence and verification in a structured way

## Base conventions

- protocol: HTTP/REST or equivalent service contract
- authentication: bearer token or equivalent credential
- authorization: role-based and capability-based checks
- versioning: `/v1` prefix with compatibility rules
- payloads: JSON
- errors: machine-readable with status and trace ID

## Core endpoints

### 1. Evidence endpoints

#### GET /v1/evidence/{id}
Returns a single EvidenceRecord.

#### POST /v1/evidence
Creates a new evidence record.

Required body:

- source
- source_type
- timestamp
- version
- hash
- confidence
- uncertainty
- assumptions
- status
- provenance

#### GET /v1/evidence
Returns filtered evidence records.

Supported filters:

- status
- source_type
- confidence threshold
- timestamp range
- dependency id

### 2. Dependency endpoints

#### GET /v1/dependencies/{id}
Returns a DependencyNode.

#### GET /v1/dependencies
Lists dependencies and freshness state.

#### POST /v1/dependencies/validate
Validates one or more dependencies and returns a validation result.

### 3. Run endpoints

#### POST /v1/runs
Creates a new RunManifest.

#### GET /v1/runs/{id}
Returns a run manifest with execution metadata and status.

#### GET /v1/runs/{id}/artifacts
Returns identifiers or links for run outputs.

### 4. Verification endpoints

#### POST /v1/verification
Creates a VerificationResult.

#### GET /v1/verification/{id}
Returns verification details.

#### GET /v1/verification?target_id={id}
Lists verification events for a target.

### 5. Test endpoints

#### POST /v1/tests/reports
Stores a TestReport.

#### GET /v1/tests/reports/{id}
Returns test report details.

### 6. Improvement flow

#### POST /v1/improvements
Creates an ImprovementProposal.

#### GET /v1/improvements/{id}
Returns proposal details.

#### POST /v1/improvements/{id}/evaluate
Runs comparison or validation and returns the outcome.

## Response model

Every response should include:

- status
- message
- trace_id
- data
- error_details (when applicable)

Example:

```json
{
  "status": "success",
  "message": "Evidence record retrieved",
  "trace_id": "7d80ed0d-5b7d-4d7c-9d56-2b08ae2f3c10",
  "data": {
    "id": "ev-001"
  }
}
```

## Android client responsibilities

Android should:

- fetch evidence and run state
- show user-safe summaries
- present verification and contradiction states
- send requests requiring explicit user intent
- require user confirmation for operations that change system state

Android should not:

- override evidence status silently
- hide contradictions or unknown results
- modify provenance without auditing that change
- act on unauthenticated or insufficiently authorized requests

## Acceptance criteria

The API contract is considered valid when:

- all core run data can be represented
- every result has provenance and verification metadata
- operations requiring change are permission-controlled
- versioning allows safe change management
- Android clients can obtain enough state to render dashboards and review flows without direct access to engine internals
