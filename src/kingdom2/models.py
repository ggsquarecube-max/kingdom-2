from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any


class EvidenceSourceType(str, Enum):
    DATASET = "dataset"
    MODEL = "model"
    OBSERVATION = "observation"
    EXTERNAL_API = "external_api"
    HUMAN_INPUT = "human_input"
    RUN_OUTPUT = "run_output"


class EvidenceStatus(str, Enum):
    SUPPORTED = "supported"
    REFUTED = "refuted"
    CONFLICTING = "conflicting"
    UNKNOWN = "unknown"


class DependencyType(str, Enum):
    DATASET = "dataset"
    MODEL = "model"
    EXTERNAL_SERVICE = "external_service"
    CONFIGURATION = "configuration"
    RUN_OUTPUT = "run_output"
    ASSUMPTION = "assumption"


class DependencyFreshness(str, Enum):
    FRESH = "fresh"
    STALE = "stale"
    MISSING = "missing"
    UNKNOWN = "unknown"


class ValidationState(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class RunStatus(str, Enum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    PARTIAL = "partial"


class VerificationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class TestStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"


class ImprovementStatus(str, Enum):
    PROPOSED = "proposed"
    TESTING = "testing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(slots=True)
class ProvenanceMetadata:
    record_id: str
    parent_ids: list[str] = field(default_factory=list)
    created_by: str = "system"
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    collection_method: str = "manual"
    environment: str = "unknown"
    transformation_steps: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceRecord:
    id: str
    source: str
    source_type: EvidenceSourceType
    timestamp: datetime
    version: str
    hash: str
    confidence: float
    uncertainty: str
    assumptions: list[str] = field(default_factory=list)
    status: EvidenceStatus = EvidenceStatus.UNKNOWN
    provenance: ProvenanceMetadata | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "source_type": self.source_type.value,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "hash": self.hash,
            "confidence": self.confidence,
            "uncertainty": self.uncertainty,
            "assumptions": self.assumptions,
            "status": self.status.value,
            "provenance": self.provenance.to_dict() if self.provenance else None,
        }


@dataclass(slots=True)
class DependencyNode:
    id: str
    name: str
    type: DependencyType
    version: str
    freshness_status: DependencyFreshness = DependencyFreshness.UNKNOWN
    last_verified_at: datetime | None = None
    requires: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)
    validation_state: ValidationState = ValidationState.UNKNOWN

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "version": self.version,
            "freshness_status": self.freshness_status.value,
            "last_verified_at": self.last_verified_at.isoformat() if self.last_verified_at else None,
            "requires": self.requires,
            "provides": self.provides,
            "validation_state": self.validation_state.value,
        }


@dataclass(slots=True)
class RunManifest:
    id: str
    started_at: datetime
    ended_at: datetime
    inputs: list[str]
    parameters: dict[str, Any]
    environment: dict[str, Any]
    execution_steps: list[str]
    outputs: list[str]
    status: RunStatus
    canonical_result_id: str | None = None
    reproducibility_hash: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat(),
            "inputs": self.inputs,
            "parameters": self.parameters,
            "environment": self.environment,
            "execution_steps": self.execution_steps,
            "outputs": self.outputs,
            "status": self.status.value,
            "canonical_result_id": self.canonical_result_id,
            "reproducibility_hash": self.reproducibility_hash,
        }


@dataclass(slots=True)
class VerificationResult:
    id: str
    target_id: str
    method: str
    verifier: str
    status: VerificationStatus
    evidence_refs: list[str] = field(default_factory=list)
    notes: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.utcnow())

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "target_id": self.target_id,
            "method": self.method,
            "verifier": self.verifier,
            "status": self.status.value,
            "evidence_refs": self.evidence_refs,
            "notes": self.notes,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass(slots=True)
class TestReport:
    id: str
    suite_name: str
    started_at: datetime
    ended_at: datetime
    passed: int
    failed: int
    skipped: int
    coverage: float
    status: TestStatus
    failing_tests: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "suite_name": self.suite_name,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat(),
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "coverage": self.coverage,
            "status": self.status.value,
            "failing_tests": self.failing_tests,
        }


@dataclass(slots=True)
class ImprovementProposal:
    id: str
    title: str
    problem_statement: str
    baseline_reference: str
    hypothesis: str
    expected_effect: str
    validation_plan: str
    status: ImprovementStatus = ImprovementStatus.PROPOSED

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "problem_statement": self.problem_statement,
            "baseline_reference": self.baseline_reference,
            "hypothesis": self.hypothesis,
            "expected_effect": self.expected_effect,
            "validation_plan": self.validation_plan,
            "status": self.status.value,
        }


@dataclass(slots=True)
class DomainModel:
    evidence: list[EvidenceRecord] = field(default_factory=list)
    dependencies: list[DependencyNode] = field(default_factory=list)
    runs: list[RunManifest] = field(default_factory=list)
    verifications: list[VerificationResult] = field(default_factory=list)
    tests: list[TestReport] = field(default_factory=list)
    improvements: list[ImprovementProposal] = field(default_factory=list)

    def add_evidence(self, record: EvidenceRecord) -> None:
        self.evidence.append(record)

    def add_dependency(self, dependency: DependencyNode) -> None:
        self.dependencies.append(dependency)

    def add_run(self, manifest: RunManifest) -> None:
        self.runs.append(manifest)

    def add_verification(self, verification: VerificationResult) -> None:
        self.verifications.append(verification)

    def add_test_report(self, test_report: TestReport) -> None:
        self.tests.append(test_report)

    def add_improvement(self, improvement: ImprovementProposal) -> None:
        self.improvements.append(improvement)


def stale_threshold() -> timedelta:
    return timedelta(days=7)


def is_stale(dep: DependencyNode, now: datetime | None = None) -> bool:
    if dep.last_verified_at is None:
        return True
    if now is None:
        now = datetime.utcnow()
    return now - dep.last_verified_at > stale_threshold()
