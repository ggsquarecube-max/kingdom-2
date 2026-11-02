from __future__ import annotations

from datetime import datetime

from kingdom2.models import (
    DependencyFreshness,
    DependencyNode,
    DependencyType,
    EvidenceRecord,
    EvidenceSourceType,
    EvidenceStatus,
    ImprovementProposal,
    ProvenanceMetadata,
    RunStatus,
)
from kingdom2.verification import (
    build_run_manifest,
    classify_evidence,
    create_verification_result,
    evaluate_dependency_freshness,
)


def build_demo_workflow() -> dict[str, object]:
    now = datetime.utcnow()

    provenance = ProvenanceMetadata(
        record_id="prov-demo-001",
        parent_ids=[],
        created_by="system",
        created_at=now,
        collection_method="demo_pipeline",
        environment="python-test",
        transformation_steps=["load_fixture", "normalize", "verify"],
    )

    evidence = EvidenceRecord(
        id="ev-demo-001",
        source="fixture://reference-dataset",
        source_type=EvidenceSourceType.DATASET,
        timestamp=now,
        version="1.0.0",
        hash="abc123",
        confidence=0.96,
        uncertainty="Low variance observed in reference sample",
        assumptions=["fixture is representative"],
        status=EvidenceStatus.SUPPORTED,
        provenance=provenance,
    )

    dependency = DependencyNode(
        id="dep-demo-001",
        name="reference-dataset",
        type=DependencyType.DATASET,
        version="1.0.0",
        freshness_status=DependencyFreshness.FRESH,
        last_verified_at=now,
        requires=[],
        provides=["ev-demo-001"],
        validation_state="valid",
    )

    manifest = build_run_manifest(
        run_id="run-demo-001",
        inputs=["fixture://reference-dataset"],
        parameters={"threshold": 0.8},
        environment={"python": "3.11", "platform": "linux"},
        execution_steps=["load", "normalize", "validate", "report"],
        outputs=["demo-output.json"],
        started_at=now,
        ended_at=now,
        status=RunStatus.SUCCEEDED,
    )

    verification = create_verification_result(
        target_id=manifest.id,
        method="independent_reference_check",
        verifier="core-verifier",
        status="pass",
        evidence_refs=[evidence.id],
        notes="Reference dataset matched expected thresholds.",
    )

    result = {
        "evidence": evidence,
        "dependency": dependency,
        "manifest": manifest,
        "verification": verification,
        "evidence_status": classify_evidence(evidence),
        "dependency_freshness": evaluate_dependency_freshness(dependency),
        "improvement": ImprovementProposal(
            id="imp-demo-001",
            title="Improve reference validation",
            problem_statement="Need stronger contradiction handling for edge-case fixtures.",
            baseline_reference="demo-run-001",
            hypothesis="A stricter validation threshold reduces false positives.",
            expected_effect="Fewer low-confidence matches are accepted.",
            validation_plan="Run regression comparisons against the reference fixture set.",
        ),
    }
    return result
