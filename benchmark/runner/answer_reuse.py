"""Reuse of unchanged answers (R-E2-029 in project/requirements/test-spending.md; DESIGN-30 in the workspace's system design).

An answer whose inputs equal those of an earlier answer is copied from the earlier run folder, and no model is called for it.
The inputs are hashed into the `inputs_hash` column of answers.csv:

- every mode: the mode, the model, its request settings (model_params, sampling, max_tokens, temperature), the run number,
  the track, the question as the model sees it in that run (stem, options in that run's order, tables) and its images,
  and whether the client is the offline mock;
- baseline: the code and prompts that build its request (answer_modes.baseline, _user, PROMPTS);
- web: the same, plus web_search_on, its tools, the web settings and the code of public_web_lookup.py;
- agent-e2: every file of knowledge/ and harness/ except the tests, the answer settings of runner_config.yaml (every key
  except those that only schedule the run) and the search method (hybrid with its embedding model, or BM25 only).

The key of a question (`## Answers`) is not an input: the model never sees it, so a reused answer is scored against the
current key. An Agent E2 answer is not reused when only the files it read are unchanged: a change to another file can
change what search finds (DESIGN-30, rejected option b).
"""
import csv
import hashlib
import inspect
import json
import os

# Keys of runner_config.yaml that schedule a run and never reach a request. Every other key counts as an answer setting.
SCHEDULE_KEYS = frozenset({
    'gateway', 'models', 'modes', 'runs', 'concurrency', 'concurrency_by_model', 'adaptive_concurrency', 'gateway_retry_minutes',
    'max_minutes', 'spread_runs_over_providers', 'concurrency_per_provider', 'provider_order', 'snapshots', 'release',
    'model_params', 'sampling',     # per model: the answering model's own entries are in its request settings
})
SKIP_DIRS = {'__pycache__', '.git', '.pytest_cache'}


def digest(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(p if isinstance(p, bytes) else json.dumps(p, sort_keys=True, default=str).encode())
        h.update(b'\0')
    return h.hexdigest()


def tree_hash(root, folders):
    """One hash of every file under the folders, by path and content. Tests are left out; line endings are made equal."""
    h = hashlib.sha256()
    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(os.path.join(root, folder)):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for name in sorted(filenames):
                if name.startswith('test_') or name.endswith('.pyc'):
                    continue
                path = os.path.join(dirpath, name)
                h.update(os.path.relpath(path, root).replace(os.sep, '/').encode() + b'\0')
                h.update(open(path, 'rb').read().replace(b'\r\n', b'\n') + b'\0')
    return h.hexdigest()


def mode_inputs(cfg, root, answer_modes, retrieval):
    """The inputs each mode adds to the inputs of a question, as one hash per mode. Computed once per run."""
    request = [inspect.getsource(answer_modes.baseline), inspect.getsource(answer_modes._user), answer_modes.PROMPTS]
    lookup = os.path.join(root, 'harness', 'public_web_lookup.py')
    web = request + [inspect.getsource(answer_modes.web_search_on), answer_modes.REF_WEB_TOOLS, cfg.get('web'),
                     cfg.get('web_max_calls', 5), open(lookup, 'rb').read() if os.path.exists(lookup) else b'']
    settings = {k: v for k, v in cfg.items() if k not in SCHEDULE_KEYS}
    return {
        'baseline': digest(*request),
        'web': digest(*web),
        answer_modes.AGENT: digest(tree_hash(root, ['knowledge', 'harness']), settings, retrieval),
    }


def inputs_hash(mode, model, settings, run, track, question_text, images, mode_hash, mock):
    """The inputs of one answer. settings: the model's request settings; images: the image parts sent with the question."""
    return digest('answer-inputs-1', mode, model, settings, int(run), track, question_text, images or [], mode_hash, bool(mock))


def earlier_answers(results_dir, skip_folder=None):
    """{inputs_hash: row} from the answers.csv of every run folder in results_dir: rows with a hash and no error.
    Folders kept as evidence of invalid settings (`-invalid-`) are not read."""
    found = {}
    if not os.path.isdir(results_dir):
        return found
    skip = os.path.abspath(skip_folder) if skip_folder else None
    for name in sorted(os.listdir(results_dir)):
        folder = os.path.join(results_dir, name)
        path = os.path.join(folder, 'answers.csv')
        if '-invalid-' in name or os.path.abspath(folder) == skip or not os.path.exists(path):
            continue
        with open(path, newline='') as fh:
            for row in csv.DictReader(fh):
                if row.get('inputs_hash') and not row.get('error'):
                    found.setdefault(row['inputs_hash'], row)
    return found


def picked_of(row):
    """The original letters an earlier answer chose, as question_files.parse returned them; None when it could not be read."""
    if str(row.get('parse_ok')) != '1':
        return None
    return [x for x in (row.get('answer_letters') or '').split(',') if x] or None


def new_spending(rows):
    """List-price cost of the answers a run asked itself; reused answers cost nothing again."""
    total = 0.0
    for r in rows:
        if r.get('reused_from'):
            continue
        try:
            total += float(r.get('cost_usd') or 0)
        except ValueError:
            pass
    return total
