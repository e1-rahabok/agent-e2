# Benchmark design

For human experts who check that the benchmark is valid and complete. Not indexed.
Runner and commands: [benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md). Question format: [benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md). Models and judge: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md). Misconception definition: `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400.

## 1. Claim
- Claim: a local open-weight model on customer hardware (one GPU is the stretch target; [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)), with this harness + agent + knowledge base, answers Level 400 vSphere operations questions better than the best frontier model without them.
- System under test: model + agent + harness + knowledge base. The model is frozen; the benchmark does not test it for its own sake (`MISSION.md`, section 1). It measures:
  - which frozen model to ship;
  - the score delta of each change to the knowledge base, harness or agent, with everything else fixed;
  - the gap to the frontier model.
- Base (the model alone) is the zero point: Agent E2 minus Base is what our work adds.
- Release gate: section 7.5 (final score at least 85%, Level 400 at least 80%, confident-wrong at most 3%, held-out set not fitted). Target: 99%. Final score: section 7.4.
- The benchmark is a proof, not a goal ([CLAUDE.md](https://github.com/e1-rahabok/agent-e2/blob/main/CLAUDE.md), Evaluation). The real test is the field: the live test with the author's real questions ([benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md)) and the operators who use Agent E2. The question set has no target size and no allocation to fill: questions are added, rewritten and retired as the knowledge base and the field show what matters.
- The benchmark must:
  1. rank candidate models against each other, on Agent E2 and on Base;
  2. show whether a configuration clears the release gate (section 7.5);
  3. show how close it is to 99%, and state what the number proves.

## 2. Scope
| Measured | Not measured (and where it is measured instead) |
|---|---|
| Correct reading of metrics: mechanism, vantage point, unit, rollup | Installation, configuration steps, UI navigation (out of scope for the product) |
| Resistance to misconceptions (see `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400) | Writing style of answers |
| Combining several facts and tables in one answer, including arithmetic | Speed and cost (logged per answer, judged separately) |
| Following a troubleshooting flow to a conclusion | Live-system troubleshooting (after 1.0) |
| Reading tables: vCenter chart exports, VCF Operations exports, esxtop batch output | More screenshots (the screenshot set grows after 1.0, section 13) |
| Knowing the limits: choosing Unsure instead of guessing | Multi-turn conversation with clarifying questions (a separate set, later); a consultation that interviews the user and computes (capacity planning): the live test, step 9 |
| Consistency: the same answer on every run | Cost and price (out of scope, author 2026-11-04) |
| Knowing every true statement and rejecting every plausible false one, among as many options as the question needs | Agent E2's own framework and the vCommunity management pack (section 6.1) |
| | Answering without options, in free text: the live test, judged by the author ([benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md), step 9; Q199) |

- Scope of 1.0: vSphere 9.1 metrics, the native VCF Operations metrics on vSphere objects (section 6.1, F2) and the Guest OS layer, for performance and capacity, in monitoring and troubleshooting (`MISSION.md`, section 1).

## 3. Question set
- Each question records what it covers in its metadata (`task`, `level`, `answer_type`, `input`, `technology`, `product`, `object`, `tool`, `misconception_type`, `knowledge`). The axes below describe the set; they are not quotas.
- Counts change with every question added, rewritten or retired. They live in code, not in this file: `python3 project/tools/coverage.py` prints the count of every tag value and marks a value with no question (`<<`). The report breaks the score down by the same axes.
- A value with no question, or a field question the set has nothing like, is a reason to write a question. A count is never a reason to keep or drop one.

### 3.1 The job
The product is a narrow expert for one reader: a VMware administrator. The administrator brings one of five tasks, with text, a table or a screenshot as evidence.

| Task | What the administrator asks |
|---|---|
| Troubleshoot | Something is slow. What do I check, in what order, and what is the cause? |
| Read a metric | What does this value mean on this object, and is it a problem? |
| Decide capacity | Is there room? How big should this VM be? What can I reclaim? |
| Explain a mechanism | Why does the counter behave this way? |
| Judge a setting | What does this setting do to performance or capacity? |

