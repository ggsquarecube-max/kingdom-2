from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta
from typing import Any

from kingdom2.models import (
    DependencyFreshness,
    DependencyNode,
    EvidenceRecord,
    EvidenceStatus,
    RunManifest,
    RunStatus,
    TestReport,
    TestStatus,
    VerificationResult,
    VerificationStatus,
)


def classify_evidence(record: EvidenceRecord) -> EvidenceStatus:
    if record.confidence >= 0.9 and record.status != EvidenceStatus.REFUTED:
        return EvidenceStatus.SUPPORTED
    if record.confidence <= 0.2:
        return EvidenceStatus.UNKNOWN
    if record.status == EvidenceStatus.CONFLICTING:
        return EvidenceStatus.CONFLICTING
    if record.status == EvidenceStatus.REFUTED:
        return EvidenceStatus.REFUTED
    return EvidenceStatus.UNKNOWN


def evaluate_dependency_freshness(dep: DependencyNode, now: datetime | None = None) -> DependencyFreshness:
    if dep.last_verified_at is None:
        return DependencyFreshness.MISSING
    if now is None:
        now = datetime.utcnow()
    if now - dep.last_verified_at > timedelta(days=7):
        return DependencyFreshness.STALE
    return DependencyFreshness.FRESH


def compute_reproducibility_hash(manifest: RunManifest) -> str:
    payload = {
        "id": manifest.id,
        "inputs": manifest.inputs,
        "parameters": manifest.parameters,
        "environment": manifest.environment,
        "execution_steps": manifest.execution_steps,
        "outputs": manifest.outputs,
        "status": manifest.status.value,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_run_manifest(
    run_id: str,
    inputs: list[str],
    parameters: dict[str, Any],
    environment: dict[str, Any],
    execution_steps: list[str],
    outputs: list[str],
    started_at: datetime | None = None,
    ended_at: datetime | None = None,
    status: RunStatus = RunStatus.SUCCEEDED,
) -> RunManifest:
    started = started_at or datetime.utcnow()
    ended = ended_at or started
    manifest = RunManifest(
        id=run_id,
        started_at=started,
        ended_at=ended,
        inputs=inputs,
        parameters=parameters,
        environment=environment,
        execution_steps=execution_steps,
        outputs=outputs,
        status=status,
    )
    manifest.reproducibility_hash = compute_reproducibility_hash(manifest)
    return manifest


def create_verification_result(
    target_id: str,
    method: str,
    verifier: str,
    status: VerificationStatus,
    evidence_refs: list[str] | None = None,
    notes: str = "",
) -> VerificationResult:
    return VerificationResult(
        id=f"vr-{target_id}-{len(evidence_refs or [])}",
        target_id=target_id,
        method=method,
        verifier=verifier,
        status=status,
        evidence_refs=evidence_refs or [],
        notes=notes,
    )


def create_test_report(
    suite_name: str,
    passed: int,
    failed: int,
    skipped: int,
    coverage: float,
    failing_tests: list[str] | None = None,
    started_at: datetime | None = None,
    ended_at: datetime | None = None,
) -> TestReport:
    start = started_at or datetime.utcnow()
    end = ended_at or start
    status = TestStatus.PASS if failed == 0 else TestStatus.FAIL
    return TestReport(
        id=f"tr-{suite_name.lower().replace(' ', '-')}",
        suite_name=suite_name,
        started_at=start,
        ended_at=end,
        passed=passed,
        failed=failed,
        skipped=skipped,
        coverage=coverage,
        status=status,
        failing_tests=failing_tests or [],
    )


def validate_manifest(manifest: RunManifest) -> bool:
    return bool(
        manifest.id
        and manifest.inputs
        and manifest.environment
        and manifest.execution_steps
        and manifest.outputs
        and manifest.reproducibility_hash
    )
