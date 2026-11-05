# Repository terms

One English word per concept in this repository (author, 2026-11-05). Not indexed.
- Vocabulary of the knowledge itself (vSphere, VCF, Guest OS terms): `knowledge/glossary.md`.
- This file: words for the repository's own parts.
- When two words name the same thing, pick one, add it here, and replace the other. When one word names two things, split it here.
- `project/tools/lint.py` flags the replaced words listed in `project/tools/tags.yaml`, `avoid_repo_terms`.
- Exempt: `project/author-questions.md` (the author's own words), `project/archive/`, `benchmark/results/` (records).

## Terms
| Use | Means | Do not use for it |
|---|---|---|
| case | One benchmark item: one file in `benchmark/cases/` with prompt, answer key and metadata | question, golden case, test case, exam question |
| case set | All cases of the benchmark | golden set, question set |
| prompt | The `## Prompt` text of a case: the only text sent to the model under test | question text |
| question | What a person asks the product. A case's prompt plays a question. Not a benchmark item | - |
| author question | One entry in `project/author-questions.md` | - |
| quiz | The author's quiz documents (vSphere Metric Quiz.docx, the book's chapter quizzes): a source of cases, `origin: quiz` | case |
| benchmark | The case set, runner, judge and results that prove the product (`benchmark/`) | Auto Test, evaluation |
| benchmark run | One execution of the runner over models, modes and cases; one folder in `benchmark/results/autotest/` | Auto Test run, test run |
| knowledge base | The content in `knowledge/` | KB (in prose) |
| harness | The software around the model (`harness/`) | wrapper, pipeline |
| runner | The benchmark code (`benchmark/runner/`) | - |
| judge | The model that scores free-text and compound answers 0-3 | grader |
| candidate | A model under test | - |
| frontier reference | The frontier model scored as the bar to beat | - |
| answer key | `answer` and `trap` letters, `## Expected key points`, `## Likely wrong answer` | key (alone) |
| kind | The sub-score a case counts for: multiple choice, screenshot, conversation | type |
| format | How a case is answered: multiple-choice, free-text, compound | - |
| attachment | A file listed in a case's `attachments` | - |
| screenshot | An image of a product UI or tool (esxtop, vCenter, VCF Operations) | - |
| author | Iwan Rahabok, who owns the knowledge and reviews it | - |

## Open: one word for two things
- run: a benchmark run, and one of the 5 answers per case, model and mode (`runs: 5`, column `run`). Proposal: keep run for the benchmark run, rename the repetition to repeat. Not changed yet: the code, the `runs` setting and the results columns use it.
- test: unit tests (`harness/test_tools.py`), the retrieval test, and the benchmark. Proposal: test only for code tests; benchmark for the benchmark; retrieval check for `retrieval_eval.py`.
- Folder `benchmark/results/autotest/` keeps its name: past results and their links use it.
