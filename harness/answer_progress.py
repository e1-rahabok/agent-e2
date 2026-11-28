"""Progress of one answer: its stage, the seconds in each stage, and the model use, for the job calls and the usage report
(R-E2-007, R-E2-010). The pipeline reports each finished step through note(); the service sets the stages that are its own.

A job's worker thread and a synchronous call each hold one Progress, found through current(). A job that ran past its time
limit is abandoned: its next stage raises Abandoned, so the thread ends without spending more of the gateway.
"""
import threading
import time

STAGES = ('topic', 'shape', 'understand', 'plan', 'compute', 'write', 'check', 'rewrite')
# The stage that runs after a pipeline step finished (answer_modes._step and expert_agent._step name the step).
AFTER = {'understand': 'plan', 'plan': 'compute', 'compute': 'write', 'coverage': 'write', 'ask': 'write', 'shape': 'write',
         'answer': 'check'}
_local = threading.local()


class Abandoned(Exception):
    """The job passed its time limit; the thread stops at its next stage."""


class Progress:
    def __init__(self, clock=time.time):
        self.clock = clock
        self.lock = threading.Lock()
        self.started = self.updated = self._since = clock()
        self.stage = None
        self.seconds = {}
        self.calls = self.prompt_tokens = self.completion_tokens = 0
        self.abandoned = False

    def enter(self, stage):
        if self.abandoned:
            raise Abandoned()
        with self.lock:
            now = self.clock()
            if self.stage:
                self.seconds[self.stage] = self.seconds.get(self.stage, 0) + now - self._since
            self.stage, self._since, self.updated = stage, now, now

    def touch(self):
        self.updated = self.clock()

    def count(self, res):
        with self.lock:
            self.calls += 1
            self.prompt_tokens += int(res.get('prompt_tokens') or 0)
            self.completion_tokens += int(res.get('completion_tokens') or 0)

    def finish(self):
        """Close the running stage; returns what the answer reports: elapsed_s, stage_seconds and usage."""
        with self.lock:
            now = self.clock()
            if self.stage:
                self.seconds[self.stage] = self.seconds.get(self.stage, 0) + now - self._since
                self._since = now
            return {'elapsed_s': round(now - self.started, 2),
                    'stage_seconds': {s: round(self.seconds[s], 2) for s in STAGES if s in self.seconds},
                    'usage': {'model_calls': self.calls, 'prompt_tokens': self.prompt_tokens,
                              'completion_tokens': self.completion_tokens}}


class Metered:
    """A model client that counts every call into a Progress and refuses to start one for an abandoned job."""

    def __init__(self, inner, progress):
        self.inner, self.progress = inner, progress

    def chat(self, *args, **kw):
        if self.progress.abandoned:
            raise Abandoned()
        res = self.inner.chat(*args, **kw)
        self.progress.count(res)
        self.progress.touch()
        return res

    def __getattr__(self, name):
        return getattr(self.inner, name)


def current():
    return getattr(_local, 'progress', None)


def note(step):
    """Called by the pipeline after each step; moves the stage on."""
    p = current()
    if p is not None and step in AFTER:
        p.enter(AFTER[step])


class use:
    """Make a Progress the current one of this thread."""

    def __init__(self, progress):
        self.progress = progress

    def __enter__(self):
        self.before = current()
        _local.progress = self.progress
        return self.progress

    def __exit__(self, *exc):
        _local.progress = self.before
