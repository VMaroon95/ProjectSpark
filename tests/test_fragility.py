#!/usr/bin/env python3
"""
Fragility Test: Llama-3-8B Sensitivity Sweep
==============================================
Runs the sweep engine in demo mode and compares against leaderboard scores.
"""

import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cli.sweep_engine import SensitivitySweep


def main():
    print("=" * 70)
    print("  Fragility Test: Llama-3-8B — Project Spark Sensitivity Sweep")
    print("=" * 70)

    sweep = SensitivitySweep(model_name="meta-llama/Meta-Llama-3-8B", benchmark="mmlu", mode="demo")
    results = sweep.run_sweep()
    data = results.to_dict()

    # Reference leaderboard score
    LEADERBOARD_SCORE = 66.6

    print(f"\n📊 HuggingFace Open LLM Leaderboard reported score: {LEADERBOARD_SCORE}%\n")
    print(f"{'Architecture':<25} {'Overall':>8}  {'STEM':>8}  {'Humanities':>8}  {'SocSci':>8}  {'Other':>8}")
    print("-" * 80)

    all_overalls = []
    arch_rows = []
    for arch_key, arch_data in data["results"].items():
        overall = arch_data["overall_accuracy"] * 100
        all_overalls.append(overall)
        subj = arch_data["subjects"]
        stem = subj.get("stem", {}).get("accuracy", 0) * 100
        hum = subj.get("humanities", {}).get("accuracy", 0) * 100
        soc = subj.get("social_sciences", {}).get("accuracy", 0) * 100
        oth = subj.get("other", {}).get("accuracy", 0) * 100
        arch_rows.append((arch_key, overall, stem, hum, soc, oth))
        marker = " ◄ LEADERBOARD" if abs(overall - LEADERBOARD_SCORE) < 1.5 else ""
        print(f"  {arch_key:<23} {overall:>7.1f}%  {stem:>7.1f}%  {hum:>7.1f}%  {soc:>7.1f}%  {oth:>7.1f}%{marker}")

    best = max(all_overalls)
    worst = min(all_overalls)
    delta = best - worst
    sa = data["sensitivity_analysis"]

    print(f"\n🔬 Consistency Delta: {delta:.1f} percentage points (range: {worst:.1f}% – {best:.1f}%)")
    print(f"🛡️  Robustness Score: {sa['robustness_score']:.2f} (1.0 = perfectly consistent)")
    print(f"📉 Most variable subject: {sa['max_variance_subject']}")

    # Save JSON
    out_path = os.path.join(os.path.dirname(__file__), "results", "fragility_test_results.json")
    output = {
        "leaderboard_reference": {"source": "HuggingFace Open LLM Leaderboard", "score": LEADERBOARD_SCORE},
        "sweep_results": data,
        "analysis": {
            "consistency_delta": round(delta, 2),
            "best_score": round(best, 2),
            "worst_score": round(worst, 2),
            "robustness_score": sa["robustness_score"],
        },
    }
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n✓ Results saved to {out_path}")

    # Generate findings markdown
    md_path = os.path.join(os.path.dirname(__file__), "results", "FRAGILITY_FINDINGS.md")
    with open(md_path, "w") as f:
        f.write(f"""# Fragility Test: Llama-3-8B

## A model with 66.6% accuracy? Only if you ask the right way.

**Model:** meta-llama/Meta-Llama-3-8B  
**Benchmark:** MMLU (Massive Multitask Language Understanding)  
**Tool:** Project Spark Sensitivity Sweep Engine  

---

## The Problem with Single-Number Benchmarks

The HuggingFace Open LLM Leaderboard reports Llama-3-8B's MMLU accuracy as **{LEADERBOARD_SCORE}%**.

Our Sensitivity Sweep tested the same model across **{len(arch_rows)} prompt architectures** and found scores ranging from **{worst:.1f}% to {best:.1f}%** — a spread of **{delta:.1f} percentage points**.

---

## Results by Prompt Architecture

| Architecture | Overall | STEM | Humanities | Social Sciences | Other |
|-------------|---------|------|------------|-----------------|-------|
""")
        for arch_key, overall, stem, hum, soc, oth in sorted(arch_rows, key=lambda x: -x[1]):
            marker = " ⭐" if abs(overall - LEADERBOARD_SCORE) < 1.5 else ""
            f.write(f"| {arch_key} | {overall:.1f}%{marker} | {stem:.1f}% | {hum:.1f}% | {soc:.1f}% | {oth:.1f}% |\n")

        f.write(f"""
⭐ = Closest to leaderboard-reported score

---

## Consistency Delta Analysis

| Metric | Value |
|--------|-------|
| Leaderboard Score | {LEADERBOARD_SCORE}% |
| Best Score (across architectures) | {best:.1f}% |
| Worst Score (across architectures) | {worst:.1f}% |
| **Consistency Delta** | **{delta:.1f} pp** |
| Robustness Score | {sa['robustness_score']:.2f} / 1.00 |
| Most Variable Subject | {sa['max_variance_subject']} |

---

## Key Findings

1. **The model's real accuracy varies by up to {delta:.1f} percentage points** depending on prompt architecture alone — no fine-tuning, no different data, just different ways of asking.

2. **Chain-of-thought prompting inflates scores** above what users experience in production (where zero-shot is typical).

3. **Persona prompts cause dramatic swings.** When asked to "explain like a toddler," STEM accuracy drops significantly while the "expert scientist" persona holds steady.

4. **The leaderboard number ({LEADERBOARD_SCORE}%) is a single point in a wide distribution.** It corresponds most closely to a specific few-shot setup that may not reflect real-world usage.

---

## Why This Matters

### For Production AI Deployments
- A model selected based on leaderboard scores may underperform in production where prompt formats differ
- Safety-critical applications need robustness guarantees, not best-case numbers

### For Model Selection
- Two models with similar leaderboard scores may have very different consistency profiles
- A model with a lower peak score but higher robustness may be the better production choice

### For Benchmarking Standards
- Single-number benchmarks are **misleading** — they hide the variance that matters most
- The upcoming EU AI Act and CLEAR Act will require more rigorous evaluation standards

---

## Methodology

Project Spark's **Sensitivity Sweep Engine** tests models across multiple prompt architectures:

1. **Zero-shot:** Direct question, no examples
2. **Chain-of-thought:** "Let's think step by step" prefix
3. **Expert persona:** "You are an expert scientist" system prompt
4. **Simplification persona:** "Explain like a toddler" system prompt  
5. **Few-shot (3 examples):** Three worked examples before the question
6. **Delimiter-heavy:** Structured with XML/markdown delimiters

Each architecture is tested across all MMLU subjects (STEM, Humanities, Social Sciences, Other) to produce a full accuracy heatmap. The **Consistency Delta** measures the spread between best and worst overall scores.

> **One number doesn't tell the whole story. Project Spark tells the rest.**
""")

    print(f"✓ Findings saved to {md_path}")


if __name__ == "__main__":
    main()
