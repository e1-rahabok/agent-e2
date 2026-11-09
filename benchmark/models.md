# Models

Candidate models, the frontier reference and the judge for the benchmark. Not indexed.
Settings: [benchmark/runner/config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/config.yaml). Why a small local model can win: [MISSION.md](../MISSION.md), section 3. Model size: section Model size and speed below.

## 1. What model the goal needs
The goal is Level 400 on a narrow domain, for VMware administrators. That sets what the model must do, and what it must not do.

### The model's job
- The knowledge base is written at Level 400 and assumes the reader knows vSphere basics (`CLAUDE.md`, section Level): cluster, host, VM, datastore, HA, DRS, vMotion, resource pools, shares, reservations, limits, vCPU, NUMA.
- So the model brings Level 100-300 vSphere knowledge from training. Public text covers it well, and it is mostly correct at that level. It is not documented in the knowledge base (author, 2026-11-05).
- The knowledge base adds the Level 400 layer: mechanisms, vantage points, and the corrections to Level 300 rules of thumb. Where the two differ, the knowledge base wins.
- The model must:
  1. know vSphere basics well enough to understand the question and the retrieved text without a definition;
  2. apply the retrieved text when it contradicts a rule of thumb the model learned (context faithfulness);
  3. follow the system prompt rules literally: the knowledge base is the source of truth; say Unsure when the text does not settle it;
  4. combine 3 or more files and follow a troubleshooting flow in order (multi-document reasoning);
  5. call tools correctly and in the right order (catalog, calculator, flow);
  6. read dense screenshots: esxtop tables, vCenter and VCF Operations charts (OCR of small UI text, chart reading);
  7. run on one GPU at the customer site.
- Traits 1 and 2 pull against each other. Memory supplies the basics; part of the same memory holds the Level 300 rules of thumb the knowledge base corrects.

### The risk: prior override
- Public Internet text teaches Level 300 readings: "Ready above 5% is bad", "memory usage at 95% means add RAM", "the VM is the Guest OS".
- A model that holds those beliefs strongly can read the correct knowledge base file and still answer from its belief. Measured on the frontier model without the knowledge base: trap answer on 16% of answers (benchmark 20261103-093742).
- Memory is not the problem in itself: the basics come from it. The problem is how firmly the model holds a rule of thumb against the context in front of it.
- Model size moves both ways: a larger model knows the basics better and follows long instructions better, and may hold rules of thumb more firmly. Which effect wins on this task is not known from theory or published results. It is measured.

### Dense or mixture-of-experts
- Total parameters set the memory (GPU size and how much was memorized). Active parameters set the compute per token, which drives instruction following, long-context reading and multi-step reasoning.
- For the GPU memory paid, a dense model gives the most compute per token. A 120B MoE with 6-12B active has less compute per token than a 31B dense model, on twice the GPU memory.
- So a dense model of about 70B is a better challenger than a 120B MoE: it fits a 48 GB GPU at 4-bit (about 40 GB), has 6-10 times the active compute, and fewer total parameters. Its cost is speed: about 0.45x the decode speed of a 32B dense model on the same GPU (section Model size and speed).
- No current-generation dense vision model of about 70B is on the gateway (checked 2026-11-05). Llama 3.3 70B is 2024 and has no vision. When one appears, it is the first challenger to add.
- The 120B MoE models were dropped (author, 2026-11-05): less compute per token than the dense candidates, on twice the GPU memory. A later MoE candidate must pass the rule below.

### What we prefer
| Prefer | Over | Reason |
|---|---|---|
| Strong instruction following and context faithfulness | Knowledge beyond vSphere basics | Basics come from training; past them, memory is where Level 300 rules of thumb live |
| Dense, 27-32B now, about 70B when available | MoE of the same GPU memory | More compute per token for the memory paid |
| Reliable tool calling | Long reasoning traces | Exact values come from tools; long traces drift and break the answer format |
| Native vision with good OCR | Vision as an add-on | Screenshots carry the values |
| Latest generation | Older or sibling models | Newer models follow instructions and use tools better at the same size |

- General knowledge benchmarks (trivia, exams) are not a selection signal. Basic vSphere knowledge is tested directly (below).

### How the benchmark tests it
- Override rate (report table `Final score`): share of knowledge base answers that state the trap although every needed file was in the context. It isolates prior override from retrieval misses. Target: 0.
- Lift: knowledge base mode score minus baseline score, per model. A model with high baseline and low lift is answering from memory.
- Basics (proposal, not built): about 10 Level 100-200 questions in baseline mode only (HA admission control, DRS, resource pool shares, vMotion). They check trait 1. A model that fails them cannot read the knowledge base, which assumes them. Not part of the final score.
- Trap rate in knowledge base modes, and the questions where the knowledge base and the vSphere documentation disagree ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.7).
- A challenger that needs more hardware (a dense model of about 70B, or any tier B model) stays only if both hold, against the best current candidate in the same mode:
  1. final score higher by more than the margin;
  2. override rate not higher.
