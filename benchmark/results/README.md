# Benchmark results: round of 2026-11-13

Analysis, changes made and recommendations: [analysis-2026-11-13.md](analysis-2026-11-13.md). The tables below are generated; the analysis is written.

- 4 runs, 196 questions, 5 runs per question, sampling {"google/gemma-4-31b-it": {"temperature": 1.0, "top_p": 0.95, "top_k": 64}}. Judge: openai/gpt-6.1-terra. Written by `benchmark/runner/summarize.py` from the run folders; every number below comes from them.
- How to read a score: the exact value is read at plus or minus 5 points; the signal is the jump from baseline to a mode, read per model on the same questions. Method and scoring: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md). Scores are not comparable with scores graded by another judge.

## Runs

| Run folder | Model | Modes | Request settings | Answers | Failed | Cut off | First to last answer | Cost US$ (judge) |
|---|---|---|---|---|---|---|---|---|
| [20261113-gemma-4-31b-it-2](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261113-gemma-4-31b-it-2/report.md) | google/gemma-4-31b-it | baseline, classic, agentic | `default` | 2940 | 0 | 0 | 67 min | 10.23 (3.80) |
| [20261113-qwen3.8-27b-2](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261113-qwen3.8-27b-2/report.md) | alibaba/qwen3.8-27b | baseline, classic, agentic | `{"reasoning": {"effort": "none"}}` | 2940 | 0 | 22 | 41 min | 11.61 (4.10) |
| [20261113-muse-glimmer-30b-2](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261113-muse-glimmer-30b-2/report.md) | meta/muse-glimmer-30b | baseline, classic, agentic | `{"reasoning": {"enabled": false}}` | 2940 | 0 | 0 | 85 min | 28.57 (4.16) |
| [20261113-claude-opus-5.5-2](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261113-claude-opus-5.5-2/report.md) | anthropic/claude-opus-5.5 | baseline, web | `{"reasoning": {"effort": "medium"}, "max_tokens": 8000}` | 1960 | 0 | 0 | 117 min | 55.82 (2.65) |

- Total cost US$ 106.24. Harness in agentic mode: up-front blocks map, rules, terms, flows, procedure; term map in the agent prompt: on.

## Final score

| Model | Mode | Final | ± margin | Level 100 | Level 200 | Level 300 | Level 400 | Confident wrong |
|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | baseline | **41%** | 7 | 66% | 58% | 49% | 34% | 51% |
| alibaba/qwen3.8-27b | classic | **69%** | 6 | 91% | 75% | 84% | 62% | 29% |
| alibaba/qwen3.8-27b | agentic | **63%** | 7 | 92% | 76% | 78% | 55% | 30% |
| google/gemma-4-31b-it | baseline | **57%** | 7 | 73% | 69% | 59% | 54% | 40% |
| google/gemma-4-31b-it | classic | **78%** | 6 | 83% | 89% | 87% | 74% | 19% |
| google/gemma-4-31b-it | agentic | **76%** | 6 | 89% | 91% | 83% | 71% | 21% |
| meta/muse-glimmer-30b | baseline | **54%** | 7 | 71% | 57% | 54% | 52% | 42% |
| meta/muse-glimmer-30b | classic | **77%** | 6 | 88% | 83% | 82% | 74% | 21% |
| meta/muse-glimmer-30b | agentic | **78%** | 6 | 92% | 80% | 86% | 75% | 20% |
| anthropic/claude-opus-5.5 | baseline | **84%** | 5 | 100% | 89% | 83% | 82% | 11% |
| anthropic/claude-opus-5.5 | web | **81%** | 5 | 98% | 87% | 81% | 79% | 12% |

Final = mean over the questions of the mean credit over the runs. Levels: the same mean within one level. The worst-run score is in each run folder's report.md (consistency; not a gate).

## Lift

Points of the final score. A difference is outside the margin when it is larger than the two margins combined.

| Model | Classic over baseline | Agentic over baseline | Agentic over classic | Web over baseline |
|---|---|---|---|---|
| alibaba/qwen3.8-27b | +28 (outside ±9) | +23 (outside ±10) | -6 (inside ±9) | - |
| anthropic/claude-opus-5.5 | - | - | - | -2 (inside ±8) |
| google/gemma-4-31b-it | +21 (outside ±9) | +19 (outside ±9) | -3 (inside ±8) | - |
| meta/muse-glimmer-30b | +23 (outside ±9) | +24 (outside ±9) | +1 (inside ±8) | - |

