"""
Sensitivity Sweep Engine
=========================
Runs a model through all prompt architectures on a benchmark,
collecting per-subject accuracy scores.
"""

import json
import csv
import random
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from .prompt_architectures import ALL_ARCHITECTURES, PromptArchitecture


class SweepResults:
    """Container for sweep results with export capabilities."""

    def __init__(self, model: str, benchmark: str, mode: str):
        self.model = model
        self.benchmark = benchmark
        self.mode = mode
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.architecture_results: Dict[str, Dict[str, Any]] = {}
        self.sensitivity_analysis: Dict[str, Any] = {}

    def add_architecture_result(self, arch_key: str, overall: float, subjects: Dict[str, Dict]):
        self.architecture_results[arch_key] = {
            "overall_accuracy": round(overall, 4),
            "subjects": subjects,
        }

    def compute_sensitivity(self):
        """Compute cross-architecture sensitivity metrics."""
        subject_variances = {}
        all_subjects = ["stem", "humanities", "social_sciences", "other"]

        for subj in all_subjects:
            scores = []
            for arch_data in self.architecture_results.values():
                if subj in arch_data["subjects"]:
                    scores.append(arch_data["subjects"][subj]["accuracy"])
            if scores:
                mean = sum(scores) / len(scores)
                variance = sum((s - mean) ** 2 for s in scores) / len(scores)
                subject_variances[subj] = round(variance, 6)

        max_var_subject = max(subject_variances, key=subject_variances.get) if subject_variances else "unknown"

        overall_scores = {k: v["overall_accuracy"] for k, v in self.architecture_results.items()}
        most_sensitive = max(overall_scores, key=overall_scores.get) if overall_scores else "unknown"

        all_scores = [v["overall_accuracy"] for v in self.architecture_results.values()]
        if all_scores:
            score_range = max(all_scores) - min(all_scores)
            robustness = round(1.0 - min(score_range / 0.5, 1.0), 2)
        else:
            robustness = 0.0

        self.sensitivity_analysis = {
            "max_variance_subject": max_var_subject,
            "most_sensitive_architecture": most_sensitive,
            "robustness_score": robustness,
            "subject_variances": subject_variances,
            "overall_range": round(score_range, 4) if all_scores else 0.0,
        }

    def to_dict(self) -> dict:
        return {
            "metadata": {
                "model": self.model,
                "benchmark": self.benchmark,
                "mode": self.mode,
                "timestamp": self.timestamp,
                "architectures_tested": len(self.architecture_results),
            },
            "results": self.architecture_results,
            "sensitivity_analysis": self.sensitivity_analysis,
        }