- Otherwise it is dropped, and a tie goes to the cheaper model.


## Model size and speed
- Decode speed and GPU memory are set by the weights: every generated token reads all active weights once.

| Size | Weights at 8-bit | Weights at 4-bit | Fits on | Relative decode speed (same GPU, same precision) |
|---|---|---|---|---|
| 8B dense | ~8 GB | ~5 GB | any 16 GB GPU | ~4x |
| 32B dense | ~32 GB | ~18 GB | one 48 GB GPU at 8-bit; one 24 GB GPU at 4-bit | 1x |
| 70B dense | ~70 GB | ~40 GB | 80 GB GPU, or one 48 GB GPU at 4-bit | ~0.45x |
| 30B MoE, 3B active | ~30 GB | ~17 GB | same as 32B | ~5-8x |
| 120B MoE, 6-12B active | ~125 GB | ~66 GB | one 96 GB GPU at 4-bit | ~2-4x |

- Add the KV cache for the retrieved context (8-12K tokens per question).
- Only two limits count (author, 2026-11-05): fit for the goal, and hardware cost (one GPU, at most 96 GB). Parameter count is not a limit.
- 8B-14B: too weak at multi-step reasoning and tool use. Measured: ministral-8b 29-40% exact; qwen-3-14b agentic 19%.
- 27-32B dense: the current bet. 70B dense: the next challenger, when a current-generation vision model of that size exists. MoE with few active parameters: fast but weak at tool use in our runs (nemotron-3-nano-30b-a3b: 24-29% exact, almost no tool calls).

## 2. Gateway in the benchmark, local server at the site
### Two ways to reach a model
| | Benchmark | Customer site |
|---|---|---|
| Where the model runs | A hosting provider's GPUs, reached through Vercel AI Gateway (`https://ai-gateway.vercel.sh/v1`, `gateway` in `config.yaml`) | The customer's own GPU VM, on its own VCF |
| Who serves it | The provider the gateway routes to (for example Baseten, Fireworks, Groq); the runner records it per answer when the gateway returns it | vLLM, llama.cpp or Ollama, installed by the VMware administrator at initial setup |
| Weights | The provider's copy and precision | Downloaded from Hugging Face, at the precision the GPU allows |
| Internet | Yes | Not required; customer data stays on site |
| Cost | Per token | GPU only, no per-token cost |

- One gateway: Vercel AI Gateway. It is an OpenAI-compatible front door to many providers and many models, so the runner tests 3 or 10 models with one API key and one code path. It is a test convenience only.
- Hugging Face is not a gateway here. It is where the open weights are published; this file uses it to check size, licence and release date, and the site downloads the weights from it.
- Both speak the same OpenAI-compatible API. The harness changes one setting ([harness/llm.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/llm.py): base URL and key); the retrieval, tools, prompts and verifier are the same code (`ARCHITECTURE.md`, section 7).
- So the gateway is not part of the product and is not relevant at the customer site. It is the reason for criterion 6: a model that is not on the gateway cannot be benchmarked cheaply, and a model without downloadable weights cannot be deployed.

### What the gateway does not prove
- Precision: a provider may serve 16-bit or 8-bit weights; the site may run 4-bit on a 48 GB GPU. 4-bit costs some accuracy on multi-step reasoning.
- Version: the provider serves what it chose to load under the id (mistral-small changed from 24B dense to Mistral Small 4 without a new id).
- Speed: gateway latency measures the provider and the network, not the customer GPU.
- Guard: before release, the chosen model is run once on the benchmark from local weights, at the deployed precision, on the target GPU. The release score is that run (open work in [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), section Evaluation).

## 3. Selection criteria
Two limits decide (author, 2026-11-05):
- Fit for the goal: the model knows vSphere basics and can become a narrow Level 400 VMware expert with this harness. Criteria 1, 4, 5 and 7 test this; the benchmark decides the rest.
- Hardware cost: it runs on one GPU at the customer site. Criterion 3.

Country of origin is not a criterion. Parameter count is not a criterion; memory and speed are.

