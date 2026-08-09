# Use Case: Enterprise Custom Policies

**Author fingerprint:** `DBHATT-Debashis2007-SystemDesignPOC-2026` — Debashis Bhattacharjee ([@Debashis2007](https://github.com/Debashis2007))

**YouTube walkthrough:** [Enterprise Custom Policies — System Design #Shorts](https://youtu.be/IfrBf6zkksE)

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [06 — Multi-Layer Safety / Moderation](./06-safety-moderation-pipeline.md)

## Users & problem

Enterprises need brand-safe or regulated add-on rules (topics, competitors, jurisdictions) without forking the core safety stack.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Packs | Policy-as-data per tenant |
| Isolation | Pack A cannot affect pack B |
| Latency | Compile to fast matchers |
| Change control | Versioned pack deploys |

## Design (from parent)

```
Base global policy → + enterprise policy pack
  → compiled rules/classifiers
  → decision plane returns base + custom reason codes
  → admin UI for pack versions
```

Reuse layered enforcement from **06**; add a **policy pack compiler**.

## Specializations

| Concern | Enterprise choice |
|---------|-------------------|
| Authors | Customer admin + legal review flow |
| Conflict | Explicit precedence: critical global > custom |
| Testing | Shadow mode before enforce |
| Audit | Per-tenant decision exports |

## Failure modes

- Rule explosion latency → compile/index; cap pack complexity.
- Custom pack weakens critical safety → forbid relaxing global critical categories.
- Mistyped rule blocks all traffic → shadow + canary pack rollout.




## Design walkthrough (opens on GitHub)

> **Watch on YouTube:** [Enterprise Custom Policies — System Design #Shorts](https://youtu.be/IfrBf6zkksE)


![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd enterprise-custom-policies
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/check -H 'Content-Type: application/json' -d '{"tenant":"acme","text":"mention competitor zxco"}' | jq

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

