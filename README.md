<p align="center">
  <img src="https://img.shields.io/badge/Isvara-Level%20400%20private%20cloud%20expertise-6e7781?style=for-the-badge&labelColor=3d444d" alt="Isvara: Level 400 private cloud expertise">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/vSphere-9.1-6e7781?logo=vmware&logoColor=white&labelColor=3d444d" alt="vSphere 9.1">
  <img src="https://img.shields.io/badge/VCF-9.1.1-6e7781?logo=vmware&logoColor=white&labelColor=3d444d" alt="VCF 9.1.1">
  <img src="https://img.shields.io/badge/model-27--32B%20open%20weights-6e7781?labelColor=3d444d" alt="Model: 27-32B open weights">
  <img src="https://img.shields.io/badge/runs-offline%20%28dark%20site%29-6e7781?labelColor=3d444d" alt="Runs offline">
  <img src="https://img.shields.io/badge/knowledge%20files-205-6e7781?labelColor=3d444d" alt="Knowledge files: 205">
  <img src="https://img.shields.io/badge/benchmark%20cases-28-6e7781?labelColor=3d444d" alt="Benchmark cases: 28">
  <img src="https://img.shields.io/badge/target-99%25%20stable%20correct-6e7781?labelColor=3d444d" alt="Target: 99% stable correct">
</p>

# Isvara: private cloud expertise

**🏛️ [Architecture](ARCHITECTURE.md) · 🧠 [Knowledge engineering](KNOWLEDGE-ENGINEERING.md) · 🧪 [Test design](benchmark/test-design.md) · ⚙️ [Harness](harness/README.md)**

**Business problem:**
- Many private cloud customers cannot send operational data to a cloud AI service: regulated industries, government and defence, and dark sites with no Internet at all.
- Others can use cloud AI but must contain its cost: per-token fees grow with every question, user and automated check.
- Frontier AI models answer vSphere performance questions from public Internet text, which repeats common misconceptions. Their answers sound expert and are often wrong at Level 400.

**Goal:** a 32B-class open-weight model, running offline on one GPU (dark site, no Internet, no per-token cost), answers Level 400 private cloud operations questions better than frontier models.

## Repository map

Three groups. Only the product is deployed.

```mermaid
flowchart LR
  subgraph Product["Product: deployed to the site"]
    K["knowledge/<br/>codified expertise<br/>(the only indexed folder)"]
    H["harness/<br/>retrieval, tools,<br/>verifier, prompts"]
    M(["open-weight model<br/>on a local GPU"])
    H -->|retrieves| K
    H -->|prompts, checks| M
  end
  subgraph Proof["Proof: not deployed"]
    B["benchmark/<br/>exam cases, runner, results"]
  end
  subgraph Project["Project: not deployed"]
    P["project/<br/>design, decisions,<br/>author questions, to-do"]
    T["project/tools/<br/>lint.py, tags.yaml"]
  end
  B -->|runs exam questions through| H
  T -->|checks| K
  T -->|checks| B
```

- Product: what runs at the customer site.
  - `knowledge/`: Level 400 mechanisms, metrics, traps and troubleshooting flows, plus exact data in `knowledge/catalog/`. Version 1.0 covers vSphere 9.1 metrics and the Guest OS layer; the end scope is the private cloud stack (vSAN, NSX, VCF Operations, Kubernetes, Linux).
  - `harness/`: the software around the model: hybrid retrieval, link expansion, exact tools (catalog lookup, calculator, flow executor), answer verifier. Reads `knowledge/`; depends on no other folder.
  - Model: a 27-32B open-weight model, chosen by benchmark. Not stored here.
- Proof: shows that the product beats a frontier model.
  - `benchmark/`: exam cases with answer keys, attachments, the runner, results. Luck removed: Unsure option, confident-wrong rate, 5 runs must agree. Never indexed: it holds the answer keys.
- Project: how this repository is built and kept correct.
  - `project/`: design, decisions, reviews, author questions, to-do, archive.
  - `project/tools/`: `lint.py` (file, tag and folder checks, run before every merge) and `tags.yaml` (allowed tag values, avoided phrases).

## Documents

| Read | For |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | How model, harness and knowledge run together; ingest, query and answer steps |
| [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md) | Forms of codified knowledge; folder, metadata, trap, flow, image and writing rules |
| [benchmark/test-design.md](benchmark/test-design.md) | How the benchmark proves the gain |
| [harness/README.md](harness/README.md) | Harness modules and commands |
| [project/solution-design.md](project/solution-design.md) | Why it can work, why 32B, which models |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add or change a file |

## Status
- Goal not achieved yet: best small model 58% vs frontier 75% on the first 17 questions.
- Findings and decisions: `project/review-2026-11-04.md`.

## Checks

```bash
python3 project/tools/lint.py
```

```bash
python3 -m unittest harness/test_tools.py
```
