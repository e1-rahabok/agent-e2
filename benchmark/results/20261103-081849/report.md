# Auto Test report: 20261103-081849

- Index version: `de5f19e22860`. Retrieval: hybrid. Temperature: 0.2. Runs: 5.
- Cases: 17 multiple-choice. Skipped (not multiple-choice): vsphere-cpu-001, vsphere-cpu-002, vsphere-cpu-003, vsphere-cpu-006, vsphere-foundations-001, vsphere-foundations-002, vsphere-foundations-003, vsphere-foundations-004, vsphere-memory-001, vsphere-storage-001, vsphere-storage-002.
- Answers: 2160 scored, 0 failed.

## Summary: one score per model

- Score = Exact: share of the 17 questions answered fully correctly, 0-100%.
- Each run asks all 17 questions once. The table shows the 5 run scores, then their average.
- Text track only. Vision track: see below.
- Modes:
  - baseline: no knowledge base.
  - classic: one lookup in the local knowledge base, results pasted into the prompt.
  - agentic: the model calls lookup tools on the local knowledge base itself, up to 8 calls.
  - No mode has internet access. "Search" in this report always means a lookup in the knowledge base files.
- Method, index version, hybrid retrieval and temperature: `tools/autotest/README.md`, section Methodology.

| Model | Baseline avg (no KB) | Classic avg (KB, one lookup) | Agentic avg (KB, model looks up) | Classic, 5 runs |
|---|---|---|---|---|
| google/gemma-4-31b-it | 34% | 58% | 49% | 47, 53, 71, 53, 65 |
| mistral/mistral-small | 34% | 51% | 32% | 47, 47, 47, 59, 53 |
| alibaba/qwen-3-32b | 41% | 48% | 45% | 53, 47, 53, 47, 41 |
| openai/gpt-oss-20b | 32% | 48% | 27% | 47, 59, 53, 41, 41 |
| google/gemma-4-26b-a4b-it | 41% | 45% | 41% | 53, 35, 53, 47, 35 |
| alibaba/qwen-3-14b | 35% | 42% | 19% | 35, 47, 47, 47, 35 |
| mistral/ministral-8b | 36% | 40% | 29% | 35, 35, 53, 41, 35 |
| nvidia/nemotron-3-nano-30b-a3b | 22% | 25% | 24% | 18, 18, 18, 35, 35 |

## Analysis

### Read with care
- 17 questions only. One question = 6 points of score.
- 95% margin on a model's score: about ±20-24 points. Most gaps between neighbouring models are inside it.
- One run swings by up to 24 points for the same model (gemma-4-31b-it classic: 47% to 71%). Use the 5-run average, not one run.
- Ranking is a first signal, not a decision. A decision needs the planned 100 questions.

### Knowledge base effect
- Classic beat baseline for all 8 models. Gain: +3 (nemotron) to +24 points (gemma-4-31b-it).
- Best result: gemma-4-31b-it classic, 58%.
- mistral-small classic has the highest Majority (65%): its most common answer per question is right more often than any single run.

### Agentic mode
- Agentic scored below classic for 7 of 8 models. It used 2-3x the tokens and cost.
- Recall shows why: agentic retrieved 0-50% of the expected files; classic retrieved 63%. The models search badly or stop early.
- Weak cases:
  - qwen-3-14b agentic: 19%, recall 0%. It rarely calls the tools.
  - nemotron agentic: 0.2 tool steps per answer, recall 1%. It answers without searching.
  - gpt-oss-20b agentic: 48% parse failures. It does not end with the `ANSWER:` line.
- Agentic mode needs prompt or tool-format work before it is a fair test.

### Parse failures
- An answer without a parseable `ANSWER:` line scores wrong.
- nemotron classic: 55% parse failures. Its score measures format compliance more than knowledge.

### Hardest questions
- vendor-neutral-general-001: 0%. Most models chose "Not covered by the knowledge base". The knowledge base has no cost content; expected.
- vsphere-cpu-011, vsphere-cpu-013: about 0%. Multi-answer questions; models pick extra options. Check the knowledge files for these traps.

### Vision track
- 2 questions with screenshots, gemma and mistral models only.
- gemma-4-26b-a4b-it classic: 90%. gemma-4-31b-it baseline: 80%.
- mistral-small and ministral-8b: 0-30%. Not usable for screenshot questions.
- 2 questions is too few for any conclusion beyond a first signal.

