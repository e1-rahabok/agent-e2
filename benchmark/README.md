# Evaluation

Questions that measure whether the knowledge base and harness improve AI answers.
Never index this folder: it contains answer keys.

## Layout

```text
benchmark/
├── questions/<id>-<slug>.md                          # one question per file, one flat folder
├── questions/<id>/                                   # the question's attachments: screenshots, logs, diagrams (only when it has any)
├── runner/                                       # Benchmark runner: run.py, questions.py, judge.py, report.py, config.yaml
├── models.md                                     # candidate models, frontier reference, judge
├── results/results.csv                           # summary: one row per question, model and mode of each benchmark
├── results/<benchmark-id>/                       # per benchmark: answers.csv, report.md, config.json (traces.jsonl not in git)
└── _templates/question.md
```

- One flat folder: a question often crosses products (vSphere, Windows, Linux, NSX, VCF Operations) and technologies, so folders cannot hold it. The slices are metadata (section Metadata tags):
  - `product`: every product the question touches (values from `project/tools/tags.yaml`);
  - `technology`: every area it touches (cpu, memory, storage, network, system). The blueprint counts these: `benchmark/design.md`, section 3.5.
- Existing ids keep their old form (`vsphere-cpu-004`); new questions get neutral ids (`question-0031`). An id is an internal key for the runner: the words in an old id (`general`, `foundations`) are not a classification. `technology`, `task` and `level` classify the question (author, 2026-11-05).
- Scope of questions: performance monitoring and troubleshooting, and the capacity view that supports it. Cost and price questions are out of scope (author, 2026-11-04).
- One file per question: scales to hundreds of questions, one diff per question, attachments per question.
- Ids never change and are never reused. Retired questions get `status: retired`. A question is deleted only when the author asks.
- Deleted on author request: `vendor-neutral-general-001` (hyperscaler VM cost; out of scope, Q039).

## Question fields
- Each question file: `# Title`, then `## Prompt`, `## Attachments` (when the question has any), `## Likely wrong answer`, `## Expected key points`, and a `## Metadata` section at the end with one yaml block. No front matter at the top.
- `## Prompt` layout, for the human reviewer: context facts as bullets, one fact per bullet; the question or instruction as its own paragraph; options as a bullet list, `- A. text`. The candidate gets the same text: the runner rebuilds the option list (shuffled, `A. text` per line), and a model reads bullets as well as prose. Consecutive `A. text` lines without bullets render on GitHub as one paragraph.
- `## Attachments` links every attachment as an image with alt text, so a reviewer sees it on GitHub. It is never sent to the model: the runner sends the files listed in `attachments`.
- Only `## Prompt` (plus attachments) is ever sent to the AI.

### Metadata tags
The tags in each question's `## Metadata` block, grouped by what they describe. Values are the complete set; lint rejects any other.

**Identity**

| Tag | Meaning | Values |
|---|---|---|
| `id` | Internal key for the runner and the results. Never changed, never reused. The words in an old id (`vsphere-cpu-004`) are not a classification | New questions: `question-<nnnn>` |
| `title` | Short name for a human reviewer | Free text |
| `status` | Review state | `draft` (written, not reviewed), `reviewed` (author approved), `retired` (kept for history, not run) |

**What the question is about**

| Tag | Meaning | Values |
|---|---|---|
| `product` | Every product the question touches. A list | `vsphere`, `vsan`, `nsx`, `vcf-operations`, `windows`, `linux`, `kubernetes` |
| `technology` | Every technology area the question touches. A list. The per-area report counts each one | `cpu`, `memory`, `storage`, `network`, `system` (the object as a whole: KPIs, capacity, availability, DRS, provider/consumer, rollups) |
| `task` | What the administrator is trying to do: one of the five tasks of the blueprint (`benchmark/design.md`, section 3.1) | `read-metric`, `troubleshoot`, `decide-capacity`, `explain-mechanism`, `judge-setting` |
| `knowledge` | The knowledge files the correct answer depends on. A list of knowledge ids. The retrieval check measures whether the harness finds them; every id must exist | Knowledge ids, e.g. `vsphere/technology/cpu/metrics/virtual-motherboard/wait` |

**How hard it is and how it is scored**

| Tag | Meaning | Values |
|---|---|---|
| `level` | Expertise level (`benchmark/design.md`, section 3.2) | `100`, `200`, `300`, `400` |
| `answer_type` | How the answer is scored (section 3.3) | `deterministic` (option letters, compared by the runner), `judged` (free text, scored 0-3 by the judge) |
| `answer` | The correct letters, as written in `## Prompt`. Deterministic only. Never sent to the candidate | Letters `A`-`H` |
| `trap` | The letters a Level 300 reader would pick. Deterministic only. Never sent to the candidate | Letters `A`-`H` |

