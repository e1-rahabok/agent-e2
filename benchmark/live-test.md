# Live test: the system on a local model

The plan to deploy the system as a customer would, on one GPU with no Internet, and prove that it works there. Not indexed.
Why it matters: the benchmark reaches models through a gateway; the mission is a local model. The gaps the gateway leaves open are in [models.md](models.md), section What the gateway does not prove. Design: [../MISSION.md](../MISSION.md), section 5. Architecture: [../ARCHITECTURE.md](../ARCHITECTURE.md), section Local deployment.

## 1. What it proves
| Claim | Proof |
|---|---|
| Works without Internet | No outbound connection during the whole test, checked at the network, not assumed. Customer data never leaves the site; Internet access is optional |
| Scores like the benchmark | The same questions, local weights at the deployed precision; final score compared with the gateway run of the same model |
| Fits the hardware | The chosen hardware tier (one GPU is the stretch target, two to four allowed); the chosen context window; no out-of-memory error |
| Fast enough to use | Time per answer and per model turn on the target GPU, on Agent E2 |
| An operator can use it | A session with the author: real questions and screenshots, judged by the author |
| Can be updated offline | A new knowledge bundle is imported and served without a network |

## 2. When
- After a gateway round has picked the leading model.
- Again before every release: the release score is the live-test score (`models.md`, section 2).

## 3. Setup
| Part | Choice | Notes |
|---|---|---|
| Host | One ESXi host on the author's lab VCF, or a rented GPU server for the first run | The lab matches the customer case; a rented server is faster to start |
| GPU | One GPU, 48 GB (tier A) or 96 GB (tier B), or two to four GPUs (tier C), to the VM by passthrough or vGPU | Tier from `models.md`, section 3 |
| VM | Linux, the GPU, 16+ vCPU, 64+ GB memory, disk for weights and index | VMware Private AI Foundation with NVIDIA is the natural platform (to verify against current product documentation) |
| Model server | vLLM, OpenAI-compatible API on the VM's network | llama.cpp as a fallback for 4-bit GGUF |
| Model | The leading candidate, at the deployed precision (8-bit if the GPU allows, else 4-bit) | Weights checked by hash against the publisher's |
| Embeddings | `qwen3-embedding-0.6b` on CPU, same server or a second vLLM instance | The model the benchmark used |
| Harness and runner | This repository at a fixed commit, with the embedding cache | Index version = commit SHA |
| Network | A firewall rule that blocks all egress from the VM; only the operator's admin network reaches it | Logged, so "no outbound connection" is evidence |

## 4. Code changes needed first
| Change | Why |
|---|---|
| Runner `--local <url>`: point [`harness/llm.py`](../harness/llm.py) at the local server; no API key required | Today the client requires `AI_GATEWAY_API_KEY` |
| Vision and context checks from config, not from the gateway model list | The runner reads the `vision` tag and context window from the gateway; a local server has no tags |
| Judge later: save judged answers offline, score them with the judge after the VM is back online | The judge is a frontier model; it is not on the offline VM |
| Timings per model turn in `answers.csv` (time to first token, tokens per second) | Speed on the target GPU is a result of this test |

## 5. Steps
1. Prepare the bundle on a connected machine: model weights and their hashes, vLLM container or packages, this repository at the release commit, the embedding cache, Python packages.
2. Build the VM, attach the GPU, copy the bundle in. Then block egress.
3. Prove the block: an outbound request from the VM fails; the firewall log shows the attempt dropped.
4. Smoke test: one question on Base and on Agent E2; the trace shows the case, the reading plan, the computed facts and the checks working.
5. Benchmark: every question of the run set, Agent E2 and Base, 5 runs, at `context_window: 32000`. Deterministic questions are scored on the VM; judged answers are saved for the judge.
6. Judge: bring the saved answers to a connected machine; the judge scores them; the report is built.
7. Compare: paired, question by question, with the gateway run of the same model on Agent E2 (`design.md`, section 8). Note any question that changes.
8. Speed: median and 95th percentile time per answer and per model turn, on Agent E2; GPU memory at peak.
9. Operator session: the author asks 20 real questions from the field, with screenshots, and judges each answer (right, partly right, wrong, unsure). The assistant runs the conversation mode (`modes.converse`): for each question, record whether it asked a clarifying question, whether asking was right (odd question, text and attachment disagree, a missing fact that changes the answer), and the answer after the reply. Every wrong answer is traced to knowledge, retrieval or model.
10. Update: import a newer knowledge bundle offline, rebuild the index, answer one question; the index version in the trace changes.

## 6. Pass criteria (proposal, for the author to set)
- Zero outbound connections in the firewall log for the whole test.
- Final score within the margin of the gateway run (`design.md`, section 7.4), and at or above the release gate.
- No answer lost to the context window or to GPU memory.
- Time per answer: the author sets the target after step 9; the benchmark records it until then.
- The operator session: no confident wrong answer the author would act on.

## 7. Results
- Stored like a benchmark: `benchmark/results/<benchmark-id>-live/`, plus `live.md` with the setup (host, GPU, precision, model hash, commit), the firewall evidence, speed, and the operator session.
