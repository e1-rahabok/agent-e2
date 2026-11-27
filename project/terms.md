# Repository terms

One English word per concept in this repository. Not indexed.
- Vocabulary of the knowledge itself (vSphere, VCF, Guest OS terms): [`knowledge/glossary.md`](../knowledge/glossary.md).
- This file: words for the repository's own parts.
- When two words name the same thing, pick one, add it here, and replace the other. When one word names two things, split it here.
- [`project/tools/rules_check.py`](tools/rules_check.py) flags the replaced words listed in [`project/tools/rules_check_values.yaml`](tools/rules_check_values.yaml), `avoid_repo_terms`.
- Exempt: [`project/author-questions.md`](author-questions.md) (the author's own words) and records: [`project/archive/`](archive), `project/review-*.md`, [`benchmark/results/`](../benchmark/results).

## Two contexts for one English word
An English word has a general meaning and a VMware operations meaning. Each word here is chosen so that both readers take it the same way.
- General: the meaning in daily life, between people.
- VMware operations: the jargon of a VMware administrator. In operations, a case is an issue to investigate and solve (a support case, a ticket). A use case is a scenario.
- So the benchmark does not say case. Its items are questions, which are answered, not investigated. A question can have several parts.
- The product does use it: the agent reads each question into a case, the issue it works on (Q-E2-210; table below).
- Quiz is the author's word for his source documents. A quiz checks what the reader knows, it does not ask for something unknown, and it reads lighter than an exam.

## Terms
| Use | Means | Do not use for it |
|---|---|---|
| sources | Source documents the knowledge is written from ([`project/sources/`](sources)): book chapters, vendor PDFs, source notes. The author adds them; Claude may edit them | raw input |
| source note | One Markdown file in [`project/sources/`](sources) per topic, a few pages, written with Claude from the author's material, documentation and the environment; its claims cite its evidence. A proposal, for the author to confirm | digest, technical note, staging file |
| evidence | Primary proof a source note cites: a vendor document with version and page, a screenshot, API output, a lab result ([`project/sources/evidence/`](sources/evidence)). A summary written by a model is not evidence. A proposal, for the author to confirm | proof, reference |
| benchmark | The proof of the product: question set, runner, results (`benchmark/`). Also one execution of it: every candidate, every mode, 5 runs; one folder per model, `benchmark/results/<date>-<model>/` (benchmark/runner/run_folder_names.py) | Auto Test, test, evaluation, benchmark run |
| run | One pass through all the questions, by one model in one mode (`baseline` or `agent-e2` for a candidate, `web` for the frontier reference). A benchmark has 5 runs (`runs: 5`, column `run`). Each run is a repeat of the same questions; the answers differ | repeat, iteration |
| question | One benchmark item: one file in [`benchmark/questions/`](../benchmark/questions) with prompt, answer key and metadata. A benchmark question plays a question a VMware administrator asks the product | case, test case, golden case, exam question |
| question set | All the questions of the benchmark | golden set, case set |
| main file | The one knowledge file that holds a question's answer or misconception; tag `knowledge_main`. A proposal, for the author to confirm | first file, primary file |
| release gate | The reference limits for the author's release decision (benchmark/design.md, section 7.5): final score, Level 400, confident-wrong, misconceptions, held-out set (the gap to the frontier model is reported, not a gate) | passing score, pass mark |
| topic | One subject inside a conversation with Agent E2. A conversation (one per PCM context: an object, tab and window) holds topics; a topic holds turns, each a question and its answer. Agent E2 decides whether a question continues the current topic ([`harness/topic_decision.py`](../harness/topic_decision.py)); the user can flip it | thread, session, chat (for one subject) |
| prompt | The `## Prompt` text of a question: the only text sent to the candidate | question text |
| quiz | The author's quiz documents (vSphere Metric Quiz.docx, the book's chapter quizzes): a source of questions, `origin: quiz` | - |
| author question | One entry in [`project/author-questions.md`](author-questions.md) | - |
| knowledge base | The content in `knowledge/` | KB (in prose) |
| Agent E2 | The product: model, harness, agent and knowledge base as shipped. Always both words, like Agent 007. Will run on isvara.io, replacing AskIO | Isvara (the website, not the product); E2 alone |
| neuro-symbolic expert system | What Agent E2 is: code holds the expert's procedure and the knowledge base's map, and decides what to read, compute and ask; the model reads the question and the reading set and writes ([`harness/AGENT.md`](../harness/AGENT.md)) (Q-E2-210) | agentic RAG, classic RAG, mode (for Agent E2 itself) |
| agent | The expert's procedure as code ([`harness/AGENT.md`](../harness/AGENT.md)): it reads the question into a case, plans the reading set from the knowledge base's map, runs the exact tools, decides whether to ask, calls the model to read and write, and checks the answer. The decisions are code; the model is called. (Q-E2-210) | tool loop (the old meaning) |
| case | The agent's structured reading of one question: kind, objects, layer, metrics with values, symptom, premise, claims, missing facts, what each screenshot shows ([`harness/AGENT.md`](../harness/AGENT.md), section 4.1; the case state of Q-E2-166). The product's word: in operations a case is an issue to investigate. The benchmark still says question for its items (Q-E2-210) | question state, query object |
| reading set | The files and sections the agent gives the model for one question, chosen by the reading plan ([`harness/reading_plan.py`](../harness/reading_plan.py)) (Q-E2-210) | context (alone), seed |
| reading plan | The code that builds the reading set: tiers of named files, search hits, mechanism links and one search per claim ([`harness/AGENT.md`](../harness/AGENT.md), section 4.2) (Q-E2-210) | retrieval (alone), routing |
| harness | The execution environment and guardrails around the model (`harness/`): search engine, catalog, calculator, flow executor, budgets, the verifier. The agent runs on it and uses its tools | wrapper |
| runner | The benchmark code ([`benchmark/runner/`](../benchmark/runner)) | - |
| Enterprise Readiness | The category of mandatory-by-policy components an enterprise requires (availability, recoverability, security, observability, governance, IT operations management, dev/test/QA copies). It is not virtualization overhead | enterprise requirement cost, enterprise overhead |
| judge | The model that scored free-text answers 0-3; archived (Q-E2-199): every question is multiple choice | grader |
| candidate | A model in the benchmark | model under test, AI under test |
| test | A code test only: [`harness/test_harness.py`](../harness/test_harness.py), [`benchmark/runner/test_runner.py`](../benchmark/runner/test_runner.py) | the benchmark |
| retrieval check | [`benchmark/runner/retrieval_check.py`](../benchmark/runner/retrieval_check.py): are the files each question needs found, without a model. Guide: [`benchmark/retrieval-check.md`](../benchmark/retrieval-check.md) | retrieval test, harness-only test |
| frontier reference | The frontier model scored as the bar to beat | - |
| answer key | `## Answers` (the correct letters), `## Explanation`, metadata `misconception` | key (alone) |
| answer type | How a question is scored: deterministic (option letters); the only type (Q-E2-199) | kind, format, multiple choice vs conversation |
| input type | What the administrator gives besides the prompt: text, table, screenshot | input kind |
| level | 100, 200, 300 or 400 ([`benchmark/design.md`](../benchmark/design.md), section 3.2) | recall, multi-hop |
| attachment | A file listed in a question's `attachments` | - |
| screenshot | An image of a product UI or tool (esxtop, vCenter, VCF Operations) | - |
| author | Iwan Rahabok, who owns the knowledge and reviews it | - |

