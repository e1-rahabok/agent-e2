# Auto Test report: 20261103-093742

- Index version: `d0477bd976d2`. Retrieval: hybrid. Temperature: 0.2. Runs: 5.
- Cases: 17 multiple-choice. Skipped (not multiple-choice): vsphere-cpu-001, vsphere-cpu-002, vsphere-cpu-003, vsphere-cpu-006, vsphere-foundations-001, vsphere-foundations-002, vsphere-foundations-003, vsphere-foundations-004, vsphere-memory-001, vsphere-storage-001, vsphere-storage-002.
- Answers: 285 scored, 65 failed.

## Summary: frontier reference (anthropic/claude-opus-5.5)

- Purpose: a ceiling reference for the 8 small models in run 20261103-081849. Same 17 questions, same knowledge base logic, same 5 runs.
- Score = Exact, 0-100%, average of 5 runs. Text track.
- "65 failed" above: first attempts refused by the gateway at concurrency 12 (HTTP 429, "No access to this model at this time"). All 65 were retried at concurrency 3 and succeeded. All 285 answers are scored.
- Cost: US$ 14.96.

| Mode | Avg | 5 runs | Trap | Recall |
|---|---|---|---|---|
| Baseline (no KB) | 75% | 71, 71, 76, 82, 76 | 16% | - |
| Classic (KB, one lookup) | 67% | 71, 65, 71, 65, 65 | 6% | 63% |
| Agentic (KB, model looks up) | 67% | 65, 71, 65, 71, 65 | 9% | 40% |

- Best small model, same questions: gemma-4-31b-it, classic 58%, baseline 34%.

## Analysis

### Main finding: the knowledge base lowered the frontier score
- Baseline 75% beat classic and agentic (67%). For the small models it was the reverse.
- The knowledge base cut the trap rate: 16% to 6-9%. Fewer confident wrong answers.
- Per question, against baseline:
  - Helped: vsphere-memory-005 (0 to 5 of 5 runs), vsphere-cpu-009 (3 to 5).
  - Hurt: vendor-neutral-general-001 (5 to 0), vsphere-cpu-013 (5 to 0), vsphere-general-001 (5 to 2).
  - Wrong in every mode: vsphere-cpu-011, vsphere-memory-003, vsphere-cpu-004 (1 of 5 at best).

### Why it hurt: the prompt forbids the model's own knowledge
- The kb-mode prompt says: answer using ONLY the knowledge base; if not covered, choose "Not covered by the knowledge base".
- When the knowledge base is silent, the model drops a correct answer it knows:
  - vendor-neutral-general-001 (hyperscaler cost): the knowledge base has no cost content. Classic and agentic chose Not covered in all 10 runs. Baseline was right in all 5.
  - vsphere-cpu-013: classic rejected a correct option because it relied on "claims the knowledge base does not make" (model's reason).
  - vsphere-general-001: Not covered in 3 of 10 kb runs.
- This is a prompt design choice, not a knowledge error. Trade-off:
  - ONLY the knowledge base: fewer invented answers, but no credit where the knowledge base is silent.
  - Knowledge base first: knowledge base wins on conflict; general knowledge fills gaps. More coverage; more risk of invented answers.

### Questions wrong in every mode
- vsphere-cpu-004: key C; models choose B (Core Utilization as the capacity measure) with and without the knowledge base. Small models also chose B most often.
- vsphere-cpu-011: key A,B,C,D; classic chose C,D, citing the knowledge base for A and D being wrong.
- vsphere-memory-003: key A,B,D,E; models drop A or D.
- For each: either the knowledge base is missing or contradicting the fact, or the key needs checking. Author check needed.

### Open items
- Author questions Q038-Q043 in `docs/author-questions.md`: prompt rule, cost case, and the 4 golden cases wrong for all models (cpu-004, cpu-011, cpu-013, memory-003).

### What it means for the targets (minimum 85%, target 99%)
- Even the frontier model reaches 67-75%. No small model can pass 85% until the knowledge base, prompt and keys are fixed.
- The 6 questions above hold most of the gap. Fixing them would move the frontier classic score toward 90%+.
- The knowledge base is the lever: it lifted 2 questions to 5 of 5 and cut traps. The gaps and the ONLY rule hold it back.

## Scores: all metrics

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Trap | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | baseline | text | 75% | 86% | 76% | 20% | 88% | 16% | 0% | - | 0% | 0.0 | 791 | 5.8 | 0.843 |
| anthropic/claude-opus-5.5 | classic | text | 67% | 78% | 71% | 22% | 94% | 6% | 0% | 63% | 0% | 1.0 | 10636 | 4.2 | 4.023 |
| anthropic/claude-opus-5.5 | agentic | text | 67% | 77% | 59% | 23% | 71% | 9% | 0% | 40% | 0% | 5.1 | 20334 | 13.4 | 7.982 |
| anthropic/claude-opus-5.5 | baseline | vision | 60% | 60% | 50% | 69% | 50% | 40% | 0% | - | 0% | 0.0 | 2899 | 8.7 | 0.210 |
| anthropic/claude-opus-5.5 | classic | vision | 50% | 50% | 50% | 69% | 100% | 50% | 0% | 68% | 0% | 1.0 | 15098 | 6.4 | 0.679 |
| anthropic/claude-opus-5.5 | agentic | vision | 70% | 70% | 50% | 69% | 50% | 30% | 0% | 29% | 0% | 4.0 | 26587 | 16.4 | 1.222 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the case `knowledge` ids the mode retrieved or read.

## Exact score by area

| Model | Mode | cpu | general | memory | storage |
|---|---|---|---|---|---|
| anthropic/claude-opus-5.5 | agentic | 67% | 20% | 80% | 100% |
| anthropic/claude-opus-5.5 | baseline | 76% | 100% | 60% | 100% |
| anthropic/claude-opus-5.5 | classic | 67% | 20% | 80% | 100% |

## Exact score by level

| Model | Mode | l400 | multi-hop | screenshot |
|---|---|---|---|---|
| anthropic/claude-opus-5.5 | agentic | 69% | 40% | 70% |
| anthropic/claude-opus-5.5 | baseline | 76% | 100% | 60% |
| anthropic/claude-opus-5.5 | classic | 67% | 100% | 50% |

## Hardest questions (knowledge base modes)

| Case | Exact | Common wrong answers |
|---|---|---|
| vendor-neutral-general-001 | 0% | NC ×10 |
| vsphere-cpu-013 | 0% | C ×5, NC ×2, D,E ×1 |
| vsphere-memory-003 | 0% | A,B,E ×5, B,D,E ×5 |
| vsphere-cpu-011 | 10% | C,D ×5, A,C,D ×4 |
| vsphere-cpu-004 | 20% | B ×15, D ×1 |
| vsphere-general-001 | 40% | NC ×3, B,D,E ×2, D ×1 |
| vsphere-cpu-005 | 70% | B ×3 |
| vsphere-cpu-007 | 100% |  |
| vsphere-cpu-008 | 100% |  |
| vsphere-cpu-009 | 100% |  |

Traces: `traces.jsonl` in this folder (one line per answer).
