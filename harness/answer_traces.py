"""Traces: what Agent E2 read, computed and checked for one answer, kept 30 days in files (R-E2-023).

A trace ID is 128 random bits, so it cannot be guessed. A trace holds the model, the knowledge commit, the files read and
the steps of the pipeline; for an attachment only its name, type and size. A restart of the service keeps the traces,
because they are files; a trace older than 30 days is deleted and reads as not found.
"""
import json
import os
import re
import secrets
import tempfile
import time

TRACE_ID = re.compile(r'^[A-Za-z0-9_-]{22}$')


class TraceStore:
    def __init__(self, folder, days=30, clock=time.time):
        self.folder, self.days, self.clock = os.path.expanduser(str(folder)), days, clock
        os.makedirs(self.folder, mode=0o700, exist_ok=True)
        self.swept = 0
        self.sweep()

    @staticmethod
    def new_id():
        return secrets.token_urlsafe(16)

    def _path(self, trace_id):
        return os.path.join(self.folder, f'{trace_id}.json')

    def save(self, trace_id, trace):
        trace = {**trace, 'trace_id': trace_id, 'created': self.clock()}
        fd, tmp = tempfile.mkstemp(dir=self.folder, suffix='.tmp')
        with os.fdopen(fd, 'w') as f:
            json.dump(trace, f, ensure_ascii=False, default=str)
        os.replace(tmp, self._path(trace_id))
        if self.clock() - self.swept > 3600:
            self.sweep()

    def get(self, trace_id):
        if not TRACE_ID.match(trace_id or ''):
            return None
        try:
            trace = json.load(open(self._path(trace_id)))
        except (OSError, ValueError):
            return None
        if self.clock() - trace.get('created', 0) > self.days * 86400:
            return None
        return trace

    def sweep(self):
        """Delete the traces older than the keeping time."""
        self.swept = self.clock()
        for name in os.listdir(self.folder):
            if not name.endswith('.json'):
                continue
            path = os.path.join(self.folder, name)
            try:
                created = json.load(open(path)).get('created', 0)
            except (OSError, ValueError):
                created = 0   # unreadable: not a trace of this service
            if self.clock() - created > self.days * 86400:
                try:
                    os.remove(path)
                except OSError:
                    pass
