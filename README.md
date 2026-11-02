# Kingdom-2

Kingdom-2 is a reproducible, adaptive computational and research system designed to coordinate evidence, models, dependencies, and verification.

This repository now includes the first implementation scaffold for the P0 core: a minimal Python package with core domain models, a verification layer, a demonstration workflow, and tests.

## Project purpose

Kingdom-2 is not an Android-first project. Android is a client interface for the system, while the core engine remains platform-independent, testable, and evidence-driven.

## Current implementation state

The repository includes:

- a Python core package under `src/kingdom2`
- data contracts for evidence, dependencies, manifests, verification results, and proposals
- a validation and verification layer
- a demonstration workflow that shows how a run is recorded and checked
- a minimal pytest suite to validate the P0 model

## Directory structure

```text
.
├── README.md
├── pyproject.toml
├── .gitignore
├── src/
│   └── kingdom2/
│       ├── __init__.py
│       ├── models.py
│       ├── verification.py
│       └── example_workflow.py
├── tests/
│   └── test_core_models.py
├── docs/
│   ├── architecture.md
│   ├── verification.md
│   ├── scorecard.md
│   ├── roadmap.md
│   ├── core-data-model.md
│   ├── api-contract.md
│   └── p0-core-spec.md
└──
```

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
```

## Core rule

Android is an observation and control interface. The core engine owns correctness, provenance, verification, and reproducible execution.
