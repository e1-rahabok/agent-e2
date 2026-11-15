# exportgen: seeded exports for benchmark questions

Writes the CSV and tool-text attachments of the practical questions (see [practical-questions-as-exports-2026-11-15.md](../../practical-questions-as-exports-2026-11-15.md)). Standard library only, Python 3.10+.

## Run (from the repo root)

```
python3 -m project.tools.exportgen list
python3 -m project.tools.exportgen generate <id>|all [--out DIR]
python3 -m project.tools.exportgen check <id>|all [--out DIR]
python3 -m unittest project/tools/test_exportgen.py
```

`python3 project/tools/exportgen` does not work (the package uses relative imports); use `-m` from the repo root. Files go to `benchmark/questions/<id>/<file>`, or `DIR/<id>/<file>` with `--out`. `check` re-reads the files on disk, runs the case's checks, the size cap (each CSV at most 24,000 characters), and compares the files with a fresh generate (an edited file fails). Exit code is non-zero on any failure.

## Layout

- `formats.py`: writers and parsers for every export format.
- `relations.py`: counter relations as pure functions.
- `core.py`: seeded random source, noise, time axes, `Case`, registry, size cap.
- `cases/`: one module per question, named `q<id>_<slug>.py` with underscores (importable), for example `q0368_task_manager_ready_high.py`. `example_*.py` are framework proofs with ids `example-1`, `example-2`.

## Add a case

1. Create `cases/q<id>_<slug>.py`. Subclass `core.Case`, decorate with `@core.register`, set `question_id` (the question's id, for example `"0368"`) and `seed`.
2. `generate(seed=None)` returns `{filename: text}` using `core.make_rng(seed, "salt")`, the format writers and the relation helpers. It must be pure: the same seed gives the same bytes.
3. `check(files)` takes the text as written, re-parses it with the `parse_*` functions and returns a list of failures. Check every relation on every row, and the key itself (the condition the answer key relies on), against the parsed rows, never against the generator's variables.
4. Run `generate <id>`, then `check <id>`, then commit the files with the question. The question's `attachments` list names them; the prompt links them (benchmark/design.md 6.3).

## Conventions

- Names are invented (VM, host, datastore, cluster), never a customer's. Lab names from the templates (sun05-..., acepod) do not appear.
- No lab values. Only names and formats come from `project/sources/export-templates/`.
- Every derived value is recomputed per row (state sums, Readiness, rollups, sums of worlds).
- Distractor columns are part of the case: near names (Readiness vs Ready, Usage vs Run) stay consistent with the relations.
- Cut the period to the event: a CSV stays under 24,000 characters.
- The seed is fixed per case and written in the module; change it only on purpose, and regenerate.

## Format assumptions (not settled by the templates)

- VCF Operations List view CSV: assumed, not captured. A `Name` column, then one column per metric labelled as the picker shows it (`CPU|Ready (%)`) and `<label> (Max)`, `(Min)`, `(First)`, `(Last)` columns. Replace when a real export is captured.
- `/proc/pressure/memory`: standard PSI text; the Photon kernel had none.
- `mpstat -P ALL`, `vmstat`, `top` summary (`%Cpu(s)` line with `st`; the template's `top` ran in a graph mode without it), `sar -u ALL` columns: standard procps/sysstat layouts, not captured.
- vCenter rollup stamps: the writer takes any time axis. Whether a Past day point is stamped at the start or the end of its 15-sample window is not settled by the sample; `core.rollup_stamps(label=...)` supports both, default start.
- esxtop batch: the captured header (12,608 fields) and data row (12,708) differ; the writer keeps both equal and raises otherwise. The group prefix is `\\host\` (two backslashes, as in the captured header; HEADERS.md writes one).
- esxtop panels: `\n` line ends (the capture has `\r\r\n` and cursor artefacts). Column widths follow the samples; the panels `u`, `d`, `v`, `n` are checked against the sample headers only.
- VCF Operations chart time: `November 15, 2026, 8:28:38 PM GMT+08:00` has a narrow no-break space (U+202F) before `PM`, as in the sample.
- typeperf: the time zone label and bias in the first field are a parameter (the template has placeholders); LF line ends; `None` prints `" "` (first sample of a rate counter).
- vCenter Ready (ms), Run, Co-stop, Wait column names (`Ready for <vm>`) are assumed from the `<Measurement> for <object>` pattern; only Usage and Readiness are captured.
- Readiness is Ready / (vCPUs x interval) as the exports document states; vCenter's own rollup of Readiness is not captured.
