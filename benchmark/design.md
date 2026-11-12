# Benchmark design

For human experts who check that the benchmark is valid and complete. Not indexed.
Runner and commands: [benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md). Question format: [benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md). Models and judge: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md). Misconception definition: `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400.

## 1. Claim
- Claim: a local open-weight model on one GPU ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)), with this harness and knowledge base, answers Level 400 vSphere operations questions better than the best frontier model without them.
- System under test: model + agent + harness + knowledge base. The model is frozen; the benchmark does not test it for its own sake (`MISSION.md`, section 2). It measures:
  - which frozen model to ship;
  - the score delta of each change to the knowledge base, harness or agent, with everything else fixed;
  - the gap to the frontier model.
- Baseline mode (the model alone) is the zero point: system minus baseline is what our work adds.
- Release gate: section 7.5 (final score at least 85%, Level 400 at least 80%, confident-wrong at most 3%, at least 15 points over the frontier model). Target: 99%. Final score: section 7.4.
- The benchmark must:
  1. rank candidate models and answer modes against each other;
  2. show whether a configuration clears the release gate (section 7.5);
  3. show how close it is to 99%, and state what the number proves.

## 2. Scope
| Measured | Not measured (and where it is measured instead) |
|---|---|
| Correct reading of metrics: mechanism, vantage point, unit, rollup | Installation, configuration steps, UI navigation (out of scope for the product) |
| Resistance to misconceptions (see `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400) | Writing style of judged answers (the judge scores facts only, section 14) |
| Combining several facts, tables and screenshots in one answer, including arithmetic | Speed and cost (logged per answer, judged separately) |
| Following a troubleshooting flow to a conclusion | Live-system troubleshooting (after 1.0) |
| Reading one or more screenshots (esxtop, vCenter UI, VCF Operations UI) and tables (spreadsheet exports) | Multi-turn conversation with clarifying questions (a separate set, later) |
| Knowing the limits: choosing Unsure instead of guessing | Cost and price (out of scope, author 2026-11-04) |
| Consistency: the same answer on every run | |
| Answering without options (free text, judged) | |

- Answer types and their reasons: section 3.3.

## 3. Blueprint
The 100 questions are designed top down, not collected bottom up. Section 3.1 states the job. Sections 3.2 to 3.5 are four independent axes. Section 3.6 allocates the 100 questions across them. Each question is then written to fill one cell, from the author's book and quizzes first.

### 3.1 The job
The product is a narrow expert for one reader: a VMware administrator. The administrator brings one of five tasks, with text, a table or screenshots as evidence.

| Task | What the administrator asks | Share of 100 |
|---|---|---|
| Read a metric | What does this value mean on this object, and is it a problem? | 30 |
| Troubleshoot | Something is slow. What do I check, in what order, and what is the cause? | 25 |
| Decide capacity | Is there room? How big should this Guest OS be? What can I reclaim? | 20 |
| Explain a mechanism | Why does the counter behave this way? | 15 |
| Judge a setting | What does this setting do to performance or capacity? | 10 |

- The shares follow what administrators ask most: reading and troubleshooting. Capacity covers sizing and rightsizing (`sp5-framework/capacity/`).
- Each task maps to a `retriever_guide` value of the knowledge base: metric-meaning, health-check, troubleshooting, how-it-works, what-to-set. Capacity decisions use metric-meaning and health-check.

