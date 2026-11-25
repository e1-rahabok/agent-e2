<p align="center">
  <img src="https://img.shields.io/badge/Agent%20E2-Level%20400%20private%20cloud%20operations%20management%20expertise-6e7781?style=for-the-badge&labelColor=3d444d" alt="Agent E2: Level 400 operations management expertise">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/-vSphere-6e7781?style=for-the-badge&logo=vmware&logoColor=white&labelColor=3d444d" alt="vSphere">
  <img src="https://img.shields.io/badge/-VCF-6e7781?style=for-the-badge&logo=vmware&logoColor=white&labelColor=3d444d" alt="VCF">
  <img src="https://img.shields.io/badge/-vSAN-6e7781?style=for-the-badge&logo=vmware&logoColor=white&labelColor=3d444d" alt="vSAN">
  <img src="https://img.shields.io/badge/-NSX-6e7781?style=for-the-badge&logo=vmware&logoColor=white&labelColor=3d444d" alt="NSX">
  <br>
  <img src="https://img.shields.io/badge/-Kubernetes-6e7781?style=for-the-badge&logo=kubernetes&logoColor=white&labelColor=3d444d" alt="Kubernetes">
  <img src="https://img.shields.io/badge/-Windows-6e7781?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZmZmZiIgZD0iTTAgMy40NSA5Ljc1IDIuMXY5LjQ1SDB6TTEwLjk1IDEuOTUgMjQgMHYxMS40SDEwLjk1ek0wIDEyLjZoOS43NXY5LjQ1TDAgMjAuN3pNMTAuOTUgMTIuNkgyNFYyNGwtMTMuMDUtMS44eiIvPjwvc3ZnPgo=&logoColor=white&labelColor=3d444d" alt="Windows">
  <img src="https://img.shields.io/badge/-Linux-6e7781?style=for-the-badge&logo=linux&logoColor=white&labelColor=3d444d" alt="Linux">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/model-open%20weights%2C%20local-6e7781?labelColor=3d444d" alt="Model: open weights, local">
  <img src="https://img.shields.io/badge/runs-locally%20%28data%20stays%20on%20site%29-6e7781?labelColor=3d444d" alt="Runs locally">
  <img src="https://img.shields.io/badge/knowledge%20files-286-6e7781?labelColor=3d444d" alt="Knowledge files: 286">
  <img src="https://img.shields.io/badge/benchmark%20questions-291-6e7781?labelColor=3d444d" alt="Benchmark questions: 291">
  <img src="https://img.shields.io/badge/target-99%25%20final%20score-6e7781?labelColor=3d444d" alt="Target: 99% final score">
</p>

**💡 [Mission](MISSION.md) · 🏛️ [Architecture](ARCHITECTURE.md) · 🧠 [Knowledge engineering](KNOWLEDGE-ENGINEERING.md) · 🤖 [Agent](harness/AGENT.md) · ⚙️ [Harness](harness/README.md) · 🧪 [Benchmark](benchmark/design.md)**

# Agent E2

- What it is:
  - A VMware consultant, not an LLM aid. It answers Level 400 questions, and it leads a consultation: asked "Can you guide me over capacity planning for a vSphere cluster? You're my expert consultant", it interviews you for what the plan needs, names every default it assumes, computes the answer with code, and explains which number limits your hosts and why.
  - Under the hood, an expert system on a local LLM. The agent and the harness lead: code follows the expert's procedure, decides what to read from the knowledge base's map, asks for missing inputs and computes the exact values; the model reads and writes ([harness/AGENT.md](harness/AGENT.md)).
  - Consultations: capacity planning in release 1.0; 14 more planned after 1.0 ([project/consultations.md](project/consultations.md)).
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

- An open-weight model, running locally on enterprise GPU (customer data stays on site), answering Level 400 VCF private cloud management questions better than frontier models.

## Why it is possible

- See [MISSION.md](MISSION.md), section 3.

## The system

The model is frozen; we do not train it. We improve the three parts around it, and choose which frozen model to ship.


