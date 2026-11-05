# Benchmark design

For human experts who check that the benchmark is valid and complete. Not indexed.
Runner and commands: `benchmark/runner/README.md`. Question format: `benchmark/README.md`. Models and judge: `benchmark/models.md`. Trap definition: `KNOWLEDGE-ENGINEERING.md`, section Traps and Level 400.

## 1. Claim
- Claim: a local open-weight model on one GPU (`benchmark/models.md`), with this harness and knowledge base, answers Level 400 vSphere operations questions better than the best frontier model without them.
- Release gate: final score at least 85%. Target: 99% (author, 2026-11-03). Final score: section 7.4.
- The benchmark must:
  1. rank candidate models and answer modes against each other;
  2. show whether a configuration clears 85%;
  3. show how close it is to 99%, and state what the number proves.

## 2. Scope
| Measured | Not measured (and where it is measured instead) |
|---|---|
| Correct reading of metrics: mechanism, vantage point, unit, rollup | Installation, configuration steps, UI navigation (out of scope for the product) |
| Resistance to traps (see `KNOWLEDGE-ENGINEERING.md`, section Traps and Level 400) | Writing style of free-text answers (the judge scores facts only, section 14) |
| Combining several facts (multi-hop), including arithmetic | Speed and cost (logged per answer, judged separately) |
| Following a troubleshooting flow to a conclusion | Live-system troubleshooting (after 1.0) |
| Reading one or more screenshots (esxtop, vCenter UI, VCF Operations UI) | Data-file parsing (release 1.2) |
| Knowing the limits: choosing Unsure instead of guessing | Cost and price (out of scope, author 2026-11-04) |
| Consistency: the same answer on every run | |
| Answering in conversation, without options (free text, judged) | |

- Multiple choice is the bulk because it can be scored without a judge, on thousands of answers, with no scorer bias. Guessing is handled by the scoring in section 7.
- Free text is kept because a real user asks without options. A model can pick the right option yet fail to raise the point unprompted. A judge scores it (section 14).

## 3. Blueprint
The blueprint defines the domain and how the 100 questions sample it. A reviewer can check coverage question by question.

### 3.1 By area (author, 2026-11-04)

| Area | Share of the 100 questions | Covers |
|---|---|---|
| CPU | 25% | vCPU states, Ready, Co-stop, Usage vs Utilization, Hyper-Threading, frequency, NUMA |
| Memory | 25% | Consumed, Active, balloon, swap, compression, Latency, tiering |
| Storage | 20% | latency stack, layers, outstanding IO, space, IP storage |
| Network | 15% | drops, throughput, units, offload |
| System | 20% | the object as a whole: KPIs, capacity, availability, DRS, admission control, provider/consumer, statistics and rollups, GPU, Guest OS vs VM boundary |

- The shares add up to more than 100% because a question can span several areas. A question on VM CPU Ready caused by host memory swapping counts for CPU and Memory.
- Each question lists every area it touches (`technology` in its metadata, values from `project/tools/tags.yaml`). The share is the minimum number of questions that touch the area.
- About 5 questions sit outside the knowledge base. The system answers them from the model's own knowledge (knowledge base first, own knowledge where it is silent: author, Q038, 2026-11-05). They test that a gap does not turn into a wrong answer. They are spread across the areas.
- Per-area scores (15-25 questions) are diagnostic only (margin about ±15-20 points). Decisions use the total.

### 3.2 By level

| Share | Level | What it proves | A failure means |
|---|---|---|---|
| 20 | Recall | The right file is found and read. | Retrieval bug, not reasoning. |
| 50 | Level 400 | Mechanism, vantage point, same-name and other traps. | Knowledge gap or reasoning limit. |
| 20 | Multi-hop | 3 or more files combined, often with arithmetic or units. | Chaining or calculation failure. |
| 10 | Screenshot | A chart or table image read correctly, then the knowledge applied. | Vision failure (compare with the text track). |

- At least 10 of the Level 400 and multi-hop questions require a troubleshooting flow (a `diagnosis/` file) to be followed in order.

### 3.2.1 By kind (proposal 2026-11-05, author to confirm: Q054)
Each question has one kind. The kinds give the sub-scores (section 7.4).

| Kind | Proposed share of 100 | Scored by |
|---|---|---|
| Multiple choice (text only) | 60 | Exact letters |
| Screenshot (one or more images, any format) | 20 | Exact letters, or the judge for free text |
| Conversation (free text or compound, no image) | 20 | The judge |

- Screenshot rises from 10 to 20: vision is now a basic requirement and a sub-score needs enough questions to read (section 13).
- The level shares above still apply across all kinds.

