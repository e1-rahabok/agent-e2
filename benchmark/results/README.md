# Benchmark results: round of 2026-11-16

- 4 runs, 291 questions, 5 runs per question, sampling {"google/gemma-4-31b-it": {"temperature": 1.0, "top_p": 0.95, "top_k": 64}}. Written by `benchmark/runner/summarize.py` from the run folders; every number below comes from them.
- How to read a score: the exact value is read at plus or minus 5 points. The benchmark is a proof: Agent E2 against the release gate and the frontier reference. Method and scoring: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md).

## Runs

| Run folder | Model | Modes | Request settings | Answers | Failed | Cut off | First to last answer | Cost US$ |
|---|---|---|---|---|---|---|---|---|
| [20261116-gemma-4-31b-it](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261116-gemma-4-31b-it/report.md) | google/gemma-4-31b-it | baseline, agent-e2 | `default` | 2910 | 17 | 0 | 216 min | 8.27 |
| [20261116-qwen3.8-27b-reasoning-off](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261116-qwen3.8-27b-reasoning-off/report.md) | alibaba/qwen3.8-27b | baseline, agent-e2 | `{"reasoning": {"effort": "none"}}` | 2910 | 22 | 97 | 94 min | 9.80 |
| [20261116-muse-glimmer-30b-effort-low](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261116-muse-glimmer-30b-effort-low/report.md) | meta/muse-glimmer-30b | baseline, agent-e2 | `{"reasoning": {"effort": "low"}}` | 2910 | 0 | 0 | 87 min | 22.73 |
| [20261116-claude-opus-5.5](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261116-claude-opus-5.5/report.md) | anthropic/claude-opus-5.5 | web | `{"reasoning": {"effort": "medium"}, "max_tokens": 8000}` | 1455 | 1 | 0 | 186 min | 57.58 |

- Total cost US$ 98.38. Agent E2: up-front blocks rules, terms; case read by the model: on; gap follow-up: on.

## Final score

| Model | Mode | Final | ± margin | Level 100 | Level 200 | Level 300 | Level 400 | Confident wrong |
|---|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | baseline | **20%** | 5 | 51% | 35% | 20% | 18% | 71% |
| alibaba/qwen3.8-27b | agent-e2 | **67%** | 5 | 97% | 85% | 72% | 61% | 32% |
| google/gemma-4-31b-it | baseline | **40%** | 6 | 60% | 69% | 41% | 36% | 60% |
| google/gemma-4-31b-it | agent-e2 | **79%** | 5 | 100% | 98% | 82% | 74% | 21% |
| meta/muse-glimmer-30b | baseline | **41%** | 6 | 71% | 64% | 43% | 37% | 58% |
| meta/muse-glimmer-30b | agent-e2 | **84%** | 4 | 100% | 96% | 85% | 83% | 15% |
| anthropic/claude-opus-5.5 | web | **79%** | 5 | 100% | 93% | 77% | 78% | 17% |

Final = mean over the questions of the mean credit over the runs. Levels: the same mean within one level. The worst-run score is in each run folder's report.md (consistency; not a gate).

## Lift

Points of the final score. A difference is outside the margin when it is larger than the two margins combined.

| Model | Agent E2 over the model alone |
|---|---|
| alibaba/qwen3.8-27b | +47 (outside ±7) |
| google/gemma-4-31b-it | +39 (outside ±7) |
| meta/muse-glimmer-30b | +44 (outside ±7) |

## Release gate (Agent E2)

Reference: anthropic/claude-opus-5.5, web mode. Limits: benchmark/design.md, section 7.5.

