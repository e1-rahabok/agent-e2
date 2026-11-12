<p align="center">
  <img src="https://img.shields.io/badge/Agent%20E2-Level%20400%20private%20cloud%20operations%20management%20expertise-6e7781?style=for-the-badge&labelColor=3d444d" alt="Agent E2: Level 400 operations management expertise">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/-vSphere-6e7781?logo=vmware&logoColor=white&labelColor=3d444d" alt="vSphere">
  <img src="https://img.shields.io/badge/-VCF-6e7781?logo=vmware&logoColor=white&labelColor=3d444d" alt="VCF">
  <img src="https://img.shields.io/badge/-vSAN-6e7781?logo=vmware&logoColor=white&labelColor=3d444d" alt="vSAN">
  <img src="https://img.shields.io/badge/-NSX-6e7781?logo=vmware&logoColor=white&labelColor=3d444d" alt="NSX">
  <img src="https://img.shields.io/badge/-Kubernetes-6e7781?logo=kubernetes&logoColor=white&labelColor=3d444d" alt="Kubernetes">
  <img src="https://img.shields.io/badge/-Windows-6e7781?labelColor=3d444d" alt="Windows">
  <img src="https://img.shields.io/badge/-Linux-6e7781?logo=linux&logoColor=white&labelColor=3d444d" alt="Linux">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/model-open%20weights%2C%20one%20GPU-6e7781?labelColor=3d444d" alt="Model: open weights, one GPU">
  <img src="https://img.shields.io/badge/runs-locally%20%28data%20stays%20on%20site%29-6e7781?labelColor=3d444d" alt="Runs locally">
  <img src="https://img.shields.io/badge/knowledge%20files-277-6e7781?labelColor=3d444d" alt="Knowledge files: 277">
  <img src="https://img.shields.io/badge/benchmark%20questions-150-6e7781?labelColor=3d444d" alt="Benchmark questions: 150">
  <img src="https://img.shields.io/badge/target-99%25%20final%20score-6e7781?labelColor=3d444d" alt="Target: 99% final score">
</p>

**💡 [Mission](MISSION.md) · 🏛️ [Architecture](ARCHITECTURE.md) · 🧠 [Knowledge engineering](KNOWLEDGE-ENGINEERING.md) · 🤖 [Agent](harness/AGENT.md) · ⚙️ [Harness](harness/README.md) · 🧪 [Benchmark](benchmark/design.md)**

# Agent E2

- What it is:
  - An LLM-based expert system, built as agentic RAG on a local LLM.
- Scope for Phase 1:
  - vSphere metrics. Performance & Capacity management. Monitoring and Troubleshooting.
- Name:
  - Agent E2 is built by Iwan 'E1' Rahabok to make his expertise and experience available 24/7.
  - Designed to replace AskIO on isvara.io.

**Three parts, one body of knowledge:**

| Part | Role |
|---|---|
| Agent E2 (this repository) | The knowledge and the agent. Downloadable for private deployment: runs locally, customer data stays on site. |
| [Isvara.io](https://isvara.io) | Where Agent E2 lives on the Internet. Try it there without installing anything. |
| [vCommunity management pack](https://github.com/e1-rahabok/VCF-vCommunity-Adapter) | Implements the knowledge of Agent E2 as a VCF Operations adapter: the KPIs and models (Cluster Performance, Cluster Consumption, Cluster Risk, Close for Business) computed in the customer's VCF Operations. |

- They reinforce each other: Agent E2 explains the scores the pack computes, and reads them; Isvara.io lets readers try Agent E2 before deploying it; the pack puts the same thresholds and models on the customer's screens.

**Business problem:**

- Many private cloud customers cannot send operational data to a cloud AI service: regulated industries, government and defence.
- Others can use cloud AI but must contain its cost: per-token fees grow with every question, user and automated check.
- Frontier AI models answer vSphere performance questions from public Internet text, which repeats common misconceptions. Their answers $\color{red}{\text{sound expert}}$ and are often wrong at Level 400.

**Mission:**

- An open-weight model, running locally on one GPU (customer data stays on site), answering Level 400 private cloud management questions better than frontier models.

## Why it is possible

- See [MISSION.md](MISSION.md), section 3.

## The system

The model is frozen; we do not train it. We improve the three parts around it, and choose which frozen model to ship.


| Part           | Job                                                                          | Where                 |
| -------------- | ---------------------------------------------------------------------------- | --------------------- |
| Knowledge base | Level 400 facts, mechanisms, misconceptions, flows and exact data                     | `knowledge/`          |
| Harness        | Retrieval, exact tools, rules, budgets, answer verifier                      | `harness/`            |
| Agent          | The model plus the tool loop: what it is told up front, how it chooses tools | `harness/AGENT.md`    |
| Model          | An open-weight vision model on one GPU, chosen by the benchmark              | `benchmark/models.md` |

- The benchmark tests the whole system, not the model: it picks the model, scores each change to the other three parts, and compares the system with the frontier model.

## Repository map

- Where each file lives: [REPOSITORY-MAP.md](REPOSITORY-MAP.md).
- How the parts fit: [ARCHITECTURE.md](ARCHITECTURE.md), section Repository.

## Documents


| Read                                                 | For                                                                                                         |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [MISSION.md](MISSION.md)                             | The mission; why it is possible; what we can change; risks; what the product must do; design considerations |
| [ARCHITECTURE.md](ARCHITECTURE.md)                   | The whole system: repository, parts, modes, local deployment, checks, query flow                                   |
| [REPOSITORY-MAP.md](REPOSITORY-MAP.md)               | Where each folder and file lives                                                                            |
| [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md) | How expertise is codified and found; folder, metadata, misconception, flow, image and writing rules                  |
| [harness/AGENT.md](harness/AGENT.md)                 | What the agent knows up front, what it decides, its rules, how it is improved                               |
| [harness/README.md](harness/README.md)               | What each harness part does for an expert answer; modules                                                   |
| [benchmark/design.md](benchmark/design.md)           | How the benchmark proves the claim; final score                                                             |
| [benchmark/models.md](benchmark/models.md)           | Model design: which frozen model to ship, size and hardware; frontier reference; judge                      |
| [benchmark/live-test.md](benchmark/live-test.md)     | The system deployed on a local model: setup, steps, pass criteria                                        |
| [project/plan.md](project/plan.md)                   | Milestones, decisions, open work                                                                            |
| [CONTRIBUTING.md](CONTRIBUTING.md)                   | How to add or change a file                                                                                 |

## Status

- Goal not achieved yet: best small model 58% vs frontier 75% on the first 17 questions.
- Plan, milestones and decisions: `project/plan.md`. Latest review: `project/review-2026-11-06.md`.

## Checks

```bash
python3 project/tools/lint.py
```

```bash
python3 -m unittest harness/test_tools.py
```
