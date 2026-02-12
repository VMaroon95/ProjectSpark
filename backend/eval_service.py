"""
Evaluation Service
===================
Service layer for managing sweep results and heatmap data.
"""

import json
import os
from typing import Dict, List, Optional, Any

from .models import SweepResult, HeatmapCell, HeatmapResponse, DashboardStats

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class EvalService:
    """Manages evaluation results storage and retrieval."""

    def __init__(self):
        self._results: Dict[str, dict] = {}
        self._load_sample_data()

    def _load_sample_data(self):
        """Load sample sweep results on startup."""
        sample_path = os.path.join(DATA_DIR, "sample_sweep_results.json")
        if os.path.exists(sample_path):
            with open(sample_path) as f:
                data = json.load(f)
            self._results["sample"] = data

    def get_latest_results(self) -> Optional[dict]:
        """Return the most recent sweep results."""
        if not self._results:
            return None
        key = list(self._results.keys())[-1]
        return self._results[key]

    def store_results(self, data: dict) -> str:
        """Store new sweep results, return key."""
        key = data.get("metadata", {}).get("timestamp", str(len(self._results)))
        self._results[key] = data
        return key

    def get_heatmap(self) -> Optional[HeatmapResponse]:
        """Generate heatmap data from latest results."""
        results = self.get_latest_results()
        if not results:
            return None

        cells = []
        architectures = []
        subjects = ["stem", "humanities", "social_sciences", "other"]

        for arch_key, arch_data in results.get("results", {}).items():
            architectures.append(arch_key)
            for subj in subjects:
                subj_data = arch_data.get("subjects", {}).get(subj, {})
                acc = subj_data.get("accuracy", 0.0)
                cells.append(HeatmapCell(
                    architecture=arch_key,
                    subject=subj,
                    accuracy=round(acc, 4),
                ))

        return HeatmapResponse(
            cells=cells,
            architectures=architectures,
            subjects=subjects,
        )

    def get_stats(self) -> DashboardStats:
        """Get dashboard overview statistics."""
        latest = self.get_latest_results()
        robustness = 0.0
        last_eval = None
        if latest:
            sa = latest.get("sensitivity_analysis", {})
            robustness = sa.get("robustness_score", 0.0)
            last_eval = latest.get("metadata", {}).get("timestamp")

        return DashboardStats(
            models_tested=len(self._results),
            avg_robustness_score=robustness,
            datasets_audited=0,
            high_risk_sources=0,
            total_sources_scanned=0,
            last_eval_date=last_eval,
        )