class SensitivitySweep:
    """Runs a model through all prompt architectures on MMLU benchmark."""

    SUBJECTS = ["stem", "humanities", "social_sciences", "other"]

    SUBJECT_TASK_COUNTS = {
        "stem": 57,
        "humanities": 52,
        "social_sciences": 48,
        "other": 43,
    }

    # Realistic demo baselines per (architecture, subject)
    DEMO_SCORES = {
        "zero_shot": {
            "stem": 0.584, "humanities": 0.671, "social_sciences": 0.689, "other": 0.614,
        },
        "chain_of_thought": {
            "stem": 0.698, "humanities": 0.723, "social_sciences": 0.741, "other": 0.712,
        },
        "persona_based": {
            "stem": 0.651, "humanities": 0.702, "social_sciences": 0.694, "other": 0.653,
        },
        "few_shot": {
            "stem": 0.672, "humanities": 0.701, "social_sciences": 0.714, "other": 0.678,
        },
        "delimiter_heavy": {
            "stem": 0.623, "humanities": 0.682, "social_sciences": 0.697, "other": 0.641,
        },
    }

    STEM_TASKS = [
        "abstract_algebra", "anatomy", "astronomy", "college_biology",
        "college_chemistry", "college_computer_science", "college_mathematics",
        "college_physics", "computer_security", "conceptual_physics",
        "electrical_engineering", "elementary_mathematics", "high_school_biology",
        "high_school_chemistry", "high_school_computer_science",
        "high_school_mathematics", "high_school_physics", "high_school_statistics",
        "machine_learning",
    ]

    HUMANITIES_TASKS = [
        "formal_logic", "high_school_european_history",
        "high_school_us_history", "high_school_world_history",
        "international_law", "jurisprudence", "logical_fallacies",
        "moral_disputes", "moral_scenarios", "philosophy",
        "prehistory", "professional_law", "world_religions",
    ]

    SOCIAL_SCIENCE_TASKS = [
        "econometrics", "high_school_geography",
        "high_school_government_and_politics", "high_school_macroeconomics",
        "high_school_microeconomics", "high_school_psychology",
        "human_sexuality", "professional_psychology", "public_relations",
        "security_studies", "sociology", "us_foreign_policy",
    ]

    OTHER_TASKS = [
        "business_ethics", "clinical_knowledge", "college_medicine",
        "global_facts", "human_aging", "management",
        "marketing", "medical_genetics", "miscellaneous",
        "nutrition", "professional_accounting", "professional_medicine",
        "virology",
    ]

    def __init__(self, model_name: str, architectures: Optional[List[PromptArchitecture]] = None,
                 benchmark: str = "mmlu", mode: str = "demo"):
        self.model_name = model_name
        self.architectures = architectures or ALL_ARCHITECTURES
        self.benchmark = benchmark
        self.mode = mode
        self.results = SweepResults(model_name, benchmark, mode)

    def _seeded_noise(self, base: float, seed_str: str, spread: float = 0.03) -> float:
        """Deterministic noise based on seed string for reproducibility."""
        h = int(hashlib.sha256(seed_str.encode()).hexdigest()[:8], 16)
        noise = ((h % 10000) / 10000.0 - 0.5) * 2 * spread
        return max(0.0, min(1.0, base + noise))

    def _generate_task_details(self, tasks: List[str], base_acc: float, arch_key: str) -> Dict:
        details = {}
        for task in tasks:
            seed = f"{self.model_name}:{arch_key}:{task}"
            acc = self._seeded_noise(base_acc, seed, spread=0.06)
            n_samples = 80 + (int(hashlib.sha256(task.encode()).hexdigest()[:4], 16) % 120)
            correct = int(n_samples * acc)
            details[task] = {
                "accuracy": round(acc, 4),
                "correct": correct,
                "total": n_samples,
            }
        return details

    def _run_demo(self):
        """Generate realistic demo results."""
        for arch in self.architectures:
            base_scores = self.DEMO_SCORES.get(arch.key, self.DEMO_SCORES["zero_shot"])
            subjects = {}
            task_map = {
                "stem": self.STEM_TASKS,
                "humanities": self.HUMANITIES_TASKS,
                "social_sciences": self.SOCIAL_SCIENCE_TASKS,
                "other": self.OTHER_TASKS,
            }

            weighted_sum = 0.0
            total_tasks = 0

            for subj in self.SUBJECTS:
                base = base_scores[subj]
                seed = f"{self.model_name}:{arch.key}:{subj}"
                acc = self._seeded_noise(base, seed, spread=0.008)
                tasks = task_map[subj]
                details = self._generate_task_details(tasks, acc, arch.key)
                n_tasks = self.SUBJECT_TASK_COUNTS[subj]

                subjects[subj] = {
                    "accuracy": round(acc, 4),
                    "tasks": n_tasks,
                    "details": details,
                }

                weighted_sum += acc * n_tasks
                total_tasks += n_tasks

            overall = weighted_sum / total_tasks if total_tasks else 0.0
            self.results.add_architecture_result(arch.key, overall, subjects)

    def _run_live(self):
        """Interface with lm-evaluation-harness for live evaluation."""
        try:
            import lm_eval
            from lm_eval import evaluator, tasks

            for arch in self.architectures:
                task_manager = tasks.TaskManager()
                results = evaluator.simple_evaluate(
                    model="hf",
                    model_args=f"pretrained={self.model_name},trust_remote_code=True",
                    tasks=["mmlu"],
                    num_fewshot=3 if arch.key == "few_shot" else 0,
                    batch_size="auto",
                )

                subjects = {}
                for subj in self.SUBJECTS:
                    subj_key = f"mmlu_{subj}"
                    if subj_key in results["results"]:
                        acc = results["results"][subj_key].get("acc,none", 0.0)
                    else:
                        acc = 0.0
                    subjects[subj] = {
                        "accuracy": round(acc, 4),
                        "tasks": self.SUBJECT_TASK_COUNTS[subj],
                        "details": {},
                    }

                overall_acc = results["results"].get("mmlu", {}).get("acc,none", 0.0)
                self.results.add_architecture_result(arch.key, overall_acc, subjects)

        except ImportError:
            print("⚠  lm-evaluation-harness not installed. Falling back to demo mode.")
            print("   Install with: pip install lm-eval")
            self._run_demo()

    def run_sweep(self) -> SweepResults:
        """Execute the sensitivity sweep."""
        if self.mode == "live":
            self._run_live()
        else:
            self._run_demo()

        self.results.compute_sensitivity()
        return self.results

    def export_json(self, path: str):
        """Export results to JSON file."""
        with open(path, "w") as f:
            json.dump(self.results.to_dict(), f, indent=2)
        print(f"✓ Results exported to {path}")

    def export_csv(self, path: str):
        """Export results to CSV file."""
        rows = []
        for arch_key, arch_data in self.results.architecture_results.items():
            for subj, subj_data in arch_data["subjects"].items():
                rows.append({
                    "model": self.model_name,
                    "architecture": arch_key,
                    "subject": subj,
                    "accuracy": subj_data["accuracy"],
                    "tasks": subj_data["tasks"],
                })

        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["model", "architecture", "subject", "accuracy", "tasks"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"✓ Results exported to {path}")
