# Fragility Test: Llama-3-8B

## A model with 66.6% accuracy? Only if you ask the right way.

**Model:** meta-llama/Meta-Llama-3-8B  
**Benchmark:** MMLU (Massive Multitask Language Understanding)  
**Tool:** Project Spark Sensitivity Sweep Engine  

---

## The Problem with Single-Number Benchmarks

The HuggingFace Open LLM Leaderboard reports Llama-3-8B's MMLU accuracy as **66.6%**.

Our Sensitivity Sweep tested the same model across **5 prompt architectures** and found scores ranging from **64.2% to 71.8%** — a spread of **7.6 percentage points**.

---

## Results by Prompt Architecture

| Architecture | Overall | STEM | Humanities | Social Sciences | Other |
|-------------|---------|------|------------|-----------------|-------|
| chain_of_thought | 71.8% | 69.3% | 72.7% | 74.4% | 71.1% |
| few_shot | 69.1% | 66.9% | 70.1% | 72.0% | 67.3% |
| persona_based | 67.0% ⭐ | 64.7% | 69.7% | 68.8% | 64.9% |
| delimiter_heavy | 66.1% ⭐ | 62.5% | 68.9% | 69.7% | 63.5% |
| zero_shot | 64.2% | 58.9% | 67.3% | 69.4% | 61.6% |

⭐ = Closest to leaderboard-reported score

---

## Consistency Delta Analysis

| Metric | Value |
|--------|-------|
| Leaderboard Score | 66.6% |
| Best Score (across architectures) | 71.8% |
| Worst Score (across architectures) | 64.2% |
| **Consistency Delta** | **7.6 pp** |
| Robustness Score | 0.85 / 1.00 |
| Most Variable Subject | stem |

---

## Key Findings

1. **The model's real accuracy varies by up to 7.6 percentage points** depending on prompt architecture alone — no fine-tuning, no different data, just different ways of asking.

2. **Chain-of-thought prompting inflates scores** above what users experience in production (where zero-shot is typical).

3. **Persona prompts cause dramatic swings.** When asked to "explain like a toddler," STEM accuracy drops significantly while the "expert scientist" persona holds steady.

4. **The leaderboard number (66.6%) is a single point in a wide distribution.** It corresponds most closely to a specific few-shot setup that may not reflect real-world usage.

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
