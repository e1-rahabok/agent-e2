"""Per-model concurrency for the benchmark runner.

Each model starts at its proven value (`concurrency`, or its entry in `concurrency_by_model`). The
governor probes upward in small steps (proven, proven + step, proven + 2 * step) and keeps a step only
when the answers per minute rise by about the same ratio and the window has no error. An HTTP 429 sends
the model back to its proven value for the rest of the run. The proven value is a floor: the governor
never goes below it. A model that rate-limits at the default has its own lower proven value in the config.

Tasks run model by model, so at most one model probes at a time; the others wait at their proven value.
A window (the answers measured at one level) holds one mode only: baseline, Agent E2 and web answers
take different times, so a window that spans two modes is thrown away and the base level is measured again.

No I/O here: the runner calls acquire and release around each answer and record after it.
"""
import threading
import time


class _Probe:
    def __init__(self, levels):
        self.levels = levels        # proven, proven + step, ...
        self.accepted = 0           # index of the last level that held up
        self.stage = 'base'         # base: measuring the accepted level; cand: measuring the next one
        self.skip = levels[0]       # completions to drop after a change (started under the old level)
        self.times, self.errors, self.tag = [], 0, None
        self.base_rate, self.base_tag = None, None
        self.done = False
        self.warned = False


class Governor:
    def __init__(self, proven, adaptive=True, step=2, max_probes=2, window=40, gain_fraction=0.5,
                 clock=time.monotonic, log=print):
        """proven: {model: proven concurrency}. gain_fraction: share of the ideal gain a step must deliver
        (0.5: going from 12 to 14 must raise the rate by at least 8.3%, half of the ideal 16.7%)."""
        self.proven = dict(proven)
        self.adaptive = adaptive
        self.window, self.gain_fraction = window, gain_fraction
        self._clock, self._log = clock, log
        self._cond = threading.Condition()
        self._inflight = {m: 0 for m in self.proven}
        self._limit = dict(self.proven)
        n = max_probes if adaptive else 0
        self._probe = {m: _Probe([p + i * step for i in range(n + 1)]) for m, p in self.proven.items()}

    @property
    def max_workers(self):
        """Threads the pool needs: the top level of the busiest model."""
        return max(p.levels[-1] for p in self._probe.values())

    def limit_of(self, model):
        return self._limit[model]

    def summary(self):
        return dict(self._limit)

    def acquire(self, model, timeout=None):
        """Wait for a free slot of the model. False only when a timeout ran out."""
        with self._cond:
            if not self._cond.wait_for(lambda: self._inflight[model] < self._limit[model], timeout):
                return False
            self._inflight[model] += 1
            return True

    def release(self, model):
        with self._cond:
            self._inflight[model] -= 1
            self._cond.notify_all()

    def record(self, model, tag, error=''):
        """One answer finished. tag = its mode; error = the error text, '' when none."""
        with self._cond:
            p = self._probe[model]
            if error and '429' in error:
                self._on_429(model, p)
                return
            if p.done:
                return
            if p.skip > 0:
                p.skip -= 1
                return
            if p.tag is not None and tag != p.tag:
                p.times, p.errors = [], 0   # a new mode: restart the window
            p.tag = tag
            p.times.append(self._clock())
            p.errors += bool(error)
            if len(p.times) >= self.window:
                self._decide(model, p)

    # --- below: called with the lock held

    def _set_limit(self, model, n):
        self._limit[model] = n
        self._cond.notify_all()

    def _on_429(self, model, p):
        floor, now = self.proven[model], self._limit[model]
        p.done = True
        if now > floor:
            self._set_limit(model, floor)
            self._log(f'concurrency {model}: HTTP 429 at {now}, back to the proven {floor} for the rest of the run')
        elif not p.warned:
            p.warned = True
            self._log(f'concurrency {model}: HTTP 429 at the proven value {floor}. It is not proven for this model: '
                      f'lower its entry in concurrency_by_model (config.yaml) and resume.')

    def _next(self, model, p):
        """Move to the next level to test, or stop when the top level held."""
        if p.accepted + 1 < len(p.levels):
            p.stage, p.skip = 'cand', p.levels[p.accepted + 1]
            self._set_limit(model, p.levels[p.accepted + 1])
        else:
            p.done = True
            self._log(f'concurrency {model}: stays at {self._limit[model]}')

    def _decide(self, model, p):
        span = max(p.times[-1] - p.times[0], 1e-9)
        rate = (len(p.times) - 1) / span * 60
        errors, tag, now = p.errors, p.tag, self._limit[model]
        p.times, p.errors = [], 0
        acc = p.levels[p.accepted]
        if p.stage == 'base':
            p.base_rate, p.base_tag = rate, tag
            self._log(f'concurrency {model}: {now} gives {rate:.1f} answers/min ({tag})')
            self._next(model, p)
        elif errors:
            self._reject(model, p, f'{errors} errors at {now}')
        elif tag != p.base_tag:
            self._log(f'concurrency {model}: the mode changed from {p.base_tag} to {tag}; measuring {acc} again')
            self._set_limit(model, acc)
            p.stage, p.skip = 'base', acc
        else:
            need = 1 + self.gain_fraction * (now / acc - 1)
            ratio = rate / p.base_rate
            if ratio >= need:
                self._log(f'concurrency {model}: {now} kept, {rate:.1f} answers/min is {ratio:.2f}x the {p.base_rate:.1f} at {acc}')
                p.accepted += 1
                p.base_rate = rate
                self._next(model, p)
            else:
                self._reject(model, p, f'{rate:.1f} answers/min is {ratio:.2f}x the {p.base_rate:.1f} at {acc}, '
                                       f'{need:.2f}x needed')

    def _reject(self, model, p, why):
        back = p.levels[p.accepted]
        p.done = True
        self._set_limit(model, back)
        self._log(f'concurrency {model}: {self._limit[model]} kept, the next level failed ({why})')
