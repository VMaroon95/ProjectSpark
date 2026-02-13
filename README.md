# ⚡ Project Spark

**AI Governance & Evaluation Platform**

*How much does a prompt really matter? And is your training data legally safe?*

> A dual-purpose platform combining LLM evaluation benchmarking with copyright compliance auditing — built for the era of AI regulation.

![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61dafb?style=flat-square&logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## The Problem

### 1. LLM Sensitivity Crisis
The same model can score **63%** or **72%** on the same benchmark depending on how you phrase the prompt. Most evaluation benchmarks don't account for this — they test one prompt format and call it a score. That's not a benchmark; it's a snapshot.

### 2. Copyright Compliance Gap
The **CLEAR Act of 2026** requires AI companies to disclose copyrighted material in their training data. Most organizations have zero tooling for auditing dataset manifests against known copyright holders. The penalty? Up to $500,000 per violation.

---

## What Project Spark Does

### Module 1: AI Eval Harness Benchmarker

A CLI tool that stress-tests LLMs across **5 prompt architectures** to measure true robustness:

| Architecture | Strategy | Typical Impact |
|---|---|---|
| **Zero-Shot** | Raw question, no scaffolding | Baseline |
| **Chain-of-Thought** | "Let's think step by step" | +8.6% on reasoning |
| **Persona-Based** | Domain expert persona wrapper | +4.2% on specialized |
| **Few-Shot** | 3 example Q&A pairs first | +5.9% consistent lift |
| **Delimiter-Heavy** | Structured ###/""" formatting | +2.5% marginal |

- Runs MMLU benchmark with **per-subject breakdowns** (STEM, Humanities, Social Sciences, Other)
- Outputs comparative accuracy data as JSON/CSV
- Visualizes results as a **Model Robustness Heatmap**

### Module 2: CLEAR Act Compliance Dashboard

- **Upload** dataset manifests (CSV format)
- **Automatic risk flagging** against 60+ known publishers and domains
- **Risk categorization:** High (active litigation) / Medium (TOS restrictions) / Low (open license)
- **Generate Federal Disclosure Form PDFs** — professional government-style documents for regulatory filing

---

## Quick Start

### Using Docker Compose

```bash
git clone https://github.com/VMaroon95/ProjectSpark.git
cd ProjectSpark
docker compose up --build
```

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npx serve -l 3000 .
# Or just open frontend/public/index.html in your browser
```

**CLI:**
```bash
# Demo mode (pre-computed realistic results)
python -m cli.runner --model meta-llama/Llama-3-8B --mode demo --output results.json

# Live mode (requires lm-evaluation-harness + GPU)
python -m cli.runner --model meta-llama/Llama-3-8B --mode live --output results.json
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Dashboard                       │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌────────────┐  │
│  │Dashboard │ │ Heatmap  │ │  Audit  │ │ Disclosure │  │
│  └────┬─────┘ └────┬─────┘ └────┬────┘ └─────┬──────┘  │
│       └─────────────┼───────────┼─────────────┘         │
└─────────────────────┼───────────┼───────────────────────┘
                      │  REST API │
┌─────────────────────┼───────────┼───────────────────────┐
│              FastAPI Backend (port 8000)                  │
│  ┌──────────────┐ ┌─────────────────┐ ┌──────────────┐  │
│  │ Eval Service │ │Compliance Audit │ │PDF Generator │  │
│  └──────┬───────┘ └────────┬────────┘ └──────────────┘  │
│         │                  │                             │
│  ┌──────┴───────┐ ┌───────┴─────────┐                   │
│  │ Sweep Engine │ │ Domain Database │                   │
│  └──────────────┘ │  (60+ domains)  │                   │
│                   └─────────────────┘                   │
└─────────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────┐
│              CLI Tool (python -m cli.runner)              │
│  ┌───────────────────┐  ┌────────────────────────────┐  │
│  │ Prompt Architectures│  │ Sensitivity Sweep Engine  │  │
│  │ (5 strategies)     │  │ (demo + live modes)       │  │
│  └───────────────────┘  └────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## API Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/eval/results` | Latest sweep results |
| `POST` | `/api/eval/upload` | Upload sweep results JSON |
| `GET` | `/api/eval/heatmap` | Heatmap-formatted data |
| `POST` | `/api/compliance/audit` | Upload CSV manifest, run audit |
| `GET` | `/api/compliance/audit/{id}` | Get audit by ID |
| `POST` | `/api/compliance/disclosure-pdf` | Generate disclosure PDF |
| `GET` | `/api/stats` | Dashboard statistics |

Full interactive docs available at `/docs` when the backend is running.

---

## Sample Data

The `data/` directory includes:
- **`sample_sweep_results.json`** — Realistic MMLU benchmark results across all 5 architectures
- **`sample_manifest.csv`** — 30-row dataset manifest with mixed-risk sources

---

## Tech Stack

- **Backend:** Python 3.11, FastAPI, Pydantic, ReportLab, Pandas
- **Frontend:** React 18, Recharts, Babel Standalone (CDN — no build step)
- **CLI:** Python, argparse, lm-evaluation-harness (optional)
- **Infrastructure:** Docker, Docker Compose, nginx

---

## 📊 Proof & Findings

We tested Project Spark against real-world data. Here's what we found:

### RedPajama Copyright Audit
> "I found 79 copyrighted sources hidden in a 'Clean' open dataset."

[Read the full findings →](tests/results/REDPAJAMA_FINDINGS.md)

### Fragility Test: Llama-3-8B
> "A model with 66.6% accuracy? Only if you ask the right way. Scores ranged from 64.2% to 71.8%."

[Read the full findings →](tests/results/FRAGILITY_FINDINGS.md)

### Copyright Ghost Test
> "Most tools catch copy-pasting. Project Spark catches unauthorized training data provenance."

[Read the full findings →](tests/results/COPYRIGHT_GHOST_FINDINGS.md)

---

## Roadmap

- [ ] Multi-model comparison (side-by-side sweeps)
- [ ] Custom benchmark support (beyond MMLU)
- [ ] Automated web crawl detection in manifests
- [ ] Integration with HuggingFace Hub for model metadata
- [ ] Export to regulatory filing portals
- [ ] Temporal drift analysis (benchmark scores over model versions)

---

## License

MIT License — Varun Meda © 2026

See [LICENSE](LICENSE) for details.
