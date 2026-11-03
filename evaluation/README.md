# Evaluation

Golden cases that measure whether the knowledge base improves AI answers.
Never index this folder: it contains answer keys.

## Layout

```text
evaluation/
├── cases/<scope>/<area>/<area>-<nnn>-<slug>.md   # one case per file
├── attachments/<case-id>/                        # screenshots, logs, diagrams for a case
├── results/results.csv                           # one row per case per run
└── _templates/case.md
```

- scope: `vendor-neutral`, `vsphere` (later `nsx`, `vsan`).
- area: `foundations`, `cpu`, `memory`, `storage`, `network`, `general` (spans several areas).
- origin `quiz`: the author's quiz documents (multiple choice, with answer key).
- One file per case: scales to hundreds of cases, one diff per case, attachments per case.
- Ids never change and are never reused. Retired cases get `status: retired`, not deleted.

## Case fields
| Field | Meaning |
|---|---|
| `input` | text, screenshot, diagram, log, mixed. Non-text inputs live in `attachments/<id>/`. |
| `tests` | concept, distinction, judgment, troubleshooting. |
| `knowledge` | Knowledge ids the answer should draw on. Used to check retrieval, not only the answer. |
| `origin` | book, quiz, live-lab, real-ticket, synthetic. |
| `source_path` | Heading path in the source document, for QA. |
| `format` | multiple-choice (auto-scored by `tools/autotest`), free-text (rubric, judge or author), compound (scored by hand). |
| `level` | recall, l400, multi-hop, screenshot. Multiple-choice only. |
| `answer` | Correct option letters as written in `## Prompt`. Multiple-choice only. Never sent to the AI. |
| `trap` | Option letters of the known wrong answer. Multiple-choice only. Never sent to the AI. |

## Automatic run
- Multiple-choice cases: `tools/autotest/run.py`. See `tools/autotest/README.md`.

## How to run (manual)
1. Send only the `## Prompt` section (plus attachments) to the AI. Never send the rest of the file.
2. Run twice with the same model and effort:
   - `baseline`: no knowledge base.
   - `kb`: retrieval from `knowledge/`.
3. Score each answer against `## Expected key points`.
4. Append one row per case per run to `results/results.csv`.

## Scoring (per case, 0–3)
| Score | Meaning |
|---|---|
| 0 | Falls into the trap, or wrong. |
| 1 | Avoids the trap, but cannot explain why. |
| 2 | Correct, with the right reason (mechanism or vantage point). |
| 3 | Correct, right reason, and states what to check next. |

## results.csv columns
| Column | Example |
|---|---|
| date | 2026-11-02 |
| model | model id |
| effort | medium / high / max |
| mode | baseline / kb |
| case_id | vsphere-cpu-003 |
| score | 0–3 |
| notes | short reason for the score |
