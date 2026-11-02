# Kingdom-2

Kingdom-2 is a reproducible, adaptive computational and research system designed to coordinate evidence, models, dependencies, and verification.

The project is not an Android app. Android is one interface for observing and controlling the system, while the core engine remains platform-independent and testable.

## Purpose

Kingdom-2 should help teams and researchers:

- Bring together information, computational methods, models, and external data.
- Represent evidence, uncertainty, contradictions, and dependencies explicitly.
- Evaluate competing hypotheses and algorithms.
- Identify missing information, invalid assumptions, and failed dependencies.
- Test proposed solutions against measurable criteria.
- Preserve exactly how results were produced so they can be reproduced and challenged.
- Improve methods using verified results rather than unsupported confidence.

## Governing principle

No result is trusted merely because the system produced it.

Every result should carry:

- provenance
- assumptions
- execution history
- dependency state
- test or verification evidence
- uncertainty and contradictions

## Architecture summary

Android interface
- dashboard
- controls
- alerts
- evidence review
- approval and audit workflows

Versioned API / service boundary
- stable contracts between client and core engine
- permission-aware operations
- authenticated access to sensitive workflows

Kingdom-2 core engine
- evidence and provenance tracking
- dependency graph management
- state management and run manifests
- verification logic
- execution and reproducibility control

Data and computation layer
- models
- external integrations
- scientific workflows
- reproducible artifacts
- test and validation records

## Verification-first engineering

Kingdom-2 is built around verification, independent checks, and continuous improvement.

The system should only promote work that:

- has a baseline measurement
- includes reproducible inputs
- passes relevant tests
- records failures and limitations
- preserves provenance and run metadata
- can be independently reviewed or reproduced

## Project documentation

- [docs/architecture.md](docs/architecture.md)
- [docs/verification.md](docs/verification.md)
- [docs/scorecard.md](docs/scorecard.md)
- [docs/roadmap.md](docs/roadmap.md)

## Immediate focus

The first milestone is a P0 core foundation, not a polished interface:

1. Define core data contracts
2. Record provenance and run manifests
3. Implement verification and dependency tracking
4. Add reproducibility and regression testing
5. Then build Android against the stable API

## Core rule

Android is an observation and control interface. It is not the source of truth.
The core engine owns correctness, evidence, provenance, reproducibility, and verification.