## Release gate (agentic mode)

Reference: anthropic/claude-opus-5.5, web mode. Limits: benchmark/design.md, section 7.5.

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| alibaba/qwen3.8-27b | Final score | 63% | at least 85% | no |
| alibaba/qwen3.8-27b | Level 400 | 55% | at least 80% | no |
| alibaba/qwen3.8-27b | Confident wrong | 30% | at most 3% | no |
| alibaba/qwen3.8-27b | Gap to the frontier model | -18% | outcome, not a gate | - |
| alibaba/qwen3.8-27b | Paired test (b 9, c 88) | p 1.000 | significant if p below 0.05 | - |
| google/gemma-4-31b-it | Final score | 76% | at least 85% | no |
| google/gemma-4-31b-it | Level 400 | 71% | at least 80% | no |
| google/gemma-4-31b-it | Confident wrong | 21% | at most 3% | no |
| google/gemma-4-31b-it | Gap to the frontier model | -5% | outcome, not a gate | - |
| google/gemma-4-31b-it | Paired test (b 19, c 46) | p 1.000 | significant if p below 0.05 | - |
| meta/muse-glimmer-30b | Final score | 78% | at least 85% | no |
| meta/muse-glimmer-30b | Level 400 | 75% | at least 80% | no |
| meta/muse-glimmer-30b | Confident wrong | 20% | at most 3% | no |
| meta/muse-glimmer-30b | Gap to the frontier model | -3% | outcome, not a gate | - |
| meta/muse-glimmer-30b | Paired test (b 25, c 44) | p 0.992 | significant if p below 0.05 | - |

Not read here: no misconception of `knowledge/misconceptions.md` stated as true (author check of the answers), and the held-out set at most 11 points below the development set (a separate run).

## Reading

- alibaba/qwen3.8-27b: baseline 41%, classic 69%, agentic 63%. Agentic is +23 points over baseline (outside the margin of 10 points). Agentic and classic are within the margin of each other (-6 points).
- google/gemma-4-31b-it: baseline 57%, classic 78%, agentic 76%. Agentic is +19 points over baseline (outside the margin of 9 points). Agentic and classic are within the margin of each other (-3 points).
- meta/muse-glimmer-30b: baseline 54%, classic 77%, agentic 78%. Agentic is +24 points over baseline (outside the margin of 9 points). Agentic and classic are within the margin of each other (+1 points).
- anthropic/claude-opus-5.5: open web search adds -2 points over the prompt alone (inside the margin of 8 points).
- Best local model in agentic mode: meta/muse-glimmer-30b, 78%; the frontier model without the knowledge base scores 81%, a gap of -3 points (an outcome, not a gate).
- Release gate in agentic mode (final score, Level 400, confident wrong): passed by no model.
- Check 20261113-qwen3.8-27b-2: 0 failed answers, 22 cut off at max_tokens, 6 with no readable letter.
- Check 20261113-muse-glimmer-30b-2: 0 failed answers, 0 cut off at max_tokens, 5 with no readable letter.
- Check 20261113-claude-opus-5.5-2: 0 failed answers, 0 cut off at max_tokens, 2 with no readable letter.

## Time and tokens

| Model | Mode | Mean latency s | Mean tool calls | Mean tokens |
|---|---|---|---|---|
| alibaba/qwen3.8-27b | baseline | 6.7 | 0.0 | 1655 |
| alibaba/qwen3.8-27b | classic | 4.0 | 1.0 | 15146 |
| alibaba/qwen3.8-27b | agentic | 9.7 | 7.2 | 52901 |
| anthropic/claude-opus-5.5 | baseline | 11.6 | 0.0 | 1810 |
| anthropic/claude-opus-5.5 | web | 15.2 | 0.6 | 4333 |
| google/gemma-4-31b-it | baseline | 7.5 | 0.0 | 1226 |
| google/gemma-4-31b-it | classic | 13.9 | 1.0 | 15126 |
| google/gemma-4-31b-it | agentic | 24.3 | 4.3 | 29210 |
| meta/muse-glimmer-30b | baseline | 9.1 | 0.0 | 1546 |
| meta/muse-glimmer-30b | classic | 11.0 | 1.0 | 14431 |
| meta/muse-glimmer-30b | agentic | 27.6 | 7.4 | 44321 |

Latency is the sum of the model calls of one answer (the judge is not in it). Per-run detail, hardest questions and consistency: the report.md of each run folder.