## Examples
- The benchmark has 5 runs, and each run goes through the same questions.
- A question's credit is the mean of its 5 runs. The worst run is reported as consistency.

## Code file names
A reviewer reads a large system top down: folder, then file name, then code. The file name is the first explanation, so it must say what the file is without opening it. Applies to every code file (`.py`, `.yaml`, `.sh`) in `harness/`, [`benchmark/runner/`](../benchmark/runner), [`project/tools/`](tools).
- Name what the file is, in 2 to 3 words, noun first: `knowledge_search.py`, `round_executor.py`. No abbreviation (`kb`, `llm`, `calc`, `refs`) and no lone generic word (`web`, `core`, `health`, `primer`).
- Python files join words with `_` (Python cannot import a name with `-`); knowledge YAML files use `-`, like every knowledge id.
- A test file is `test_<what it tests>`.
- Names fixed by Python or Claude Code stay: `__init__.py`, `__main__.py`, `settings.json`. Export modules keep their question number: `q0368_task_manager_ready_high.py`.
- One word, one meaning across all file names. A word a VMware administrator already uses (host, snapshot, case, health check) is not used for anything else.

| Word in a file name | Means | Not used for |
|---|---|---|
| question | benchmark question | the user's question (`user_`), an author question (`author_`) |
| user | the person who asks Agent E2 | - |
| author | the knowledge owner | - |
| answer | the reply to a question | the author's reply (`author_replies`) |
| run | one model's pass through the questions (noun) | the verb: a whole round is `round_executor` |
| round | all runs of one benchmark execution | - |
| check | verify against an expectation | (`verify` is not used) |
| search | search in the knowledge base | the public web (`public_web_lookup`) |
| knowledge | the knowledge base | - |
| executor | code that carries out steps one by one | - |
| inference provider | a company hosting the model behind the gateway | ESXi host |
| backup | copy of the run folders | VM snapshot |
| export | a file in a product's export format | - |

## Open: one word for two things
- None.