**What the administrator gives besides the prompt**

| Tag | Meaning | Values |
|---|---|---|
| `input` | Input types (section 3.4). A list, derived from `attachments`; lint checks they agree | `text` (no attachment), `table`, `screenshot` |
| `attachments` | Files sent with the prompt, relative to `benchmark/questions/`. They live in `questions/<id>/`, next to the question file. No `.md` files there: the runner and lint read every `.md` under `questions/` as a question | Paths; `.png`, `.jpg`, `.webp` are screenshots; `.csv`, `.xlsx` are tables |

**Where it comes from**

| Tag | Meaning | Values |
|---|---|---|
| `origin` | Source of the question | `book` (the author's book), `quiz` (the author's quiz documents), `real-ticket` (a field question or support ticket), `synthetic` (drafted by Claude; counts only after author approval) |
| `source_path` | Where in the source, for QA: a heading path or the quiz question | Free text |

### Tags removed (2026-11-05)
One tag per concept (`project/terms.md`):
- `scope`: every question had `vsphere`. It is a knowledge-file tag (how general a fact is: vendor-neutral, vsphere, guest-os); for a question, `product` says the same and more.
- `area`: the main item of `technology`. Two tags for one concept; `technology` stays, as a list. The author's rule for `area: operations-management` (performance troubleshooting, capacity planning, rightsizing) is now `task`: troubleshoot or decide-capacity.
- `tests` (concept, distinction, judgment, troubleshooting): replaced by `task`, which matches the blueprint and avoids the word test (`project/terms.md`).
- `pillar`: on one question only. Performance against capacity is now in `task` (decide-capacity) and in the knowledge files the question links.
- `format`, old `level` values, old `input` values: replaced on 2026-11-05 by `answer_type`, levels 100-400 and `input` [text, table, screenshot].

## Deterministic scoring
- Runner: `benchmark/runner/run.py`. Commands and full methodology: `benchmark/runner/README.md`.
- Options are shuffled per run. One option is appended to every question: "Unsure". No "Not covered" option: knowledge base first, own knowledge where it is silent (author, Q038, 2026-11-05).
- Every question says there can be more than one correct option. The number of correct options is never revealed.
- Each question runs 5 times per model and mode.

| Answer | Class |
|---|---|
| Exactly the correct letters | Correct |
| Unsure, chosen alone | Unsure (not correct, not wrong) |
| Anything else: wrong, partly right, Unsure mixed with other letters, unparseable | Confident wrong |

- The model is told that a wrong answer is worse than Unsure. No points and no -1: see `benchmark/design.md`, section 7.1.
- Headline: **Stable correct**, the share of questions answered exactly right in all 5 runs. Target: at least 85%, aim 99% (author, 2026-11-03).
- Also reported: Luck (right in some runs only), confident-wrong rate, Unsure rate, accuracy when answered, trap rate, retrieval recall, tools used, verifier flags.
- Reason and design: `benchmark/design.md` (blueprint, why 100 questions, scoring, validity threats).

## Judged scoring (0-3)
- The runner sends the prompt (and images) without options, then a judge model scores the answer against `## Expected key points` and `## Likely wrong answer`.
- Rubric, judge rules and checks: `benchmark/design.md`, section 14. Judge model: `benchmark/models.md`.
- `## Expected key points` is the answer key for the judge: the facts a correct answer must state, one per bullet, as many as the question takes (most take 2-5); not the wording the candidate must use. Meaning and an example: `benchmark/design.md`, section 14.
- Write `## Likely wrong answer` in the words a user would use: the judge flags an answer that states it.

## Final score
- One score, 0-100%, with sub-scores by answer type, input type and level. Method: `benchmark/design.md`, section 7.4.

## results.csv columns

| Column | Example |
|---|---|
| date | 2026-11-03 |
| model | model id |
| effort | n/a for gateway models; medium / high / max where the model has an effort setting |
| mode | baseline, classic, agentic (`-vision` suffix for the screenshot track) |
| question_id | vsphere-cpu-004 |
| score | Benchmark runner: mean credit over the runs, 0-1 (exact letters 1 or 0; free text: judge score / 3). Older rows: exact-match mean, or manual 0-3. |
| notes | benchmark id and scale, e.g. "benchmark 20261105-090000; score = mean credit 0-1 (exact letters, or judge score / 3) over 5 runs; temp 0.2" |