### Run notes
- Started at concurrency 4, stopped after 128 answers, resumed at concurrency 12. No answer lost. `config.json` holds the resumed settings.
- Duration 42 minutes. Cost US$ 1.89 at gateway list prices.

## Scores: all metrics

| Model | Mode | Track | Exact | Partial | Majority | ± margin | Consistency | Trap | Parse fail | Recall | Fallback | Steps | Tokens | Latency s | Cost US$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mistral/mistral-small | classic | text | 51% | 62% | 65% | 23% | 41% | 26% | 0% | 63% | 0% | 1.0 | 6736 | 1.3 | 0.088 |
| google/gemma-4-31b-it | classic | text | 58% | 70% | 59% | 23% | 53% | 9% | 0% | 63% | 0% | 1.0 | 6923 | 4.5 | 0.084 |
| alibaba/qwen-3-32b | agentic | text | 45% | 60% | 59% | 23% | 24% | 28% | 5% | 10% | 0% | 1.8 | 4943 | 2.7 | 0.068 |
| alibaba/qwen-3-32b | baseline | text | 41% | 58% | 53% | 24% | 35% | 35% | 0% | - | 0% | 0.0 | 282 | 1.1 | 0.005 |
| google/gemma-4-26b-a4b-it | classic | text | 45% | 60% | 53% | 24% | 35% | 8% | 6% | 63% | 0% | 1.0 | 6920 | 1.3 | 0.090 |
| google/gemma-4-31b-it | agentic | text | 49% | 62% | 47% | 24% | 41% | 22% | 0% | 30% | 0% | 5.0 | 17196 | 16.5 | 0.210 |
| alibaba/qwen-3-32b | classic | text | 48% | 64% | 47% | 24% | 47% | 28% | 0% | 63% | 0% | 1.0 | 6600 | 1.4 | 0.086 |
| openai/gpt-oss-20b | classic | text | 48% | 59% | 47% | 24% | 47% | 24% | 6% | 63% | 0% | 1.0 | 7452 | 8.6 | 0.028 |
| alibaba/qwen-3-14b | classic | text | 42% | 59% | 47% | 24% | 35% | 22% | 5% | 63% | 0% | 1.0 | 7690 | 58.1 | 0.090 |
| google/gemma-4-31b-it | baseline | text | 34% | 49% | 41% | 23% | 59% | 42% | 0% | - | 0% | 0.0 | 296 | 3.3 | 0.005 |
| mistral/mistral-small | baseline | text | 34% | 50% | 41% | 23% | 24% | 41% | 0% | - | 0% | 0.0 | 281 | 1.1 | 0.005 |
| google/gemma-4-26b-a4b-it | baseline | text | 41% | 56% | 41% | 23% | 47% | 32% | 0% | - | 0% | 0.0 | 299 | 0.9 | 0.006 |
| google/gemma-4-26b-a4b-it | agentic | text | 41% | 60% | 41% | 23% | 41% | 14% | 4% | 33% | 0% | 4.9 | 18240 | 7.7 | 0.245 |
| alibaba/qwen-3-14b | baseline | text | 35% | 50% | 41% | 23% | 29% | 41% | 0% | - | 0% | 0.0 | 1113 | 52.8 | 0.020 |
| mistral/ministral-8b | baseline | text | 36% | 52% | 41% | 23% | 18% | 38% | 1% | - | 0% | 0.0 | 271 | 1.2 | 0.003 |
| mistral/mistral-small | agentic | text | 32% | 47% | 35% | 23% | 41% | 34% | 1% | 50% | 0% | 7.8 | 21156 | 7.6 | 0.280 |
| openai/gpt-oss-20b | baseline | text | 32% | 52% | 35% | 23% | 29% | 39% | 0% | - | 0% | 0.0 | 1037 | 6.9 | 0.010 |
| mistral/ministral-8b | classic | text | 40% | 55% | 35% | 23% | 47% | 24% | 0% | 63% | 0% | 1.0 | 6737 | 1.5 | 0.086 |
| mistral/ministral-8b | agentic | text | 29% | 44% | 35% | 23% | 29% | 26% | 1% | 29% | 0% | 7.3 | 14505 | 7.3 | 0.185 |
| nvidia/nemotron-3-nano-30b-a3b | agentic | text | 24% | 41% | 29% | 22% | 24% | 47% | 1% | 1% | 0% | 0.2 | 2037 | 1.5 | 0.010 |
| openai/gpt-oss-20b | agentic | text | 27% | 32% | 29% | 22% | 41% | 6% | 48% | 24% | 0% | 4.3 | 10732 | 11.0 | 0.035 |
| nvidia/nemotron-3-nano-30b-a3b | baseline | text | 22% | 41% | 24% | 20% | 18% | 53% | 0% | - | 0% | 0.0 | 302 | 0.9 | 0.002 |
| nvidia/nemotron-3-nano-30b-a3b | classic | text | 25% | 25% | 18% | 18% | 41% | 13% | 55% | 63% | 0% | 1.0 | 6735 | 1.4 | 0.029 |
| alibaba/qwen-3-14b | agentic | text | 19% | 28% | 18% | 18% | 12% | 18% | 2% | 0% | 0% | 0.7 | 2911 | 34.0 | 0.042 |
| google/gemma-4-31b-it | baseline | vision | 80% | 80% | 100% | 0% | 0% | 10% | 0% | - | 0% | 0.0 | 711 | 4.3 | 0.001 |
| google/gemma-4-26b-a4b-it | classic | vision | 90% | 90% | 100% | 0% | 50% | 0% | 0% | 68% | 0% | 1.0 | 9381 | 1.6 | 0.014 |
| google/gemma-4-31b-it | classic | vision | 60% | 60% | 50% | 69% | 50% | 30% | 0% | 68% | 0% | 1.0 | 9251 | 5.2 | 0.013 |
| google/gemma-4-31b-it | agentic | vision | 50% | 50% | 50% | 69% | 100% | 50% | 0% | 29% | 0% | 3.5 | 11330 | 14.9 | 0.016 |
| mistral/mistral-small | classic | vision | 30% | 30% | 50% | 69% | 0% | 50% | 0% | 68% | 0% | 1.0 | 10347 | 1.9 | 0.016 |
| google/gemma-4-26b-a4b-it | baseline | vision | 30% | 30% | 50% | 69% | 50% | 50% | 0% | - | 0% | 0.0 | 798 | 1.5 | 0.001 |
| google/gemma-4-26b-a4b-it | agentic | vision | 50% | 50% | 50% | 69% | 100% | 50% | 0% | 52% | 0% | 4.9 | 18591 | 8.7 | 0.029 |
| mistral/mistral-small | baseline | vision | 0% | 0% | 0% | 0% | 0% | 90% | 0% | - | 0% | 0.0 | 1971 | 1.6 | 0.003 |
| mistral/mistral-small | agentic | vision | 10% | 10% | 0% | 0% | 50% | 70% | 0% | 52% | 0% | 5.6 | 26787 | 8.6 | 0.041 |
| mistral/ministral-8b | baseline | vision | 10% | 10% | 0% | 0% | 50% | 10% | 50% | - | 0% | 0.0 | 1962 | 2.8 | 0.003 |
| mistral/ministral-8b | classic | vision | 10% | 10% | 0% | 0% | 0% | 40% | 0% | 68% | 0% | 1.0 | 10337 | 1.9 | 0.016 |
| mistral/ministral-8b | agentic | vision | 0% | 0% | 0% | 0% | 0% | 20% | 0% | 46% | 0% | 7.5 | 20677 | 8.4 | 0.031 |