| Part           | Job                                                                          | Where                 |
| -------------- | ---------------------------------------------------------------------------- | --------------------- |
| Knowledge base | Level 400 facts, mechanisms, misconceptions, flows and exact data                     | `knowledge/`          |
| Harness        | Retrieval, exact tools, rules, budgets, answer verifier                      | `harness/`            |
| Agent          | The expert's procedure as code: reads the question into a case, plans what to read, computes, checks; calls the model to read and write | [`harness/AGENT.md`](harness/AGENT.md)    |
| Model          | An open-weight vision model on local GPUs, chosen by the benchmark           | [`benchmark/models.md`](benchmark/models.md) |

- The benchmark tests the whole system, not the model. It is a proof, not a goal: Agent E2 against the release gate and the frontier model; it also picks the model.

## Repository map

- Where each file lives: [REPOSITORY-MAP.md](REPOSITORY-MAP.md).
- How the parts fit: [ARCHITECTURE.md](ARCHITECTURE.md), section Repository.

## Documents


| Read                                                 | For                                                                                                         |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [MISSION.md](MISSION.md)                             | The mission; why it is possible; what we can change; risks; what the product must do; design considerations |
| [ARCHITECTURE.md](ARCHITECTURE.md)                   | The whole system: repository, parts, control, local deployment, checks, query flow                                 |
| [REPOSITORY-MAP.md](REPOSITORY-MAP.md)               | Where each folder and file lives                                                                            |
| [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md) | How expertise is codified and found; folder, metadata, misconception, flow, image and writing rules                  |
| [harness/AGENT.md](harness/AGENT.md)                 | What the agent knows up front, what it decides, its rules, how it is improved                               |
| [harness/README.md](harness/README.md)               | What each harness part does for an expert answer; modules                                                   |
| [benchmark/design.md](benchmark/design.md)           | How the benchmark proves the claim; final score                                                             |
| [benchmark/models.md](benchmark/models.md)           | Model design: which frozen model to ship, size and hardware; frontier reference                             |
| [benchmark/live-test.md](benchmark/live-test.md)     | The system deployed on a local model: setup, steps, pass criteria                                        |
| [project/plan.md](project/plan.md)                   | Milestones, open work                                                                            |
| [project/consultations.md](project/consultations.md) | The consultations Agent E2 leads: capacity planning in 1.0, 14 more after 1.0                                |
| [CONTRIBUTING.md](CONTRIBUTING.md)                   | How to add or change a file                                                                                 |

## Status

- Goal not achieved yet. Latest round ([`benchmark/results/README.md`](benchmark/results/README.md)): Agent E2 on Muse-Glimmer-30B scored 84% final, the frontier reference 79%. It fails the release gate on the final score (limit 85%) and on confident-wrong (15%, limit 3%). The knowledge base and the harness have changed since that round.
- A round runs two runs per candidate model, Base (the model alone) and Agent E2, and the frontier reference ([`benchmark/RUN.md`](benchmark/RUN.md)).
- Benchmark questions: 291 run, 8 deferred (not run). 8 of the run set are screenshot questions. The run set by area and level:

| Area | Level 100 | Level 200 | Level 300 | Level 400 | Total |
|---|---|---|---|---|---|
| CPU | 1 | 2 | 38 | 77 | 118 |
| Memory | 1 | 3 | 36 | 59 | 99 |
| Storage | 2 | 2 | 25 | 40 | 69 |
| Network | 1 | 2 | 21 | 21 | 45 |
| System (cluster, resource pools, capacity, statistics) | 3 | 3 | 27 | 38 | 71 |
| Guest OS layer (Windows, Linux) | 1 | 3 | 28 | 44 | 76 |
| GPU | 0 | 1 | 0 | 0 | 1 |
| Questions | 7 | 11 | 111 | 162 | 291 |

- A question counts in every area it touches, so the area rows add up to more than 291. Current counts: `python3 project/tools/question_coverage.py`.
- Retrieval check: current numbers in [`project/plan.md`](project/plan.md), milestone M3.
- Earlier generations (classic and agentic modes) and their results are archived in [`project/archive/`](project/archive) and not compared.
- Plan and milestones: [`project/plan.md`](project/plan.md).

## Checks

```bash
python3 project/tools/rules_check.py
```

```bash
python3 -m unittest harness/test_harness.py
```

```bash
python3 -m unittest benchmark/runner/test_runner.py
```