### 3.2 By level
Levels follow `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400.

| Level | The expert can | Share of 100 | Example |
|---|---|---|---|
| 100 | Name and recognise: which counter, which object, which tool | 10 | Which vCenter counter shows the time a vCPU was ready to run but waited for a physical CPU? A. Ready B. Co-stop C. Wait D. Latency |
| 200 | Define and explain one item in isolation | 15 | What does VM CPU Co-stop measure, and why does it apply only to VMs with more than one vCPU? |
| 300 | Apply common practice correctly: read a value, convert a unit, apply a published threshold | 25 | A 4-vCPU VM shows cpu.ready.summation = 8,000 ms in one 20-second real-time sample. What is its Ready per vCPU, in %? |
| 400 | Explain the mechanism, know when a reading misleads, and combine several facts, tables or screenshots to a conclusion | 50 | [VM (virtual motherboard) vs Guest OS metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-08-vm-is-a-virtual-motherboard.md): a slow Windows VM, six Guest OS and VM counters from VCF Operations; which statements hold, and why the two layers disagree |

- Level 400 is hard and complex, not tricky. It tests knowledge of the system, not reading of English. To stay unambiguous it is often long: the situation, the values, the tool, the time window, and one clear question.
- Level 400 combines facts inside one answer: several knowledge files, a calculation, a flow, several inputs. There is no back-and-forth with the user; the agent does the chaining with its tool calls. (This replaces the earlier "multi-hop" level.)
- Why Level 100-300 are in the benchmark, when the claim is about Level 400:
  1. The knowledge base assumes the basics and does not teach them ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 1). A candidate that fails Level 100-200 cannot read the knowledge base. A Level 400 failure is then a model failure, not a knowledge gap.
  2. Administrators ask basic questions too. One wrong basic answer costs the product its credibility.
  3. Non-regression: the knowledge base corrects Level 300 rules of thumb. The candidate must not over-correct a practice that is right (a correct unit conversion, a published threshold that does apply).
  4. Diagnosis: the frontier model is expected to be near perfect at Level 100-300 and to lose points at Level 400. The per-level sub-score shows where a candidate stands, and whether the knowledge base helps at Level 400 without hurting below it.
- Level 100-200 questions are short and mostly deterministic. Level 400 carries most of the judged questions and most of the tables and screenshots (section 3.6).

### 3.3 By answer type
Two answer types, by how the answer is scored.

| Answer type | The answer is | Scored by | Share of 100 |
|---|---|---|---|
| Deterministic | One or more option letters (A, B, C, ...). Exactly right or not | The runner, by comparing letters | 70 |
| Judged | Free text. It cannot be scored as right or wrong by a rule | A judge model, 0-3 against the key points (section 14). The judge is not fully reliable either | 30 |

- Deterministic is the bulk: it is exact, cheap, and free of scorer bias.
- Judged is kept because a real administrator asks without options. A model can pick the right option yet fail to raise the point unprompted.
- Example, deterministic ([CPU reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-05-cpu-reservation-behaviour.md)): "Choose all the correct statements" about CPU reservation, options A to G. Key: A, B, C, D. Any other set of letters is wrong.
- Example, judged ([High CPU Wait](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-01-cpu-wait-includes-idle.md)): "A VM shows CPU Wait at 90%. The application owner says the VM must be stuck waiting on disk or memory. Are they right?" Key points: Wait includes idle time; 90% Wait on a quiet VM is normal; check Ready, Co-stop and the Guest OS before blaming storage. The judge scores 3 when the answer says all of that, 0 when it agrees with the owner.
- A question with several parts, each with letters ([ESXi CPU capacity: threads, not hertz](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-05-esxi-cpu-capacity-threads-not-hertz.md): one answer per host), is judged today. Proposal: split it into one deterministic question per part.
- Metadata: `answer_type: deterministic | judged`.

### 3.4 By input type
Three input types: what the administrator gives the product besides the question.

| Input type | What it is | How it reaches the model | Share of 100 (questions that include it) |
|---|---|---|---|
| Text | The prompt alone. It may hold a few values or a small table typed into the prompt | As text | 60 (text only) |
| Table | A data file: typically a Microsoft Excel spreadsheet exported from VCF Operations or vCenter, or a CSV. Dozens of columns, hundreds of rows | The agent or harness converts it to CSV and gives the model a table tool to filter, sort and aggregate it: hundreds of rows do not fit or read reliably in the context | at least 15 |
| Screenshot | An image of a product UI, as the administrator sees it: esxtop, the vCenter UI, the VCF Operations UI. An image of anything else (a quiz table, a vendor web page) is not a screenshot: its content goes into the prompt as text | As an image, to a vision model | at least 25 |

- Administrators upload data in bulk: a spreadsheet of every VM, or several screenshots of one problem.
- A question can combine input types. A Level 400 question may carry several tables and screenshots. It counts for each input type it includes.
- Every question has a prompt, so every question has text. Text as an input type means the prompt alone.
- Metadata: `input: [text]`, `[table]`, `[screenshot]` or `[table, screenshot]`, derived from `attachments` and checked by lint.
- Not built yet: the table tool in the harness and table attachments in the runner (section 13.1).
- URL questions: a question that carries a link to a public page with a known Level 300 error (vendor KB, documentation, blog). The key point is that the answer corrects the page with the mechanism, not that it summarizes it. A frontier model tends to agree with the page; this question type shows the mission directly. The page is fetched live, so the key also records the page's date; a changed page is re-checked before scoring. Pages: the author's list ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M2).
- Examples:
  - Text: [Memory usage: VM vs ESXi](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-09-usage-vm-vs-esxi.md): every VM shows Memory Usage below 25% and the host shows 95%; the customer wants more RAM.
  - Table (to write): a VCF Operations export of 400 VMs with CPU Ready, Co-stop, Run, vCPU count and host; "which VMs suffer contention, and is it the host or the VM size?".
  - Screenshot: [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md): a vCenter chart of Usage, Core Utilization and Utilization.
  - Table and screenshot (to write): an esxtop screenshot of one host and a spreadsheet of its VMs; "which VM causes the Co-stop on the others?".

### 3.5 By area

| Area | Share of the 100 questions | Covers |
|---|---|---|
| CPU | 25% | vCPU states, Ready, Co-stop, Usage vs Utilization, Hyper-Threading, frequency, NUMA |
| Memory | 25% | Consumed, Active, balloon, swap, compression, Latency, tiering |
| Storage | 20% | latency stack, layers, outstanding IO, space, IP storage |
| Network | 15% | drops, throughput, units, offload |
| System | 20% | the object as a whole: KPIs, capacity, availability, DRS, admission control, provider/consumer, statistics and rollups, GPU, Guest OS vs VM boundary |

- The shares add up to more than 100% because a question can span several areas. A question on VM CPU Ready caused by host memory swapping counts for CPU and Memory.
- Each question lists every area it touches (`technology` in its metadata, values from [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml)). The share is the minimum number of questions that touch the area.
- About 5 questions sit outside the knowledge base. The system answers them from the model's own knowledge (knowledge base first, own knowledge where it is silent: author, Q038, 2026-11-05). They check that a gap does not turn into a wrong answer.
- Per-area scores (15-25 questions) are diagnostic only (margin about ±15-20 points). Decisions use the total.

### 3.6 Allocation
Level against answer type:

| Level | Deterministic | Judged | Total |
|---|---|---|---|
| 100 | 10 | 0 | 10 |
| 200 | 12 | 3 | 15 |
| 300 | 20 | 5 | 25 |
| 400 | 28 | 22 | 50 |
| Total | 70 | 30 | 100 |

Level against input type (questions that include it):

| Level | Text only | Table | Screenshot |
|---|---|---|---|
| 100 | 8 | 0 | 2 |
| 200 | 11 | 1 | 3 |
| 300 | 17 | 4 | 5 |
| 400 | 24 | 10 | 15 |
| Total | 60 | at least 15 | at least 25 |

- Judged questions sit mostly at Level 400: that is where troubleshooting is open-ended, as it is for a real administrator.
- Tables and screenshots sit mostly at Level 400: reading evidence and combining it is the expert's work. At least 5 Level 400 questions combine a table and a screenshot.
- The 5 tasks (section 3.1) and 5 areas (section 3.5) are spread across every row.
- Decided by the author (Q054, 2026-11-05).

### 3.7 Coverage constraints
| Constraint | Minimum |
|---|---|
| Each misconception type in `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400 (12 types) | 3 questions each |
| Same-name pairs: one label asked on two objects (VM vs ESXi, ESXi vs cluster) | 5 pairs |
| Questions about the VM / ESXi / cluster / datastore | 30 / 20 / 10 / 5 |
| Questions outside the knowledge base (answered from the model's own knowledge) | 5 |
| Questions where the knowledge base and the vSphere documentation disagree | 3 |
| Questions needing the calculator (summation to %, units, capacity) | 5 |
| Questions that follow a troubleshooting flow (a `troubleshooting/` file) in order | 10 |
| Screenshot questions per source: esxtop, vCenter UI, VCF Operations UI | 5 each |
| Table questions with at least 100 rows | 5 |
| Long, complex questions: many screenshots and tables, many key points, as close as one prompt gets to a long troubleshooting discussion | 1 |

- Every question records what it covers in its metadata (`task`, `level`, `answer_type`, `input`, `technology`, `knowledge`; `misconception_type` to be added; tags: [benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md), section Metadata tags), so coverage is counted by a script, not by eye.

### 3.8 Answer-key shape (deterministic)
- Options: 4-8 written options, plus Unsure appended to every question. No Not covered option since 2026-11-05 (Q038).
- The number of correct options varies: about 30% of questions have 1 correct option, 50% have 2-3, 20% have 4 or more. The model is never told how many.
- A model that learns "usually one answer" or "usually all but one" gains nothing.

## 4. Sample size
The headline score is a share of questions. Its precision depends on the number of questions. More runs remove run-to-run noise; they do not remove the luck of which questions were picked.

| Questions | 95% margin at 85% | 1 question is worth | Lower bound if all correct (Wilson 95%) | Lower bound with 1 wrong | Author time to write and verify keys |
|---|---|---|---|---|---|
| 50 | ±9.9 points | 2 points | 92.9% | 89.5% | 0.5x |
| **100** | **±7.0 points** | **1 point** | **96.3%** | **94.6%** | **1x** |
| 150 | ±5.7 points | 0.67 points | 97.5% | 96.3% | 1.5x |
| 200 | ±4.9 points | 0.5 points | 98.1% | 97.2% | 2x |
| 300 | ±4.0 points | 0.33 points | 98.7% | 98.1% | 3x |

- 50 is too few:
  - the 85% gate cannot be read: a true 80% model and a true 90% model overlap;
  - 99% cannot even be expressed: one wrong answer is 98%.
- 100 is the smallest set that:
  - reads the 85% gate with a margin of about ±7 points;
  - separates candidate models whose scores differ by more than about 10 points (paired, question by question, the separation is better than the margin suggests);
  - gives a clean reading: one question is one point, so 99% means exactly one miss.
- 150 adds little: margin improves from ±7.0 to ±5.7 points (precision grows with the square root of the count) for 50% more author time. Author time is the constraint: every key is checked by hand.
- 100 cannot prove 99%. Even a perfect score only shows at least 96.3% with 95% confidence. Proving 99% needs about 300 questions with no wrong answer (rule of three: 0 misses in 300 → error rate below 1%).
- Plan:
  - 100 questions: model and mode selection, the 85% gate, and tracking progress. Version 1.0.
  - 300 questions: the 99% claim for release, built over later releases from book quizzes, real tickets and held-out questions.

## 5. Set design
The set must measure one thing (Level 400 operations knowledge) evenly, so the total has meaning.
- Coverage: the blueprint (section 3) makes every area, object, layer and misconception type count. No area can carry the score alone.
- Balance of difficulty: Level 100-200 questions anchor the scale. If they fail, the problem is the model's basics or retrieval, and Level 400 failures are not interpreted (section 3.2).
- Paired questions: the same concept on two objects. A model that answers both right understands the vantage point; one that answers one right was lucky or pattern-matched.
- Independence: no question gives away another's answer. No two questions test the same single fact.
- Every option is decidable from the knowledge base (or, for questions outside it, from established vSphere knowledge the author confirms). A question the knowledge base cannot settle is rewritten or removed, never kept as a coin flip.

## 6. Question writing
- Stem: a realistic situation with the values an operator would see (counter names, numbers, units, time window). Not a definition prompt, except at Level 100-200.
- Options:
  - one fact per option;
  - similar length and style, so length gives no hint;
  - no "all of the above", no double negatives;
  - every wrong option is wrong for a reason the knowledge base states;
  - one option is the misconception: the conclusion a Level 300 reader would draw. It is named in `## Likely wrong answer`.
- Wording: paraphrased, never copied from the knowledge base. The benchmark checks reasoning, not string matching.
- Key: `answer` letters, and `## Expected key points` with the reason for every option and the knowledge file ids.
- Sources: the author's books and quizzes first; then real tickets and field questions; then synthetic questions drafted by Claude. A synthetic question needs the author's approval before it counts.

## 7. Scoring
- Answer format fixed: `ANSWER: <letters>` then `REASON: <one line>`. An unparseable answer scores as wrong.
- Option order shuffled per run; letters mapped back before scoring. Removes position bias.
- Each answer falls in one of three classes:

| Answer | Class | Counts toward |
|---|---|---|
| Exactly the correct letters | Correct | Stable correct (if correct in all 5 runs) |
| Unsure, chosen alone | Unsure | Not correct; not counted as wrong |
| Anything else: wrong, partly right, Unsure mixed with other letters, unparseable | Confident wrong | Confident-wrong rate |

- Two numbers are reported for deterministic questions: **Stable correct** (absolute, against the fixed set; it is the deterministic question credit in the final score, section 7.4) and **confident-wrong rate** (share of answers that are wrong and not Unsure; target near 0).
- The model is told: a wrong answer is worse than Unsure, because an operator would act on it; if it cannot decide every option, choose Unsure.

### 7.1 No points, no -1
- An earlier version scored +1 / 0 / -1 and reported "Net points". It was dropped:
  - The benchmark is an absolute measurement against a fixed question set, not a ranking against other benchmarks. Stable correct already counts only exact answers; a wrong answer and an Unsure both count as not correct, so the -1 never changed the headline.
  - Net points mixed two things an operator cares about separately: how often the system is right, and how often it is confidently wrong. Two plain shares say both without arithmetic.
- In practice the -1 changed the model's behaviour through the prompt: told that a wrong answer costs a point, models chose Unsure instead of guessing. That behaviour is kept with a plain rule in the prompt ("a wrong answer is worse than Unsure").
- Unsure applies to an AI too. An operator acts on the answer without checking it elsewhere, so "the knowledge base does not settle this" is the safe answer.
- Unsure means the sources do not decide the question. This can be checked against the cited files.
- Check after the next benchmark: if models guess more under the plain rule (confident-wrong rate rises, Unsure rate falls), put the scoring sentence back in the prompt only. Grading stays as above either way.

### 7.2 Five runs
- Hosted models do not answer the same way twice, even at the same temperature: sampling, batching on shared GPUs, provider routing, silent serving updates.
- A question counts as known (Stable correct) only when all 5 runs are exactly right. Right in some runs only = Luck, counted as not known.
- Chance of passing all runs, by per-run probability of being right:

| Runs | Pure guess (50%) | 80% | 90% | 95% | 99% |
|---|---|---|---|---|---|
| 3 | 12.5% | 51% | 73% | 86% | 97% |
| **5** | **3.1%** | **33%** | **59%** | **77%** | **95%** |
| 10 | 0.1% | 11% | 35% | 60% | 90% |

- 3 runs let a coin-flip question pass 1 time in 8.
- 5 runs cut that to 1 in 32, and still reward a model that is right 99% of the time (95% pass).
- 10 runs double the cost for little gain, and penalize a good model (99% per run passes only 90%).

### 7.3 Secondary measures
| Measure | Why |
|---|---|
| Luck | How much of a model's score is unstable. |
| Confident-wrong rate | Answers that would mislead an operator. |
| Unsure rate, accuracy when answered | A cautious model with gaps vs a reckless one. |
| Misconception rate | How often the misconception option is picked. The core Level 400 signal. |
| Not-covered accuracy | Guessing outside the knowledge base. |
| Retrieval recall | Whether the right files were found; separates retrieval from reasoning. |
| Tools used, verifier flags | Whether the harness tools were used (agentic mode). |
| Per area, per level | Diagnosis only (small counts). |

### 7.4 Final score
- One number, 0-100%, for each model and mode. Sub-scores support it: by answer type (deterministic, judged), by input type (text, table, screenshot), by level (100-400).
- Question credit, 0 to 1, taken from the worst of the 5 runs:
  - deterministic: 1 if the letters are exactly right in every run, else 0 (Stable correct);
  - judged: the lowest judge score over the runs, divided by 3 (0, 0.33, 0.67, 1).
- Final score = sum of question credits / number of questions. Every question weighs the same, whatever its level, answer type or input type.
- Sub-score = the same mean within one group. A question counts for every input type it includes. The allocation (section 3.6) sets how much each group weighs in the final score.
- Screenshot questions are scored with their images. There is no text-only track: every candidate reads images ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)).
- Reasons:
  - worst run, not mean: the same rule as Stable correct. An answer right in 4 runs of 5 is luck, and an operator gets one run;
  - one weight per question: no group can carry the score by a formula choice; the blueprint decides the mix;
  - judge score / 3: a partly right judged answer (right conclusion, missing reason) earns part credit, as a human examiner would give. A deterministic answer has no part credit, because a partly right set of letters is a wrong answer an operator would act on.