- Exact and Partial: mean over all runs. Majority: most common answer per question. Margin: 95% interval on Majority from the number of questions.
- Consistency: share of questions answered identically in every run. Recall: share of the case `knowledge` ids the mode retrieved or read.

## Exact score by area

| Model | Mode | cpu | general | memory | storage |
|---|---|---|---|---|---|
| alibaba/qwen-3-14b | agentic | 13% | 0% | 40% | 0% |
| alibaba/qwen-3-14b | baseline | 24% | 10% | 64% | 40% |
| alibaba/qwen-3-14b | classic | 44% | 0% | 52% | 60% |
| alibaba/qwen-3-32b | agentic | 40% | 30% | 52% | 80% |
| alibaba/qwen-3-32b | baseline | 38% | 50% | 36% | 80% |
| alibaba/qwen-3-32b | classic | 47% | 0% | 64% | 80% |
| google/gemma-4-26b-a4b-it | agentic | 42% | 0% | 44% | 100% |
| google/gemma-4-26b-a4b-it | baseline | 33% | 50% | 40% | 100% |
| google/gemma-4-26b-a4b-it | classic | 58% | 0% | 48% | 0% |
| google/gemma-4-31b-it | agentic | 60% | 0% | 52% | 40% |
| google/gemma-4-31b-it | baseline | 29% | 30% | 32% | 100% |
| google/gemma-4-31b-it | classic | 62% | 0% | 64% | 100% |
| mistral/ministral-8b | agentic | 27% | 0% | 48% | 20% |
| mistral/ministral-8b | baseline | 22% | 30% | 56% | 80% |
| mistral/ministral-8b | classic | 38% | 10% | 64% | 0% |
| mistral/mistral-small | agentic | 20% | 0% | 60% | 60% |
| mistral/mistral-small | baseline | 18% | 20% | 60% | 80% |
| mistral/mistral-small | classic | 51% | 20% | 72% | 0% |
| nvidia/nemotron-3-nano-30b-a3b | agentic | 29% | 0% | 16% | 60% |
| nvidia/nemotron-3-nano-30b-a3b | baseline | 18% | 10% | 28% | 60% |
| nvidia/nemotron-3-nano-30b-a3b | classic | 18% | 0% | 44% | 40% |
| openai/gpt-oss-20b | agentic | 27% | 0% | 24% | 100% |
| openai/gpt-oss-20b | baseline | 16% | 10% | 56% | 100% |
| openai/gpt-oss-20b | classic | 44% | 10% | 60% | 100% |