All are required. A model that fails one is not a candidate.
1. Vision: reads screenshots. Administrators upload several screenshots per question, from esxtop, the vCenter UI and the VCF Operations UI (author, 2026-11-05). Checked by the `vision` tag in the gateway model list; the runner refuses a model without it when screenshot questions are in the run.
2. Open weights, with a licence that allows commercial on-premises use. Checked per model before deployment.
3. Fits one GPU with at most 96 GB of memory: all weights at 4-bit or better, plus the KV cache for a 32K context.
   - Memory is set by total parameters, also for a mixture-of-experts (MoE) model: every expert must be loaded. Speed is set by active parameters.
   - A 4-bit model needs about 0.55 GB per billion total parameters; 8-bit about 1.05 GB. Add 5-10 GB for the KV cache and runtime.
   - Two tiers, reported separately so the author can weigh score against hardware cost:

| Tier | GPU memory | Fits (4-bit) |
|---|---|---|
| A | 48 GB | dense up to about 70B at 4-bit or 35B at 8-bit; MoE up to about 70B total |
| B | 96 GB | MoE up to about 150B total, for example 120B with 6-12B active |

   - More than one GPU is out: the cost doubles for one model.
4. Tool calling, for agentic retrieval and the calculator, catalog and flow tools.
5. Context window of at least 32K tokens: system prompt + 8-12K retrieved text + images + answer.
6. Available both on the benchmark gateway and as downloadable weights, so the tested model is the deployed model.
7. Latest generation only: one model per family and generation. An older generation or a smaller sibling of the same generation is a duplicate (author, 2026-11-05).

Preferred, not required:
- Vendor diversity: different training data fails on different questions. A mix shows whether a failure is a knowledge gap (all fail) or a model gap (one fails).

## 4. Candidates
| Model | Tier | Size, licence | Why in the benchmark | Result so far |
|---|---|---|---|---|
| google/gemma-4-31b-it | A | 31B dense, Gemma licence | Strong instruction following; long context | Best: 58% exact with one lookup (17 questions, old scoring) |
| alibaba/qwen3.8-27b | A | 27.8B dense, Apache 2.0 | Newest Qwen dense model (weights 2026-08) | Added 2026-11-04 |
| meta/muse-glimmer-30b | A | 29.8B, Apache 2.0 | Built for agentic, multi-turn tool use (weights 2026-08) | Added 2026-11-05 |

- 3 candidates from 3 vendors (Google, Alibaba, Meta), all dense, all tier A (one 48 GB GPU at 4-bit or 8-bit).
- Next challenger: a current-generation dense vision model of about 70B, when one is published and on the gateway (open work in [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), section Evaluation).
- Vision tags checked in the gateway model list on 2026-11-05.
- Muse-Glimmer-30B: the gateway does not tag it `open-weights`; the weights and the Apache 2.0 licence are on Hugging Face (`meta-models/Muse-Glimmer-30B`, 29.8B parameters, checked 2026-11-05).
- mistral-small (removed, section 7): the gateway description says the id serves Mistral Small 4 (2026-03, `mistralai/Mistral-Small-4-119B-2603`), the latest Mistral Small in the Mistral model list (https://docs.mistral.ai/models, checked 2026-11-05). The gateway's 2024-09 release date is older than the model the id now serves; the description is the authority. It is 119B MoE, not 24B dense as this file said before.
- Licences checked on Hugging Face 2026-11-05. The Gemma licence allows commercial use; read it before deployment.

## 5. Frontier reference
- One frontier model, scored the same way with and without the knowledge base, in every benchmark: anthropic/claude-opus-5.5 so far.
- The claim ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 1) is met when a candidate with the knowledge base beats the frontier reference without it by more than the margin.
- Run it with `--models anthropic/claude-opus-5.5 --concurrency 3` (it rate-limits at 12).

## 6. Judge
- Grades judged answers 0-3: [benchmark/runner/judge.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/judge.py). Method: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 14.
- Model: `judge_model` in `config.yaml`, now openai/gpt-5.6-sol.
- Rules:
  - never a candidate (the runner refuses the benchmark);
  - a different vendor from the frontier reference, so no model family grades its own answers;
  - vision, because screenshot questions can be free text;
  - temperature 0.
- The judge is a frontier model on the benchmark gateway only. It is never deployed: at a customer site nothing is graded.

