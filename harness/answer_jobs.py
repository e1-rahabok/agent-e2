"""Answer jobs: a caller starts an answer, reads its stage every few seconds, and takes the result (R-E2-007, R-E2-008).

Jobs live in the memory of this process (DESIGN-14). At most `max_running` run at once, up to `max_queued` wait, and a
further call is refused with Busy. A job that runs past the time limit fails with `time_limit`: its thread is told to
stop at its next stage. A finished or failed job can be read for `keep_s` seconds. A restart loses the jobs.

A watcher thread moves `updated_at` of every waiting or running job each `heartbeat_s` seconds, so a caller sees that the
service is alive during one long model call. `run(body, progress)` is the service's answer; it returns the result
object or raises ValueError (refused), LLMError (the model) or anything else (a fault of the service).
"""
import collections
import secrets
import threading
import time
from datetime import datetime, timezone

import answer_progress
from model_client import LLMError

MESSAGES = {'model_error': 'Agent E2 could not get an answer from its model. Ask again in a minute.',
            'time_limit': 'The answer took longer than the time limit, so Agent E2 stopped it. Ask again, or ask a smaller question.',
            'internal_error': 'Agent E2 failed while writing the answer. Ask again in a minute.'}


class Busy(Exception):
    """The running and the waiting jobs are full."""


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


class Job:
    def __init__(self, job_id, body, now):
        self.id, self.body, self.created = job_id, body, now
        self.state, self.progress = 'queued', None
        self.started = self.finished = None
        self.updated = now
        self.result = self.error = None


class JobStore:
    def __init__(self, run, max_running=4, max_queued=20, time_limit=600, keep_s=900, heartbeat_s=5, clock=time.time):
        self.run, self.max_running, self.max_queued = run, max_running, max_queued
        self.time_limit, self.keep_s, self.heartbeat_s, self.clock = time_limit, keep_s, heartbeat_s, clock
        self.jobs, self.queue, self.lock = {}, collections.deque(), threading.Lock()
        threading.Thread(target=self._watch, daemon=True).start()

    def submit(self, body):
        """Accept a job: returns its id. Raises Busy when the running and the waiting jobs are full."""
        with self.lock:
            running = sum(j.state == 'running' for j in self.jobs.values())
            if running >= self.max_running and len(self.queue) >= self.max_queued:
                raise Busy()
            job = Job(secrets.token_urlsafe(16), body, self.clock())
            self.jobs[job.id] = job
            self.queue.append(job)
        self._dispatch()
        return job.id

    def _dispatch(self):
        while True:
            with self.lock:
                if not self.queue or sum(j.state == 'running' for j in self.jobs.values()) >= self.max_running:
                    return
                job = self.queue.popleft()
                job.state, job.started = 'running', self.clock()
                job.progress = answer_progress.Progress(self.clock)
                job.updated = job.started
            threading.Thread(target=self._work, args=(job,), daemon=True).start()

    def _work(self, job):
        try:
            with answer_progress.use(job.progress):
                result = self.run(job.body, job.progress)
            self._end(job, 'done', result=result)
        except answer_progress.Abandoned:
            pass   # the watcher has already failed the job
        except LLMError:
            self._end(job, 'failed', error=self._error('model_error'))
        except Exception as e:   # a fault of the service: the caller is told, the detail stays in the log
            print(f'job {job.id}: {type(e).__name__}', flush=True)
            self._end(job, 'failed', error=self._error('internal_error'))
        self._dispatch()

    @staticmethod
    def _error(reason):
        return {'reason': reason, 'message': MESSAGES[reason]}

    def _end(self, job, state, result=None, error=None):
        with self.lock:
            if job.state != 'running':
                return   # already failed by the time limit
            job.state, job.result, job.error, job.finished = state, result, error, self.clock()
            job.updated = job.finished

    def _watch(self):
        while True:
            time.sleep(min(self.heartbeat_s, 1))
            now = self.clock()
            with self.lock:
                for job in list(self.jobs.values()):
                    if job.state in ('queued', 'running'):
                        if now - job.updated >= self.heartbeat_s:
                            job.updated = now
                        if job.state == 'running' and now - job.started > self.time_limit:
                            job.progress.abandoned = True
                            job.state, job.finished, job.updated = 'failed', now, now
                            job.error = self._error('time_limit')
                    elif now - job.finished > self.keep_s:
                        del self.jobs[job.id]
            self._dispatch()

    def get(self, job_id):
        """The job as the caller reads it, or None when unknown or older than the keeping time."""
        with self.lock:
            job = self.jobs.get(job_id)
            if job is None:
                return None
            now = self.clock()
            if job.finished and now - job.finished > self.keep_s:
                return None
            out = {'job': job.id, 'state': job.state, 'stage': None, 'updated_at': iso(job.updated),
                   'elapsed_s': round((job.finished or now) - job.created, 1)}
            if job.progress is not None:
                out['stage'] = job.progress.stage
                if job.state == 'running':
                    out['updated_at'] = iso(max(job.updated, job.progress.updated))
            if job.state == 'done':
                out['result'] = job.result
            if job.state == 'failed':
                out['error'] = job.error
            return out