- Confident-wrong rate covers both: wrong letters that are not Unsure, and judged answers scored 0 that do not say the information does not settle it.
- Margin: 95% interval on the final score from the number of questions (section 4). Sub-scores have wider margins (20 questions: about ±16 points) and are diagnostic.
- Runner: [benchmark/runner/report.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/report.py), function `final`. Report table `Final score`.

### 7.5 Release gate
- Read on Agent E2 as shipped: the local model in agentic mode, with the deployment profile (section 8). Classic mode is the floor and the fallback; it carries the retrieval levels (section 9).
- All must hold. One number alone can be carried by easy questions or bought with confident guesses.

| Gate | Limit | Why |
|---|---|---|
| Final score, development set (100) | at least 85% | Margin ±7 at 100 questions (section 4); below 85 an operator stops trusting the answers |
| Level 400 sub-score | at least 80% | About 50 questions (margin about ±10): the one sub-score that gates. The mission is Level 400; Level 100-300 can carry the total |
| Confident-wrong rate | at most 3% | The answers an operator acts on. A wrong answer marked Unsure is not one of them |
| Misconceptions of [knowledge/misconceptions.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/misconceptions.md) | none stated as true | They are given up front; stating one is a harness or model defect, not a gap. Author check of the answers |
| Held-out set (section 10) | within 5 points of the development set | A larger drop means the knowledge base or retrieval is fitted to the visible questions |
| Gap to the frontier model (section 8) | at least 15 points, paired test significant | The claim of section 1 |

