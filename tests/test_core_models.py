from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from kingdom2.example_workflow import build_demo_workflow
from kingdom2.models import (
    DependencyFreshness,
    DependencyNode,
    DependencyType,
    EvidenceRecord,
    EvidenceSourceType,
    EvidenceStatus,
    ProvenanceMetadata,
    TestReport,
    TestStatus,
    VerificationStatus,
)
from kingdom2.verification import (
    build_run_manifest,
    classify_evidence,
    compute_reproducibility_hash,
    create_test_report,
    create_verification_result,
    dependency_status,
    evaluate_dependency_freshness,
    invalidate_downstream,
    validate_dependency_graph,
    validate_manifest,
    validate_test_report,
)


def test_conflicting_evidence_never_becomes_supported():
    record = EvidenceRecord(
        id="ev-1",
        source="fixture://conflict",
        source_type=EvidenceSourceType.DATASET,
        timestamp=datetime.utcnow(),
        version="1.0",
        hash="hash-1",
        confidence=0.99,
        uncertainty="conflict",
        assumptions=["v1"],
        status=EvidenceStatus.CONFLICTING,
    )

    assert classify_evidence(record) == EvidenceStatus.CONFLICTING


def test_provenance_round_trip():
    now = datetime.utcnow()
    provenance = ProvenanceMetadata(
        record_id="prov-1",
        parent_ids=["base-1"],
        created_by="system",
        created_at=now,
        collection_method="demo_pipeline",
        environment="python-test",
        transformation_steps=["load", "verify"],
    )

    payload = provenance.to_dict()
    assert payload["record_id"] == "prov-1"
    assert payload["parent_ids"] == ["base-1"]
    assert payload["environment"] == "python-test"

    record = EvidenceRecord(
        id="ev-2",
        source="fixture://roundtrip",
        source_type=EvidenceSourceType.DATASET,
        timestamp=now,
        version="1.0",
        hash="hash-2",
        confidence=0.95,
        uncertainty="stable",
        assumptions=["roundtrip"],
        status=EvidenceStatus.SUPPORTED,
        provenance=provenance,
    )
    serialized = record.to_dict()
    assert serialized["provenance"]["record_id"] == "prov-1"
    assert serialized["status"] == "supported"


def test_reproducibility_ignores_run_id():
    first = build_run_manifest(
        run_id="run-a",
        inputs=["input-1"],
        parameters={"threshold": 0.9},
        environment={"python": "3.11"},
        execution_steps=["load", "validate"],
        outputs=["out.json"],
    )
    second = build_run_manifest(
        run_id="run-b",
        inputs=["input-1"],
        parameters={"threshold": 0.9},
        environment={"python": "3.11"},
        execution_steps=["load", "validate"],
        outputs=["out.json"],
    )
    assert compute_reproducibility_hash(first) == compute_reproducibility_hash(second)


def test_parameter_change_changes_hash():
    first = build_run_manifest(
        run_id="run-a",
        inputs=["input-1"],
        parameters={"threshold": 0.9},
        environment={"python": "3.11"},
        execution_steps=["load", "validate"],
        outputs=["out.json"],
    )
    second = build_run_manifest(
        run_id="run-a",
        inputs=["input-1"],
        parameters={"threshold": 0.8},
        environment={"python": "3.11"},
        execution_steps=["load", "validate"],
        outputs=["out.json"],
    )
    assert compute_reproducibility_hash(first) != compute_reproducibility_hash(second)


def test_missing_dependency_fails():
    dep = DependencyNode(
        id="dep-missing",
        name="missing-root",
        type=DependencyType.DATASET,
        version="1.0",
        last_verified_at=None,
    )
    assert evaluate_dependency_freshness(dep) == DependencyFreshness.MISSING


def test_dependency_cycle_fails():
    graph = {
        "a": DependencyNode(
            id="a",
            name="a",
            type=DependencyType.DATASET,
            version="1.0",
            requires=["b"],
        ),
        "b": DependencyNode(
            id="b",
            name="b",
            type=DependencyType.DATASET,
            version="1.0",
            requires=["a"],
        ),
    }
    errors = validate_dependency_graph(graph)
    assert any("cycle" in item.lower() for item in errors)


def test_upstream_change_invalidates_downstream():
    graph = {
        "source": DependencyNode(
            id="source",
            name="source",
            type=DependencyType.DATASET,
            version="1.0",
            requires=[],
        ),
        "middle": DependencyNode(
            id="middle",
            name="middle",
            type=DependencyType.DATASET,
            version="1.0",
            requires=["source"],
        ),
        "consumer": DependencyNode(
            id="consumer",
            name="consumer",
            type=DependencyType.DATASET,
            version="1.0",
            requires=["middle"],
        ),
    }
    assert invalidate_downstream(graph, "source") == {"middle", "consumer"}


def test_unknown_is_not_pass():
    result = create_verification_result(
        target_id="target-1",
        method="reference-check",
        verifier="verifier",
        status=VerificationStatus.UNKNOWN,
        evidence_refs=[],
        notes="No reliable result",
    )
    assert result.status != VerificationStatus.PASS
    assert result.status == VerificationStatus.UNKNOWN


def test_invalid_report_counts_rejected():
    report = TestReport(
        id="tr-bad",
        suite_name="suite-bad",
        started_at=datetime.utcnow(),
        ended_at=datetime.utcnow() + timedelta(minutes=1),
        passed=-1,
        failed=1,
        skipped=0,
        coverage=0.8,
        status=TestStatus.FAIL,
    )
    assert validate_test_report(report) is False


def test_demo_matches_reference_fixture():
    demo = build_demo_workflow()
    assert demo["evidence_status"] == EvidenceStatus.SUPPORTED
    assert demo["manifest_valid"] is True
    assert demo["verification"].status.value == "pass"


def test_manifest_validation_recomputes_and_checks_timestamps():
    start = datetime.utcnow()
    end = start + timedelta(minutes=1)
    manifest = build_run_manifest(
        run_id="run-manifest-check",
        inputs=["fixture://reference"],
        parameters={"threshold": 0.7},
        environment={"python": "3.11"},
        execution_steps=["load", "verify"],
        outputs=["result.json"],
        started_at=start,
        ended_at=end,
    )
    assert validate_manifest(manifest) is True


def test_inconclusive_or_partial_reporting_stays_distinct():
    partial = create_test_report(
        suite_name="partial-suite",
        passed=2,
        failed=0,
        skipped=1,
        coverage=0.8,
    )
    assert partial.status == TestStatus.PARTIAL
    assert partial.failed == 0
    assert partial.skipped == 1

    good = create_test_report(
        suite_name="good-suite",
        passed=3,
        failed=0,
        skipped=0,
        coverage=1.0,
    )
    assert good.status == TestStatus.PASS
