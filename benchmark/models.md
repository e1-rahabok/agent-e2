# Models

Candidate models, the frontier reference and the judge for the benchmark. Not indexed.
Settings: `benchmark/runner/config.yaml`. Why a 27-32B model: `project/solution-design.md`, sections 3 and 4.

## 1. Selection criteria
All are required. A model that fails one is not a candidate.
1. Vision: reads screenshots. Administrators upload several screenshots per question, from esxtop, the vCenter UI and the VCF Operations UI (author, 2026-11-05). Checked by the `vision` tag in the gateway model list; the runner refuses a model without it when screenshot cases are in the run.
2. Open weights, with a licence that allows commercial on-premises use. Checked per model before deployment.
3. Size 24-35B total parameters: fits one data-center GPU.
4. Tool calling, for agentic retrieval and the calculator, catalog and flow tools.
5. Context window of at least 32K tokens: system prompt + 8-12K retrieved text + images + answer.
6. Available both on the test gateway and as downloadable weights, so the tested model is the deployed model.

Preferred, not required:
- Vendor diversity: different training data fails on different questions. A mix shows whether a failure is a knowledge gap (all fail) or a model gap (one fails).

## 2. Candidates
| Model | Type | Why in the test | Result so far (17 questions, old scoring) |
|---|---|---|---|
| google/gemma-4-31b-it | 31B dense, vision | Strong instruction following; long context | Best: 58% exact with one lookup |
| google/gemma-4-26b-a4b-it | 26B MoE, 4B active, vision | Same family, much faster: speed option | 45% |
| mistral/mistral-small | 24B dense, vision | Different vendor | 51% |
| alibaba/qwen3.8-27b | 27.8B dense, vision, Apache 2.0 | Newest Qwen dense model in the class (weights published 2026-08) | Added 2026-11-04 |
| alibaba/qwen3.6-27b | 27.8B dense, vision, Apache 2.0 | Previous Qwen generation (2026-04): shows the gain between generations | Added 2026-11-04 |

- 5 candidates from 3 vendors (Google, Mistral, Alibaba).
- Vision tags checked in the gateway model list on 2026-11-05.

## 3. Frontier reference
- One frontier model, scored the same way with and without the knowledge base, in every run: anthropic/claude-opus-5.5 so far.
- The claim (`benchmark/test-design.md`, section 1) is met when a candidate with the knowledge base beats the frontier reference without it by more than the margin.
- Run it with `--models anthropic/claude-opus-5.5 --concurrency 3` (it rate-limits at 12).

## 4. Judge
- Grades free-text and compound answers 0-3: `benchmark/runner/judge.py`. Method: `benchmark/test-design.md`, section 14.
- Model: `judge_model` in `config.yaml`, now openai/gpt-5.6-sol.
- Rules:
  - never a candidate (the runner refuses the run);
  - a different vendor from the frontier reference, so no model family grades its own answers;
  - vision, because screenshot cases can be free text;
  - temperature 0.
- The judge is a frontier model on the test gateway only. It is never deployed: at a customer site nothing is graded.

## 5. Removed
| Model | Date | Reason |
|---|---|---|
| alibaba/qwen-3-32b | 2026-11-05 | No vision. Was the reference dense model of the class (48%). |
| alibaba/qwen-3-14b | 2026-11-05 | No vision; below the size range (42%). |
| openai/gpt-oss-20b | 2026-11-05 | No vision (48%; often broke the answer format in agentic mode). |
| nvidia/nemotron-3-nano-30b-a3b | 2026-11-05 | No vision (25%). |
| zai/glm-4.7-flash | 2026-11-05 | No vision. Added 2026-11-04, never run. |
| mistral/ministral-8b | 2026-11-03 | 29-40% exact in run 20261103-081849; below the size range. |

## 6. Not chosen
| Model | Reason |
|---|---|
| Llama 3.3 70B | 70B: twice the hardware; older generation; no vision. |
| gpt-oss-120b, Nemotron 3 Super 120B, Qwen3 Next 80B | Over 80B total weights: multi-GPU or 80 GB GPU. MoE speed does not remove the memory need. |
| DeepSeek-R1-Distill-Qwen-32B | Early-2025 reasoning distill, superseded by newer 27-32B models with native tool use; no vision. Not on the gateway. |
| Devstral Small, Qwen3 Coder 30B | Tuned for code, not for technical reading comprehension. |

## 7. History
- 2026-11-05: vision made a basic requirement (author); 5 text-only models removed; judge added.
- 2026-11-04: added qwen3.8-27b, qwen3.6-27b and glm-4.7-flash. Licences and sizes checked on Hugging Face: Qwen/Qwen3.8-27B and Qwen/Qwen3.6-27B Apache 2.0, 27.8B parameters; zai-org/GLM-4.7-Flash MIT, 31.2B parameters.
- 2026-11-03: the 7 earlier models kept until 100 questions; ministral-8b dropped. Candidate list was in `project/solution-design.md`, section 5, until 2026-11-05.