- Troubleshooting leads: the mission is monitoring and troubleshooting (`MISSION.md`, section 1). Real operator questions are mostly "why does this counter do that" and "what is wrong" (the author's samples, 2026-11-12).
- Each task maps to a `retriever_guide` value of the knowledge base: troubleshooting, metric-meaning, health-check and decision-tree, how-it-works, what-to-set.

### 3.2 By level
Levels follow `KNOWLEDGE-ENGINEERING.md`, section Misconceptions and Level 400.

| Level | The expert can | Example |
|---|---|---|
| 100 | Name and recognise: which counter, which object, which tool | [Device latency in esxtop](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L1-02-esxtop-device-latency-davg.md) |
| 200 | Define and explain one item in isolation | [Co-stop on a multi-vCPU VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L2-14-co-stop-multi-vcpu.md) |
| 300 | Apply common practice correctly: read a value, convert a unit, apply a published threshold | [High CPU Wait](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-01-cpu-wait-includes-idle.md) |
| 400 | Explain the mechanism, know when a reading misleads, and combine several facts or tables to a conclusion | [VM vs Guest OS metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-08-vm-vs-guest-os-metrics.md) |

- Level 400 is hard and complex, not tricky. It tests knowledge of the system, not reading of English. To stay unambiguous it is often long: the situation, the values, the tool, the time window, and one clear question.
- Level 400 combines facts inside one answer: several knowledge files, a calculation, a flow, several inputs. There is no back-and-forth with the user; the agent's code does the chaining (the reading plan and the computed facts of [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)).
- Level 400 holds most of the set and most of the tables: the claim is about Level 400.
- Why Level 100-300 are in the set:
  1. The knowledge base assumes the basics and does not teach them. A candidate that fails Level 100-200 cannot read the knowledge base; a Level 400 failure is then a model failure, not a knowledge gap.
  2. Administrators ask basic questions too. One wrong basic answer costs the product its credibility.
  3. Non-regression (Level 300): the knowledge base corrects Level 300 rules of thumb. The candidate must not over-correct a practice that is right.
- Level 100 stays small: every model scores about 95% there, so its questions separate nothing. They stay as a guard.

### 3.3 By answer type
| Answer type | The answer is | Scored by |
|---|---|---|
| Deterministic | One or more option letters (A, B, C, ...). Exactly right or not | The runner, by comparing letters |

- Every question of the run set is deterministic (author, Q199 F, 2026-11-14): exact, cheap, free of scorer bias, and covered by consensus of samples. The judge scored free text unreliably: a 250-word answer scored 0 when one side sentence contradicted a key point, and judged answers carried most of the confident-wrong rate.
- What options lose, and where it is measured instead: a real administrator asks without options, and options can reward recognition. The guard in the set: many plausible false options, each wrong for a reason the knowledge base states, the Level 300 misconception among them, and exact match of the whole set (section 3.8). The free-text answer itself is measured in the live test, judged by the author.
- Example, deterministic ([CPU reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-05-cpu-reservation-behaviour.md)): "Choose all the correct statements" about CPU reservation, options A to G. Key: A, B, C, D. Any other set of letters is wrong.
- Metadata: `answer_type: deterministic` (lint rejects any other value).

### 3.4 By input type
| Input type | What it is | How it reaches the model |
|---|---|---|
| Text | The prompt alone. It may hold a few values or a small table typed into the prompt (an esxtop excerpt, a resource pool tree) | As text |
| Table | A CSV file: a vCenter performance chart export, a VCF Operations metric chart or list view export, or esxtop batch output | As text, after the prompt (section 13.1) |
| Screenshot | An image of a product UI | As an image, to a vision model |

- 1.0 adds no more screenshots. A chart becomes its CSV export: the operator can export any vCenter or VCF Operations chart, and the question tests the reading, not the eyes. The screenshot set grows after 1.0 (section 13).
- A question can combine input types; it counts for each input type it includes. Every question has a prompt, so text as an input type means the prompt alone.
- Metadata: `input: [text]`, `[table]` or `[screenshot]`, derived from `attachments` and checked by lint.
- URL questions: a question that carries a link to a public page with a known Level 300 error. The key point is that the answer corrects the page with the mechanism. The page is fetched live; the key records the page's date; a changed page is re-checked before scoring. None in 1.0: the first one (0091, VM Contention dashboard) was retired after the author had the official page fixed (Q184). More pages: the author's list ([project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M2).

### 3.5 By area
Each question lists every area it touches in `technology` (values from [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml)). The Guest OS layer is counted by `product` (windows, linux).

| Area | Covers |
|---|---|
| CPU | vCPU states, Ready, Co-stop, Run, Used, Usage, Demand, Hyper-Threading, frequency, NUMA |
| Memory | Consumed, Active, Granted, balloon, swap, compression, contention, sharing, tiering |
| Storage | latency stack, queues, outstanding IO, IO size, space, snapshots, IP storage |
| Network | drops, throughput, packet rate, units, teaming, offload |
| System | the object as a whole: cluster, DRS, admission control, resource pools, statistics and rollups, capacity, availability |
| Guest OS layer | Windows and Linux counters, and where they meet the VM counters |
| Outside the knowledge base | A few questions answered from the model's own knowledge (knowledge base first, own knowledge where it is silent: author, Q038). They check that a gap does not turn into a wrong answer |

- Per-area scores rest on a few dozen questions each (margin about ±12-17 points): diagnostic only. Decisions use the total.

### 3.6 Mix
- No group can carry the score alone: every question weighs the same (section 7.4), so the mix of the set is what weighs each group. Coverage keeps it honest: every area, object, tool and misconception type is tested, and none dominates by accident.
- Tables and long scenarios sit mostly at Level 400: reading evidence and combining it is the expert's work.
- The five tasks (section 3.1) and the areas (section 3.5) are spread across every level.

### 3.7 Coverage rules
| Rule | Checked by |
|---|---|
| Every misconception type of `KNOWLEDGE-ENGINEERING.md` is tested | `misconception_type` |
| Every object type (VM, ESXi, cluster, datastore, Guest OS, resource pool, network) is read | `object` |
| Every tool (vCenter, VCF Operations, esxtop, Guest OS tools) is shown | `tool` |
| Troubleshooting flows (a `troubleshooting/` file) are followed in order | `knowledge` |
| Calculations (summation to %, units, capacity) | review |
| The knowledge base and the vendor document disagree, with the evidence in the question | review |
| Long, multi-area scenarios | review |

- `coverage.py` prints each count and marks a zero. The review rules are checked by the reviewer (section 11).

### 3.8 Answer-key shape (deterministic)
- Options: as many as the question needs, no fixed count (author, Q199, 2026-11-14): the reader is a model, not a person, so a list of 20 is no burden. The runner takes up to 25 written options (letters A-Y) and appends Unsure as the next letter. No Not covered option since 2026-11-05 (Q038).
- The number of correct options varies from one to all of them (1 correct and 19 wrong is valid). The model is never told how many: every question carries the same instruction, "Choose all the correct options. There can be more than one."
- A model that learns "usually one answer" or "usually all but one" gains nothing, and with many options a guess is almost never exactly right (6 options plus Unsure: about 1 in 64).

## 4. Sample size
- The set has no target size. What its size buys is precision, and the report prints it for the set as run: the 95% margin on the final score (`report.py`, `_margin`; the summary README).
- Rule of thumb for a score near 85%: about ±7 points at 100 questions, ±5 at 200, ±4 at 300. The margin shrinks with the square root of the count: four times the questions for half the margin.
- The comparison with the frontier model is paired, question by question (a one-sided exact McNemar test at α 0.05, section 8). Power to find a real 15-point win, simulated at 196 questions: about 100%, 98% and 97% when the frontier model is right and Agent E2 wrong on 5%, 8% and 10% of the questions (the reverse share).
- Level 400 alone (about two thirds of the set) reads at about ±7 points at 80%.
- What size cannot buy:
  - fitness to the field: more questions read the gate more finely; they do not show that real questions look like them. The field shows that (section 1; the live test);
  - freedom from fitting: only questions nobody tuned on show that the knowledge base was not fitted to the set (the held-out set, section 7.5).
- 99% cannot be proven at this size. Even a perfect score on 200 questions only shows at least 98.5% with 95% confidence; proving 99% needs about 300 questions with no wrong answer (rule of three). 99% stays a direction.
- Author time is the constraint: every key is checked by hand.

## 5. Set design
The set must measure one thing (Level 400 operations knowledge on public mechanisms) evenly, so the total has meaning.
- Coverage: every area, object, layer and misconception type is tested (section 3.7). No area can carry the score alone.
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
- F4. The rules hold for the title, the prompt, the options, `## Likely wrong answer` and `## Expected key points`: reviewers read the key points as the reasons of the key.
- F5. Evidence first. A Level 300-400 stem is an operator's situation with the data a tool shows: values, a table, a time window. Not a knowledge-file sentence turned into a question (the 2026-11-11 review found most synthetic questions tested recall of the knowledge base).
- F6. No question is picked or dropped because the frontier model fails it. An adversarial set, if ever used, is declared and reported apart.
- Lint checks F1, F2 and F4 against the list `question_fairness` in [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml). F3, F5 and F6 are review items (section 11).

### 6.2 Stem, options, key
- Stem: a realistic situation with the values an operator would see (counter names, numbers, units, time window, tool). Not a definition prompt, except at Level 100-200.
- No hints in the prompt (author, 2026-11-14): no line that explains a mechanism, defines a counter, interprets a value or points to the answer ("Hint:", "Be aware of", "Do not select", "the cores run below the base clock"). A frontier model uses a hint; a local model does not, so a hint measures the model, not the knowledge base. A hint that helps a reviewer goes in `## Notes`. Case facts stay: values, settings, versions, what changed, and limits on scope ("ignore the VMX swap file").
- The stem never tells how many options are correct (Q199): plural wording ("Which statements are correct?"), matching the runner's closing line "Choose all the correct options. There can be more than one."
- Lint checks both against `question_prompt_hints` in [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml).
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

- Two numbers are reported for deterministic questions: **Stable correct** (absolute, against the fixed set: correct in every run; reported as consistency since 2026-11-13, when the final score moved to the mean of the runs, section 7.4) and **confident-wrong rate** (share of answers that are wrong and not Unsure; target near 0).
- The model is told: a wrong answer is worse than Unsure, because an operator would act on it; if it cannot decide every option, choose Unsure.

### 7.1 No points, no -1
- An earlier version scored +1 / 0 / -1 and reported "Net points". It was dropped:
  - The benchmark is an absolute measurement against a fixed question set. Stable correct already counts only exact answers; a wrong answer and an Unsure both count as not correct, so the -1 never changed the headline.
  - Net points mixed two things an operator cares about separately: how often the system is right, and how often it is confidently wrong. Two plain shares say both without arithmetic.
- The -1 changed the model's behaviour through the prompt: told that a wrong answer costs a point, models chose Unsure instead of guessing. That behaviour is kept with a plain rule in the prompt ("a wrong answer is worse than Unsure").
- Unsure means the sources do not decide the question. This can be checked against the cited files.
- Check after the next benchmark: if models guess more under the plain rule (confident-wrong rate rises, Unsure rate falls), put the scoring sentence back in the prompt only. Grading stays as above either way.
- Read on the previous generation (round of 2026-11-13): the local models chose Unsure in 1-6% of multiple-choice answers and were confident wrong in 10-22% of them with the knowledge base. A rule in the prompt does not make a 30B model abstain. The harness now abstains for it: consensus of samples (`consensus_samples`, [harness/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/README.md), section 6a). Analysis (archived): [analysis-2026-11-13.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md).

### 7.2 Five runs
- One run is one draw of the answer, not the answer. Agent E2 makes two model calls (stage 1 and stage 5 of [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)):
  - the case (stage 1) is asked at temperature 0, so the same question reads into the same case and gets the same reading set;
  - the answer (stage 5) is sampled with the settings of the model's own card (temperature 1.0 for the three candidates, `sampling` in `config.yaml`), because a local server applies them by default and the operator meets that answer (author, 2026-11-13). Two runs of the same question can give different letters.
- Base and the frontier reference also sample (the card's settings; the provider's default for Opus).
- Temperature 0 would not make one run enough either: hosted models do not answer the same way twice even at temperature 0 (batching on shared GPUs, provider routing, silent serving updates).
- So each question runs 5 times. The 5 runs give:
  - the final score: the mean of the runs, the best estimate of the one answer an operator gets (section 7.4);
  - the consensus projection: the shipped profile asks 3 samples and keeps only unanimous letters (`consensus_samples: 3`); the report computes it exactly from all draws of 3 of the 5 runs (section 7.5);
  - consistency: Stable correct (right in all 5) and Luck (right in some only).
- Chance of passing all runs, by per-run probability of being right:

| Runs | Pure guess (50%) | 80% | 90% | 95% | 99% |
|---|---|---|---|---|---|
| 3 | 12.5% | 51% | 73% | 86% | 97% |
| **5** | **3.1%** | **33%** | **59%** | **77%** | **95%** |
| 10 | 0.1% | 11% | 35% | 60% | 90% |

- 3 runs let a coin-flip question pass 1 time in 8, and give only one draw of 3 for the consensus projection. 5 runs cut the coin flip to 1 in 32 and give 10 draws of 3. 10 runs double the cost for little gain.

### 7.3 Secondary measures
| Measure | Why |
|---|---|
| Luck | How much of a model's score is unstable. |
| Confident-wrong rate | Answers that would mislead an operator. |
| Unsure rate, accuracy when answered | A cautious model with gaps vs a reckless one. |
| Misconception rate | How often the misconception option is picked. The core Level 400 signal. |
| Override rate | Agent E2 answers that state the misconception although every needed file was read ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 1). |
| Retrieval recall | Agent E2 only: whether the needed files reached the model; separates retrieval from reasoning. |
| Stages used, verifier flags | Which stages of Agent E2 acted (compute, gap follow-up, repair, consensus), and the web reference's tool calls. |
| Per area, per task, per level, per input | Diagnosis only (small counts). |

### 7.4 Final score
- One number, 0-100%, for each model and mode (Base, Agent E2, web). Sub-scores support it: by answer type, by input type, by level.
- Question credit, 0 to 1, the mean of the 5 runs (author, 2026-11-13):
  - the share of runs with exactly the right letters.
- Worst run: the same score with each question on its lowest run. Reported next to the final score as consistency; not a gate.
- Final score = sum of question credits / number of questions. Every question weighs the same, whatever its level, answer type or input type.
- Sub-score = the same mean within one group. A question counts for every input type it includes. The mix of the set (section 3.6) sets how much each group weighs in the final score.
- Reasons:
  - mean, not worst run: an operator asks once and gets one answer; the mean of the runs is the best estimate of that answer's quality. The worst run measures something else (does it never fail?) and stays in the report as consistency. Until 2026-11-13 the worst run counted;
  - one weight per question: no group can carry the score by a formula choice; coverage keeps the mix honest (section 3.7);
  - no part credit: a partly right set of letters is a wrong answer an operator would act on.
- Confident-wrong rate: wrong letters that are not Unsure.
- Margin: 95% interval on the final score from the number of questions (section 4).
- Runner: [benchmark/runner/report.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/report.py), function `final`. Report table `Final score`.

### 7.5 Release gate
- Read on Agent E2 as shipped: the local model running the one pipeline of [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md) (author, 2026-11-14), with the deployment profile (section 8). The retrieval levels (section 9) are read on its reading set.
- All must hold. One number alone can be carried by easy questions or bought with confident guesses.

| Gate | Limit | Why |
|---|---|---|
| Final score, run set | at least 85% | Margin about ±5 at 200 questions (section 4); below 85 an operator stops trusting the answers |
| Level 400 sub-score | at least 80% | The one sub-score that gates. The mission is Level 400; Level 100-300 can carry the total |
| Confident-wrong rate | at most 3% | The answers an operator acts on. A wrong answer marked Unsure is not one of them |
| Up-front misconceptions (the `## Misconceptions` lines marked `up_front`) | none stated as true | They are given up front; stating one is a harness or model defect, not a gap. Author check of the answers |
| Held-out set (30) | at most 11 points below the run set | One-sided 95% for about 200 against 30 questions at about 87%: a larger drop means the knowledge base or retrieval is fitted to the visible questions |

- Consensus: the deployed profile sets `consensus_samples: 3`; the benchmark runs one sample and reads the projection next to the gate in each `report.md` (section Consensus of 3, projected), the exact mean over all draws of 3 of the 5 runs. Same result at a third of the cost.
- The gap to the frontier model is not a gate. It is an outcome, reported next to the gate with its paired test (section 8). The benchmark is not designed to beat anyone: it is fair (section 6.1) and its questions are hard; a deeper knowledge base shows as a higher score.
- Why 85%, not 90%: at about 200 questions 85 and 90 still overlap inside the margin (±5); the confident-wrong limit does more for the operator than 5 more points.
- Reading the gap: within the margin (printed in the report) it is a tie; the paired test says whether a larger gap is more than luck.
- Held-out set:
  - 30 questions drawn at release in the proportions of the run set at that time (level, answer type, input; `coverage.py`), from real questions where the author has them (Q207).
  - Written by a session that does not edit the knowledge base, reviewed by the author, never committed to the repository. Run once, on the release configuration.
  - Why drawn at release, not now: a question that exists while the knowledge base is still edited can leak into it. A fresh draw cannot.
  - Why the 11-point limit replaces "within 5 points": on 20-30 questions the noise alone is about ±13 points, so a 5-point rule fails or passes by luck.
- Expected frontier score: about 80%. Measured on 2026-11-13 (Claude Opus 5.5 with web search, previous state of the question set, archived): final 81%, Level 400 79%, confident-wrong 12%. It fails the gate too. The expert estimate of 2026-11-12 (about 70%) was too low: the frontier model knows each public mechanism, and loses mostly on the vantage point, the combination of readings and the Level 300 rule of thumb.
- Target: 99%, a direction. The set cannot prove it (section 4).
- Runner: [benchmark/runner/report.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/report.py), functions `gate` and `mcnemar`, report table `Release gate`: final score, Level 400 and confident-wrong as the gate; the gap and the paired test as outcomes. The misconception check and the held-out set are read outside the report.

## 8. Comparison design
- Agent E2 has one pipeline (author, 2026-11-14): the benchmark runs it as shipped, not modes of it. The benchmark is a proof, not a goal ([CLAUDE.md](https://github.com/e1-rahabok/agent-e2/blob/main/CLAUDE.md), Evaluation). Why classic and agentic mode were removed: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 2.
- The release score uses the deployment profile of the harness: same prompt, reading plan, context window and budgets as the product. Time is replaced by a turn limit derived from the target GPU. Other settings run only as named experiments. See [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 5.
- Two runs per candidate (author, 2026-11-14): Base, the model alone (`baseline`), and Agent E2 as shipped (`agent-e2`) ([benchmark/runner/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/README.md)). Scores of earlier generations (classic and agentic modes) are archived and not compared.
- Reference: the frontier model as an administrator uses it: Claude Opus 5.5 with web search available (mode `web`), effort medium, no knowledge base (Q164). The model gets the baseline prompt and two tools, web search and page fetch, offered with `tool_choice: auto` and no instruction to search: it decides whether to search, and can answer with no search at all, as in a chat product with search on. At most 5 tool calls. The mode name says what is available, not what is forced. No run with the tools removed: a user cannot switch search off in a chat product by typing, so that run measures nothing a user meets (author, 2026-11-13). The report records the tool calls per answer (`tools_used`), so how often Opus chose to search is read from the results. The report gives the gap to it and a one-sided exact McNemar test at α 0.05: an outcome, not a gate (section 7.5).
- Paired comparison: models are compared question by question on the same set, not only by totals.
- Between candidate models, a gap smaller than the margin is a tie; the smaller model wins a tie. Against the frontier model, a gap within the margin is a tie.
- Run matrix of a round: 3 candidates x 2 modes (Base, Agent E2) plus the frontier reference x 1 mode (`web`), every question of the run set, 5 runs. Time and cost: [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md), projected by the preflight sample. Prices, rate limits and a model's thinking change both numbers: run the preflight before each round.

## 9. Retrieval check
- The final score mixes harness and model. The retrieval check separates them: [benchmark/runner/retrieval_eval.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/retrieval_eval.py) checks, without a model, whether each question's `knowledge` files are found and placed in Agent E2's reading set (the code-only case). Guide: [benchmark/retrieval-check.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/retrieval-check.md).
- Levels and current numbers: [benchmark/retrieval-check.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/retrieval-check.md) and [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M3. Re-baselined when the question set changes (Q206).
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
| Frontier model knows public material | Base and the web reference test exactly that. The knowledge base must add what public material lacks. |
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
9. Does `coverage.py` show a tag value with no question (section 3.7)?
10. Does a field question the set has nothing like call for a new question?

## 12. Status
- The run set is every question with status draft or reviewed. Its counts: `python3 project/tools/coverage.py`. Retired questions: [project/archive/benchmark-questions](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-questions).
- Every synthetic question was checked by an independent review agent, which tried to break each key against the knowledge files and the vendor documents; the defects found were fixed. Author questions from the review: all answered (Q182-Q191). Knowledge fixes found on the way: [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), M1.
- Status draft: each question counts after the author's review (section 6.2).

## 13. Screenshot questions (after 1.0)
- Purpose: administrators upload screenshots and ask the agent to explain the problem, often several at once, from different tools.
- 1.0 has the author's L4-03 and the five reactivated on 2026-11-13. After 1.0 the screenshot set grows, a few per source (esxtop, vCenter, VCF Operations).
- Reading screenshots stays a basic requirement: a model without vision is not a candidate ([benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md)).
- A screenshot question carries all its images in `attachments`; every image is sent with the same prompt. The prompt states the problem in words; the images supply the values. Images are masked (host and customer names) before commit.

### 13.1 Table questions
- Purpose: administrators export data and ask about it: a vCenter chart export, a VCF Operations list or metric export, esxtop batch output.
- 1.0 tables are small: at most about 3,000 tokens (`question_csv_max_chars` in [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml), checked by lint), about 60 rows by 8 columns. The runner puts the CSV after the prompt as text (`Question.tables`); the deployed model's window is 32,000 tokens.
- Larger exports (hundreds of rows) need a table tool in the harness (filter, sort, aggregate, top-N). After 1.0.
- Column names are the product's metric names (for example `CPU|Ready (%)`, `Usage for vm-01 (Percent)`), so the reading follows the product, not the header's English.
- A CSV is generated by a seeded script, then checked: every value the key relies on is in it, and nothing contradicts the key. Time stamps, object names and noise are realistic; names are invented, never a customer's.

## 14. Free-text answers
- Not in the benchmark (author, Q199 F, 2026-11-14). The judge model that scored them 0-3 is archived with its rubric ([project/archive/legacy/judge-2026-11-14/judge.py](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/legacy/judge-2026-11-14/judge.py)); this section's earlier rules are in git history.
- Free-text answers are measured in the field: the author judges real questions in the live test ([benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md), step 9) and operators rate every answer in the product ([MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md), section 5, Feedback).

## 15. Target history
- Goal: the local model with the knowledge base answers better than the best frontier model without it.
- Target: 99% final score on Agent E2. See section 7.4.
- Minimum: the release gate, section 7.5 (Q130, 2026-11-12; set size and held-out rule revised 2026-11-12, question set 1.0).
- No candidate is dropped on a partial run or a small sample.
- What 99% requires: at about 200 questions, 99% allows 2 wrong questions; proving 99% needs about 300 questions with none wrong (section 4). Answer keys must be correct: every wrong answer from the best model gets an author check.
- Status: no round on Agent E2 yet (built 2026-11-14). The previous generation and the frontier reference both failed the gate (archived: [analysis-2026-11-13.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md)).

## 16. Decision rules
- Mode: one pipeline, Agent E2, the neuro-symbolic expert system ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md)), carries the release gate (author, 2026-11-14; replaces Q130, agentic as the shipped mode). No fallback mode: the model makes no tool calls.
- Pick the model: highest final score on Agent E2; then lowest confident-wrong rate; ties go to the smaller model.
- A model that breaks the answer format on more than 10% of answers is dropped. (An unreadable case does not count: the code-only case takes its place.)
- Knowledge base lift: Agent E2 must beat Base in every area. An area with no lift is a knowledge or retrieval problem, not a model problem.
- 70B challenger: only if the best 30B-band result loses points through reasoning errors (the trace shows the right files were read).
- A challenger that needs more hardware (dense about 70B, or a 96 GB GPU) is kept only if it beats the best current candidate by more than the margin and its override rate is not higher. Reason: [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md), section 1.

## 17. Outputs
- [benchmark/results/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/README.md): one analysis of all runs of a round, written when the last run finishes. One folder per run, named `<date>-<model>`.
- A short report per run in [benchmark/results](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results): score matrix, consistency, worst cases, trace links.
- Every wrong answer tagged with a cause (knowledge gap, retrieval miss, model error) and turned into a plan item or an author question.
