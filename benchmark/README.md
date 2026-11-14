# Benchmark

Question format and tags. Questions measure whether the knowledge base, harness and agent improve answers. Design and scoring: [design.md](design.md). Running it: [runner/README.md](runner/README.md).
Never index this folder: it contains answer keys.

## Layout

```text
benchmark/
├── questions/L<level>-<nn>-<slug>.md                 # one question per file, one flat folder
├── questions/<id>/                                   # the question's attachments: screenshots, logs, diagrams (only when it has any)
├── runner/                                       # Benchmark runner: run.py, run_all.py, preflight.py, health.py, summarize.py, judge.py, report.py, governor.py, config.yaml
├── models.md                                     # candidate models, frontier reference, judge
├── RUN.md                                        # how to run a benchmark round: the prompt, approvals, time, cost
├── live-test.md                                  # the system on an offline model: plan and pass criteria
├── results/README.md                             # one analysis of all runs of a round (written when the last run finishes)
├── results/<date>-<model>/                       # per run: answers.csv, report.md, config.json (traces.jsonl not in git)
└── _templates/question.md
```

- One flat folder: a question often crosses products (vSphere, Windows, Linux, NSX, VCF Operations) and technologies, so folders cannot hold it. The slices are metadata (section Metadata tags):
  - `product`: every product the question touches (values from [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml));
  - `technology`: every area it touches (cpu, memory, storage, network, system): [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.5.
- Counts of every tag over the run set: `python3 project/tools/coverage.py`. The set has no target size: it changes as questions are added, rewritten and retired ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3).
- File name: `L<level>-<nn>-<slug>.md`, numbered from 01 within each level, in id order. The last number of a level is its count.
- The id is a 4-digit running number in the metadata only (`id: "0007"`). It never changes and is never reused. The runner and the results use it; people do not need it. A new question takes the next free id, counting the archived questions too.
- A question that changes level: edit `level:`, then run `python3 project/tools/renumber_questions.py`. It renumbers the files so each level runs from 01 without gaps, and updates the question links in the documents listed in `DOCS` of [project/tools/link_refs.py](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/link_refs.py). The id, the results and the attachments stay.
- Attachments live in a folder named by the id: [benchmark/questions/0007](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/0007).
- In documents, link a question by its title: `[title](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/<file>)`.
- Scope of questions: performance monitoring and troubleshooting, and the capacity view that supports it, on vSphere 9.1 and the Guest OS layer. Cost and price questions are out of scope.
- One file per question: scales to hundreds of questions, one diff per question, attachments per question.
- Ids never change and are never reused. A retired question gets `status: retired`, a note with the reason, and moves to [project/archive/benchmark-questions](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-questions). A question is deleted only when the author asks.
- Deleted on author request: `vendor-neutral-general-001` (hyperscaler VM cost; out of scope, Q039).

## Question fields
- Each question file: `# Title`, then `## Prompt`, `## Attachments` (when the question has any), `## Likely wrong answer`, `## Expected key points`, and a `## Metadata` section at the end with one yaml block. No front matter at the top.
- `## Prompt` layout, for the human reviewer: context facts as bullets, one fact per bullet; the question or instruction as its own paragraph; options as a bullet list, `- A. text`. The candidate gets the same text: the runner rebuilds the option list (shuffled, `A. text` per line), and a model reads bullets as well as prose. Consecutive `A. text` lines without bullets render on GitHub as one paragraph.
- `## Input to supply` (only while `status: awaiting-input`): what the author captures or exports, exactly enough for the answer key to hold. Removed when the file is added.
- In `## Prompt`, the words that refer to an attachment link to it: `[the attached chart export](0123/vm-cpu.csv)`. A reviewer clicks through on GitHub (a CSV renders as a table). The runner sends the words only, not the path, so the link costs no tokens. Lint checks that every attachment is linked and every link is an attachment ([design.md](design.md), section 6.3).
- `## Attachments` (optional) shows an image inline with alt text, for the reviewer. It is never sent to the model: the runner sends the files listed in `attachments`, images as images and CSV files as text after the prompt.
- Only `## Prompt` (plus attachments) is ever sent to the AI.
- Fairness: the title, prompt, likely wrong answer and key points use public vocabulary only: no Agent E2 terms, no vCommunity management pack metrics ([design.md](design.md), section 6.1; lint list `question_fairness`).

### Metadata tags
The tags in each question's `## Metadata` block, grouped by what they describe. Values are the complete set; lint rejects any other.

**Identity**

| Tag | Meaning | Values |
|---|---|---|
| `id` | Internal key for the runner and the results. 4-digit number, quoted. Never changed, never reused. Not in the file name | `"0007"` |
| `title` | Short name for a human reviewer | Free text |
| `status` | Review state | `draft` (written, not reviewed), `awaiting-input` (the screenshot or table is not supplied yet: the `## Input to supply` section describes it; not run), `reviewed` (author approved), `deferred` (kept for a later release, not run), `retired` (archived, not run) |

**What the question is about**