## Exact score by level

| Model | Mode | l400 | multi-hop | screenshot |
|---|---|---|---|---|
| alibaba/qwen-3-14b | agentic | 19% | 0% | 30% |
| alibaba/qwen-3-14b | baseline | 31% | 60% | 50% |
| alibaba/qwen-3-14b | classic | 37% | 100% | 50% |
| alibaba/qwen-3-32b | agentic | 37% | 100% | 70% |
| alibaba/qwen-3-32b | baseline | 30% | 100% | 90% |
| alibaba/qwen-3-32b | classic | 44% | 100% | 50% |
| google/gemma-4-26b-a4b-it | agentic | 41% | 20% | 50% |
| google/gemma-4-26b-a4b-it | baseline | 37% | 80% | 50% |
| google/gemma-4-26b-a4b-it | classic | 34% | 100% | 90% |
| google/gemma-4-31b-it | agentic | 41% | 100% | 80% |
| google/gemma-4-31b-it | baseline | 29% | 0% | 90% |
| google/gemma-4-31b-it | classic | 54% | 100% | 60% |
| mistral/ministral-8b | agentic | 29% | 60% | 20% |
| mistral/ministral-8b | baseline | 36% | 60% | 30% |
| mistral/ministral-8b | classic | 41% | 100% | 0% |
| mistral/mistral-small | agentic | 30% | 100% | 10% |
| mistral/mistral-small | baseline | 34% | 80% | 10% |
| mistral/mistral-small | classic | 50% | 100% | 30% |
| nvidia/nemotron-3-nano-30b-a3b | agentic | 14% | 100% | 50% |
| nvidia/nemotron-3-nano-30b-a3b | baseline | 20% | 60% | 20% |
| nvidia/nemotron-3-nano-30b-a3b | classic | 23% | 40% | 30% |
| openai/gpt-oss-20b | agentic | 20% | 60% | 60% |
| openai/gpt-oss-20b | baseline | 29% | 60% | 40% |
| openai/gpt-oss-20b | classic | 47% | 100% | 30% |

## Hardest questions (knowledge base modes)

| Case | Exact | Common wrong answers |
|---|---|---|
| vendor-neutral-general-001 | 0% | NC ×72, (unparsed) ×8 |
| vsphere-cpu-011 | 0% | B,C,D,G ×11, B,C,D,E,G ×7, (unparsed) ×7 |
| vsphere-cpu-013 | 1% | C,E ×26, C,D,E ×19, (unparsed) ×13 |
| vsphere-general-001 | 9% | B,C,D,E ×36, (unparsed) ×16, NC ×8 |
| vsphere-memory-003 | 9% | A,B,E ×26, B,D,E ×19, (unparsed) ×9 |
| vsphere-memory-005 | 10% | A,B,D,E ×32, A,B,E ×13, A,B,D ×9 |
| vsphere-cpu-009 | 15% | A,B ×38, A,B,D ×14, (unparsed) ×8 |
| vsphere-cpu-004 | 22% | B ×34, A ×25, E ×15 |
| vsphere-cpu-012 | 25% | B ×32, C ×21, (unparsed) ×4 |
| vsphere-storage-003 | 52% | A ×18, NC ×11, C ×5 |

Traces: `traces.jsonl` in this folder (one line per answer).
