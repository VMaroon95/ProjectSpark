"""
ProjectSpark Backend — FastAPI Application
============================================
"""

import io
import json
import csv as csv_module
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from .models import (
    SweepResult, HeatmapResponse, AuditResult, DisclosureFormData,
    DashboardStats, ManifestRow,
)
from .eval_service import EvalService
from .compliance_service import ComplianceAuditor
from .pdf_generator import generate_disclosure_pdf

app = FastAPI(
    title="ProjectSpark API",
    description="AI Governance & Evaluation Platform — LLM benchmark sensitivity analysis + CLEAR Act compliance",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
eval_service = EvalService()
auditor = ComplianceAuditor()

# In-memory audit storage
_audits: dict = {}


@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "ProjectSpark", "version": "1.0.0"}


@app.get("/api/eval/results")
async def get_eval_results():
    """Return latest sweep results."""
    results = eval_service.get_latest_results()
    if not results:
        raise HTTPException(status_code=404, detail="No evaluation results found")
    return results


@app.post("/api/eval/upload")
async def upload_eval_results(file: UploadFile = File(...)):
    """Upload new sweep results JSON."""
    try:
        content = await file.read()
        data = json.loads(content)
        key = eval_service.store_results(data)
        return {"status": "uploaded", "key": key}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")


@app.get("/api/eval/heatmap", response_model=HeatmapResponse)
async def get_heatmap():
    """Return heatmap-formatted data (architecture x subject matrix)."""
    heatmap = eval_service.get_heatmap()
    if not heatmap:
        raise HTTPException(status_code=404, detail="No evaluation results found")
    return heatmap


@app.post("/api/compliance/audit", response_model=AuditResult)
async def run_audit(file: UploadFile = File(...)):
    """Upload CSV manifest, return audit results."""
    try:
        content = (await file.read()).decode("utf-8")
        reader = csv_module.DictReader(io.StringIO(content))
        rows = []
        for row in reader:
            rows.append(ManifestRow(
                source_url=row.get("source_url", ""),
                domain=row.get("domain", ""),
                content_type=row.get("content_type", ""),
                word_count=int(row.get("word_count", 0) or 0),
                date_collected=row.get("date_collected", ""),
                license=row.get("license", ""),
                copyright_holder=row.get("copyright_holder", ""),
            ))

        result = auditor.audit_manifest(rows)
        _audits[result.audit_id] = result

        # Update stats
        eval_service.get_stats().datasets_audited += 1

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


@app.get("/api/compliance/audit/{audit_id}", response_model=AuditResult)
async def get_audit(audit_id: str):
    """Get audit results by ID."""
    if audit_id not in _audits:
        raise HTTPException(status_code=404, detail=f"Audit {audit_id} not found")
    return _audits[audit_id]


@app.post("/api/compliance/disclosure-pdf")
async def generate_disclosure(form_data: DisclosureFormData):
    """Generate Federal Disclosure Form PDF."""
    audit = None
    if form_data.audit_id and form_data.audit_id in _audits:
        audit = _audits[form_data.audit_id]

    pdf_bytes = generate_disclosure_pdf(form_data, audit)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=CLEAR_Act_Disclosure_Form.pdf"},
    )


@app.get("/api/stats", response_model=DashboardStats)
async def get_stats():
    """Dashboard overview stats."""
    stats = eval_service.get_stats()
    stats.datasets_audited = len(_audits)
    stats.high_risk_sources = sum(
        a.summary.high_risk_count for a in _audits.values()
    )
    stats.total_sources_scanned = sum(
        a.summary.total_sources for a in _audits.values()
    )
    if _audits:
        stats.last_audit_date = list(_audits.values())[-1].timestamp
    return stats
