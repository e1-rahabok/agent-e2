# Repository terms

One English word per concept in this repository. Not indexed.
- Vocabulary of the knowledge itself (vSphere, VCF, Guest OS terms): [`knowledge/glossary.md`](../knowledge/glossary.md).
- This file: words for the repository's own parts.
- When two words name the same thing, pick one, add it here, and replace the other. When one word names two things, split it here.
- [`project/tools/lint.py`](tools/lint.py) flags the replaced words listed in [`project/tools/tags.yaml`](tools/tags.yaml), `avoid_repo_terms`.
- Exempt: [`project/author-questions.md`](author-questions.md) (the author's own words) and records: [`project/archive/`](archive), `project/review-*.md`, [`benchmark/results/`](../benchmark/results).

## Two contexts for one English word
English words carry a general meaning and a VMware operations meaning. A word is chosen so that both readers take it the same way.
- General: the meaning in daily life, between people.
- VMware operations: the jargon of a VMware administrator. In operations, a case is an issue to investigate and solve (a support case, a ticket). A use case is a scenario.
- So the benchmark does not use case. Its items are questions: they are answered, not investigated. A question can have several parts.
- The product does: the agent reads each question into a case, the issue it works on (proposal, 2026-11-14, table below).
- Quiz is the author's word for his source documents: it checks what the reader knows (it is not a request for something unknown), and it reads lighter than an exam.

## Terms
| Use | Means | Do not use for it |
|---|---|---|
| sources | Source documents the knowledge is written from ([`project/sources/`](sources)): book chapters, vendor PDFs. Read-only. Proposal, for the author | raw input |
| benchmark | The proof of the product: question set, runner, judge, results (`benchmark/`). Also one execution of it: every candidate, every mode, 5 runs; one folder per model, `benchmark/results/<date>-<model>/` (benchmark/runner/naming.py) | Auto Test, test, evaluation, benchmark run |
| run | One pass through all the questions, by one model in one mode (`baseline` or `agent-e2` for a candidate, `web` for the frontier reference). A benchmark has 5 runs (`runs: 5`, column `run`). Each run is a repeat of the same questions; the answers differ | repeat, iteration |
| question | One benchmark item: one file in [`benchmark/questions/`](../benchmark/questions) with prompt, answer key and metadata. A benchmark question plays a question a VMware administrator asks the product | case, test case, golden case, exam question |
| question set | All the questions of the benchmark | golden set, case set |
| main file | The one knowledge file that holds a question's answer or misconception; tag `knowledge_main`. Proposal, for the author | first file, primary file |
| release gate | The limits Agent E2 must meet to ship (benchmark/design.md, section 7.5): final score, Level 400, confident-wrong, misconceptions, held-out set (the gap to the frontier model is reported, not a gate) | passing score, pass mark |
| prompt | The `## Prompt` text of a question: the only text sent to the candidate | question text |
| quiz | The author's quiz documents (vSphere Metric Quiz.docx, the book's chapter quizzes): a source of questions, `origin: quiz` | - |
| author question | One entry in [`project/author-questions.md`](author-questions.md) | - |
| knowledge base | The content in `knowledge/` | KB (in prose) |
| Agent E2 | The product: model, harness, agent and knowledge base as shipped. Always both words, like Agent 007. Will run on isvara.io, replacing AskIO | Isvara (the website, not the product); E2 alone |
| neuro-symbolic expert system | What Agent E2 is (2026-11-14): code holds the expert's procedure and the knowledge base's map and decides what to read, compute and ask; the model reads the question and the reading set and writes ([`harness/AGENT.md`](../harness/AGENT.md)) (author, 2026-11-14, Q210) | agentic RAG, classic RAG, mode (for Agent E2 itself) |
| agent | The expert's procedure as code ([`harness/AGENT.md`](../harness/AGENT.md)): it reads the question into a case, plans the reading set from the knowledge base's map, runs the exact tools, decides whether to ask, calls the model to read and write, and checks the answer. The decisions are code; the model is called. Changed 2026-11-14 (was: the model plus the tool loop, in agentic mode, now removed) (author, 2026-11-14, Q210) | tool loop (the old meaning) |
| case | The agent's structured reading of one question: kind, objects, layer, metrics with values, symptom, premise, claims, missing facts, what each screenshot shows ([`harness/AGENT.md`](../harness/AGENT.md), section 4.1; the case state of Q166). The product's word: in operations a case is an issue to investigate. The benchmark still says question for its items (author, 2026-11-14, Q210) | question state, query object |
| reading set | The files and sections the agent gives the model for one question, chosen by the reading plan ([`harness/planner.py`](../harness/planner.py)) (author, 2026-11-14, Q210) | context (alone), seed |
| reading plan | The code that builds the reading set: tiers of named files, search hits, mechanism links and one search per claim ([`harness/AGENT.md`](../harness/AGENT.md), section 4.2) (author, 2026-11-14, Q210) | retrieval (alone), routing |
| harness | The execution environment and guardrails around the model (`harness/`): search engine, catalog, calculator, flow executor, budgets, the verifier. The agent runs on it and uses its tools | wrapper |
| runner | The benchmark code ([`benchmark/runner/`](../benchmark/runner)) | - |
| judge | The model that scores free-text and compound answers 0-3 | grader |
| candidate | A model in the benchmark | model under test, AI under test |
| test | A code test only: [`harness/test_tools.py`](../harness/test_tools.py), [`benchmark/runner/test_runner.py`](../benchmark/runner/test_runner.py) | the benchmark |
| retrieval check | [`benchmark/runner/retrieval_eval.py`](../benchmark/runner/retrieval_eval.py): are the files each question needs found, without a model. Guide: [`benchmark/retrieval-check.md`](../benchmark/retrieval-check.md) | retrieval test, harness-only test |
| frontier reference | The frontier model scored as the bar to beat | - |
| answer key | `answer` and `misconception` letters, `## Expected key points`, `## Likely wrong answer` | key (alone) |
| answer type | How a question is scored: deterministic (option letters) or judged (free text, by the judge) | kind, format, multiple choice vs conversation |
| input type | What the administrator gives besides the prompt: text, table, screenshot | input kind |
| level | 100, 200, 300 or 400 ([`benchmark/design.md`](../benchmark/design.md), section 3.2) | recall, multi-hop |
| attachment | A file listed in a question's `attachments` | - |
| screenshot | An image of a product UI or tool (esxtop, vCenter, VCF Operations) | - |
| author | Iwan Rahabok, who owns the knowledge and reviews it | - |

## Examples
- The benchmark has 5 runs; each run goes through the same questions.
- A question's credit is the mean of its 5 runs; the worst run is reported as consistency (since 2026-11-13).

## Open: one word for two things
- None.
