# Repository terms

One English word per concept in this repository (author, 2026-11-05). Not indexed.
- Vocabulary of the knowledge itself (vSphere, VCF, Guest OS terms): `knowledge/glossary.md`.
- This file: words for the repository's own parts.
- When two words name the same thing, pick one, add it here, and replace the other. When one word names two things, split it here.
- `project/tools/lint.py` flags the replaced words listed in `project/tools/tags.yaml`, `avoid_repo_terms`.
- Exempt: `project/author-questions.md` (the author's own words) and records: `project/archive/`, `project/review-*.md`, `benchmark/results/`.

## Two contexts for one English word
English words carry a general meaning and a VMware operations meaning. A word is chosen so that both readers take it the same way.
- General: the meaning in daily life, between people.
- VMware operations: the jargon of a VMware administrator. In operations, a case is an issue to investigate and solve (a support case, a ticket). A use case is a scenario.
- So the benchmark does not use case. Its items are questions: they are answered, not investigated. A question can have several parts (`format: compound`).
- Quiz is the author's word for his source documents: it checks what the reader knows (it is not a request for something unknown), and it reads lighter than an exam.

## Terms
| Use | Means | Do not use for it |
|---|---|---|
| benchmark | The proof of the product: question set, runner, judge, results (`benchmark/`). Also one execution of it: every candidate, every mode, 5 runs; one folder `benchmark/results/<benchmark-id>/` | Auto Test, test, evaluation, benchmark run |
| run | One pass through all the questions, by one model in one mode. A benchmark has 5 runs (`runs: 5`, column `run`). Each run is a repeat of the same questions; the answers differ | repeat, iteration |
| question | One benchmark item: one file in `benchmark/questions/` with prompt, answer key and metadata. A benchmark question plays a question a VMware administrator asks the product | case, test case, golden case, exam question |
| question set | All the questions of the benchmark | golden set, case set |
| prompt | The `## Prompt` text of a question: the only text sent to the candidate | question text |
| quiz | The author's quiz documents (vSphere Metric Quiz.docx, the book's chapter quizzes): a source of questions, `origin: quiz` | - |
| author question | One entry in `project/author-questions.md` | - |
| knowledge base | The content in `knowledge/` | KB (in prose) |
| agent | The model plus the tool loop, in agentic mode only: it chooses the next tool, query and file, and when to answer. The loop code is in the harness; the decisions are the model's | - |
| harness | The execution environment and guardrails around the model (`harness/`): search engine, catalog, calculator, flow executor, the loop's rules, the verifier. It hosts the agent and constrains it | wrapper, pipeline |
| runner | The benchmark code (`benchmark/runner/`) | - |
| judge | The model that scores free-text and compound answers 0-3 | grader |
| candidate | A model in the benchmark | model under test, AI under test |
| test | A code test only: `harness/test_tools.py`, `benchmark/runner/test_runner.py` (author, 2026-11-05) | the benchmark |
| retrieval check | `benchmark/runner/retrieval_eval.py`: are the files each question needs found, without a model | retrieval test, harness-only test |
| frontier reference | The frontier model scored as the bar to beat | - |
| answer key | `answer` and `trap` letters, `## Expected key points`, `## Likely wrong answer` | key (alone) |
| kind | The sub-score a question counts for: multiple choice, screenshot, conversation | type |
| format | How a question is answered: multiple-choice, free-text, compound | - |
| attachment | A file listed in a question's `attachments` | - |
| screenshot | An image of a product UI or tool (esxtop, vCenter, VCF Operations) | - |
| author | Iwan Rahabok, who owns the knowledge and reviews it | - |

## Examples
- The benchmark has 5 runs; each run goes through the same 100 questions.
- Benchmark 20261103-081849 had 5 runs of 17 multiple-choice questions per model and mode.
- A question counts as known only when all 5 runs answer it exactly right.

## Open: one word for two things
- None.
