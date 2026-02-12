"""Pydantic models for ProjectSpark API."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


# ── Eval Models ──────────────────────────────────────────────

class SubjectScore(BaseModel):
    accuracy: float
    tasks: int
    details: Dict[str, Any] = Field(default_factory=dict)


class ArchitectureResult(BaseModel):
    overall_accuracy: float
    subjects: Dict[str, SubjectScore]


class SensitivityAnalysis(BaseModel):
    max_variance_subject: str
    most_sensitive_architecture: str
    robustness_score: float
    subject_variances: Dict[str, float] = Field(default_factory=dict)
    overall_range: float = 0.0


class SweepMetadata(BaseModel):
    model: str
    benchmark: str
    mode: str = "demo"
    timestamp: str
    architectures_tested: int


class SweepResult(BaseModel):
    metadata: SweepMetadata
    results: Dict[str, ArchitectureResult]
    sensitivity_analysis: Optional[SensitivityAnalysis] = None


class HeatmapCell(BaseModel):
    architecture: str
    subject: str
    accuracy: float


class HeatmapResponse(BaseModel):
    cells: List[HeatmapCell]
    architectures: List[str]
    subjects: List[str]


# ── Compliance Models ────────────────────────────────────────

class ManifestRow(BaseModel):
    source_url: str
    domain: str
    content_type: str = ""
    word_count: int = 0
    date_collected: str = ""
    license: str = ""
    copyright_holder: str = ""


class AuditedRow(BaseModel):
    source_url: str
    domain: str
    content_type: str
    word_count: int
    date_collected: str
    license: str
    copyright_holder: str
    risk_level: RiskLevel
    risk_reason: str
    publisher: str = ""


class AuditSummary(BaseModel):
    total_sources: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    unknown_risk_count: int
    high_risk_percentage: float
    top_risky_domains: List[Dict[str, Any]]
    recommendations: List[str]


class AuditResult(BaseModel):
    audit_id: str
    timestamp: str
    rows: List[AuditedRow]
    summary: AuditSummary


# ── Disclosure Form ──────────────────────────────────────────

class DisclosureFormData(BaseModel):
    organization_name: str
    model_name: str
    date: str
    contact_name: str = ""
    contact_email: str = ""
    audit_id: Optional[str] = None


# ── Stats ────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    models_tested: int
    avg_robustness_score: float
    datasets_audited: int
    high_risk_sources: int
    total_sources_scanned: int
    last_eval_date: Optional[str] = None
    last_audit_date: Optional[str] = None
