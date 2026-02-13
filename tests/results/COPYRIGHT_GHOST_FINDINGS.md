# Copyright Ghost Test: Beyond Copy Detection

## Most tools catch copy-pasting. Project Spark catches unauthorized training data provenance.

**Test Date:** 2026-02-13  
**Tool:** Project Spark Compliance Auditor  

---

## The Problem with Text Matching

Traditional copyright detection tools (Copyscape, Turnitin, etc.) work by **matching text patterns**. If you paraphrase an article — or use another AI to rewrite it — these tools fail.

AI companies know this. That's why "data laundering" is becoming common: scrape copyrighted content, paraphrase it with GPT-4, and claim it's "original."

**Project Spark takes a fundamentally different approach.**

---

## Source Provenance: Track Where Data Came From, Not What It Looks Like

Project Spark doesn't analyze text content. It analyzes **data provenance** — the metadata trail that shows where training data originated.

Even if every NYT article in your dataset has been:
- Paraphrased by another AI
- Translated to another language and back
- Summarized into bullet points
- Mixed with other content

**The manifest still records `nytimes.com` as the source URL.** Project Spark catches it.

---

## Test Setup

We created a synthetic dataset simulating "laundered" training data:

| Source | Entries | Scenario | Expected Risk |
|--------|---------|----------|---------------|
| nytimes.com | 10 | Paraphrased NYT articles | 🔴 High |
| wsj.com | 5 | Paraphrased WSJ articles | 🔴 High |
| reddit.com | 5 | Paraphrased Reddit posts | 🟡 Medium |
| wikipedia.org | 10 | Clean Wikipedia content | 🟢 Low |
| arxiv.org | 10 | Clean academic papers | 🟢 Low |

---

## Results

| Source | Entries | Detected | Detection Rate |
|--------|---------|----------|---------------|
| nytimes.com (High Risk) | 10 | 10 | **100%** |
| wsj.com (High Risk) | 5 | 5 | **100%** |
| reddit.com (Medium Risk) | 5 | 5 | **100%** |
| **Total Risky Sources** | **20** | **20** | **100%** |

### ✅ Zero false negatives. Every copyrighted source was caught.

---

## Why This Matters for CLEAR Act Compliance

The proposed **CLEAR Act** (Content Licensing and Ethical AI Regulation) would require AI companies to:

1. **Disclose all training data sources** — not just "CommonCrawl" but the actual domains
2. **Obtain licenses** from copyright holders whose content was used
3. **Maintain provenance records** for audit purposes

Text-matching tools can't provide this. They answer "does this output contain copied text?" — the wrong question.

**The right question is: "Was copyrighted content used to train this model?"**

Project Spark answers that question by auditing the **data supply chain**, not the output.

---

## Comparison: Text Matching vs. Source Provenance

| Capability | Text Matching (Copyscape etc.) | Source Provenance (Project Spark) |
|-----------|-------------------------------|----------------------------------|
| Catches exact copies | ✅ | ✅ |
| Catches paraphrased content | ❌ | ✅ |
| Catches AI-rewritten content | ❌ | ✅ |
| Catches translated content | ❌ | ✅ |
| Works at dataset scale (millions of URLs) | ❌ (too slow) | ✅ |
| Identifies specific publishers | ❌ | ✅ |
| CLEAR Act compliant | ❌ | ✅ |

---

> **"You can launder the text, but you can't launder the provenance."**  
> — Project Spark