- Effective bar: Agent E2 at least the larger of 85% and frontier + 15.
- Why 85%, not 90%: at 100 questions 85 and 90 overlap inside the margin; the confident-wrong limit does more for the operator than 5 more points.
- Why 15 points: 10 points equals the margin and has 68% paired power at 100 questions (one benchmark in three would miss a real win); 15 points has 91% ([project/review-2026-11-11.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-11.md), section 5). With the frontier model near 72%, a 10-point win could land below 85%: the claim would rest on a configuration not fit to ship.
- Expected frontier score (expert estimate, 2026-11-12; replaced by the first M4 benchmark): about 65%, range 60-72%.

| Level | Share | Frontier expected | Why |
|---|---|---|---|
| 100 | 10 | about 95% | Public counter names |
| 200 | 15 | about 90% | Public definitions; exact multi-select costs a few |
| 300 | 25 | about 80% | Public practice, but some published thresholds are the ones the knowledge base corrects |
| 400, public mechanism | about 30 | about 60% | Knows each mechanism alone; misses the vantage point and the combination of readings, and picks the Level 300 rule of thumb. Web search returns the same Level 300 pages |
| 400, author framework and current VCF Operations | about 20 | about 25% | Not in public text, or wrong there |

- So in the expected case the 85% gate binds; the 15-point gap binds when the frontier model scores above 70%.
- No sealed set and no `knowledge_class` tag (Q165, closed 2026-11-12: questions need not come from real tickets). The gap is read on the development set and confirmed on the held-out set.
- Ceiling, not a gate: the frontier model in agentic mode with the knowledge base. Agent E2 within 5 points of it shows the local model is not the bottleneck. If the frontier model scores lower with the knowledge base than without, the knowledge base or the harness misleads a strong model: fixed before any gap is read.
- Target: 99%, a direction. 100 questions cannot prove it (section 4).
- Runner: [benchmark/runner/report.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/report.py), functions `gate` and `mcnemar`, report table `Release gate`: final score, Level 400, confident-wrong, gap and paired test. The misconception check and the held-out set are read outside the report.

