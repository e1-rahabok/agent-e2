"""The spending stop of a test run (R-E2-030 in project/requirements/test-spending.md; DESIGN-31 in the workspace's system design).

A run counts the larger of two figures and stops starting answers when it reaches its limit (runner_config.yaml,
release.max_cost_usd, US$100 by CONSTRAINT-1):
- the list price of the tokens of the answers it asked (the `cost_usd` column; reused answers cost nothing again). It also
  counts calls that the author's own provider key pays (BYOK), which the gateway's balance never sees;
- the drop in the gateway's credit balance since the run started. It also counts what list prices miss: web searches,
  retries, calls of answers that failed, and a provider's price above the list.
The balance is read at most once a minute. When it cannot be read, the list price counts alone.

round_executor.py writes STOP_FILE into each run folder when the limit is reached; run_executor.py starts no new answer while
the file is there, and exits with exit_codes.STOPPED. A resume removes the files and checks the limit again.
"""
import time

STOP_FILE = '.spending-stop'


class SpendingStop:
    def __init__(self, limit_usd, list_price, start_balance=None, balance=None, every_seconds=60, clock=time.monotonic):
        """limit_usd: the limit. list_price: a function that returns the list-price cost so far. start_balance: the credit
        balance when the run started, or None. balance: a function that reads the balance now (may raise)."""
        self.limit, self.list_price = float(limit_usd), list_price
        self.start, self.balance, self.every, self.clock = start_balance, balance, every_seconds, clock
        self._drop, self._read_at = 0.0, None

    def balance_drop(self):
        if self.start is None or self.balance is None:
            return 0.0
        now = self.clock()
        if self._read_at is None or now - self._read_at >= self.every:
            self._read_at = now
            try:
                self._drop = max(0.0, float(self.start) - float(self.balance()))
            except Exception:   # noqa: BLE001  an unreadable balance leaves the list price to count alone
                pass
        return self._drop

    def spent(self):
        return max(float(self.list_price()), self.balance_drop())

    def reached(self):
        return self.spent() >= self.limit
