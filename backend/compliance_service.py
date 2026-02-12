"""
Compliance Auditing Service
=============================
Audits dataset manifests for copyright risk using the known publisher database.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from urllib.parse import urlparse

from .models import (
    ManifestRow, AuditedRow, AuditResult, AuditSummary, RiskLevel,
)
from .copyright_domains import HIGH_RISK_DOMAINS, MEDIUM_RISK_DOMAINS, LOW_RISK_DOMAINS


class ComplianceAuditor:
    """Audits dataset manifests for copyright risk."""

    def __init__(self):
        self._high = HIGH_RISK_DOMAINS
        self._medium = MEDIUM_RISK_DOMAINS
        self._low = LOW_RISK_DOMAINS

    def _extract_domain(self, url_or_domain: str) -> str:
        """Extract the registrable domain from a URL or domain string."""
        if not url_or_domain:
            return ""
        if "://" not in url_or_domain:
            url_or_domain = "https://" + url_or_domain
        try:
            parsed = urlparse(url_or_domain)
            host = parsed.hostname or ""
        except Exception:
            host = url_or_domain

        host = host.lower().strip()
        if host.startswith("www."):
            host = host[4:]
        return host

    def _classify_domain(self, domain: str) -> tuple:
        """Returns (risk_level, reason, publisher)."""
        domain = domain.lower().strip()
        if domain.startswith("www."):
            domain = domain[4:]

        # Check exact match first, then suffix match
        for db, level in [
            (self._high, RiskLevel.HIGH),
            (self._medium, RiskLevel.MEDIUM),
            (self._low, RiskLevel.LOW),
        ]:
            if domain in db:
                info = db[domain]
                return level, info["reason"], info.get("publisher", "")
            # Check if domain ends with a known domain (subdomain match)
            for known_domain, info in db.items():
                if domain.endswith("." + known_domain) or domain == known_domain:
                    return level, info["reason"], info.get("publisher", "")

        return RiskLevel.UNKNOWN, "Domain not in known database — manual review recommended", ""

    def audit_manifest(self, rows: List[ManifestRow]) -> AuditResult:
        """Audit each row in the manifest and return a detailed report."""
        audited_rows = []

        for row in rows:
            domain = self._extract_domain(row.domain or row.source_url)
            risk_level, reason, publisher = self._classify_domain(domain)

            audited_rows.append(AuditedRow(
                source_url=row.source_url,
                domain=domain,
                content_type=row.content_type,
                word_count=row.word_count,
                date_collected=row.date_collected,
                license=row.license,
                copyright_holder=row.copyright_holder or publisher,
                risk_level=risk_level,
                risk_reason=reason,
                publisher=publisher,
            ))

        summary = self.generate_summary(audited_rows)

        return AuditResult(
            audit_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(timezone.utc).isoformat(),
            rows=audited_rows,
            summary=summary,
        )

    def generate_summary(self, rows: List[AuditedRow]) -> AuditSummary:
        """Generate summary statistics from audited rows."""
        total = len(rows)
        high = sum(1 for r in rows if r.risk_level == RiskLevel.HIGH)
        medium = sum(1 for r in rows if r.risk_level == RiskLevel.MEDIUM)
        low = sum(1 for r in rows if r.risk_level == RiskLevel.LOW)
        unknown = sum(1 for r in rows if r.risk_level == RiskLevel.UNKNOWN)

        # Top risky domains
        domain_risk: Dict[str, Dict[str, Any]] = {}
        for r in rows:
            if r.risk_level in (RiskLevel.HIGH, RiskLevel.MEDIUM):
                if r.domain not in domain_risk:
                    domain_risk[r.domain] = {
                        "domain": r.domain,
                        "publisher": r.publisher,
                        "risk_level": r.risk_level.value,
                        "count": 0,
                        "total_words": 0,
                    }
                domain_risk[r.domain]["count"] += 1
                domain_risk[r.domain]["total_words"] += r.word_count

        top_risky = sorted(domain_risk.values(), key=lambda x: (-1 if x["risk_level"] == "high" else 0, -x["count"]))[:10]

        # Recommendations
        recommendations = []
        if high > 0:
            recommendations.append(f"⚠️  {high} high-risk sources detected — remove or obtain licensing agreements before training.")
        if medium > 0:
            recommendations.append(f"⚡ {medium} medium-risk sources — verify attribution requirements and TOS compliance.")
        if unknown > 0:
            recommendations.append(f"❓ {unknown} sources from unknown domains — conduct manual copyright review.")
        if high == 0 and medium == 0:
            recommendations.append("✅ No high or medium risk sources detected. Dataset appears compliant.")
        recommendations.append("📋 Generate a Federal Disclosure Form for regulatory filing.")

        return AuditSummary(
            total_sources=total,
            high_risk_count=high,
            medium_risk_count=medium,
            low_risk_count=low,
            unknown_risk_count=unknown,
            high_risk_percentage=round(high / total * 100, 1) if total else 0.0,
            top_risky_domains=top_risky,
            recommendations=recommendations,
        )
