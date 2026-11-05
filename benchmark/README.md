# Evaluation

Golden cases that measure whether the knowledge base and harness improve AI answers.
Never index this folder: it contains answer keys.

## Layout

```text
benchmark/
├── cases/<id>-<slug>.md                          # one case per file, one flat folder
├── cases/<id>/                                   # the case's attachments: screenshots, logs, diagrams (only when it has any)
├── runner/                                       # Auto Test: run.py, cases.py, judge.py, report.py, config.yaml
├── models.md                                     # candidate models, frontier reference, judge
├── results/results.csv                           # summary: one row per case per model per mode per run set
├── results/autotest/<run-id>/                    # per run: answers.csv, report.md, config.json (traces.jsonl not in git)
└── _templates/case.md
```

- One flat folder: a case often crosses products (vSphere, Windows, Linux, NSX, VCF Operations) and areas, so folders cannot hold it. The slices are metadata:
  - `product`: every product the case touches (values from `project/tools/tags.yaml`);
  - `technology`: every area it touches (cpu, memory, storage, network, system). The blueprint counts these: `benchmark/test-design.md`, section 3.1.
- Existing ids keep their old form (`vsphere-cpu-004`); new cases get neutral ids (`case-0031`). An id is an internal key for the runner: the words in an old id (`general`, `foundations`) are not a classification. `area`, `technology` and `pillar` classify the case (author, 2026-11-05).
- Scope of questions: performance monitoring and troubleshooting, and the capacity view that supports it. Cost and price questions are out of scope (author, 2026-11-04).
- One file per case: scales to hundreds of cases, one diff per case, attachments per case.
- Ids never change and are never reused. Retired cases get `status: retired`. A case is deleted only when the author asks.
- Deleted on author request: `vendor-neutral-general-001` (hyperscaler VM cost; out of scope, Q039).

## Case fields
- Each case file: `# Title`, then `## Prompt`, `## Likely wrong answer`, `## Expected key points`, and a `## Metadata` section at the end with one yaml block. No front matter at the top.
- Only `## Prompt` (plus attachments) is ever sent to the AI.

| Field | Meaning |
|---|---|
| `id` | Never reused. New cases: `case-<nnnn>`. |
| `product` | Every product the case touches: vsphere, vsan, nsx, vcf-operations, windows, linux, kubernetes. |
| `technology` | Every area the case touches: cpu, memory, storage, network, system. |
| `pillar` | Optional. Pillars of operations the case tests, values from `project/tools/tags.yaml`. |
| `area` | Main area, for the per-area report: cpu, memory, storage, network, system, operations-management. `operations-management` when the topic is performance troubleshooting, capacity planning or rightsizing (author, 2026-11-05). |
| `input` | text, screenshot, diagram, log, mixed. Non-text inputs live in `cases/<id>/`, next to the case file. No `.md` files there: the runner and lint read every `.md` under `cases/` as a case. |
| `tests` | concept, distinction, judgment, troubleshooting. |
| `knowledge` | Knowledge ids the answer should draw on. Used to measure retrieval recall, not only the answer. |
| `origin` | book, quiz, live-lab, real-ticket, synthetic. |
| `source_path` | Heading path in the source document, for QA. |
| `format` | multiple-choice (scored by letters), free-text or compound (scored 0-3 by the judge). All scored automatically by `benchmark/runner`. |
| `level` | recall, l400, multi-hop, screenshot. Multiple-choice only. |
| `answer` | Correct option letters as written in `## Prompt`. Multiple-choice only. Never sent to the AI. |
| `trap` | Option letters of the known wrong answer. Multiple-choice only. Never sent to the AI. |
| `status` | draft, reviewed, retired. |

## Multiple-choice scoring (automatic)
- Runner: `benchmark/runner/run.py`. Commands and full methodology: `benchmark/runner/README.md`.
- Options are shuffled per run. Two options are appended to every question: "Not covered by the knowledge base" and "Unsure".
- Every question says there can be more than one correct option. The number of correct options is never revealed.
- Each question runs 5 times per model and mode.

| Answer | Class |
|---|---|
| Exactly the correct letters | Correct |
| Unsure, chosen alone | Unsure (not correct, not wrong) |
| Anything else: wrong, partly right, Unsure mixed with other letters, unparseable | Confident wrong |

- The model is told that a wrong answer is worse than Unsure. No points and no -1: see `benchmark/test-design.md`, section 7.1.
- Headline: **Stable correct**, the share of questions answered exactly right in all 5 runs. Target: at least 85%, aim 99% (author, 2026-11-03).
- Also reported: Luck (right in some runs only), confident-wrong rate, Unsure rate, accuracy when answered, trap rate, retrieval recall, tools used, verifier flags.
- Reason and design: `benchmark/test-design.md` (blueprint, why 100 questions, scoring, validity threats).

## Free-text and compound scoring (judge, 0-3)
- The runner sends the prompt (and images) without options, then a judge model scores the answer against `## Expected key points` and `## Likely wrong answer`.
- Rubric, judge rules and checks: `benchmark/test-design.md`, section 14. Judge model: `benchmark/models.md`.
- Write `## Expected key points` as one testable fact per bullet: the judge scores against them and nothing else.
- Write `## Likely wrong answer` in the words a user would use: the judge flags an answer that states it.

## Final score
- One score, 0-100%, with sub-scores for multiple choice, screenshot and conversation. Method: `benchmark/test-design.md`, section 7.4.

## results.csv columns

| Column | Example |
|---|---|
| date | 2026-11-03 |
| model | model id |
| effort | n/a for gateway models; medium / high / max where the model has an effort setting |
| mode | baseline, classic, agentic (`-vision` suffix for the screenshot track) |
| case_id | vsphere-cpu-004 |
| score | Auto Test: mean credit over the runs, 0-1 (exact letters 1 or 0; free text: judge score / 3). Older rows: exact-match mean, or manual 0-3. |
| notes | run id and scale, e.g. "autotest 20261105-090000; score = mean credit 0-1 (exact letters, or judge score / 3) over 5 runs; temp 0.2" |
