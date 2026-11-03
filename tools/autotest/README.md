# Auto Test runner

Runs the golden multiple-choice questions against candidate open-weight models through Vercel AI Gateway, scores them automatically, and writes a report.
Design: `docs/design-kb-test-site.md`, section Auto Test plan. Not indexed.

## Setup
- Python 3.10+ with `pyyaml` and `requests`.
- Environment variable `AI_GATEWAY_API_KEY` (Vercel AI Gateway API key). Never commit it.
- Settings: `config.yaml` (models, modes, runs, temperature, budgets, provider pinning).

## Commands
```bash
python3 tools/autotest/run.py --dry-run
```
- Shows the matrix, the number of answers and a cost estimate. No API calls.

```bash
python3 tools/autotest/run.py --mock --runs 2
```
- Offline pipeline check: random answers, real retrieval, no API calls.

```bash
python3 tools/autotest/run.py --models openai/gpt-oss-20b --modes classic --runs 1 --cases cpu-004
```
- Smallest real test: one model, one mode, one question.

```bash
python3 tools/autotest/run.py
```
- Full matrix from `config.yaml`.

```bash
python3 tools/autotest/run.py --resume evaluation/results/autotest/<run-id>
```
- Continue a run; failed answers are retried.

## What it does
1. Loads `knowledge/` exactly as README, section How a local LLM uses it: metadata split off, body chunked by `##` heading.
2. Builds the index: BM25, plus embeddings (`embedding_model`) when the API key is set. Embeddings are cached in `tools/autotest/.cache/`.
3. Loads golden cases with `format: multiple-choice`. Other formats are listed as skipped.
4. For each model, mode, case and run:
   - shuffles the options (same order for every model and mode within a run) and appends "Not covered by the knowledge base";
   - answers in the mode:
     - `baseline`: no knowledge base;
     - `classic`: one search, link expansion (`same_name`, `related`), 8K-token context;
     - `agentic`: tool loop with `search`, `read_file`, `follow_links`, `get_images`; at most 8 calls and 12K tokens of tool output. Search first, no repeated calls, a same_name reminder. Falls back to classic after 2 tool-format errors;
   - parses `ANSWER:` and maps letters back;
   - scores exact match, partial credit, trap hit, Not-covered pick.
5. Questions with image attachments get a second `vision` track on models tagged `vision` on the gateway.
6. Writes the run folder and appends one summary row per model, mode and case to `evaluation/results/results.csv`.

## Output: `evaluation/results/autotest/<run-id>/`
| File | Content | In git |
|---|---|---|
| `config.json` | Index version (git SHA), models with tags and prices, settings | Yes |
| `answers.csv` | One row per answer: model, provider, mode, track, case, run, option order, letters, scores, retrieval recall, tool steps, tokens, latency, cost | Yes |
| `report.md` | Score matrix (exact, partial, majority, margin, consistency, trap, parse failures, recall, fallback, cost), by area and level, hardest questions | Yes |
| `traces.jsonl` | Full question and retrieval trace per answer | No (large); keep locally |

## Golden case fields used
| Field | Meaning |
|---|---|
| `format` | `multiple-choice` (auto-scored), `free-text` (judge or author), `compound` (scored by hand) |
| `level` | `recall`, `l400`, `multi-hop`, `screenshot` |
| `answer` | Correct option letters, as in `## Prompt` |
| `trap` | Option letters that are the known wrong answer |
| `knowledge` | Files the answer should come from; used for retrieval recall |
- Options in `## Prompt` are lines starting with `A. ` to `H. `. Text after the options (for example `Hint:`) is kept below them.
- The prompt text must stand alone without the image: the text track sends no image.
- `scripts/validate.py` checks these fields.

## Limits
- Provider name is recorded when the gateway returns it; the field is not documented as stable.
- Cost is estimated from gateway list prices in `/models`; check the Vercel invoice.
- Mock runs prove the pipeline only. Their scores are random.
