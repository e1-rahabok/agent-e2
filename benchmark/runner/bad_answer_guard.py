"""Health check while a run is going: stop a run whose answers are invalid, before it spends hours and money on them.

What went wrong in the first full benchmark: reasoning models spent their 4,000 tokens thinking, the answer was cut off
before the ANSWER line, the parser found no letter and the answer scored as wrong. Nothing failed, so nothing
stopped the run. 85% of the baseline answers of one model were cut off and the run took twice as long as it should.
A model that answers wrongly costs a score point; a model whose answers are cut off or unparsable measures nothing.

A bad answer is: an API error of the request (HTTP 400 and the like), a multiple-choice answer with no readable letter, or an answer cut at max_tokens.
The check looks at the last `window` answers of each model. When `max_bad` of them are bad it trips (exit 5: the settings are wrong).
A failure of the gateway or a provider (HTTP 5xx, 429, a dropped connection) is not bad in that sense. It has its own window and trips
with exit 8, GATEWAY_DOWN: the orchestrator waits and resumes the same folder; it never restarts the run with other settings.
An HTTP 402 (credits or key budget) or 401 or 403 (key) trips at once: every further answer would fail the same way.

No I/O here: the runner calls record after each answer and stops starting new ones when it returns a reason.
"""
import re
import threading
from collections import deque

from exit_codes import BUDGET, GATEWAY_DOWN, UNHEALTHY

# An answer that failed because the gateway or a provider did, not because of the model or its settings: HTTP 408, 429, 5xx
# (after the client's retries) or a dropped connection. 2026-11-16: a 2-minute burst of HTTP 503 counted as invalid answers,
# stopped Qwen and Muse, and the runner restarted both from zero with the next settings.
GATEWAY_ERROR = re.compile(r'HTTP (408|429|5\d\d)\b|ConnectionError|ReadTimeout|ConnectTimeout|Timeout|timed out|Connection (reset|aborted|refused)|RemoteDisconnected', re.I)


class StopRunOnBadAnswers:
    def __init__(self, window=40, max_bad=0.25, min_answers=20):
        self.window, self.max_bad, self.min_answers = window, max_bad, min_answers
        self._recent = {}       # per model: is each answer bad, gateway failures left out
        self._gateway = {}      # per model: did each answer fail on the gateway or a provider
        self._lock = threading.Lock()
        self.reason, self.code = None, None

    @staticmethod
    def is_bad(row):
        """row: the answers.csv row of one answer (strings or numbers)."""
        if row.get('error'):
            return True
        if str(row.get('truncated') or '0') == '1':
            return True
        return row.get('answer_type') == 'deterministic' and str(row.get('parse_ok')) == '0'

    @staticmethod
    def is_gateway_error(row):
        return bool(GATEWAY_ERROR.search(str(row.get('error') or '')))

    def record(self, row):
        """Return None while healthy; the reason (and set self.code) when the run must stop.
        Gateway failures never count against the model's settings: they have their own window and their own exit code (8)."""
        err = str(row.get('error') or '')
        with self._lock:
            if self.reason:
                return self.reason
            for status, why in (('HTTP 402', 'the gateway refused for credits or the key budget (HTTP 402)'),
                                ('HTTP 401', 'the gateway refused the key (HTTP 401)'),
                                ('HTTP 403', 'the gateway refused the key (HTTP 403)')):
                if status in err:
                    self.reason, self.code = why, BUDGET
                    return self.reason
            g = self._gateway.setdefault(row['model'], deque(maxlen=self.window))
            g.append(self.is_gateway_error(row))
            if len(g) >= self.min_answers and sum(g) / len(g) >= self.max_bad:
                self.reason = (f'{row["model"]}: {sum(g)} of the last {len(g)} answers failed on the gateway or a provider '
                               '(HTTP 5xx, 429 or a dropped connection). Not a setting problem: wait, then resume the same folder.')
                self.code = GATEWAY_DOWN
                return self.reason
            if self.is_gateway_error(row):
                return None
            q = self._recent.setdefault(row['model'], deque(maxlen=self.window))
            q.append(self.is_bad(row))
            if len(q) >= self.min_answers and sum(q) / len(q) >= self.max_bad:
                kinds = 'errors, answers cut off at max_tokens or with no readable letter'
                self.reason = (f'{row["model"]}: {sum(q)} of the last {len(q)} answers are invalid ({kinds}). '
                               'Fix the model settings (reasoning, max_tokens) before the run goes on.')
                self.code = UNHEALTHY
            return self.reason