### 3.3 Coverage constraints
| Constraint | Minimum |
|---|---|
| Each trap type in `KNOWLEDGE-ENGINEERING.md`, section Traps and Level 400 (12 types) | 3 questions each |
| Same-name pairs: one label asked on two objects (VM vs ESXi, ESXi vs cluster) | 5 pairs |
| Questions about the VM / ESXi / cluster / datastore | 30 / 20 / 10 / 5 |
| Questions outside the knowledge base (answered from the model's own knowledge) | 5 |
| Questions where the knowledge base and the vSphere documentation disagree | 3 |
| Questions needing the calculator (summation to %, units, capacity) | 5 |
| Screenshot questions per source: esxtop, vCenter UI, VCF Operations UI | 5 each |
| Screenshot questions with 2 or more images (for example a chart and its esxtop view) | 5 |

- Every question records what it covers in its metadata (`level`, `tests`, `knowledge`; `trap_type` to be added), so coverage is counted by a script, not by eye.

### 3.4 Answer-key shape
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
- Coverage: the blueprint (section 3) makes every area, object, layer and trap type count. No area can carry the score alone.
- Balance of difficulty: recall questions anchor the scale. If recall fails, the problem is retrieval, and harder questions are not interpreted.
- Paired questions: the same concept on two objects. A model that answers both right understands the vantage point; one that answers one right was lucky or pattern-matched.
- Independence: no question gives away another's answer. No two questions test the same single fact.
- Every option is decidable from the knowledge base (or, for questions outside it, from established vSphere knowledge the author confirms). A question the knowledge base cannot settle is rewritten or removed, never kept as a coin flip.

## 6. Question writing
- Stem: a realistic situation with the values an operator would see (counter names, numbers, units, time window). Not a definition prompt, except for recall questions.
- Options:
  - one fact per option;
  - similar length and style, so length gives no hint;
  - no "all of the above", no double negatives;
  - every wrong option is wrong for a reason the knowledge base states;
  - one option is the trap: the conclusion a Level 300 reader would draw. It is named in `## Likely wrong answer`.
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

- Two numbers are reported for multiple choice: **Stable correct** (absolute, against the fixed set; it is the multiple-choice question credit in the final score, section 7.4) and **confident-wrong rate** (share of answers that are wrong and not Unsure; target near 0).
- The model is told: a wrong answer is worse than Unsure, because an operator would act on it; if it cannot decide every option, choose Unsure.

### 7.1 No points, no -1 (author, 2026-11-04)
- An earlier version scored +1 / 0 / -1 and reported "Net points". It was dropped:
  - The benchmark is an absolute measurement against a fixed question set, not a ranking against other benchmarks. Stable correct already counts only exact answers; a wrong answer and an Unsure both count as not correct, so the -1 never changed the headline.
  - Net points mixed two things an operator cares about separately: how often the system is right, and how often it is confidently wrong. Two plain shares say both without arithmetic.
- In practice the -1 changed the model's behaviour through the prompt: told that a wrong answer costs a point, models chose Unsure instead of guessing. That behaviour is kept with a plain rule in the prompt ("a wrong answer is worse than Unsure").
- Unsure applies to an AI too. On a dark site nobody checks the answer against the Internet, so "the knowledge base does not settle this" is the safe answer.
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
| Trap rate | How often the trap option is picked. The core Level 400 signal. |
| Not-covered accuracy | Guessing outside the knowledge base. |
| Retrieval recall | Whether the right files were found; separates retrieval from reasoning. |
| Tools used, verifier flags | Whether the harness tools were used (agentic mode). |
| Per area, per level | Diagnosis only (small counts). |

### 7.4 Final score (author, 2026-11-05)
- One number, 0-100%, for each model and mode. Sub-scores support it: multiple choice, screenshot, conversation.
- Question credit, 0 to 1, taken from the worst of the 5 runs:
  - multiple choice: 1 if the letters are exactly right in every run, else 0 (Stable correct);
  - free text and compound: the lowest judge score over the runs, divided by 3 (0, 0.33, 0.67, 1).
- Final score = sum of question credits / number of questions. Every question weighs the same, whatever its kind.
- Sub-score = the same mean within one kind. Final = the sub-scores weighted by their question counts, so the set mix (section 3.2.1) sets the weights.
- Screenshot questions are scored with their images. There is no text-only track: every candidate reads images (`benchmark/models.md`).
- Reasons:
  - worst run, not mean: the same rule as Stable correct. An answer right in 4 runs of 5 is luck, and an operator gets one run;
  - one weight per question: no kind can carry the score by a formula choice; the blueprint decides the mix;
  - judge score / 3: a partly right free-text answer (right conclusion, missing reason) earns part credit, as a human examiner would give. Multiple choice has no part credit, because a partly right set of letters is a wrong answer an operator would act on.
- Confident-wrong rate covers both: wrong letters that are not Unsure, and free-text answers scored 0 that do not say the information does not settle it.
- Margin: 95% interval on the final score from the number of questions (section 4). Sub-scores have wider margins (20 questions: about ±16 points) and are diagnostic.
- Runner: `benchmark/runner/report.py`, function `final`. Report table `Final score`.

## 8. Comparison design
- Reasons for running both modes and for the call limit: `ARCHITECTURE.md`, sections 3 and 4.
- The release score uses the deployment profile of the harness: same prompt, tools, context window and budgets as the product. Time is replaced by a turn limit derived from the target GPU. Other settings run only as named experiments. See `ARCHITECTURE.md`, section Benchmark and deployment.
- Every model runs in three modes on the same questions: baseline (no knowledge base), classic (one lookup), agentic (model-driven lookups). See `benchmark/runner/README.md`.
- Reference: the best frontier model in baseline mode. The claim in section 1 is met when a local configuration's final score exceeds it by more than the margin.
- Paired comparison: models are compared question by question on the same set, not only by totals.
- A gap smaller than the margin is a tie; the smaller model wins a tie.
- Run matrix at 100 questions: 10 models x 3 modes x 100 questions x 5 runs = 15,000 answers, about US$ 25-40 and 2-4 hours (re-check prices and rate limits before each run).

## 9. Retrieval check
- The final score mixes harness and model. The retrieval check separates them: `benchmark/runner/retrieval_eval.py` checks, without a model, whether each question's `knowledge` files are found and placed in the classic context.
- Result 2026-11-04 (28 questions, hybrid search): 67% of needed files reach the context; all needed files in 12 of 28 questions. This caps classic mode. Improve it before judging the model.
- Every wrong answer is classified: file not in context (harness or knowledge), file in context but answer wrong (model or prompt), file not in the knowledge base (gap). Detail: `ARCHITECTURE.md`, section 8.

## 10. Validity threats
| Threat | Guard |
|---|---|
| Wrong answer key | Every wrong answer from the best model is checked by the author: model error, knowledge gap, or key error. Keys cite knowledge ids. |
| Knowledge base fitted to the benchmark (Claude edits the knowledge base and can read the questions) | A held-out set of about 20% of the questions, kept by the author outside the repository and run only before releases. Fixes to the knowledge base must be general (a fact or a trap), never a question-specific answer. |
| Questions written by the knowledge base's own author favour its wording | Paraphrased stems; questions from real tickets and field forums; frontier baseline as an outside reference. |
| Synthetic questions drafted by Claude mirror Claude's view | Author approval required; share capped at about 30% of the set. |
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
3. Is the trap option a mistake a competent Level 300 operator would plausibly make?
4. Does any option give the answer away by wording, length or count?
5. Does it duplicate another question's fact?
6. Does it test operations knowledge, not trivia (UI clicks, product history, prices)?

For the set:
7. Do the counts match the blueprint in section 3?
8. Is every trap type covered at least 3 times?
9. Are at least 20% of questions from sources other than the author's books?

## 12. Status (2026-11-05)
- 28 questions, all scored automatically: 15 multiple choice, 3 screenshot (2 multiple choice, 1 compound), 10 conversation (free text). Before 2026-11-05 the runner skipped the 11 free-text and compound questions.
- Gaps against the blueprint: screenshot 3 of 20 (vCenter and spec sheets only; no esxtop or VCF Operations; one question with 2 images), network 0 of 15, storage 1 of 20, system about 3 of 20, recall 0 of 20, Not covered 0 of 5; multi-area tagging (`technology`) and `trap_type` not yet recorded.
- Next: write the questions to the blueprint from the author's book quizzes; add `trap_type`; add a coverage script; set up the held-out set.

## 13. Screenshot questions
- Purpose: administrators upload screenshots and ask the agent to explain the problem. Often several at once, from different tools: esxtop, the vCenter UI, the VCF Operations UI (author, 2026-11-05).
- Reading screenshots is a basic requirement. A model without vision is not a candidate (`benchmark/models.md`). There is no text-only track.
- A screenshot question can be multiple choice or free text. It carries all its images in `attachments`; every image is sent with the same prompt.
- Coverage: section 3.3 (5 questions per source, 5 questions with 2 or more images).
- Sample size: the sub-score margin at 85% is about ±22 points with 10 questions, ±16 with 20, ±13 with 30. 20 is the proposal (section 3.2.1); 30 is needed before the sub-score alone decides between two models.
- The prompt states the problem in words. The images supply the values.
- Images: author screenshots with host and customer names masked before commit.

## 14. Free-text questions and the judge
- Questions with `format: free-text` or `compound` are answered without options and scored 0-3 by a judge model. Code: `benchmark/runner/judge.py`.
- The candidate gets the same harness, modes and tools as for multiple choice, with an open-answer prompt: plain text, at most 250 words, conclusion first, then mechanism and reason, then what to check next; say so when the information does not settle the question. Code: `harness/modes.py`, `PROMPTS['open']`.
- The judge gets: the prompt, the images, `## Expected key points`, `## Likely wrong answer`, and the answer. The candidate never sees the key.
- Rubric:

| Score | Meaning |
|---|---|
| 0 | Wrong, falls into the likely wrong answer, or contradicts a key point. Also: says the information does not settle it (marked unsure). |
| 1 | Avoids the likely wrong answer, but the reason is missing or wrong. |
| 2 | Correct conclusion with the right reason (mechanism or vantage point from the key points). |
| 3 | As 2, and states what to check next, or covers every key point. |

- Judge rules (in its prompt): judge facts, not style or length; a contradiction of a key point caps the score at 0; the key points are the truth even where general IT practice differs; reward nothing the key points do not contain.
- Reply: one JSON object (`score`, `trap`, `unsure`, `missed`, `reason`). One retry when it is not valid JSON; then the answer counts as failed and `--resume` retries it.
- Each run of a question is judged separately. The question credit is the lowest score / 3 (section 7.4).
- Judge choice: a frontier model, never a candidate, from a different vendor than the frontier reference, with vision, temperature 0. See `benchmark/models.md`, section 6.
- Recorded per answer in `answers.csv`: `judge_model`, `judge_score`, `judge_missed`, `reason`, `trap`, `unsure`, and the answer text.
- Checks on the judge:
  - the author reviews every score 0 and every question where runs disagree by 2 or more points;
  - an author score overrides the judge: correct the key points, then re-score;
  - a key point the judge misreads is rewritten as one testable fact per bullet.
- Cost: one judge call per free-text answer, about 1,500 input tokens.

## 15. Target history (author, 2026-11-03)
- Goal: the local model with the knowledge base answers better than the best frontier model without it.
- Target: 99% final score on the question set (chosen mode). See section 7.4. (Before 2026-11-05: Stable correct on multiple choice only.)
- Minimum: 85% final score. A model below 85% is not usable.
- mistral/ministral-8b dropped from future runs (author, 2026-11-03): 29-40% exact in benchmark 20261103-081849.
- The other candidates stay until the question set reaches 100 (author, 2026-11-03); 3 were added on 2026-11-04 (10 in total). No model is dropped on the 17-question results: the margin (about ±20-24 points) is too wide.
- Reference point: the best frontier model in baseline mode (no knowledge base). Measured in each benchmark.
- What 99% requires:
  - At 17 questions, 99% allows no wrong question. One wrong question = 94%.
  - At 100 questions, 99% allows 1 wrong question, but even a perfect score proves only about 96% (section 4). Proving 99% needs about 300 questions.
  - Answer keys must be correct. Every wrong answer from the best model gets an author check: model error, knowledge-base gap, or key error.
- Status at benchmark 20261103-081849: best small model 58% exact (classic). Gap: 41 points.

## 16. Decision rules
- Pick the mode: agentic must beat classic RAG by more than the margin on the same model, or classic RAG stays the default (simpler, cheaper).
- Pick the model: highest final score in the chosen mode; then lowest confident-wrong rate; ties go to the smaller model.
- Agentic is dropped for a model with more than 10% fallbacks.
- Knowledge base lift: kb modes must beat baseline in every area. An area with no lift is a knowledge or retrieval problem, not a model problem.
- Screenshot upload is part of the product. A model whose screenshot sub-score is far below its multiple-choice sub-score (more than the margin) is a vision problem: check the image, then the model.
- 70B challenger: only if the best 30B-band result loses points through reasoning errors (trace shows the right files were read).
- A challenger that needs more hardware (dense about 70B, or a 96 GB GPU) is kept only if it beats the best current candidate by more than the margin and its override rate is not higher. Reason: `benchmark/models.md`, section 1.

## 17. Outputs
- `benchmark/results/results.csv`: one row per answer (add columns: mode, run, provider, temperature, options_order, answer_letters, exact, partial, trap, retrieval_recall, steps, tokens, parse_ok).
- A short report per run in `benchmark/results/`: score matrix, consistency, worst cases, trace links.
- Every wrong answer tagged with a cause (knowledge gap, retrieval miss, model error) and turned into a to-do or author question.