## 7. Removed
| Model | Date | Reason |
|---|---|---|
| alibaba/qwen-3-32b | 2026-11-05 | No vision. Was the reference dense model of the class (48%). |
| alibaba/qwen-3-14b | 2026-11-05 | No vision (42%). |
| openai/gpt-oss-20b | 2026-11-05 | No vision (48%; often broke the answer format in agentic mode). |
| nvidia/nemotron-3-nano-30b-a3b | 2026-11-05 | No vision (25%). |
| zai/glm-4.7-flash | 2026-11-05 | No vision. Added 2026-11-04, never run. |
| alibaba/qwen3.6-27b | 2026-11-05 | Previous generation of qwen3.8-27b: duplicate (rule 7). Added 2026-11-04, never run. |
| google/gemma-4-26b-a4b-it | 2026-11-05 | Smaller sibling of gemma-4-31b-it: duplicate (rule 7). Was the speed option (26B MoE, 4B active; 45%). |
| mistral/mistral-small | 2026-11-05 | Serves Mistral Small 4: 119B MoE, 6.5B active. Less compute per token than the dense candidates on twice the GPU memory (section 1). 51% on 17 questions (old scoring; served version then not recorded). |
| inclusionai/ling-3.0-flash-vl | 2026-11-05 | 125B MoE, MIT. Same reason. Added and removed the same day, never run. |
| nvidia/nemotron-3.5-super-vl | 2026-11-05 | 120B MoE, 12B active, OpenMDW 1.1. Same reason. Added and removed the same day, never run. |
| mistral/ministral-8b | 2026-11-03 | 29-40% exact in benchmark 20261103-081849. |

## 8. Not chosen
| Model | Reason |
|---|---|
| Llama 3.3 70B | 70B: twice the hardware; older generation; no vision. |
| gpt-oss-120b, Nemotron 3 Super 120B, Qwen3 Next 80B | Over 80B total weights: multi-GPU or 80 GB GPU. MoE speed does not remove the memory need. |
| DeepSeek-R1-Distill-Qwen-32B | Early-2025 reasoning distill; no vision. Not on the gateway. |
| DeepSeek V4.1 Flash (and V4-Flash-Vision-Exp) | 763B (V4: 304B), MIT. Vision and tool use fit the goal; the size does not: about 420 GB at 4-bit, several GPUs. |
| Inkling-Small (Thinking Machines) | 266B (NVFP4: 156 GB): more than one 96 GB GPU. |
| MiMo V2.6 Flash (Xiaomi), MiniMax M3.1 Flash, Step 3.7 Flash (StepFun), GLM-5.3-Flash (Z.ai) | 198-320B total: more than one 96 GB GPU at 4-bit. |
| Kimi K2.x and K3 (Moonshot), Llama 4 Maverick, Mistral Large 3 and 4, Qwen3.8 Max | Hundreds of billions to trillions of parameters. |
| Llama 4 Scout | 109B, fits tier B, but Meta's previous generation: Muse-Glimmer-30B is the latest (rule 7). |
| Qwen3-VL-235B | 235B, and the previous Qwen generation. |
| Ministral 3 14B | Fits tier A easily. Not chosen: 8-14B models scored lowest so far (qwen-3-14b 42%, ministral-8b 29-40%). Reserve if a smaller GPU is wanted. |
| Devstral Small, Qwen3 Coder 30B | Tuned for code, not for technical reading comprehension. |
| InternVL2-26B | Released 2024-06: two generations old (InternVL2.5, then InternVL3.5 in 2025-08). Not on the gateway. Its latest sibling in the size range, InternVL3.5-30B-A3B, is not on the gateway either (rule 6). |

## 9. History
- 2026-11-05: vision made a basic requirement (author); 5 text-only models removed; judge added. Then latest generation only (author): qwen3.6-27b and gemma-4-26b-a4b-it removed; muse-glimmer-30b added. Then the size rule changed from 24-35B parameters to one GPU of at most 96 GB (author: the only limits are fit for the goal and hardware cost); mistral-small identified as Mistral Small 4; ling-3.0-flash-vl and nemotron-3.5-super-vl added. All open-weight vision models on the gateway were checked; reasons in section 8. Then the selection reasoning (section 1) and the override rate were added. Then corrected (author): the model brings vSphere basics from training; the knowledge base holds Level 400 only. Dense about 70B named as a better challenger than 120B MoE; none available on the gateway. Then the 3 MoE models dropped (author); 3 dense candidates remain. Section 2 (gateway vs site) added.
- 2026-11-04: added qwen3.8-27b, qwen3.6-27b and glm-4.7-flash. Licences and sizes checked on Hugging Face: Qwen/Qwen3.8-27B and Qwen/Qwen3.6-27B Apache 2.0, 27.8B parameters; zai-org/GLM-4.7-Flash MIT, 31.2B parameters.
- 2026-11-03: the 7 earlier models kept until 100 questions; ministral-8b dropped. Candidate list was in [project/archive/solution-design.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/solution-design.md), section 5, until 2026-11-05.