| Model | Gate | Value | Limit | Pass |
|---|---|---|---|---|
| alibaba/qwen3.8-27b | Final score | 67% | at least 85% | no |
| alibaba/qwen3.8-27b | Level 400 | 61% | at least 80% | no |
| alibaba/qwen3.8-27b | Confident wrong | 32% | at most 3% | no |
| alibaba/qwen3.8-27b | Gap to the frontier model | -12% | outcome, not a gate | - |
| alibaba/qwen3.8-27b | Paired test (b 29, c 131) | p 1.000 | significant if p below 0.05 | - |
| google/gemma-4-31b-it | Final score | 79% | at least 85% | no |
| google/gemma-4-31b-it | Level 400 | 74% | at least 80% | no |
| google/gemma-4-31b-it | Confident wrong | 21% | at most 3% | no |
| google/gemma-4-31b-it | Gap to the frontier model | 0% | outcome, not a gate | - |
| google/gemma-4-31b-it | Paired test (b 46, c 72) | p 0.994 | significant if p below 0.05 | - |
| meta/muse-glimmer-30b | Final score | 84% | at least 85% | no |
| meta/muse-glimmer-30b | Level 400 | 83% | at least 80% | yes |
| meta/muse-glimmer-30b | Confident wrong | 15% | at most 3% | no |
| meta/muse-glimmer-30b | Gap to the frontier model | 6% | outcome, not a gate | - |
| meta/muse-glimmer-30b | Paired test (b 67, c 62) | p 0.362 | significant if p below 0.05 | - |

Not read here: no up-front misconception (lines marked `up_front`) stated as true (author check of the answers), and the held-out set at most 11 points below the development set (a separate run).

## Consensus of 3, projected

What the shipped setting `consensus_samples: 3` would give: multiple-choice letters stand only when 3 samples agree; otherwise Unsure. Projected from the recorded runs, no new model call (`report.py`, function `consensus`). Judged answers unchanged.

| Model | Mode | Final | Final, consensus | Confident wrong | Confident wrong, consensus | Multiple choice: confident wrong, consensus | Multiple choice: Unsure, consensus |
|---|---|---|---|---|---|---|---|
| alibaba/qwen3.8-27b | agent-e2 | 67% | 43% | 32% | 2% | 2% | 54% |
| google/gemma-4-31b-it | agent-e2 | 79% | 66% | 21% | 7% | 7% | 27% |
| meta/muse-glimmer-30b | agent-e2 | 84% | 75% | 15% | 5% | 5% | 20% |

## Reading

- alibaba/qwen3.8-27b: baseline 20%, agent-e2 67%. Agent E2 is +47 points over the model alone (outside the margin of 7 points).
- google/gemma-4-31b-it: baseline 40%, agent-e2 79%. Agent E2 is +39 points over the model alone (outside the margin of 7 points).
- meta/muse-glimmer-30b: baseline 41%, agent-e2 84%. Agent E2 is +44 points over the model alone (outside the margin of 7 points).
- Best local model with Agent E2: meta/muse-glimmer-30b, 84%; the frontier model without the knowledge base scores 79%, a gap of +6 points (an outcome, not a gate).
- Release gate on Agent E2 (final score, Level 400, confident wrong): passed by no model.
- Check 20261116-gemma-4-31b-it: 17 failed answers, 0 cut off at max_tokens, 0 with no readable letter.
- Check 20261116-qwen3.8-27b-reasoning-off: 22 failed answers, 97 cut off at max_tokens, 22 with no readable letter.
- Check 20261116-claude-opus-5.5: 1 failed answers, 0 cut off at max_tokens, 0 with no readable letter.

## Time and tokens

| Model | Mode | Mean latency s | Mean model calls | Mean tokens |
|---|---|---|---|---|
| alibaba/qwen3.8-27b | baseline | 5.2 | 1.0 | 2870 |
| alibaba/qwen3.8-27b | agent-e2 | 9.2 | 2.0 | 38396 |
| anthropic/claude-opus-5.5 | web | 12.0 | 1.7 | 5802 |
| google/gemma-4-31b-it | baseline | 3.1 | 1.0 | 2145 |
| google/gemma-4-31b-it | agent-e2 | 65.0 | 2.0 | 36901 |
| meta/muse-glimmer-30b | baseline | 9.7 | 1.0 | 4463 |
| meta/muse-glimmer-30b | agent-e2 | 28.3 | 2.0 | 34056 |

Latency is the sum of the model calls of one answer Per-run detail, hardest questions and consistency: the report.md of each run folder.
