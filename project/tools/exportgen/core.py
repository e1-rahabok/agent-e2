"""Seeded random source, noise helpers, time axes, the Case base class and
the registry.

Everything random comes from one random.Random(seed) per case, so the same
seed always writes the same bytes. No clock, no global state.
"""

import datetime as dt
import importlib
import pkgutil
import random
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
QUESTIONS_DIR = REPO_ROOT / "benchmark" / "questions"
CSV_MAX_CHARS = 24_000  # question_csv_max_chars after the change set (exports document 7.1)

UTC = dt.timezone.utc

# vCenter statistics intervals: name -> seconds per point
INTERVAL_S = {"realtime": 20, "day": 300, "week": 1800, "month": 7200}
# Fixed anchor so output never depends on the clock; a case may pass its own.
DEFAULT_START = dt.datetime(2026, 11, 10, 9, 0, 0, tzinfo=UTC)


def make_rng(seed, salt=""):
    """A random.Random for a seed; salt gives independent streams per purpose."""
    return random.Random(f"{seed}:{salt}")


# ---- noise ------------------------------------------------------------------

def clamp(x, lo, hi):
    """x limited to [lo, hi]."""
    return max(lo, min(hi, x))


def bounded_walk(rng, n, start, step, lo, hi):
    """Random walk of n points, each step gaussian(0, step), clamped to [lo, hi]."""
    out, x = [], start
    for _ in range(n):
        x = clamp(x + rng.gauss(0, step), lo, hi)
        out.append(x)
    return out


def noisy(rng, base, rel=0.05, floor=0.0):
    """base with gaussian relative noise, not below floor."""
    return max(floor, base * (1 + rng.gauss(0, rel)))


def burst_profile(n, start, length, ramp=2):
    """Weights 0..1 per index: 1 inside [start, start+length), linear ramp
    of `ramp` samples on each side, 0 elsewhere."""
    out = []
    for i in range(n):
        if start <= i < start + length:
            w = 1.0
        elif ramp and start - ramp <= i < start:
            w = (i - (start - ramp) + 1) / (ramp + 1)
        elif ramp and start + length <= i < start + length + ramp:
            w = (start + length + ramp - i) / (ramp + 1)
        else:
            w = 0.0
        out.append(w)
    return out


def blend(low, high, w):
    """Linear mix: low at w=0, high at w=1."""
    return low + (high - low) * w


# ---- time -------------------------------------------------------------------

def time_axis(start, n, interval_s):
    """n UTC datetimes from start, interval_s apart."""
    return [start + dt.timedelta(seconds=interval_s * i) for i in range(n)]


def align_down(t, interval_s):
    """Floor a datetime to a multiple of interval_s since the epoch."""
    ts = int(t.timestamp())
    return dt.datetime.fromtimestamp(ts - ts % interval_s, tz=UTC)


def rollup_stamps(times, per_window, label="start"):
    """One stamp per window of per_window samples: the window's first
    sample time (label="start") or the time after its last sample
    (label="end"). Which one vCenter uses is not settled by the templates."""
    out = []
    for i in range(len(times) // per_window):
        first = times[i * per_window]
        last = times[(i + 1) * per_window - 1]
        if label == "start":
            out.append(first)
        else:
            out.append(last + (times[1] - times[0]))
    return out


# ---- case base and registry -------------------------------------------------

class Case:
    """One benchmark question's export(s).

    Subclasses set question_id and seed, implement generate() and check().
    generate(seed) must be pure: same seed, same dict of file name -> text.
    check(files) gets the text of the files as written (read from disk by the
    CLI) and re-parses them; it returns a list of failure strings, empty when
    every key condition holds.
    """

    question_id = ""
    seed = 0

    def generate(self, seed=None):
        """Return {filename: text}. Use self.seed when seed is None."""
        raise NotImplementedError

    def check(self, files):
        """Return a list of failures (strings). Empty list means pass."""
        raise NotImplementedError

    def generate_inline(self, seed=None):
        """Return {N: text} for the generated ```text blocks of the question's
        ## Prompt (N is 1-based, the spec's inline:N). Blocks not listed are
        hand-written and stay as they are. Default: none."""
        return {}

    def check_inline(self, blocks, files):
        """blocks is {N: text} of every ```text block of ## Prompt as it is
        on disk (generated and literal); files is {name: text} as in check(). Return a list of failures."""
        return []


CASES = {}


def register(cls):
    """Class decorator: add one instance of cls to the registry by question_id."""
    case = cls()
    if not case.question_id:
        raise ValueError(f"{cls.__name__} has no question_id")
    if case.question_id in CASES:
        raise ValueError(f"duplicate question_id {case.question_id}")
    CASES[case.question_id] = case
    return cls


def load_cases():
    """Import every module in the cases package so it registers itself."""
    from . import cases
    for m in pkgutil.iter_modules(cases.__path__):
        importlib.import_module(f"{cases.__name__}.{m.name}")
    return CASES


def check_size_cap(files, cap=CSV_MAX_CHARS):
    """Failures for every .csv file longer than cap characters."""
    return [f"{name}: {len(text)} characters, cap is {cap}"
            for name, text in files.items()
            if name.endswith(".csv") and len(text) > cap]


def write_files(files, out_dir):
    """Write {name: text} under out_dir as UTF-8, no newline translation."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        with open(out_dir / name, "w", encoding="utf-8", newline="") as f:
            f.write(text)


def read_files(names, in_dir):
    """Read files back as text (UTF-8, BOM kept as U+FEFF, no newline translation)."""
    out = {}
    for name in names:
        with open(Path(in_dir) / name, encoding="utf-8", newline="") as f:
            out[name] = f.read()
    return out


# ---- inline text blocks of the question prompt --------------------------------

def question_path(question_id, questions_dir=None):
    """The question file whose metadata has id: "<question_id>", or None."""
    d = Path(questions_dir or QUESTIONS_DIR)
    needle = f'id: "{question_id}"'
    for p in sorted(d.glob("*.md")):
        with open(p, encoding="utf-8", newline="") as f:
            if any(ln.rstrip("\r\n") == needle for ln in f):
                return p
    return None


def _prompt_blocks(md):
    """Spans (start, end) of the content of each ```text block inside ## Prompt:
    start is after the opening fence line, end is the start of the closing fence line."""
    m = re.search(r"^## Prompt[ \t]*\n", md, re.M)
    if not m:
        return []
    nxt = re.search(r"^## ", md[m.end():], re.M)
    stop = m.end() + nxt.start() if nxt else len(md)
    spans, pos = [], m.end()
    while True:
        o = re.compile(r"^```text[ \t]*\n", re.M).search(md, pos, stop)
        if not o:
            return spans
        c = re.compile(r"^```[ \t]*$", re.M).search(md, o.end(), stop)
        if not c:
            return spans
        spans.append((o.end(), c.start()))
        pos = c.end()


def read_inline_blocks(md):
    """{N: text} of every ```text block of ## Prompt, without the final newline."""
    return {i + 1: md[a:b].rstrip("\n") for i, (a, b) in enumerate(_prompt_blocks(md))}


def write_inline_blocks(md, blocks):
    """md with the listed blocks ({N: text}) replaced. Raises ValueError when a block is missing."""
    spans = _prompt_blocks(md)
    for n in sorted(blocks, reverse=True):
        if not 1 <= n <= len(spans):
            raise ValueError(f"no ```text block {n} in ## Prompt ({len(spans)} found)")
        a, b = spans[n - 1]
        md = md[:a] + blocks[n].rstrip("\n") + "\n" + md[b:]
    return md
