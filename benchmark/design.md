# Benchmark design

For human experts who check that the benchmark is valid and complete. Not indexed.
Runner and commands: [benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md). Question format: [benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md). Models and judge: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md). Misconception definition: `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400.

## 1. Claim
- Claim: a local open-weight model on customer hardware (one GPU is the stretch target; [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)), with this harness + agent + knowledge base, answers Level 400 vSphere operations questions better than the best frontier model without them.
- System under test: model + agent + harness + knowledge base. The model is frozen; the benchmark does not test it for its own sake (`MISSION.md`, section 2). It measures:
  - which frozen model to ship;
  - the score delta of each change to the knowledge base, harness or agent, with everything else fixed;
  - the gap to the frontier model.
- Baseline mode (the model alone) is the zero point: system minus baseline is what our work adds.
- Release gate: section 7.5 (final score at least 85%, Level 400 at least 80%, confident-wrong at most 3%, at least 15 points over the frontier model, held-out set not fitted). Target: 99%. Final score: section 7.4.
- The question set is one test, designed top down (section 3): what it must decide, then its size (section 4), its rules (section 6), its allocation, its slots, and only then the questions.
- The benchmark must:
  1. rank candidate models and answer modes against each other;
  2. show whether a configuration clears the release gate (section 7.5);
  3. show how close it is to 99%, and state what the number proves.

## 2. Scope
| Measured | Not measured (and where it is measured instead) |
|---|---|
| Correct reading of metrics: mechanism, vantage point, unit, rollup | Installation, configuration steps, UI navigation (out of scope for the product) |
| Resistance to misconceptions (see `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400) | Writing style of judged answers (the judge scores facts only, section 14) |
| Combining several facts and tables in one answer, including arithmetic | Speed and cost (logged per answer, judged separately) |
| Following a troubleshooting flow to a conclusion | Live-system troubleshooting (after 1.0) |
| Reading tables: vCenter chart exports, VCF Operations exports, esxtop batch output | Screenshots (the screenshot set after 1.0, section 13) |
| Knowing the limits: choosing Unsure instead of guessing | Multi-turn conversation with clarifying questions (a separate set, later) |
| Consistency: the same answer on every run | Cost and price (out of scope, author 2026-11-04) |
| Answering without options (free text, judged) | Agent E2's own framework and the vCommunity management pack (section 6.1) |

- Scope of 1.0: vSphere 9.1 metrics and the Guest OS layer, for performance and capacity, in monitoring and troubleshooting (`MISSION.md`, section 1).

