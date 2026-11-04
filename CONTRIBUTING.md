# Contributing

How to help build Isvara: knowledge, questions, reviews and code. Not indexed.

## Open work
| What | Where |
|---|---|
| Questions waiting for the author | [project/author-questions.md](project/author-questions.md) |
| Open work | [project/todo.md](project/todo.md) |
| How the system works | [ARCHITECTURE.md](ARCHITECTURE.md) |
| How knowledge is captured | [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md) |
| How the system is tested | [benchmark/test-design.md](benchmark/test-design.md) |

## Ways to contribute
- **Answer an author question.** Write after `Answer:` in `project/author-questions.md`. The answer is applied to the knowledge files and the entry moves to Resolved.
- **Review a knowledge file.** Check every fact against its source in the metadata (`source`, `review_notes`, `corrections`). Report a wrong fact, a missing trap or a missing link.
- **Add a benchmark case.** Use `benchmark/_templates/case.md`. A realistic situation with values, 4-8 options, a trap option, the knowledge ids that answer it, and `product` and `technology` tags. New ids: `case-<nnnn>`. Never send `## Expected key points` or `## Likely wrong answer` to a model.
- **Report a wrong answer.** Give the question, the answer, and the run or trace. It is classified as a knowledge gap, a retrieval miss or a model error.
- **Improve the harness.** Code in `harness/`, tests in `harness/test_tools.py`.

## Rules for knowledge files
- Level 400: mechanism and reason, traps, edge cases. No definitions a vSphere administrator already knows.
- One fact per bullet. One managed object type per metric file.
- A threshold only with its source. No invented numbers.
- Facts not from the author's book are recorded in `review_notes` until the author confirms them.
- Folder, tag and writing rules: [README.md](README.md), sections Layout and Writing rules. Terms: [knowledge/glossary.md](knowledge/glossary.md).
- `knowledge/raw-input/` is read-only.

## Before a pull request
```bash
python3 tools/lint.py
```
```bash
python3 -m unittest harness/test_tools.py
```
- Lint must pass with 0 problems. Run the unit tests after changing `harness/` or `knowledge/catalog/`.
- One change set per pull request, merged with a merge commit. Commit messages describe the change.