## 8. Comparison design
- Reasons for running both modes and for the call limit: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), sections 8 and 9.
- The release score uses the deployment profile of the harness: same prompt, tools, context window and budgets as the product. Time is replaced by a turn limit derived from the target GPU. Other settings run only as named experiments. See [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 8, Benchmark and deployment.
- Every model runs in three modes on the same questions: baseline (no knowledge base), classic (one lookup), agentic (model-driven lookups). See [benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md).
- Reference: the frontier model in baseline mode: Claude Opus 5.5, web search on, effort capped at medium, no knowledge base (Q164). The claim in section 1 is met when Agent E2 exceeds it by at least 15 points and a one-sided exact McNemar test on the questions is significant at α 0.05 (section 7.5).
- Paired comparison: models are compared question by question on the same set, not only by totals.
- Between candidate models, a gap smaller than the margin is a tie; the smaller model wins a tie. Against the frontier model, a gap below 15 points does not support the claim.
- Run matrix at 100 questions: 10 models x 3 modes x 100 questions x 5 runs = 15,000 answers, about US$ 25-40 and 2-4 hours (re-check prices and rate limits before each run).

## 9. Retrieval check
- The final score mixes harness and model. The retrieval check separates them: [benchmark/runner/retrieval_eval.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/retrieval_eval.py) checks, without a model, whether each question's `knowledge` files are found and placed in the classic context. Guide: [benchmark/retrieval-check.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/retrieval-check.md).
- Result 2026-11-06 (90 questions), before the retrieval fixes: keyword search 70-71% of needed files reach the classic context, hybrid 72%; all needed files in 51 of 90 questions. After `expand_derive` and `route_troubleshooting`: keyword 73% (53 of 90), hybrid 75% (57 of 90). This caps classic mode. Improve it before judging the model ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M3). Earlier: 2026-11-04, 28 questions, hybrid 67%, 12 of 28 complete.
- Every wrong answer is classified: file not in context (harness or knowledge), file in context but answer wrong (model or prompt), file not in the knowledge base (gap). Detail: `ARCHITECTURE.md`, section 6.

