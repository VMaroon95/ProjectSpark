"""
Result Parser
==============
Parses lm-evaluation-harness output into the normalized ProjectSpark schema.
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .prompt_architectures import ARCHITECTURE_MAP


def parse_lm_eval_output(raw_output: dict, model: str, architecture_key: str) -> Dict[str, Any]:
    """
    Parse raw lm-evaluation-harness JSON output into normalized per-architecture result.

    Expected raw format (lm-eval v0.4+):
    {
        "results": {
            "mmlu_stem": {"acc,none": 0.584, "acc_stderr,none": 0.012},
            "mmlu_humanities": {"acc,none": 0.671, ...},
            ...
        },
        "config": {...},
        "versions": {...}
    }
    """
    SUBJECT_MAPPING = {
        "stem": ["mmlu_stem", "mmlu_abstract_algebra", "mmlu_anatomy", "mmlu_astronomy",
                 "mmlu_college_biology", "mmlu_college_chemistry", "mmlu_college_computer_science",
                 "mmlu_college_mathematics", "mmlu_college_physics"],
        "humanities": ["mmlu_humanities", "mmlu_formal_logic", "mmlu_philosophy",
                       "mmlu_high_school_european_history", "mmlu_high_school_us_history",
                       "mmlu_international_law", "mmlu_jurisprudence"],
        "social_sciences": ["mmlu_social_sciences", "mmlu_econometrics",
                            "mmlu_high_school_geography", "mmlu_high_school_psychology",
                            "mmlu_sociology", "mmlu_us_foreign_policy"],
        "other": ["mmlu_other", "mmlu_business_ethics", "mmlu_clinical_knowledge",
                  "mmlu_global_facts", "mmlu_management", "mmlu_marketing"],
    }

    TASK_COUNTS = {"stem": 57, "humanities": 52, "social_sciences": 48, "other": 43}

    results_data = raw_output.get("results", {})
    subjects = {}

    for subject, possible_keys in SUBJECT_MAPPING.items():
        acc = 0.0
        details = {}
        for key in possible_keys:
            if key in results_data:
                task_acc = results_data[key].get("acc,none", results_data[key].get("acc", 0.0))
                stderr = results_data[key].get("acc_stderr,none", results_data[key].get("acc_stderr", 0.0))
                if key.startswith(f"mmlu_{subject}") and key != f"mmlu_{subject}":
                    task_name = key.replace("mmlu_", "")
                    details[task_name] = {
                        "accuracy": round(task_acc, 4),
                        "stderr": round(stderr, 4) if stderr else None,
                    }
                elif key == f"mmlu_{subject}":
                    acc = task_acc

        subjects[subject] = {
            "accuracy": round(acc, 4),
            "tasks": TASK_COUNTS[subject],
            "details": details if details else {},
        }

    all_accs = [s["accuracy"] for s in subjects.values() if s["accuracy"] > 0]
    overall = sum(all_accs) / len(all_accs) if all_accs else 0.0

    return {
        "overall_accuracy": round(overall, 4),
        "subjects": subjects,
    }


def normalize_sweep_results(
    architecture_results: Dict[str, Dict],
    model: str,
    benchmark: str = "mmlu",
) -> Dict[str, Any]:
    """
    Build the full normalized ProjectSpark result schema from per-architecture results.
    """
    output = {
        "metadata": {
            "model": model,
            "benchmark": benchmark,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "architectures_tested": len(architecture_results),
        },
        "results": architecture_results,
        "sensitivity_analysis": _compute_sensitivity(architecture_results),
    }
    return output


def _compute_sensitivity(arch_results: Dict[str, Dict]) -> Dict[str, Any]:
    """Compute sensitivity analysis from architecture results."""
    subjects = ["stem", "humanities", "social_sciences", "other"]
    subject_variances = {}

    for subj in subjects:
        scores = []
        for arch_data in arch_results.values():
            if subj in arch_data.get("subjects", {}):
                scores.append(arch_data["subjects"][subj]["accuracy"])
        if scores:
            mean = sum(scores) / len(scores)
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)
            subject_variances[subj] = round(variance, 6)

    max_var = max(subject_variances, key=subject_variances.get) if subject_variances else "unknown"

    overall_scores = {k: v.get("overall_accuracy", 0) for k, v in arch_results.items()}
    most_sensitive = max(overall_scores, key=overall_scores.get) if overall_scores else "unknown"

    all_overall = list(overall_scores.values())
    score_range = max(all_overall) - min(all_overall) if all_overall else 0.0
    robustness = round(1.0 - min(score_range / 0.5, 1.0), 2)

    return {
        "max_variance_subject": max_var,
        "most_sensitive_architecture": most_sensitive,
        "robustness_score": robustness,
        "subject_variances": subject_variances,
        "overall_range": round(score_range, 4),
    }


def load_results(path: str) -> Dict[str, Any]:
    """Load and validate a ProjectSpark results JSON file."""
    with open(path) as f:
        data = json.load(f)

    required_keys = {"metadata", "results"}
    if not required_keys.issubset(data.keys()):
        raise ValueError(f"Missing required keys: {required_keys - data.keys()}")

    return data


def results_summary_table(data: Dict[str, Any]) -> str:
    """Generate a printable summary table from results."""
    lines = []
    meta = data["metadata"]
    lines.append(f"Model: {meta['model']}  |  Benchmark: {meta['benchmark']}  |  {meta['timestamp']}")
    lines.append("=" * 80)
    lines.append(f"{'Architecture':<20} {'Overall':>8} {'STEM':>8} {'Human.':>8} {'Soc.Sci':>8} {'Other':>8}")
    lines.append("-" * 80)

    for arch_key, arch_data in data["results"].items():
        overall = arch_data.get("overall_accuracy", 0)
        stem = arch_data.get("subjects", {}).get("stem", {}).get("accuracy", 0)
        hum = arch_data.get("subjects", {}).get("humanities", {}).get("accuracy", 0)
        soc = arch_data.get("subjects", {}).get("social_sciences", {}).get("accuracy", 0)
        oth = arch_data.get("subjects", {}).get("other", {}).get("accuracy", 0)
        lines.append(f"{arch_key:<20} {overall:>7.1%} {stem:>7.1%} {hum:>7.1%} {soc:>7.1%} {oth:>7.1%}")

    lines.append("=" * 80)

    if "sensitivity_analysis" in data:
        sa = data["sensitivity_analysis"]
        lines.append(f"Robustness Score: {sa.get('robustness_score', 'N/A')}")
        lines.append(f"Most Sensitive Subject: {sa.get('max_variance_subject', 'N/A')}")
        lines.append(f"Highest-Performing Architecture: {sa.get('most_sensitive_architecture', 'N/A')}")

    return "\n".join(lines)