| Tag | Meaning | Values |
|---|---|---|
| `product` | Every product the question touches. A list | `vsphere`, `vsan`, `nsx`, `vcf-operations`, `windows`, `linux`, `kubernetes` |
| `technology` | Every technology area the question touches. A list. The per-area report counts each one | `cpu`, `memory`, `storage`, `network`, `system` (the object as a whole: KPIs, capacity, availability, DRS, provider/consumer, rollups) |
| `task` | What the administrator is trying to do: one of the five tasks ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.1) | `read-metric`, `troubleshoot`, `decide-capacity`, `explain-mechanism`, `judge-setting` |
| `knowledge` | The knowledge files the correct answer depends on. A list of knowledge ids. The retrieval check measures whether the harness finds them; every id must exist | Knowledge ids, e.g. [VM CPU Wait](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/wait.md) |
| `object` | Every object type the question reads. A list. Counted by `coverage.py` ([design.md](design.md), section 3.7) | `vm`, `esxi`, `cluster`, `resource-pool`, `datastore`, `network`, `guest-os` |
| `tool` | Every tool whose output the question shows or asks about. A list | `vcenter`, `vcf-operations`, `esxtop`, `guest-os-tools` (Windows or Linux counters), `none` |
| `knowledge_main` | The one file that holds the answer or the misconception. Also listed in `knowledge` (lint checks it). Not the list order. The retrieval check reports a missing main file as a defect ([retrieval-check.md](retrieval-check.md)). Set by the author in the question review (Q130) | One knowledge id |

**How hard it is and how it is scored**

| Tag | Meaning | Values |
|---|---|---|
| `level` | Expertise level ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.2) | `100`, `200`, `300`, `400` |
| `answer_type` | How the answer is scored (section 3.3). Every question of the run set is `deterministic` since 2026-11-14 (Q199) | `deterministic` (option letters, compared by the runner), `judged` (free text, scored 0-3 by the judge) |
| `answer` | The correct letters, as written in `## Prompt`: one, several or all. Deterministic only. Never sent to the candidate | Letters `A`-`Y` (no fixed option count; Unsure is appended by the runner) |
| `misconception` | The letters a Level 300 reader would pick. Deterministic only. Never sent to the candidate | Letters `A`-`Y` |
| `misconception_type` | The misconception types the question tests, from `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400. A list; may be empty at Level 100-200 | Values in [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml), `misconception_type` |

**What the administrator gives besides the prompt**

| Tag | Meaning | Values |
|---|---|---|
| `input` | Input types (section 3.4). A list, derived from `attachments`; lint checks they agree | `text` (no attachment), `table`, `screenshot` |
| `attachments` | Files sent with the prompt, relative to [benchmark/questions](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions). They live in `questions/<id>/`, next to the question file. No `.md` files there: the runner and lint read every `.md` under `questions/` as a question | Paths; `.png`, `.jpg`, `.webp` are screenshots; `.csv` are tables (1.0: at most about 3,000 tokens, [design.md](design.md), section 13.1) |

**Where it comes from**

| Tag | Meaning | Values |
|---|---|---|
| `origin` | Source of the question | `book` (the author's book and samples), `quiz` (the author's quiz documents), `real-ticket` (a field question, support ticket or real exchange), `synthetic` (drafted by Claude; counts only after author approval) |
| `source_path` | Where in the source, for QA: a heading path or the quiz question | Free text |

### Tags removed (2026-11-05)
One tag per concept ([project/terms.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/terms.md)):
- `scope`: every question had `vsphere`. It is a knowledge-file tag (how general a fact is: vendor-neutral, vsphere, guest-os); for a question, `product` says the same and more.
- `area`: the main item of `technology`. Two tags for one concept; `technology` stays, as a list. The author's rule for `area: operations-management` (performance troubleshooting, capacity planning, rightsizing) is now `task`: troubleshoot or decide-capacity.
- `tests` (concept, distinction, judgment, troubleshooting): replaced by `task`, which names the administrator's job and avoids the word test ([project/terms.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/terms.md)).
- `pillar`: on one question only. Performance against capacity is now in `task` (decide-capacity) and in the knowledge files the question links.
- `format`, old `level` values, old `input` values: replaced on 2026-11-05 by `answer_type`, levels 100-400 and `input` [text, table, screenshot].

## Scoring
- Classes, Stable correct, the 0-3 judge rubric and the final score: `design.md`, sections 7 and 14. Runner details: `runner/README.md`, section Methodology.
- Writing the answer key of a multiple-choice question: `## Expected key points` starts with `- Answer: <letters>.`, then one bullet per option with the reason it is true or false (for reviewers; never sent to a model). Options: as many as the question needs, one fact each, similar in length; the false ones wrong for a reason the knowledge base states ([design.md](design.md), sections 3.8 and 6.2).
- Writing the answer key of a judged question (none in the run set since 2026-11-14):
  - `## Expected key points` is the judge's answer key: the facts a correct answer must state, one per bullet, as many as the question takes; not the wording the candidate must use;
  - write `## Likely wrong answer` in the words a user would use: the judge flags an answer that states it.