## 10. Validity threats
| Threat | Guard |
|---|---|
| Wrong answer key | Every wrong answer from the best model is checked by the author: model error, knowledge gap, or key error. Keys cite knowledge ids. |
| Knowledge base fitted to the benchmark (Claude edits the knowledge base and can read the questions) | A held-out set of about 20% of the questions, kept by the author outside the repository and run only before releases. Fixes to the knowledge base must be general (a fact or a misconception), never a question-specific answer. |
| Questions written by the knowledge base's own author favour its wording | Paraphrased stems; questions from real tickets and field forums; frontier baseline as an outside reference. |
| Synthetic questions drafted by Claude mirror Claude's view | The author reviews every question one by one; no cap on the share. What matters is the allocation and distribution. |
| Ambiguous options | A question with a disputed option is fixed or removed, and the benchmark is re-scored. |
| Position, length and count bias | Shuffled options; similar option length; varied number of correct options. |
| Guessing | Unsure option, the prompt rule that a wrong answer is worse than Unsure, confident-wrong rate, 5-run stability. |
| Leakage into the model | Questions are never indexed, never used for fine-tuning, and `## Expected key points` is never sent to the model. |
| Frontier model knows public material | Baseline tests exactly that. The knowledge base must add what public material lacks. |
| Version drift | Every benchmark records the index version (git commit), model, provider and settings. Scores are compared only within one scoring scheme. |

## 11. Review checklist
For each question:
1. Is the situation realistic for an operator of vSphere 9.1?
2. Is every option decidable from the cited knowledge files, and is the key right?
3. Is the misconception option a mistake a competent Level 300 operator would plausibly make?
4. Does any option give the answer away by wording, length or count?
5. Does it duplicate another question's fact?
6. Does it test operations knowledge, not trivia (UI clicks, product history, prices)?