## 3. Blueprint
Six independent axes (3.1 to 3.5, 3.7), allocated in section 3.6. Each question fills one slot of the blueprint. The slot list lives in [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M2, until every slot is written; the coverage script ([project/tools/coverage.py](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/coverage.py)) counts the set against every target below.

### 3.1 The job
The product is a narrow expert for one reader: a VMware administrator. The administrator brings one of five tasks, with text or a table as evidence.

| Task | What the administrator asks | Of 150 |
|---|---|---|
| Troubleshoot | Something is slow. What do I check, in what order, and what is the cause? | 45 |
| Read a metric | What does this value mean on this object, and is it a problem? | 35 |
| Decide capacity | Is there room? How big should this VM be? What can I reclaim? | 30 |
| Explain a mechanism | Why does the counter behave this way? | 25 |
| Judge a setting | What does this setting do to performance or capacity? | 15 |

- Troubleshooting leads: the mission is monitoring and troubleshooting (`MISSION.md`, section 1). Real operator questions are mostly "why does this counter do that" and "what is wrong" (the author's samples, 2026-11-12).
- Each task maps to a `retriever_guide` value of the knowledge base: troubleshooting, metric-meaning, health-check and decision-tree, how-it-works, what-to-set.

### 3.2 By level
Levels follow `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400.

| Level | The expert can | Of 150 | Example |
|---|---|---|---|
| 100 | Name and recognise: which counter, which object, which tool | 5 | [Device latency in esxtop](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L1-02-esxtop-device-latency-davg.md) |
| 200 | Define and explain one item in isolation | 15 | [Co-stop on a multi-vCPU VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L2-14-co-stop-multi-vcpu.md) |
| 300 | Apply common practice correctly: read a value, convert a unit, apply a published threshold | 40 | [High CPU Wait](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-01-cpu-wait-includes-idle.md) |
| 400 | Explain the mechanism, know when a reading misleads, and combine several facts or tables to a conclusion | 90 | [VM vs Guest OS metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-08-vm-vs-guest-os-metrics.md) |

- Level 400 is hard and complex, not tricky. It tests knowledge of the system, not reading of English. To stay unambiguous it is often long: the situation, the values, the tool, the time window, and one clear question.
- Level 400 combines facts inside one answer: several knowledge files, a calculation, a flow, several inputs. There is no back-and-forth with the user; the agent does the chaining with its tool calls.
- Why Level 100-300 are in the set, when the claim is about Level 400:
  1. The knowledge base assumes the basics and does not teach them. A candidate that fails Level 100-200 cannot read the knowledge base; a Level 400 failure is then a model failure, not a knowledge gap.
  2. Administrators ask basic questions too. One wrong basic answer costs the product its credibility.
  3. Non-regression (Level 300): the knowledge base corrects Level 300 rules of thumb. The candidate must not over-correct a practice that is right.
- Why only 5 at Level 100: every model scores about 95% there, so the questions separate nothing and add no power to the paired test (section 4). They stay as a guard.
- Level 400 carries most of the judged questions and most of the tables (section 3.6).

### 3.3 By answer type
| Answer type | The answer is | Scored by | Of 150 |
|---|---|---|---|
| Deterministic | One or more option letters (A, B, C, ...). Exactly right or not | The runner, by comparing letters | 90 (60%) |
| Judged | Free text. It cannot be scored as right or wrong by a rule | A judge model, 0-3 against the key points (section 14) | 60 (40%) |

- Deterministic is the majority: it is exact, cheap, and free of scorer bias.
- Judged is 40%, up from 30%: a real administrator asks without options, and options reward recognition. A small model can pick the right option yet fail to raise the point unprompted.
- Example, deterministic ([CPU reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-05-cpu-reservation-behaviour.md)): "Choose all the correct statements" about CPU reservation, options A to G. Key: A, B, C, D. Any other set of letters is wrong.
- Example, judged ([High CPU Wait](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-01-cpu-wait-includes-idle.md)): "A VM shows CPU Wait at 90%. The application owner says the VM must be stuck waiting on disk or memory. Are they right?"
- Metadata: `answer_type: deterministic | judged`.

### 3.4 By input type
| Input type | What it is | How it reaches the model | Of 150 (questions that include it) |
|---|---|---|---|
| Text | The prompt alone. It may hold a few values or a small table typed into the prompt (an esxtop excerpt, a resource pool tree) | As text | about 114 (text only) |
| Table | A CSV file: a vCenter performance chart export, a VCF Operations metric chart or list view export, or esxtop batch output | As text, after the prompt (section 13.1) | about 35 |
| Screenshot | An image of a product UI | As an image, to a vision model | 1 in 1.0 (the author's [ESXi utilization for capacity](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md)) |

- 1.0 has no new screenshots (author, 2026-11-12). A chart becomes its CSV export: the operator can export any vCenter or VCF Operations chart, and the question tests the reading, not the eyes. The screenshot set follows 1.0 (section 13).
- A question can combine input types; it counts for each input type it includes. Every question has a prompt, so text as an input type means the prompt alone.
- Metadata: `input: [text]`, `[table]` or `[screenshot]`, derived from `attachments` and checked by lint.
- URL questions: a question that carries a link to a public page with a known Level 300 error. The key point is that the answer corrects the page with the mechanism. The page is fetched live; the key records the page's date; a changed page is re-checked before scoring. None in 1.0: the first one (0091, VM Contention dashboard) was retired after the author had the official page fixed (Q184). More pages: the author's list ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M2).

### 3.5 By area
Each question has one primary area for the allocation, and lists every area it touches in `technology` (values from [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml)). The Guest OS layer is counted by `product` (windows, linux).

| Area | Primary, of 150 | Touched, at least | Covers |
|---|---|---|---|
| CPU | 36 | 40 | vCPU states, Ready, Co-stop, Run, Used, Usage, Demand, Hyper-Threading, frequency, NUMA |
| Memory | 28 | 35 | Consumed, Active, Granted, balloon, swap, compression, contention, sharing, tiering |
| Storage | 25 | 28 | latency stack, queues, outstanding IO, IO size, space, snapshots, IP storage |
| Network | 18 | 20 | drops, throughput, packet rate, units, teaming, offload |
| System | 25 | 30 | the object as a whole: cluster, DRS, admission control, resource pools, statistics and rollups, capacity, availability |
| Guest OS layer | 15 | 20 | Windows and Linux counters, and where they meet the VM counters |
| Outside the knowledge base | 3 | 3 | Answered from the model's own knowledge (knowledge base first, own knowledge where it is silent: author, Q038). They check that a gap does not turn into a wrong answer |

- Per-area scores (18-36 questions) are diagnostic only (margin about ±12-17 points). Decisions use the total.

### 3.6 Allocation
Level against answer type:

| Level | Deterministic | Judged | Total |
|---|---|---|---|
| 100 | 5 | 0 | 5 |
| 200 | 11 | 4 | 15 |
| 300 | 26 | 14 | 40 |
| 400 | 48 | 42 | 90 |
| Total | 90 | 60 | 150 |

Level against input type (questions that include it):

| Level | Text only | Table | Screenshot |
|---|---|---|---|
| 100 | 5 | 0 | 0 |
| 200 | 14 | 1 | 0 |
| 300 | 33 | 7 | 0 |
| 400 | 62 | 27 | 1 |
| Total | 114 | 35 | 1 |

- Judged questions and tables sit mostly at Level 400: reading evidence and combining it is the expert's work, and open-ended troubleshooting is where a real administrator asks without options.
- The 5 tasks (section 3.1) and the areas (section 3.5) are spread across every row.
- A cell may move by 2 questions while writing; the totals hold.

### 3.7 Coverage constraints
| Constraint | Minimum | Counted by |
|---|---|---|
| Each of the 12 misconception types | 5 questions each | `misconception_type` |
| Same name, other object (one label on two objects) | 8 | `misconception_type: same-name-other-object` |
| Objects: VM / ESXi / cluster / datastore / Guest OS / resource pool / network | 45 / 30 / 15 / 8 / 20 / 4 / 8 | `object` |
| Tools: vCenter / VCF Operations / esxtop / Guest OS tools | 30 / 25 / 10 / 10 | `tool` |
| Follow a troubleshooting flow (a `troubleshooting/` file) in order | 15 | `knowledge` |
| Calculation (summation to %, units, capacity) | 8 | review |
| The knowledge base and the vendor document disagree, with the evidence in the question | 3 | review |
| Long, multi-area scenario | 2 | review |

- Every question records what it covers in its metadata (`task`, `level`, `answer_type`, `input`, `technology`, `product`, `object`, `tool`, `misconception_type`, `knowledge`), so coverage is counted by a script, not by eye.

### 3.8 Answer-key shape (deterministic)
- Options: 4-8 written options, plus Unsure appended to every question. No Not covered option since 2026-11-05 (Q038).
- The number of correct options varies: about 30% of questions have 1 correct option, 50% have 2-3, 20% have 4 or more. The model is never told how many.
- A model that learns "usually one answer" or "usually all but one" gains nothing.

## 4. Sample size
150 questions in the development set, and 30 held-out questions drawn at release (section 7.5). The number follows from the decisions the set supports.

| Questions | 95% margin at 85% | Level 400 questions (margin at 80%) | Paired test power, 15-point gap, reverse 5% | reverse 8% | reverse 10% | Author time |
|---|---|---|---|---|---|---|
| 100 | ±7.0 | 60 (±10) | 91% | 84% | 80% | 1x |
| **150** | **±5.7** | **90 (±8)** | **98%** | **95%** | **91%** | **1.5x** |
| 200 | ±4.9 | 120 (±7) | ~100% | 98% | 97% | 2x |

- Reverse: the share of questions the frontier model gets right and Agent E2 gets wrong. Power of a one-sided exact McNemar test at α 0.05, simulated.
- Why not 100:
  - The fairness rules (section 6.1) remove the questions on Agent E2's own framework and the vCommunity models: the frontier model could not know them, so they made the gap cheap. Every question now rests on public mechanisms, where the frontier model is stronger, and the local model will lose more questions the frontier model gets right. At a reverse share of 10%, 100 questions miss a real 15-point win 1 time in 5; 150 questions, 1 time in 11.
  - The Level 400 gate (80%) is read on 60 questions at ±10 points: an 80% and a 90% system overlap. 90 questions give ±8.
- Why not 200: the margin improves by less than 1 point per 50 questions, for one third more author time. Author time is the constraint: every key is checked by hand.
- Why a held-out set on top, not more development questions: more questions read the gate more finely; they do not show that the knowledge base was not fitted to them. Only questions nobody tuned on show that (section 7.5).
- 150 cannot prove 99%. Even a perfect score only shows at least 97.5% with 95% confidence. Proving 99% needs about 300 questions with no wrong answer (rule of three). 99% stays a direction.
- One question is worth 0.67 points.

## 5. Set design
The set must measure one thing (Level 400 operations knowledge on public mechanisms) evenly, so the total has meaning.
- Coverage: the blueprint (section 3) makes every area, object, layer and misconception type count. No area can carry the score alone.
- Balance of difficulty: Level 100-200 questions anchor the scale. If they fail, the problem is the model's basics or retrieval, and Level 400 failures are not interpreted (section 3.2).
- Paired questions: the same concept on two objects. A model that answers both right understands the vantage point; one that answers one right was lucky or pattern-matched.
- Independence: no question gives away another's answer. No two questions test the same single fact.
- Every option is decidable from the knowledge base (or, for questions outside it, from the vendor documents). A question the knowledge base cannot settle is rewritten or removed, never kept as a coin flip.

## 6. Question writing
### 6.1 Fairness
The frontier model must be able to answer every question from public knowledge. Agent E2 wins on depth, not on vocabulary.
- F1. Public words only. Counter and feature names as the product shows them (vCenter, VCF Operations, esxtop, Windows, Linux). No Agent E2 terms: SP5 Framework, Triple See Method, KPI, realm, IaaS high utilization, virtual motherboard (say VM), Close for Business.
- F2. No vCommunity management pack metrics: Cluster Performance, Cluster Consumption and Cluster Risk, Close for Business, VM, Guest OS and ESXi Performance (%), inter-host imbalance, any `vCommunity|` key. Native VCF Operations metrics are allowed: CPU Contention (%), Memory Contention (%), the 20-second peak metrics, Capacity Remaining.
- F3. Decidable from mechanisms and public documents. A strong expert without Agent E2 could answer it. An author threshold appears only when the prompt states it ("your team alerts at 10 ms").
- F4. The rules hold for the title, the prompt, the options, `## Likely wrong answer` and `## Expected key points`: the judge reads the key points, and a frontier answer cannot state a term it has never seen.
- F5. Evidence first. A Level 300-400 stem is an operator's situation with the data a tool shows: values, a table, a time window. Not a knowledge-file sentence turned into a question (the 2026-11-11 review found most synthetic questions tested recall of the knowledge base).
- F6. No question is picked or dropped because the frontier model fails it. An adversarial set, if ever used, is declared and reported apart.
- Lint checks F1, F2 and F4 against the list `question_fairness` in [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml). F3, F5 and F6 are review items (section 11).

### 6.2 Stem, options, key
- Stem: a realistic situation with the values an operator would see (counter names, numbers, units, time window, tool). Not a definition prompt, except at Level 100-200.
- Options:
  - one fact per option;
  - similar length and style, so length gives no hint;
  - no "all of the above", no double negatives;
  - every wrong option is wrong for a reason the knowledge base states;
  - one option is the misconception: the conclusion a Level 300 reader would draw. It is named in `## Likely wrong answer` and in metadata `misconception`.
- Wording: paraphrased, never copied from the knowledge base. The benchmark checks reasoning, not string matching.
- Key: `answer` letters, and `## Expected key points` with the reason for every option. Product behaviour that is not in the knowledge base is checked against the current vendor document, and its URL goes in `## Notes`.
- Sources: the author's books, quizzes and samples first; then real tickets and field questions; then synthetic questions drafted by Claude. A synthetic question needs the author's approval before it counts.

### 6.3 Attachments
- Every reference to an attachment in `## Prompt` is a relative link to the file: `[the attached chart export](0123/vm-cpu.csv)`. A reviewer opens it on GitHub, which renders a CSV as a table and an image as an image.
- The runner sends only the link text, never the path (`ATTACH_LINK` in [benchmark/runner/questions.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/questions.py)), as the harness does for knowledge links: no token cost.
- Lint: every attachment is linked in the prompt, and every link in the prompt is an attachment.

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
  - The benchmark is an absolute measurement against a fixed question set. Stable correct already counts only exact answers; a wrong answer and an Unsure both count as not correct, so the -1 never changed the headline.
  - Net points mixed two things an operator cares about separately: how often the system is right, and how often it is confidently wrong. Two plain shares say both without arithmetic.
- The -1 changed the model's behaviour through the prompt: told that a wrong answer costs a point, models chose Unsure instead of guessing. That behaviour is kept with a plain rule in the prompt ("a wrong answer is worse than Unsure").
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

- 3 runs let a coin-flip question pass 1 time in 8. 5 runs cut that to 1 in 32, and still reward a model that is right 99% of the time (95% pass). 10 runs double the cost for little gain.

### 7.3 Secondary measures
| Measure | Why |
|---|---|
| Luck | How much of a model's score is unstable. |
| Confident-wrong rate | Answers that would mislead an operator. |
| Unsure rate, accuracy when answered | A cautious model with gaps vs a reckless one. |
| Misconception rate, per `misconception_type` | How often the misconception option is picked. The core Level 400 signal. |
| Not-covered accuracy | Guessing outside the knowledge base. |
| Retrieval recall | Whether the right files were found; separates retrieval from reasoning. |
| Tools used, verifier flags | Whether the harness tools were used (agentic mode). |
| Per area, per level, per input | Diagnosis only (small counts). |

### 7.4 Final score
- One number, 0-100%, for each model and mode. Sub-scores support it: by answer type, by input type, by level.
- Question credit, 0 to 1, taken from the worst of the 5 runs:
  - deterministic: 1 if the letters are exactly right in every run, else 0 (Stable correct);
  - judged: the lowest judge score over the runs, divided by 3 (0, 0.33, 0.67, 1).
- Final score = sum of question credits / number of questions. Every question weighs the same, whatever its level, answer type or input type.
- Sub-score = the same mean within one group. A question counts for every input type it includes. The allocation (section 3.6) sets how much each group weighs in the final score.
- Reasons:
  - worst run, not mean: the same rule as Stable correct. An answer right in 4 runs of 5 is luck, and an operator gets one run;
  - one weight per question: no group can carry the score by a formula choice; the blueprint decides the mix;
  - judge score / 3: a partly right judged answer earns part credit, as a human examiner would give. A deterministic answer has no part credit, because a partly right set of letters is a wrong answer an operator would act on.
- Confident-wrong rate covers both: wrong letters that are not Unsure, and judged answers scored 0 that do not say the information does not settle it.
- Margin: 95% interval on the final score from the number of questions (section 4).
- Runner: [benchmark/runner/report.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/report.py), function `final`. Report table `Final score`.

### 7.5 Release gate
- Read on Agent E2 as shipped: the local model in agentic mode, with the deployment profile (section 8). Classic mode is the floor and the fallback; it carries the retrieval levels (section 9).
- All must hold. One number alone can be carried by easy questions or bought with confident guesses.

| Gate | Limit | Why |
|---|---|---|
| Final score, development set (150) | at least 85% | Margin ±5.7 (section 4); below 85 an operator stops trusting the answers |
| Level 400 sub-score | at least 80% | 90 questions (margin ±8): the one sub-score that gates. The mission is Level 400; Level 100-300 can carry the total |
| Confident-wrong rate | at most 3% | The answers an operator acts on. A wrong answer marked Unsure is not one of them |
| Misconceptions of [knowledge/misconceptions.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/misconceptions.md) | none stated as true | They are given up front; stating one is a harness or model defect, not a gap. Author check of the answers |
| Held-out set (30) | at most 11 points below the development set | One-sided 95% for 150 against 30 questions at about 87%: a larger drop means the knowledge base or retrieval is fitted to the visible questions |
| Gap to the frontier model (section 8) | at least 15 points, paired test significant | The claim of section 1 |

- Effective bar: Agent E2 at least the larger of 85% and frontier + 15.
- Why 85%, not 90%: at 150 questions 85 and 90 still overlap inside the margin; the confident-wrong limit does more for the operator than 5 more points.
- Why 15 points: 10 points is about twice the margin and has low paired power ([project/review-2026-11-11.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-11.md), section 5); 15 points has 91% or more at 150 questions (section 4).
- Held-out set:
  - 30 questions drawn at release from the same blueprint, in proportion (about 1 at Level 100, 3 at 200, 8 at 300, 18 at 400; 12 judged, 6 with a table).
  - Written by a session that does not edit the knowledge base, reviewed by the author, never committed to the repository. Run once, on the release configuration.
  - Why drawn at release, not now: a question that exists while the knowledge base is still edited can leak into it. A fresh draw cannot.
  - Why the 11-point limit replaces "within 5 points": on 20-30 questions the noise alone is about ±13 points, so a 5-point rule fails or passes by luck.
- Expected frontier score (expert estimate, 2026-11-12; replaced by the first M4 benchmark): about 70%.

| Level | Of 150 | Frontier expected | Why |
|---|---|---|---|
| 100 | 5 | about 95% | Public counter names |
| 200 | 15 | about 90% | Public definitions; exact multi-select costs a few |
| 300 | 40 | about 80% | Public practice, but some published thresholds are the ones the knowledge base corrects |
| 400 | 90 | about 60% | Knows each mechanism alone; misses the vantage point and the combination of readings, and picks the Level 300 rule of thumb. Web search returns the same Level 300 pages |

- So the 85% gate and the 15-point gap bind at about the same place. The author-framework row of the earlier estimate (about 25%) is gone with the fairness rules: the gap must be won on public mechanisms.
- Ceiling, not a gate: the frontier model in agentic mode with the knowledge base. Agent E2 within 5 points of it shows the local model is not the bottleneck. If the frontier model scores lower with the knowledge base than without, the knowledge base or the harness misleads a strong model: fixed before any gap is read.
- Target: 99%, a direction. 150 questions cannot prove it (section 4).
- Runner: [benchmark/runner/report.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/report.py), functions `gate` and `mcnemar`, report table `Release gate`: final score, Level 400, confident-wrong, gap and paired test. The misconception check and the held-out set are read outside the report.

## 8. Comparison design
- Reasons for running both modes and for the call limit: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), sections 8 and 9.
- The release score uses the deployment profile of the harness: same prompt, tools, context window and budgets as the product. Time is replaced by a turn limit derived from the target GPU. Other settings run only as named experiments. See [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 8, Benchmark and deployment.
- Every model runs in three modes on the same questions: baseline (no knowledge base), classic (one lookup), agentic (model-driven lookups). See [benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md).
- Reference: the frontier model in baseline mode: Claude Opus 5.5, web search on, effort capped at medium, no knowledge base (Q164). The claim in section 1 is met when Agent E2 exceeds it by at least 15 points and a one-sided exact McNemar test on the questions is significant at α 0.05 (section 7.5).
- Paired comparison: models are compared question by question on the same set, not only by totals.
- Between candidate models, a gap smaller than the margin is a tie; the smaller model wins a tie. Against the frontier model, a gap below 15 points does not support the claim.
- Run matrix of the final round: 3 candidates x 3 modes plus the frontier reference x 2 modes (baseline, web), 196 questions, 5 runs = 10,780 answers, about US$ 90 and 2-4 hours, from the preflight sample ([benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md)). Prices, rate limits and a model's thinking change both numbers: run the preflight before each round.

## 9. Retrieval check
- The final score mixes harness and model. The retrieval check separates them: [benchmark/runner/retrieval_eval.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/retrieval_eval.py) checks, without a model, whether each question's `knowledge` files are found and placed in the classic context. Guide: [benchmark/retrieval-check.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/retrieval-check.md).
- Paused (author, 2026-11-12) until the question set of section 3 is written; then a new baseline on the 150 questions. Last numbers, on the old 95: search 60%, classic context 78%, 61 of 95 complete.
- Every wrong answer is classified: file not in context (harness or knowledge), file in context but answer wrong (model or prompt), file not in the knowledge base (gap). Detail: `ARCHITECTURE.md`, section 6.

## 10. Validity threats
| Threat | Guard |
|---|---|
| Wrong answer key | Every wrong answer from the best model is checked by the author: model error, knowledge gap, or key error. Keys cite knowledge ids; product behaviour outside the knowledge base cites the vendor document. |
| Knowledge base fitted to the benchmark (Claude edits the knowledge base and can read the questions) | The held-out set of section 7.5, drawn at release. Fixes to the knowledge base must be general (a fact or a misconception), never a question-specific answer. |
| Unfair to the frontier model (terms and metrics it cannot know) | Fairness rules, section 6.1; lint checks the terms. |
| Questions written by the knowledge base's own author favour its wording | Paraphrased stems; evidence-first stems; the author's real-world samples; frontier baseline as an outside reference. |
| Synthetic questions drafted by Claude mirror Claude's view, and the frontier reference is also Claude | The author reviews every question; an independent reviewer agent tries to break each key before the author sees it; no question picked by frontier failure (F6). |
| Ambiguous options | A question with a disputed option is fixed or removed, and the benchmark is re-scored. |
| Position, length and count bias | Shuffled options; similar option length; varied number of correct options. |
| Guessing | Unsure option, the prompt rule that a wrong answer is worse than Unsure, confident-wrong rate, 5-run stability. |
| Leakage into the model | Questions are never indexed, never used for fine-tuning, and `## Expected key points` is never sent to the model. |
| Frontier model knows public material | Baseline tests exactly that. The knowledge base must add what public material lacks. |
| Version drift | Every benchmark records the index version (git commit), model, provider and settings. Scores are compared only within one scoring scheme. |

## 11. Review checklist
For each question:
1. Is the situation realistic for an operator of vSphere 9.1?
2. Is every option decidable from the cited knowledge files or vendor documents, and is the key right?
3. Could a strong expert without Agent E2 answer it from public knowledge (section 6.1)?
4. Is the misconception option a mistake a competent Level 300 operator would plausibly make?
5. Does any option give the answer away by wording, length or count?
6. Does it duplicate another question's fact?
7. Does it test operations knowledge, not trivia (UI clicks, product history, prices, file names)?
8. Does a CSV hold every value the key relies on, and nothing that contradicts it?

For the set:
9. Do the counts match the blueprint in section 3 (coverage script)?
10. Is every misconception type covered at least 5 times?

## 12. Status
- 2026-11-12: 150 questions run, at the allocation of section 3 (`python3 project/tools/coverage.py`; tasks within 2 of target: decide-capacity 31, explain-mechanism 24). Plus 5 deferred screenshot questions; 12 retired to [project/archive/benchmark-questions](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-questions).
- Origin: 35 by the author (17 quiz, 10 book, 8 from the author's samples of 2026-11-12), 2 real exchanges, 113 synthetic. 35 carry a CSV; 1 a screenshot.
- Every synthetic question was checked by an independent review agent, which tried to break each key against the knowledge files and the vendor documents; the defects found were fixed. Author questions from the review: all answered (Q182-Q191). Knowledge fixes found on the way: [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M1.
- Status draft: each question counts after the author's review (section 6.2).

## 13. Screenshot questions (after 1.0)
- Purpose: administrators upload screenshots and ask the agent to explain the problem, often several at once, from different tools.
- 1.0 has one (the author's L4-03). The screenshot set after 1.0 starts from the 5 deferred questions (`status: deferred`), with images the author already supplied, and grows to about 25 (5 per source: esxtop, vCenter, VCF Operations).
- Reading screenshots stays a basic requirement: a model without vision is not a candidate ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)).
- A screenshot question carries all its images in `attachments`; every image is sent with the same prompt. The prompt states the problem in words; the images supply the values. Images are masked (host and customer names) before commit.

### 13.1 Table questions
- Purpose: administrators export data and ask about it: a vCenter chart export, a VCF Operations list or metric export, esxtop batch output.
- 1.0 tables are small: at most about 3,000 tokens (`question_csv_max_chars` in [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml), checked by lint), about 60 rows by 8 columns. The runner puts the CSV after the prompt as text (`Question.tables`); the deployed model's window is 32,000 tokens.
- Larger exports (hundreds of rows) need a table tool in the harness (filter, sort, aggregate, top-N). After 1.0.
- Column names are the product's metric names (for example `CPU|Ready (%)`, `Usage for vm-01 (Percent)`), so the reading follows the product, not the header's English.
- A CSV is generated by a seeded script, then checked: every value the key relies on is in it, and nothing contradicts the key. Time stamps, object names and noise are realistic; names are invented, never a customer's.

## 14. Judged questions and the judge
- Questions with `answer_type: judged` are answered without options and scored 0-3 by a judge model. Code: [benchmark/runner/judge.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/judge.py).
- The candidate gets the same harness, modes and tools as for deterministic questions, with an open-answer prompt: plain text, at most 250 words, conclusion first, then mechanism and reason, then what to check next; say so when the information does not settle the question. Code: [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py), `PROMPTS['open']`.
- The judge gets: the prompt with its tables, the images, `## Expected key points`, `## Likely wrong answer`, and the answer. The candidate never sees the key.
- `## Expected key points` is the answer key for the judge, not a script for the candidate:
  - each bullet is one fact a correct answer must state, in any words, in any order;
  - a full answer covers every key point. Four key points take about 3-6 sentences (80-150 words), the length an expert gives a colleague;
  - order: the conclusion first, then the reason, then what to check next;
  - as many key points as the question takes. Most questions take 2-5. A long scenario can take more; the 250-word limit is then too short (a per-question answer length is a to-do);
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
- Cost: one judge call per judged answer, about 1,500 input tokens (more with a table).

## 15. Target history
- Goal: the local model with the knowledge base answers better than the best frontier model without it.
- Target: 99% final score on the question set (chosen mode). See section 7.4.
- Minimum: the release gate, section 7.5 (Q130, 2026-11-12; set size and held-out rule revised 2026-11-12, question set 1.0).
- The other candidates stay until the question set is complete; no model is dropped on a small set.
- What 99% requires: at 150 questions, 99% allows 1 wrong question and proves only about 97.5%; proving 99% needs about 300 questions (section 4). Answer keys must be correct: every wrong answer from the best model gets an author check.
- Status at benchmark 2026-11-12 (150 questions): best small model 67% in classic mode and 56% in agentic mode against the 85% gate; frontier model without the knowledge base 67%.

## 16. Decision rules
- Mode: agentic is the shipped mode and carries the release gate (Q130, 2026-11-12). Classic stays as the floor and the fallback; it is reported in every benchmark.
- Pick the model: highest final score in the chosen mode; then lowest confident-wrong rate; ties go to the smaller model.
- Agentic is dropped for a model with more than 10% fallbacks.
- Knowledge base lift: kb modes must beat baseline in every area. An area with no lift is a knowledge or retrieval problem, not a model problem.
- 70B challenger: only if the best 30B-band result loses points through reasoning errors (trace shows the right files were read).
- A challenger that needs more hardware (dense about 70B, or a 96 GB GPU) is kept only if it beats the best current candidate by more than the margin and its override rate is not higher. Reason: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 1.

## 17. Outputs
- [benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md): one analysis of all runs of a round, written when the last run finishes. One folder per run, named `<date>-<model>`.
- A short report per run in [benchmark/results](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results): score matrix, consistency, worst cases, trace links.
- Every wrong answer tagged with a cause (knowledge gap, retrieval miss, model error) and turned into a plan item or an author question.