For the set:
7. Do the counts match the blueprint in section 3?
8. Is every misconception type covered at least 3 times?
9. Are at least 20% of questions from sources other than the author's books?

## 12. Status (2026-11-05)
- 90 questions: 10 at Level 100, 14 at Level 200, 16 at Level 300, 50 at Level 400 ([Where the storage latency sits in esxtop](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-16-esxtop-disk-device-where-is-latency.md) moved to Level 300 by the author). 59 deterministic, 31 judged. 59 text only, 19 screenshot, 7 table, 5 table + screenshot.
- Level 400 (50): the 37 new ones (L4-14 to L4-49) are 20 deterministic and 17 judged; 13 text, 13 screenshot (esxtop 5, vCenter 4, VCF Operations 4), 6 table, 5 table + screenshot. [ERP slow after the change window](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-49-erp-slow-after-change-window.md) is the long, complex question.
- 24 are `awaiting-input`: the author supplies the screenshot or table described in each question's `## Input to supply` (L4-26 to L4-48). Supplied 2026-11-05: [Latency counters in a vCenter virtual disk chart](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L1-06-vcenter-virtual-disk-latency-counters.md), [Recognise the tool and the object](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L1-09-recognise-vcf-operations-vm-metrics.md), [Contention counters in a vCenter host network chart](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L2-04-vcenter-host-network-contention-counters.md), [Is the datastore full: provisioned vs used space](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L2-08-datastore-provisioned-vs-used.md), [Where the storage latency sits in esxtop](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-16-esxtop-disk-device-where-is-latency.md), [Guest OS metrics in the VM metric tree](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L2-12-vcf-operations-guest-vs-vm-metrics.md).
- Tasks: read-metric 32, troubleshoot 23, decide-capacity 15, explain-mechanism 12, judge-setting 8.
- Technology (a question can carry several): cpu 26, system 26, storage 22, memory 21, network 15.
- Origin: 63 synthetic (drafted by Claude), 17 quiz, 10 book. No cap on the synthetic share: the author reviews every question (Q058).
- Remaining: 1 question at Level 200 and 9 at Level 300. Fill the tasks below allocation first: decide-capacity, troubleshoot, judge-setting, explain-mechanism; no more read-metric.
- Next: `misconception_type` per question; a coverage script that prints these counts; the held-out set.

## 13. Screenshot questions
- Purpose: administrators upload screenshots and ask the agent to explain the problem. Often several at once, from different tools: esxtop, the vCenter UI, the VCF Operations UI.
- Reading screenshots is a basic requirement. A model without vision is not a candidate ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)). There is no text-only track.
- A screenshot question can be deterministic or judged. It carries all its images in `attachments`; every image is sent with the same prompt.
- Coverage: section 3.7 (5 questions per source).
- Sample size: the sub-score margin at 85% is about ±22 points with 10 questions, ±16 with 20, ±13 with 30. 25 is the allocation (section 3.6); 30 is needed before the sub-score alone decides between two models.
- The prompt states the problem in words. The images supply the values.
- Images: author screenshots with host and customer names masked before commit.

### 13.1 Table questions
- Purpose: administrators export data in bulk and ask about it: a VCF Operations view or report, a vCenter list, a spreadsheet of every VM or host.
- Typical size: dozens of columns, hundreds of rows. Excel or CSV.
- The model does not read the whole table. The harness converts it to CSV and gives the agent a table tool: list the columns, filter, sort, aggregate, top-N. The model reasons over the results. Reason: hundreds of rows do not fit a 32K context, and models misread long tables.
- Every column name must map to a metric the knowledge base defines (catalog lookup), so the reading follows the knowledge base, not the column header's English.
- Not built yet: the table tool, the export formats and their misconceptions (plan, M2), table attachments in the runner. Table questions are written now and scored once the tool exists.
- Images and tables can be combined in one question (section 3.4).

## 14. Judged questions and the judge
- Questions with `answer_type: judged` are answered without options and scored 0-3 by a judge model. Code: [benchmark/runner/judge.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/judge.py).
- The candidate gets the same harness, modes and tools as for deterministic questions, with an open-answer prompt: plain text, at most 250 words, conclusion first, then mechanism and reason, then what to check next; say so when the information does not settle the question. Code: [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py), `PROMPTS['open']`.
- The judge gets: the prompt, the images, `## Expected key points`, `## Likely wrong answer`, and the answer. The candidate never sees the key.
- `## Expected key points` is the answer key for the judge, not a script for the candidate:
  - each bullet is one fact a correct answer must state, in any words, in any order;
  - the candidate never sees it; the open-answer prompt asks for the conclusion, the mechanism and reason, and what to check next, in at most 250 words;
  - a full answer covers every key point. Four key points take about 3-6 sentences (80-150 words), the length an expert gives a colleague;
  - order: the conclusion first, then the reason, then what to check next;
  - as many key points as the question takes. Most questions take 2-5. A long, complex question can take many more (real troubleshooting runs long, over a dozen screenshots). The 250-word limit of the open-answer prompt is too short for it: a per-question answer length is a to-do;
  - a key point that is only nice to know is not a key point: it goes in `## Notes`.
- Example ([CPU Latency without contention](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-01-cpu-latency-frequency.md)): a full answer reads like: No. Ready and Co-stop are flat, so the VM is not waiting for a physical CPU. CPU Latency rose because the BIOS power policy lowered the clock speed: the VM runs slower, as on an older CPU. Unlike Disk or Memory Latency, CPU Latency does not always mean a performance problem. Check the power policy and the frequency.
- Rubric:

| Score | Meaning |
|---|---|
| 0 | Wrong, falls into the likely wrong answer, or contradicts a key point. Also: says the information does not settle it (marked unsure). |
| 1 | Avoids the likely wrong answer, but the reason is missing or wrong. |
| 2 | Correct conclusion with the right reason (mechanism or vantage point from the key points). |
| 3 | As 2, and states what to check next, or covers every key point. |

- Judge rules (in its prompt): judge facts, not style or length; a contradiction of a key point caps the score at 0; the key points are the truth even where general IT practice differs; reward nothing the key points do not contain.
- Reply: one JSON object (`score`, `misconception`, `unsure`, `missed`, `reason`). One retry when it is not valid JSON; then the answer counts as failed and `--resume` retries it.
- Each run of a question is judged separately. The question credit is the lowest score / 3 (section 7.4).
- Judge choice: a frontier model, never a candidate, from a different vendor than the frontier reference, with vision, temperature 0. See [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 6.
- Recorded per answer in `answers.csv`: `judge_model`, `judge_score`, `judge_missed`, `reason`, `misconception`, `unsure`, and the answer text.
- Checks on the judge:
  - the author reviews every score 0 and every question where runs disagree by 2 or more points;
  - an author score overrides the judge: correct the key points, then re-score;
  - a key point the judge misreads is rewritten as one testable fact per bullet.
- Cost: one judge call per judged answer, about 1,500 input tokens.

## 15. Target history
- Goal: the local model with the knowledge base answers better than the best frontier model without it.
- Target: 99% final score on the question set (chosen mode). See section 7.4. (Before 2026-11-05: Stable correct on multiple-choice questions only.)
- Minimum: the release gate, section 7.5 (Q130, 2026-11-12).
- mistral/ministral-8b dropped from future runs: 29-40% exact in benchmark 20261103-081849.
- The other candidates stay until the question set reaches 100; 3 were added on 2026-11-04 (10 in total). No model is dropped on the 17-question results: the margin (about ±20-24 points) is too wide.
- Reference point: the best frontier model in baseline mode (no knowledge base). Measured in each benchmark.
- What 99% requires:
  - At 17 questions, 99% allows no wrong question. One wrong question = 94%.
  - At 100 questions, 99% allows 1 wrong question, but even a perfect score proves only about 96% (section 4). Proving 99% needs about 300 questions.
  - Answer keys must be correct. Every wrong answer from the best model gets an author check: model error, knowledge-base gap, or key error.
- Status at benchmark 20261103-081849: best small model 58% exact (classic). Gap: 41 points.

## 16. Decision rules
- Mode: agentic is the shipped mode and carries the release gate (Q130, 2026-11-12). Classic stays as the floor and the fallback; it is reported in every benchmark.
- Pick the model: highest final score in the chosen mode; then lowest confident-wrong rate; ties go to the smaller model.
- Agentic is dropped for a model with more than 10% fallbacks.
- Knowledge base lift: kb modes must beat baseline in every area. An area with no lift is a knowledge or retrieval problem, not a model problem.
- Screenshot upload is part of the product. A model whose screenshot sub-score is far below its text-only sub-score (more than the margin) is a vision problem: check the image, then the model.
- 70B challenger: only if the best 30B-band result loses points through reasoning errors (trace shows the right files were read).
- A challenger that needs more hardware (dense about 70B, or a 96 GB GPU) is kept only if it beats the best current candidate by more than the margin and its override rate is not higher. Reason: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 1.

## 17. Outputs
- [benchmark/results/results.csv](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/results.csv): one row per answer (add columns: mode, run, provider, temperature, options_order, answer_letters, exact, partial, misconception, retrieval_recall, steps, tokens, parse_ok).
- A short report per run in [benchmark/results](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results): score matrix, consistency, worst cases, trace links.
- Every wrong answer tagged with a cause (knowledge gap, retrieval miss, model error) and turned into a plan item or an author question.
