"""Tests for the benchmark runner scoring: judge reply parsing and the final score. No model calls.
Run: python3 -m unittest benchmark/runner/test_runner.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import question_files  # noqa: E402
import adaptive_concurrency  # noqa: E402
import score_report  # noqa: E402
import exit_codes  # noqa: E402
import bad_answer_guard  # noqa: E402
import run_folder_names  # noqa: E402
import round_sample_check  # noqa: E402
import round_executor  # noqa: E402
import round_summary  # noqa: E402
import round_alive_check  # noqa: E402
import run_folders_backup  # noqa: E402
import inference_providers  # noqa: E402
import round_resume  # noqa: E402
from model_client import MockClient, ParamClient  # noqa: E402


def row(question, answer_type, inp, level, credit, run, track='text', exact=None, unsure=0, cw=''):
    return {'model': 'm', 'mode': 'agent-e2', 'question_id': question, 'answer_type': answer_type, 'input': inp,
            'level': str(level), 'track': track, 'run': str(run),
            'credit': str(credit), 'exact': str(int(credit == 1) if exact is None else exact), 'unsure': str(unsure),
            'confident_wrong': cw}


class AttachmentTest(unittest.TestCase):
    """A CSV attachment reaches the model as text; a link to an attachment reaches it as its words only."""
    def _question(self):
        import tempfile
        body = ('# T\n\n## Prompt\n- [The attached table](0046/datastore-ds01-vm-disk-space.csv) lists the VMs.\n\n'
                'Which is right?\n\n- A. One\n- B. Two\n\n## Answers\nA\n\n## Explanation\n- A is correct.\n- B is wrong.\n\n## Metadata\n```yaml\n'
                'id: "9999"\nanswer_type: deterministic\nattachments: [0046/datastore-ds01-vm-disk-space.csv]\n```\n')
        d = tempfile.mkdtemp()
        path = os.path.join(d, 'L2-99-t.md')
        open(path, 'w').write(body)
        return question_files.Question(path)

    def test_link_target_stripped(self):
        q = self._question()
        self.assertIn('The attached table lists the VMs.', q.prompt)
        self.assertNotIn('0046/', q.prompt)

    def test_csv_in_text_not_in_images(self):
        import random
        q = self._question()
        text, _ = q.render(random.Random(0))
        self.assertIn('```csv', text)
        self.assertIn('Provisioned Space', text)
        self.assertIn('Provisioned Space', q.open_text())
        self.assertEqual(q.image_parts(), [])
        self.assertEqual(q.input_types, ['table'])


class FinalScoreTest(unittest.TestCase):
    def test_mean_of_runs_counts_and_worst_run_is_reported(self):
        rows = [row('a', 'deterministic', 'text', 100, 1, 1), row('a', 'deterministic', 'text', 100, 1, 2),        # stable: 1
                row('b', 'deterministic', 'text', 400, 1, 1), row('b', 'deterministic', 'text', 400, 0, 2),        # luck: 0
                row('c', 'judged', 'text', 400, 1, 1), row('c', 'judged', 'text', 400, 0.667, 2),
                row('d', 'deterministic', 'table screenshot', 400, 1, 1, track='vision'),
                row('d', 'deterministic', 'table screenshot', 400, 1, 2, track='vision')]
        s = score_report.final(rows)[('m', 'agent-e2')]
        self.assertAlmostEqual(s['final'], (1 + 0.5 + 0.8335 + 1) / 4, places=3)      # mean of the runs per question
        self.assertAlmostEqual(s['worst'], (1 + 0 + 0.667 + 1) / 4, places=3)        # lowest run per question: reported
        self.assertAlmostEqual(s['answer:deterministic'], 2.5 / 3, places=3)
        self.assertAlmostEqual(s['answer:judged'], 0.8335, places=3)
        self.assertEqual(s['input:table'], 1)
        self.assertEqual(s['input:screenshot'], 1)
        self.assertEqual(s['input:table_n'], 1)
        self.assertEqual(s['level:100'], 1)
        self.assertAlmostEqual(s['level:400'], (0.5 + 0.8335 + 1) / 3, places=3)
        self.assertEqual(s['luck'], 0.5)

    def test_old_text_track_ignored_when_vision_exists(self):
        rows = [row('d', 'deterministic', 'screenshot', 400, 0, 1, track='text'),
                row('d', 'deterministic', 'screenshot', 400, 1, 1, track='vision')]
        self.assertEqual(score_report.final(rows)[('m', 'agent-e2')]['final'], 1)


class ReleaseGateTest(unittest.TestCase):
    def test_gap_and_paired_test_against_reference(self):
        rows = []
        for i in range(10):  # the model right on all 10, the reference on 2
            q = f'q{i}'
            rows.append(dict(row(q, 'deterministic', 'text', 400, 1, 1), model='e2', mode='agent-e2'))
            rows.append(dict(row(q, 'deterministic', 'text', 400, int(i < 2), 1), model=score_report.REFERENCE[0], mode=score_report.REFERENCE[1]))
        fin = score_report.final(rows)
        b, c, p = score_report.mcnemar(rows, 'e2', 'agent-e2')
        self.assertEqual((b, c), (8, 0))
        self.assertAlmostEqual(p, 1 / 256)
        g = {name.split(' (')[0]: ok for name, _, _, ok in score_report.gate(fin, rows, 'e2')}
        self.assertTrue(all(g[k] for k in ('Final score', 'Level 400', 'Confident wrong')), g)
        self.assertIsNone(g['Gap to the frontier model'])  # an outcome, not a gate
        self.assertIsNone(g['Paired test'])

    def test_fails_below_final_score(self):
        rows = [dict(row(f'q{i}', 'deterministic', 'text', 400, int(i < 8), 1), model='e2', mode='agent-e2') for i in range(10)]
        g = {name: ok for name, _, _, ok in score_report.gate(score_report.final(rows), rows, 'e2')}
        self.assertFalse(g['Final score'])
        self.assertNotIn('Gap to the frontier model', g)


class RetrievalSummaryTest(unittest.TestCase):
    def test_main_file_misses_are_counted(self):
        import retrieval_check
        rows = [('0001', ['a', 'b'], ['a'], ['a', 'b'], 'a'),
                ('0002', ['c', 'd'], ['c'], ['c'], 'd'),
                ('0003', ['e'], [], [], '')]
        s = retrieval_check.summary(rows)
        self.assertEqual(s['complete'], 1)
        self.assertEqual((s['main_keyed'], s['main_missed']), (2, ['0002']))
        self.assertAlmostEqual(s['context'], 3 / 5)


class PromptSplitTest(unittest.TestCase):
    def test_bullet_options_and_blank_lines(self):
        stem, opts, footer = question_files.Question._split_prompt('- Fact one.\n- Fact two.\n\nChoose:\n\n- A. one\n- B. two\n\n- C. three\n\nHint: x')
        self.assertEqual([o[0] for o in opts], ['A', 'B', 'C'])
        self.assertTrue(stem.startswith('- Fact one.'))
        self.assertEqual(footer, 'Hint: x')

    def test_plain_options_still_parse(self):
        stem, opts, footer = question_files.Question._split_prompt('Stem\n\nA. one\nB. two')
        self.assertEqual([o[1] for o in opts], ['one', 'two'])

    def test_many_options_render_and_parse(self):
        # Q-E2-199 (2026-11-14): no fixed option count; 20 written options take A-T and Unsure takes U.
        import random
        letters = question_files.LETTERS[:20]
        stem, opts, footer = question_files.Question._split_prompt('Stem\n\n' + '\n'.join(f'- {x}. option {x}' for x in letters))
        self.assertEqual([o[0] for o in opts], list(letters))
        q = question_files.Question.__new__(question_files.Question)
        q.stem, q.options, q.tables, q.footer = stem, opts, '', ''
        text, mapping = q.render(random.Random(1))
        self.assertEqual(mapping['U'], 'UN')
        self.assertIn('U. Unsure', text)
        shown = next(k for k, v in mapping.items() if v == 'S')
        self.assertEqual(question_files.parse(f'ANSWER: {shown}', mapping), ['S'])
        self.assertEqual(question_files.parse('ANSWER: T, U', mapping), sorted([mapping['T'], 'UN']))


class AnswerParseTest(unittest.TestCase):
    def test_letters_not_taken_from_words_and_bold_kept(self):
        m = {c: c for c in 'ABCDEFG'}
        self.assertEqual(question_files.parse('ANSWER: C and E', m), ['C', 'E'])          # was A, C, D, E: the letters of "and"
        self.assertEqual(question_files.parse('ANSWER: **B**, **D**', m), ['B', 'D'])     # was B only
        self.assertEqual(question_files.parse('ANSWER: B. Because A is wrong', m), ['B'])
        self.assertEqual(question_files.parse('draft ANSWER: A\nANSWER: D & F', m), ['D', 'F'])   # the last ANSWER line counts
        self.assertIsNone(question_files.parse('ANSWER: none', m))

class OverrideTest(unittest.TestCase):
    def test_misconception_with_full_recall_counts(self):
        rows = [{'mode': 'agent-e2', 'retrieval_recall': '1.0', 'misconception': '1'},
                {'mode': 'agent-e2', 'retrieval_recall': '1.0', 'misconception': '0'},
                {'mode': 'agent-e2', 'retrieval_recall': '0.5', 'misconception': '1'},   # file missing: not an override
                {'mode': 'baseline', 'retrieval_recall': '', 'misconception': '1'}]     # no knowledge base: not an override
        self.assertEqual(score_report.override(rows), 0.5)


class QuestionFieldsTest(unittest.TestCase):
    def test_every_question_has_groups_and_an_answer_key(self):
        for c in question_files.load():
            self.assertIn(c.answer_type, score_report.ANSWER_TYPES)
            self.assertTrue(set(c.input_types) <= set(score_report.INPUT_TYPES), c.id)
            self.assertIn(str(c.level), score_report.LEVELS, c.id)
            self.assertTrue(c.answer, c.id)
            self.assertTrue(set(c.answer) <= {o[0] for o in c.options}, c.id)
            self.assertTrue(set(c.misconception) <= {o[0] for o in c.options}, c.id)


class _Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


class AdaptiveConcurrencyTest(unittest.TestCase):
    """Concurrency per model: probe above the proven value, never below it. A fake clock stands in for time."""

    def make(self, proven=None, **kw):
        self.clock, self.lines = _Clock(), []
        return adaptive_concurrency.AdaptiveConcurrency(proven or {'m': 12}, window=10, clock=self.clock, log=self.lines.append, **kw)

    def drive(self, gov, n, rate_of, model='m', tag='agent-e2', error=lambda i: ''):
        """n answers finish; the time between two is 1 / rate_of(current limit) minutes."""
        for i in range(n):
            self.clock.t += 60.0 / rate_of(gov.limit_of(model))
            gov.record(model, tag, error(i))
            self.assertGreaterEqual(gov.limit_of(model), gov.proven[model])

    def test_rate_rising_with_concurrency_reaches_the_top(self):
        g = self.make()
        self.drive(g, 200, lambda c: 3.0 * c)
        self.assertEqual(g.limit_of('m'), 16)

    def test_flat_rate_stays_at_the_proven_value(self):
        g = self.make()
        self.drive(g, 200, lambda c: 36.0)
        self.assertEqual(g.limit_of('m'), 12)

    def test_gain_below_half_of_the_ideal_is_rejected(self):
        g = self.make()
        self.drive(g, 200, lambda c: 10.0 * c ** 0.4)    # 12 -> 14 gives +6.4%, 8.3% needed
        self.assertEqual(g.limit_of('m'), 12)

    def test_gain_above_half_of_the_ideal_is_kept(self):
        g = self.make()
        self.drive(g, 200, lambda c: 10.0 * c ** 0.6)    # +9.7% and +8.3%
        self.assertEqual(g.limit_of('m'), 16)

    def test_429_while_probing_returns_to_proven_for_good(self):
        g = self.make()
        self.drive(g, 60, lambda c: 3.0 * c)
        self.assertGreater(g.limit_of('m'), 12)
        g.record('m', 'agent-e2', 'HTTP 429: rate limited')
        self.assertEqual(g.limit_of('m'), 12)
        self.drive(g, 200, lambda c: 3.0 * c)
        self.assertEqual(g.limit_of('m'), 12)

    def test_429_after_the_probe_ended_returns_to_proven(self):
        g = self.make()
        self.drive(g, 200, lambda c: 3.0 * c)
        self.assertEqual(g.limit_of('m'), 16)
        g.record('m', 'agent-e2', 'HTTP 429: x')
        self.assertEqual(g.limit_of('m'), 12)

    def test_429_at_the_proven_value_never_lowers_it(self):
        g = self.make({'opus': 3})
        g.record('opus', 'agent-e2', 'HTTP 429: no access')
        g.record('opus', 'agent-e2', 'HTTP 429: no access')
        self.assertEqual(g.limit_of('opus'), 3)
        self.assertEqual(sum('proven value' in s for s in self.lines), 1)    # warned once

    def test_other_error_in_the_window_rejects_the_step(self):
        g = self.make()
        self.drive(g, 200, lambda c: 3.0 * c, error=lambda i: 'HTTP 400: bad request' if 36 <= i <= 40 else '')
        self.assertEqual(g.limit_of('m'), 12)                       # the window of the first probe (answers 36 to 45) has errors

    def test_gateway_outage_neither_counts_nor_rejects(self):
        g = self.make()
        self.drive(g, 200, lambda c: 3.0 * c, error=lambda i: 'HTTP 503: unavailable' if 14 <= i <= 40 else '')
        self.assertEqual(g.limit_of('m'), 16)                       # the burst was skipped, probing went on
        self.assertFalse(any('errors' in s for s in self.lines))

    def test_gateway_outage_does_not_end_probing(self):
        g = self.make()
        self.drive(g, 20, lambda c: 3.0 * c)                        # the base window is in progress
        for _ in range(100):
            g.record('m', 'agent-e2', 'HTTP 503: unavailable')      # an outage of any length
        self.drive(g, 200, lambda c: 3.0 * c)
        self.assertEqual(g.limit_of('m'), 16)

    def test_errors_at_the_base_level_are_measured_again(self):
        g = self.make()
        self.drive(g, 30, lambda c: 3.0 * c, error=lambda i: 'HTTP 400: bad request')   # base window (after the 12 skipped) with errors
        self.assertEqual(g.limit_of('m'), 12)                       # the floor holds
        self.assertTrue(any('measuring 12 again' in s for s in self.lines))
        self.drive(g, 200, lambda c: 3.0 * c)                       # clean now: probing starts and reaches the top
        self.assertEqual(g.limit_of('m'), 16)

    def test_noise_does_not_raise_a_flat_rate(self):
        """Answer times vary by 10% (1 standard deviation) around a flat rate: no level may be kept by chance.
        Measured 2026-11-17 with the default window of 40: 0 of 200 seeds at 10%, 5% of seeds at 20% noise."""
        import random
        for seed in range(50):
            rng, t = random.Random(seed), [0.0]
            g = adaptive_concurrency.AdaptiveConcurrency({'m': 12}, clock=lambda: t[0], log=lambda s: None)
            for _ in range(400):
                t[0] += 60.0 / 36.0 * max(0.05, rng.gauss(1.0, 0.10))
                g.record('m', 'agent-e2', '')
            self.assertEqual(g.limit_of('m'), 12, f'seed {seed}')

    def test_window_across_two_modes_is_measured_again(self):
        g = self.make()
        self.drive(g, 25, lambda c: 10.0 * c, tag='baseline')       # fast mode
        self.drive(g, 200, lambda c: 2.0 * c, tag='agent-e2')        # slow mode, same shape
        self.assertEqual(g.limit_of('m'), 16)                       # not rejected for the slower mode
        self.assertTrue(any('mode changed' in s for s in self.lines))

    def test_each_model_has_its_own_proven_value_and_levels(self):
        g = self.make({'a': 12, 'b': 3})
        self.assertEqual((g.limit_of('a'), g.limit_of('b')), (12, 3))
        self.assertEqual(g.max_workers, 16)
        self.drive(g, 200, lambda c: 3.0 * c, model='b')
        self.assertEqual(g.limit_of('b'), 7)                        # 3, 5, 7
        self.assertEqual(g.limit_of('a'), 12)                       # the other model did not move

    def test_slots_are_capped_per_model(self):
        g = self.make({'m': 2, 'n': 1})
        self.assertTrue(g.acquire('m', 0.01) and g.acquire('m', 0.01))
        self.assertFalse(g.acquire('m', 0.01))
        self.assertTrue(g.acquire('n', 0.01))                       # another model has its own slots
        g.release('m')
        self.assertTrue(g.acquire('m', 0.01))

    def test_adaptive_off_keeps_the_proven_value(self):
        g = self.make(adaptive=False)
        self.drive(g, 200, lambda c: 3.0 * c)
        self.assertEqual(g.limit_of('m'), 12)
        self.assertEqual(g.max_workers, 12)


class StopAndResumeTest(unittest.TestCase):
    """--max-minutes stops cleanly; --resume continues with the settings saved in the folder. Offline (--mock)."""

    RUN = os.path.join(os.path.dirname(__file__), 'run_executor.py')

    def run_py(self, *args):
        import subprocess
        return subprocess.run([sys.executable, self.RUN, '--mock', *args], capture_output=True, text=True, timeout=300)

    def test_stop_at_the_limit_then_resume_without_flags(self):
        import csv
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as out:
            r = self.run_py('--models', 'x/one,x/two', '--modes', 'agent-e2', '--runs', '1', '--questions', 'L1-001',
                            '--out', out, '--max-minutes', '0')
            self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
            self.assertIn('--resume', r.stdout)
            folder = os.path.join(out, os.listdir(out)[0])
            self.assertFalse(os.path.exists(os.path.join(folder, 'report.md')))       # a partial run gets no report
            with open(os.path.join(folder, 'answers.csv')) as fh:
                self.assertEqual(len(list(csv.DictReader(fh))), 0)
            started = json.load(open(os.path.join(folder, 'config.json')))['started']

            r = self.run_py('--resume', folder)                                         # no --models, --modes, --runs
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(os.path.join(folder, 'answers.csv')) as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(sorted(x['model'] for x in rows), ['x/one', 'x/two'])      # only the run's own models
            self.assertEqual({x['mode'] for x in rows}, {'agent-e2'})
            self.assertTrue(os.path.exists(os.path.join(folder, 'report.md')))
            cfg = json.load(open(os.path.join(folder, 'config.json')))
            self.assertEqual(cfg['started'], started)                                   # the original start is kept
            self.assertEqual(len(cfg['resumed']), 1)
            self.assertEqual(list(cfg['models']), ['x/one', 'x/two'])


class NamingTest(unittest.TestCase):
    def test_slug_keeps_the_model_name(self):
        self.assertEqual(run_folder_names.slug('google/gemma-4-31b-it'), 'gemma-4-31b-it')
        self.assertEqual(run_folder_names.slug('alibaba/qwen3.8-27b'), 'qwen3.8-27b')
        self.assertEqual(run_folder_names.slug('anthropic/claude-opus-5.5'), 'claude-opus-5.5')

    def test_folder_is_date_then_model_and_never_overwrites(self):
        import datetime
        import tempfile
        day = datetime.date(2026, 11, 14)
        with tempfile.TemporaryDirectory() as out:
            self.assertEqual(run_folder_names.run_name(['google/gemma-4-31b-it'], out, today=day), '20261114-gemma-4-31b-it')
            os.makedirs(os.path.join(out, '20261114-gemma-4-31b-it'))
            self.assertEqual(run_folder_names.run_name(['google/gemma-4-31b-it'], out, today=day), '20261114-gemma-4-31b-it-2')
            self.assertEqual(run_folder_names.run_name(['a/x', 'b/y'], out, mock=True, today=day), '20261114-x+y-mock')


class StopRunOnBadAnswersTest(unittest.TestCase):
    def row(self, **kw):
        r = {'model': 'm', 'answer_type': 'deterministic', 'parse_ok': 1, 'error': '', 'truncated': 0}
        r.update(kw)
        return r

    def test_healthy_run_never_trips(self):
        h = bad_answer_guard.StopRunOnBadAnswers()
        self.assertTrue(all(h.record(self.row()) is None for _ in range(100)))

    def test_cut_off_answers_trip_the_check_after_enough_answers(self):
        h = bad_answer_guard.StopRunOnBadAnswers(window=40, max_bad=0.25, min_answers=20)
        for _ in range(15):
            self.assertIsNone(h.record(self.row(truncated=1, parse_ok=0)))         # too few answers to judge
        reason = None
        for _ in range(10):
            reason = h.record(self.row(truncated=1, parse_ok=0))
        self.assertIn('invalid', reason)
        self.assertEqual(h.code, exit_codes.UNHEALTHY)

    def test_a_few_wrong_or_unparsed_answers_are_not_a_problem(self):
        h = bad_answer_guard.StopRunOnBadAnswers()
        for i in range(60):
            self.assertIsNone(h.record(self.row(parse_ok=0 if i % 10 == 0 else 1)))     # 10% unparsed

    def test_unparsable_free_text_is_not_counted_but_an_error_is(self):
        self.assertFalse(bad_answer_guard.StopRunOnBadAnswers.is_bad(self.row(answer_type='judged', parse_ok=0)))
        self.assertTrue(bad_answer_guard.StopRunOnBadAnswers.is_bad(self.row(error='HTTP 500')))

    def test_budget_refusal_trips_at_once(self):
        h = bad_answer_guard.StopRunOnBadAnswers()
        reason = h.record(self.row(error='HTTP 402: Insufficient funds'))
        self.assertIn('402', reason)
        self.assertEqual(h.code, exit_codes.BUDGET)

    def test_a_burst_of_gateway_errors_stops_with_the_gateway_code_not_the_settings_code(self):
        # 2026-11-16: 54 answers failed with HTTP 503 in two minutes; the check read them as invalid settings and the runner restarted two runs from zero.
        h = bad_answer_guard.StopRunOnBadAnswers(window=40, max_bad=0.25, min_answers=20)
        reason = None
        for _ in range(30):
            reason = h.record(self.row(error='HTTP 503: {"error":{"message":"Service temporarily unavailable."}}'))
        self.assertIn('gateway', reason)
        self.assertEqual(h.code, exit_codes.GATEWAY_DOWN)
        self.assertNotEqual(h.code, exit_codes.UNHEALTHY)

    def test_gateway_errors_do_not_count_against_the_settings(self):
        h = bad_answer_guard.StopRunOnBadAnswers(window=40, max_bad=0.25, min_answers=20)
        for i in range(200):
            e = 'HTTP 503: unavailable' if i % 10 == 0 else ''        # 10% gateway errors: below the gateway limit
            self.assertIsNone(h.record(self.row(error=e)))

    def test_gateway_error_kinds(self):
        for e in ('HTTP 503: x', 'HTTP 502: x', 'HTTP 429: rate', 'HTTP 408: t', 'ReadTimeout: x', 'ConnectionError: x', 'Connection reset by peer'):
            self.assertTrue(bad_answer_guard.StopRunOnBadAnswers.is_gateway_error(self.row(error=e)), e)
        for e in ('', 'HTTP 400: bad request', 'HTTP 404: model', 'HTTP 402: budget'):
            self.assertFalse(bad_answer_guard.StopRunOnBadAnswers.is_gateway_error(self.row(error=e)), e)

    def test_request_errors_still_count_against_the_settings(self):
        h = bad_answer_guard.StopRunOnBadAnswers(window=40, max_bad=0.25, min_answers=20)
        reason = None
        for _ in range(30):
            reason = h.record(self.row(error='HTTP 400: context too long'))
        self.assertEqual(h.code, exit_codes.UNHEALTHY)
        self.assertIn('invalid', reason)

    def test_each_model_has_its_own_window(self):
        h = bad_answer_guard.StopRunOnBadAnswers(min_answers=20)
        for _ in range(30):
            h.record(self.row(model='good'))
        for _ in range(25):
            h.record(self.row(model='bad', truncated=1))
        self.assertIn('bad', h.reason)


class ParamClientTest(unittest.TestCase):
    def test_settings_of_the_model_reach_the_request_and_others_pass_through(self):
        seen = []

        class Rec(MockClient):
            def chat(self, model, messages, **kw):
                seen.append((model, kw))
                return super().chat(model, messages, **kw)
        c = ParamClient(Rec(), {'a/one': {'reasoning': {'effort': 'none'}, 'max_tokens': 8000}})
        c.chat('a/one', [{'role': 'user', 'content': 'x'}], max_tokens=4000)
        c.chat('b/two', [{'role': 'user', 'content': 'x'}], max_tokens=4000)
        self.assertEqual(seen[0][1]['reasoning'], {'effort': 'none'})
        self.assertEqual(seen[0][1]['max_tokens'], 8000)
        self.assertNotIn('reasoning', seen[1][1])
        self.assertEqual(seen[1][1]['max_tokens'], 4000)

    def test_card_sampling_replaces_the_run_temperature_and_empty_means_provider_default(self):
        seen = []

        class Rec(MockClient):
            def chat(self, model, messages, **kw):
                seen.append(kw)
                return super().chat(model, messages, **kw)
        c = ParamClient(Rec(), {}, {'a/one': {'temperature': 1.0, 'top_p': 0.95, 'top_k': 64}, 'ref/x': {}})
        c.chat('a/one', [{'role': 'user', 'content': 'x'}], temperature=0.2)
        c.chat('ref/x', [{'role': 'user', 'content': 'x'}], temperature=0.2)
        c.chat('judge/z', [{'role': 'user', 'content': 'x'}], temperature=0)
        self.assertEqual((seen[0]['temperature'], seen[0]['top_p'], seen[0]['top_k']), (1.0, 0.95, 64))
        self.assertIsNone(seen[1]['temperature'])        # None: not sent, the provider's default
        self.assertEqual(seen[2]['temperature'], 0)      # a model without an entry (the judge) keeps its own setting


class _Q:
    def __init__(self, id, choice=True, images=False, scorable=True):
        self.id, self.choice, self.has_images, self.scorable = id, choice, images, scorable


class PreflightTest(unittest.TestCase):
    def srow(self, mode='agent-e2', **kw):
        r = {'mode': mode, 'answer_type': 'deterministic', 'parse_ok': '1', 'error': '', 'truncated': '0', 'latency': '10',
             'completion_tokens': '100', 'prompt_tokens': '8000', 'cost_usd': '0.01', 'steps': '1'}
        r.update(kw)
        return r

    def test_sample_is_spread_and_has_each_kind(self):
        qs = [_Q(f'c{i}') for i in range(40)] + [_Q('v1', images=True), _Q('skip', scorable=False)]
        ids = [q.id for q in round_sample_check.pick_sample(qs, 7)]
        self.assertEqual(len(ids), 7)
        self.assertEqual(sum(i.startswith('c') for i in ids), 6)
        self.assertIn('v1', ids)
        self.assertNotIn('skip', ids)
        self.assertEqual(ids, [q.id for q in round_sample_check.pick_sample(qs, 7)])          # the same sample every time

    def test_good_sample_has_no_problem(self):
        rows = [self.srow('baseline'), self.srow('agent-e2', steps='4')]
        problems, stats = round_sample_check.evaluate(rows, 4000, ['baseline', 'agent-e2'])
        self.assertEqual(problems, [])
        self.assertEqual(stats['agent-e2']['steps'], 4)

    def test_cut_off_answers_are_a_problem(self):
        rows = [self.srow(truncated='1', completion_tokens='4000'), self.srow()]
        problems, _ = round_sample_check.evaluate(rows, 4000, ['agent-e2'])
        self.assertTrue(any('cut off' in p for p in problems))

    def test_unreadable_letters_and_errors_are_problems(self):
        rows = [self.srow(parse_ok='0'), self.srow(parse_ok='0'), self.srow(), self.srow(error='HTTP 400: reasoning not supported')]
        problems = round_sample_check.evaluate(rows, 4000, ['agent-e2'])[0]
        self.assertTrue(any('readable letter' in p for p in problems))
        self.assertTrue(any('HTTP 400' in p for p in problems))

    def test_thinking_tokens_close_to_the_cap_are_a_problem_even_when_the_answer_is_not_cut(self):
        problems = round_sample_check.evaluate([self.srow(completion_tokens='3000')], 4000, ['agent-e2'])[0]
        self.assertTrue(any('max_tokens' in p for p in problems))

    def test_a_mode_without_a_valid_answer_is_a_problem(self):
        problems = round_sample_check.evaluate([self.srow('agent-e2')], 4000, ['agent-e2', 'web'])[0]
        self.assertTrue(any('web' in p for p in problems))

    def test_projection_scales_with_answers_and_concurrency(self):
        stats = {'agent-e2': {'latency': 12.0, 'cost': 0.01}}
        minutes, cost = round_sample_check.project(stats, n_questions=150, runs=5, concurrency=12)
        self.assertAlmostEqual(minutes, 750 * 12 / 12 / 60, places=6)
        self.assertAlmostEqual(cost, 750 * 0.01, places=6)


class RoundHelpersTest(unittest.TestCase):
    def test_exit_codes_map_to_actions(self):
        self.assertEqual([round_executor.classify(c) for c in (0, 3, 5, 6, 1, 137)], ['complete', 'stopped', 'invalid', 'refused', 'crashed', 'crashed'])

    def test_unresolved_counts_only_failures_never_answered_later(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, 'answers.csv'), 'w').write(
                'model,mode,question_id,track,run,error\n'
                'm,agent-e2,Q1,text,1,HTTP 500\n'
                'm,agent-e2,Q1,text,1,\n'              # retried and answered
                'm,agent-e2,Q2,text,1,HTTP 500\n')     # still failing
            self.assertEqual(round_executor.unresolved(d), {('m', 'agent-e2', 'Q2', 'text', '1')})

    def test_earlier_run_folders_move_to_the_archive_and_the_round_stays(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            for n in ('old-a', 'new-a'):
                os.makedirs(os.path.join(d, 'results', n))
                open(os.path.join(d, 'results', n, 'config.json'), 'w').write('{}')
            open(os.path.join(d, 'results', 'README.md'), 'w').write('x')
            moved = round_executor.archive_old(os.path.join(d, 'results'), {'new-a'}, os.path.join(d, 'arch'))
            self.assertEqual(moved, ['old-a'])
            self.assertTrue(os.path.isdir(os.path.join(d, 'arch', 'old-a')))
            self.assertTrue(os.path.isdir(os.path.join(d, 'results', 'new-a')))
            self.assertTrue(os.path.exists(os.path.join(d, 'results', 'README.md')))

    def test_first_launch_names_the_folder_and_a_resume_names_only_the_folder(self):
        e = {'model': 'a/m', 'modes': ['baseline', 'web'], 'folder': '20261114-m', 'params': {'reasoning': {'effort': 'none'}}}
        first = round_executor.child_cmd(e, '/out', 50, resume=False)
        self.assertIn('--name', first)
        self.assertEqual(first[first.index('--modes') + 1], 'baseline,web')
        self.assertIn('"effort": "none"', first[first.index('--params') + 1])
        again = round_executor.child_cmd(e, '/out', 50, resume=True)
        self.assertEqual(again[again.index('--resume') + 1], os.path.join('/out', '20261114-m'))
        self.assertNotIn('--models', again)


class RoundRecoveryTest(unittest.TestCase):
    """round_executor.py with a fake run_executor.py that exits with scripted codes: recovery without any model call."""

    FAKE = (
        "import sys, os, json\n"
        "a = sys.argv\n"
        "seq = json.load(open(os.environ['FAKE_SEQ']))\n"
        "code = seq.pop(0) if seq else 0\n"
        "json.dump(seq, open(os.environ['FAKE_SEQ'], 'w'))\n"
        "open(os.environ['FAKE_LOG'], 'a').write(json.dumps(a[1:]) + '\\n')\n"
        "out = a[a.index('--out') + 1]\n"
        "folder = a[a.index('--resume') + 1] if '--resume' in a else os.path.join(out, a[a.index('--name') + 1])\n"
        "os.makedirs(folder, exist_ok=True)\n"
        "json.dump({}, open(os.path.join(folder, 'config.json'), 'w'))\n"
        "open(os.path.join(folder, 'answers.csv'), 'w').write('model,mode,question_id,track,run,error\\n')\n"
        "sys.exit(code)\n")

    def round_(self, model, seq, *extra):
        import json
        import subprocess
        import tempfile
        d = tempfile.mkdtemp()
        self.addCleanup(__import__('shutil').rmtree, d, True)
        open(os.path.join(d, 'child.py'), 'w').write(self.FAKE)
        json.dump(seq, open(os.path.join(d, 'seq.json'), 'w'))
        env = dict(os.environ, AI_GATEWAY_API_KEY='x', RUN_ALL_FAST='1', RUN_ALL_CHILD=os.path.join(d, 'child.py'),
                   FAKE_SEQ=os.path.join(d, 'seq.json'), FAKE_LOG=os.path.join(d, 'log.txt'))
        out = os.path.join(d, 'out')
        os.makedirs(out)
        p = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'round_executor.py'), '--out', out, '--skip-preflight',
                            '--only', model, *extra], capture_output=True, text=True, env=env, timeout=120)
        calls = [json.loads(x) for x in open(os.path.join(d, 'log.txt')).read().splitlines()] if os.path.exists(os.path.join(d, 'log.txt')) else []
        return p, calls, out

    def test_a_crashed_run_is_relaunched_with_resume_then_given_up(self):
        p, calls, _ = self.round_('google/gemma-4-31b-it', [1, 1, 1, 1])
        self.assertEqual(len(calls), 3)                                   # the first launch and 2 retries (release.retries)
        self.assertNotIn('--resume', calls[0])
        self.assertIn('--resume', calls[1])
        self.assertEqual(p.returncode, exit_codes.UNHEALTHY, p.stdout + p.stderr)
        self.assertIn('NOT complete', p.stdout)

    def test_a_gateway_outage_waits_and_resumes_the_same_folder_without_new_settings(self):
        p, calls, out = self.round_('alibaba/qwen3.8-27b', [exit_codes.GATEWAY_DOWN, exit_codes.GATEWAY_DOWN, exit_codes.STOPPED])
        self.assertEqual(len(calls), 3, p.stdout + p.stderr)
        self.assertNotIn('--resume', calls[0])
        self.assertIn('--resume', calls[1])
        self.assertIn('--resume', calls[2])
        self.assertEqual(calls[1][calls[1].index('--resume') + 1], calls[2][calls[2].index('--resume') + 1])   # the same folder
        self.assertFalse([n for n in os.listdir(out) if 'invalid' in n])      # nothing restarted, nothing archived
        self.assertEqual(p.returncode, exit_codes.STOPPED)

    def test_an_outage_that_never_ends_fails_the_run_after_the_waits_and_keeps_the_answers(self):
        p, calls, out = self.round_('google/gemma-4-31b-it', [exit_codes.GATEWAY_DOWN] * 30)
        self.assertEqual(len(calls), 13)                                  # the first launch and release.outage_waits (12) resumes
        self.assertEqual(p.returncode, exit_codes.UNHEALTHY)
        self.assertIn('NOT complete', p.stdout)
        self.assertFalse([n for n in os.listdir(out) if 'invalid' in n])

    def test_invalid_answers_restart_the_run_with_the_next_settings_and_keep_the_folder_as_evidence(self):
        p, calls, out = self.round_('alibaba/qwen3.8-27b', [exit_codes.UNHEALTHY, exit_codes.STOPPED])
        self.assertEqual(len(calls), 2, p.stdout + p.stderr)
        self.assertIn('"none"', calls[0][calls[0].index('--params') + 1])
        self.assertIn('"low"', calls[1][calls[1].index('--params') + 1])
        self.assertNotIn('--resume', calls[1])                            # from the beginning: mixed settings would measure nothing
        self.assertTrue([n for n in os.listdir(out) if '-invalid-0' in n])
        self.assertEqual(p.returncode, exit_codes.STOPPED)

    def test_invalid_answers_on_the_last_settings_fail_the_run(self):
        p, calls, _ = self.round_('google/gemma-4-31b-it', [exit_codes.UNHEALTHY])
        self.assertEqual(len(calls), 1)                                   # gemma has one entry: nothing to try
        self.assertEqual(p.returncode, exit_codes.UNHEALTHY)

    def test_a_refused_key_stops_the_round_with_the_budget_code(self):
        p, calls, _ = self.round_('google/gemma-4-31b-it', [exit_codes.BUDGET])
        self.assertEqual(p.returncode, exit_codes.BUDGET)
        self.assertIn('raise the key budget', p.stdout)

    def test_a_limit_stop_asks_for_a_relaunch_and_a_second_start_needs_resume(self):
        p, calls, out = self.round_('google/gemma-4-31b-it', [exit_codes.STOPPED])
        self.assertEqual(p.returncode, exit_codes.STOPPED)
        self.assertIn('--resume', p.stdout)
        self.assertTrue(os.path.exists(os.path.join(out, '.round.json')))


class ResumeOnSessionStartTest(unittest.TestCase):
    """The SessionStart hook resumes an interrupted round, and does nothing otherwise."""

    CFG = {'runs': 1}

    def setUp(self):
        import tempfile
        self.d = tempfile.mkdtemp()
        self.addCleanup(__import__('shutil').rmtree, self.d, True)

    def state(self, runs):
        import json
        json.dump({'started': '2026-11-16T10:00:00', 'runs': runs}, open(os.path.join(self.d, round_executor.STATE), 'w'))

    def folder(self, name, good):
        os.makedirs(os.path.join(self.d, name), exist_ok=True)
        with open(os.path.join(self.d, name, 'answers.csv'), 'w') as f:
            f.write('model,mode,question_id,track,run,error\n')
            for i in range(good):
                f.write(f'm,baseline,q{i},text,1,\n')

    def entry(self, name, status='running'):
        return {'model': 'm', 'modes': ['baseline'], 'folder': name, 'status': status}

    def test_no_round_no_action(self):
        self.assertEqual(round_resume.decide(self.d, self.CFG, 4, [])[0], 'nothing')

    def test_an_unfinished_run_with_no_process_is_resumed(self):
        self.state([self.entry('r1')])
        self.folder('r1', 2)
        self.assertEqual(round_resume.decide(self.d, self.CFG, 4, []), ('resume', ['r1']))

    def test_a_run_with_a_live_process_is_left_alone(self):
        self.state([self.entry('r1')])
        self.folder('r1', 2)
        ps = ['python3 benchmark/runner/run_executor.py --resume benchmark/results/r1']
        self.assertEqual(round_resume.decide(self.d, self.CFG, 4, ps)[0], 'nothing')

    def test_a_state_file_whose_folders_are_gone_is_left_alone(self):
        self.state([self.entry('renamed-or-archived')])
        self.assertEqual(round_resume.decide(self.d, self.CFG, 4, [])[0], 'nothing')

    def test_a_finished_round_is_left_alone(self):
        self.state([self.entry('r1', 'complete')])
        self.folder('r1', 4)
        self.assertEqual(round_resume.decide(self.d, self.CFG, 4, [])[0], 'nothing')

    def test_a_run_that_waits_for_the_author_is_not_resumed(self):
        self.state([self.entry('r1', 'invalid')])
        self.folder('r1', 2)
        self.assertEqual(round_resume.decide(self.d, self.CFG, 4, [])[0], 'nothing')

    def test_a_refused_or_stopped_run_is_resumed(self):
        for status in ('refused', 'stopped', 'outage', 'failed'):
            self.state([self.entry('r1', status)])
            self.folder('r1', 1)
            self.assertEqual(round_resume.decide(self.d, self.CFG, 4, [])[0], 'resume', status)

    def test_the_hook_script_does_nothing_outside_a_remote_session_or_without_a_round(self):
        import subprocess
        hook = os.path.join(os.path.dirname(__file__), '..', '..', '.claude', 'hooks', 'resume_unfinished_benchmark_round.sh')
        for env in ({'CLAUDE_CODE_REMOTE': ''}, {'CLAUDE_CODE_REMOTE': 'true', 'CLAUDE_PROJECT_DIR': self.d}):
            p = subprocess.run(['bash', hook], capture_output=True, text=True, env=dict(os.environ, **env), timeout=60)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(p.stdout.strip(), '')


class SnapshotBranchTest(unittest.TestCase):
    """Snapshots go to their own branch, built with a temporary index: the working branch is not touched."""

    def sh(self, repo, *args):
        import subprocess
        return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, check=True).stdout.strip()

    def setUp(self):
        import tempfile
        self.d = tempfile.mkdtemp()
        self.addCleanup(__import__('shutil').rmtree, self.d, True)
        self.remote, self.repo = os.path.join(self.d, 'remote.git'), os.path.join(self.d, 'repo')
        os.makedirs(self.remote)
        os.makedirs(self.repo)
        self.sh(self.remote, 'init', '-q', '--bare')
        self.sh(self.repo, 'init', '-q', '-b', 'work')
        self.sh(self.repo, 'config', 'user.name', 't')
        self.sh(self.repo, 'config', 'user.email', 't@x')
        open(os.path.join(self.repo, 'README.md'), 'w').write('x')
        self.sh(self.repo, 'add', 'README.md')
        self.sh(self.repo, 'commit', '-q', '-m', 'first')
        self.sh(self.repo, 'remote', 'add', 'origin', self.remote)
        self.results = os.path.join(self.repo, 'benchmark', 'results')
        run = os.path.join(self.results, 'r1')
        os.makedirs(run)
        for n, t in (('answers.csv', 'a'), ('config.json', '{}'), ('report.md', '# r'), ('traces.jsonl', 'big'), ('run.log', 'log')):
            open(os.path.join(run, n), 'w').write(t)

    def test_a_snapshot_holds_the_answers_configs_and_reports_but_not_the_traces(self):
        c = run_folders_backup.snapshot(self.repo, self.results, 'snapshots/round-x', 'origin')
        self.assertTrue(c)
        files = self.sh(self.remote, 'ls-tree', '-r', '--name-only', 'snapshots/round-x').splitlines()
        self.assertIn('benchmark/results/r1/answers.csv', files)
        self.assertIn('benchmark/results/r1/config.json', files)
        self.assertIn('benchmark/results/r1/report.md', files)
        self.assertNotIn('benchmark/results/r1/traces.jsonl', files)
        self.assertNotIn('benchmark/results/r1/run.log', files)
        self.assertIn('README.md', files)                                  # the tree of HEAD is kept

    def test_the_working_branch_index_and_files_are_not_touched(self):
        head = self.sh(self.repo, 'rev-parse', 'HEAD')
        run_folders_backup.snapshot(self.repo, self.results, 'snapshots/round-x', 'origin')
        self.assertEqual(self.sh(self.repo, 'rev-parse', 'HEAD'), head)
        self.assertEqual(self.sh(self.repo, 'branch', '--show-current'), 'work')
        self.assertEqual(self.sh(self.repo, 'diff', '--cached', '--name-only'), '')           # nothing staged
        self.assertTrue(os.path.exists(os.path.join(self.results, 'r1', 'traces.jsonl')))

    def test_no_change_gives_no_new_commit_and_a_change_chains_on_the_previous_snapshot(self):
        c1 = run_folders_backup.snapshot(self.repo, self.results, 'snapshots/round-x', 'origin')
        self.assertIsNone(run_folders_backup.snapshot(self.repo, self.results, 'snapshots/round-x', 'origin'))
        open(os.path.join(self.results, 'r1', 'answers.csv'), 'w').write('a,b')
        c2 = run_folders_backup.snapshot(self.repo, self.results, 'snapshots/round-x', 'origin')
        self.assertNotEqual(c1, c2)
        self.assertEqual(self.sh(self.repo, 'rev-parse', f'{c2}^'), c1)
        self.assertEqual(self.sh(self.remote, 'rev-parse', 'snapshots/round-x'), c2)

    def test_folders_outside_the_repository_are_skipped(self):
        import tempfile
        other = tempfile.mkdtemp()
        self.addCleanup(__import__('shutil').rmtree, other, True)
        os.makedirs(os.path.join(other, 'r'))
        open(os.path.join(other, 'r', 'config.json'), 'w').write('{}')
        self.assertIsNone(run_folders_backup.snapshot(self.repo, other, 'snapshots/round-y', 'origin'))


class CheckRoundIsAliveTest(unittest.TestCase):
    """The progress check must not read stale counts as progress (2026-11-16: a machine restart killed two runs unseen for 25 minutes)."""

    def setUp(self):
        import tempfile
        self.d = tempfile.mkdtemp()
        self.addCleanup(__import__('shutil').rmtree, self.d, True)
        self.now = __import__('datetime').datetime(2026, 11, 16, 14, 0, 0)

    def folder(self, name, good, minutes_ago, total_q=4):
        import json
        import time
        f = os.path.join(self.d, name)
        os.makedirs(f)
        json.dump({'questions': [f'q{i}' for i in range(total_q)], 'runs': 1, 'modes': ['baseline']}, open(os.path.join(f, 'config.json'), 'w'))
        with open(os.path.join(f, 'answers.csv'), 'w') as fh:
            fh.write('model,mode,question_id,track,run,error,cost_usd\n')
            for i in range(good):
                fh.write(f'm,baseline,q{i},text,1,,0.5\n')
        t = time.mktime((self.now - __import__('datetime').timedelta(minutes=minutes_ago)).timetuple())
        os.utime(os.path.join(f, 'answers.csv'), (t, t))
        return f

    PS = ['python3 benchmark/runner/run_executor.py --out o --resume benchmark/results/run-a']

    def status(self, f, ps, boot=None):
        return round_alive_check.run_status(f, self.now, ps, boot)

    def test_a_finished_folder_is_done(self):
        self.assertEqual(self.status(self.folder('run-a', 4, 90), [])['verdict'], 'DONE')

    def test_a_process_and_a_recent_write_is_alive(self):
        self.assertEqual(self.status(self.folder('run-a', 2, 1), self.PS)['verdict'], 'ALIVE')

    def test_a_process_with_no_write_for_minutes_is_stalled(self):
        self.assertEqual(self.status(self.folder('run-a', 2, 12), self.PS)['verdict'], 'STALLED')

    def test_no_process_and_an_unfinished_folder_is_dead(self):
        self.assertEqual(self.status(self.folder('run-a', 2, 3), [])['verdict'], 'DEAD')

    def test_a_boot_after_the_last_write_says_machine_restarted(self):
        import datetime
        boot = self.now - datetime.timedelta(minutes=5)
        self.assertEqual(self.status(self.folder('run-a', 2, 30), [], boot)['verdict'], 'MACHINE RESTARTED')

    def test_the_process_of_another_folder_does_not_count(self):
        self.assertEqual(self.status(self.folder('run-b', 2, 1), self.PS)['verdict'], 'DEAD')

    def test_the_old_script_name_counts_as_a_process(self):
        self.assertTrue(round_alive_check.processes_for('run-a', ['python3 benchmark/runner/run.py --resume benchmark/results/run-a']))

    def test_good_answers_and_cost_are_counted(self):
        r = self.status(self.folder('run-a', 3, 1), self.PS)
        self.assertEqual((r['good'], r['total']), (3, 4))
        self.assertAlmostEqual(r['cost'], 1.5)


class ReconcileWithFoldersTest(unittest.TestCase):
    """A resume starts from the folders: what the state file says can be out of date (a run finished by hand, a key topped up)."""

    def setUp(self):
        import tempfile
        self.d = tempfile.mkdtemp()
        self.addCleanup(__import__('shutil').rmtree, self.d, True)
        self.cfg = {'runs': 1}

    def folder(self, name, rows):
        os.makedirs(os.path.join(self.d, name))
        with open(os.path.join(self.d, name, 'answers.csv'), 'w') as f:
            f.write('model,mode,question_id,track,run,error\n')
            for q, e in rows:
                f.write(f'm,baseline,{q},text,1,{e}\n')

    def entry(self, name, status):
        return {'model': 'm', 'modes': ['baseline'], 'folder': name, 'status': status, 'retries': 2, 'outage_waits': 3}

    def test_a_finished_folder_is_complete_whatever_the_state_says(self):
        self.folder('a', [('q1', ''), ('q2', '')])
        st = {'runs': [self.entry('a', 'invalid')]}
        round_executor.reconcile_with_folders(st, self.d, self.cfg, 2)
        self.assertEqual(st['runs'][0]['status'], 'complete')

    def test_every_stop_but_a_real_settings_failure_becomes_pending(self):
        for status in ('refused', 'stopped', 'running', 'failed', 'outage', 'pending'):
            self.folder(status, [('q1', '')])
            st = {'runs': [self.entry(status, status)]}
            round_executor.reconcile_with_folders(st, self.d, self.cfg, 2)
            self.assertEqual(st['runs'][0]['status'], 'pending', status)
            self.assertEqual((st['runs'][0]['retries'], st['runs'][0]['outage_waits']), (0, 0))

    def test_a_run_with_unresolved_failures_is_not_complete(self):
        self.folder('b', [('q1', ''), ('q2', 'HTTP 503: x')])
        st = {'runs': [self.entry('b', 'stopped')]}
        round_executor.reconcile_with_folders(st, self.d, self.cfg, 2)
        self.assertEqual(st['runs'][0]['status'], 'pending')

    def test_a_run_marked_invalid_for_its_settings_stays_invalid(self):
        self.folder('c', [('q1', '')])
        st = {'runs': [self.entry('c', 'invalid')]}
        round_executor.reconcile_with_folders(st, self.d, self.cfg, 2)
        self.assertEqual(st['runs'][0]['status'], 'invalid')


class RoundMockTest(unittest.TestCase):
    """The whole round offline: runs in parallel, one folder per model, README, earlier folders archived."""

    def test_round_end_to_end(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            out, arch = os.path.join(d, 'out'), os.path.join(d, 'arch')
            os.makedirs(os.path.join(out, '20261101-old'))
            open(os.path.join(out, '20261101-old', 'config.json'), 'w').write('{}')
            p = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'round_executor.py'), '--out', out, '--archive-dir', arch,
                                '--skip-preflight', '--child-args', '--mock --runs 1 --questions L1-001,L1-002'],
                               capture_output=True, text=True, env=dict(os.environ, AI_GATEWAY_API_KEY='x'), timeout=300)
            self.assertEqual(p.returncode, exit_codes.OK, p.stdout + p.stderr)
            names = sorted(n for n in os.listdir(out))
            self.assertEqual([n.split('-', 1)[1] for n in names if n != 'README.md'],
                             ['claude-opus-5.5', 'gemma-4-31b-it', 'muse-glimmer-30b', 'qwen3.8-27b'])
            self.assertIn('README.md', names)
            self.assertNotIn('.round.json', os.listdir(out))               # a finished round leaves no state
            self.assertTrue(os.path.isdir(os.path.join(arch, '20261101-old')))
            text = open(os.path.join(out, 'README.md')).read()
            for m in ('gemma-4-31b-it', 'qwen3.8-27b', 'muse-glimmer-30b', 'claude-opus-5.5'):
                self.assertIn(m, text)
            self.assertIn('## Reading', text)


class ProviderHostsTest(unittest.TestCase):
    """The five runs of a question prefer different provider hosts; a host that fails is left out."""

    REPLY = {'choices': [{'message': {'content': 'OK', 'provider_metadata': {'gateway': {'routing': {
        'finalProvider': 'novita', 'fallbacksAvailable': ['friendli', 'gmicloud', 'parasail']}}}}}]}

    class Fake:
        def __init__(self, reply, down=()):
            self.reply, self.down, self.calls = reply, set(down), []

        def _post(self, path, body):
            only = ((body.get('providerOptions') or {}).get('gateway') or {}).get('only')
            self.calls.append(only)
            if only and only[0] in self.down:
                raise RuntimeError('HTTP 503: Service temporarily unavailable')
            return self.reply, {}, 0.1

    def test_the_routing_names_the_host_and_the_others(self):
        self.assertEqual(inference_providers.hosts_in(inference_providers.routing_of(self.REPLY)), ['novita', 'friendli', 'gmicloud', 'parasail'])

    def test_a_reply_without_routing_gives_no_hosts(self):
        self.assertEqual(inference_providers.hosts_in(inference_providers.routing_of({'choices': [{'message': {'content': 'OK'}}]})), [])

    def test_each_run_prefers_another_host_and_the_others_follow(self):
        hosts = ['a', 'b', 'c']
        self.assertEqual([inference_providers.order_for_run(hosts, r)[0] for r in (1, 2, 3, 4, 5)], ['a', 'b', 'c', 'a', 'b'])
        self.assertEqual(inference_providers.order_for_run(hosts, 2), ['b', 'a', 'c'])
        self.assertEqual(sorted(inference_providers.order_for_run(hosts, 3)), ['a', 'b', 'c'])      # every host stays as a fallback

    def test_one_host_means_no_spreading(self):
        self.assertEqual(inference_providers.order_for_run(['a'], 3), [])
        self.assertEqual(inference_providers.order_for_run([], 1), [])

    def test_a_host_that_fails_is_left_out_of_the_round(self):
        client, lines = self.Fake(self.REPLY, down={'gmicloud'}), []
        good = inference_providers.choose_hosts(client, 'google/gemma-4-31b-it', log=lines.append)
        self.assertEqual(good, ['novita', 'friendli', 'parasail'])
        self.assertTrue([x for x in lines if 'gmicloud' in x])

    def test_fewer_than_two_working_hosts_means_the_gateway_chooses(self):
        client = self.Fake(self.REPLY, down={'friendli', 'gmicloud', 'parasail'})
        self.assertEqual(inference_providers.choose_hosts(client, 'm', log=lambda s: None), [])

    def test_a_model_with_one_host_is_not_spread(self):
        one = {'choices': [{'message': {'provider_metadata': {'gateway': {'routing': {'finalProvider': 'x', 'fallbacksAvailable': []}}}}}]}
        self.assertEqual(inference_providers.choose_hosts(self.Fake(one), 'm', log=lambda s: None), [])

    def test_a_run_gets_its_hosts_and_records_the_preferred_host_offline(self):
        import csv
        import json
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, 'out')
            os.makedirs(out)
            hosts = json.dumps({'google/gemma-4-31b-it': ['a', 'b', 'c']})
            p = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'run_executor.py'), '--out', out, '--mock',
                                '--models', 'google/gemma-4-31b-it', '--modes', 'baseline', '--runs', '3', '--questions', 'L1-001', '--hosts', hosts],
                               capture_output=True, text=True, env=dict(os.environ, AI_GATEWAY_API_KEY='x'), timeout=120)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            run_dir = os.path.join(out, os.listdir(out)[0])
            rows = sorted(csv.DictReader(open(os.path.join(run_dir, 'answers.csv'), encoding='utf-8')), key=lambda r: r['run'])
            self.assertEqual([r['provider'] for r in rows], ['a', 'b', 'c'])        # run 1, 2, 3 prefer a, b, c
            self.assertEqual(json.load(open(os.path.join(run_dir, 'config.json')))['hosts'], {'google/gemma-4-31b-it': ['a', 'b', 'c']})


class SummarizeTest(unittest.TestCase):
    def test_summary_reads_the_numbers_from_the_folders(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as out:
            run = os.path.join(os.path.dirname(__file__), 'run_executor.py')
            for m in ('x/one', 'x/two'):
                subprocess.run([sys.executable, run, '--mock', '--models', m, '--modes', 'baseline,agent-e2', '--runs', '1',
                                '--questions', 'L1-001,L1-002,L2-001', '--out', out], capture_output=True, text=True, timeout=300, check=True)
            folders = [os.path.join(out, n) for n in sorted(os.listdir(out))]
            text = round_summary.build(folders)
            self.assertIn('## Final score', text)
            self.assertIn('## Lift', text)
            self.assertIn('x/one', text)
            self.assertIn('Agent E2 is', text)
            self.assertEqual(len(folders), 2)


class PreflightLadderTest(unittest.TestCase):
    """check_model tries the settings of a model in order and keeps the first that answers cleanly (run_sample replaced: no model call)."""

    def good(self, mode='agent-e2'):
        return {'mode': mode, 'answer_type': 'deterministic', 'parse_ok': '1', 'error': '', 'truncated': '0', 'latency': '5',
                'completion_tokens': '120', 'prompt_tokens': '9000', 'cost_usd': '0.002', 'steps': '1'}

    def run_check(self, results):
        calls = []

        def fake(model, modes, ids, params, cfg_path, log):
            calls.append(params)
            return results[len(calls) - 1], ''
        real = round_sample_check.run_sample
        round_sample_check.run_sample = fake
        try:
            pf = {'min_parse_rate': 0.95, 'max_token_share': 0.5}
            ladder = [{'reasoning': {'effort': 'none'}}, {'reasoning': {'effort': 'low'}}, {'reasoning': {'effort': 'low'}, 'max_tokens': 8000}]
            v = round_sample_check.check_model('x/m', ['agent-e2'], ladder, {'max_tokens': 4000}, 'cfg', [_Q('a')], {}, pf, lambda s: None)
        finally:
            round_sample_check.run_sample = real
        return v, calls

    def test_first_clean_setting_wins(self):
        v, calls = self.run_check([[self.good()]])
        self.assertTrue(v['ok'])
        self.assertEqual(len(calls), 1)
        self.assertEqual(v['params'], {'reasoning': {'effort': 'none'}})

    def test_a_cut_off_sample_moves_to_the_next_setting(self):
        cut = dict(self.good(), truncated='1', completion_tokens='4000')
        v, calls = self.run_check([[cut], [self.good()]])
        self.assertTrue(v['ok'])
        self.assertEqual(v['params'], {'reasoning': {'effort': 'low'}})
        self.assertEqual(len(v['attempts']), 2)

    def test_the_cap_that_is_judged_is_the_one_of_the_setting(self):
        # 3,000 tokens is over half of 4,000 but under half of 8,000: only the last entry passes
        heavy = dict(self.good(), completion_tokens='3000')
        v, calls = self.run_check([[heavy], [heavy], [heavy]])
        self.assertTrue(v['ok'])
        self.assertEqual(v['params']['max_tokens'], 8000)

    def test_no_clean_setting_fails_the_model(self):
        cut = dict(self.good(), truncated='1')
        v, calls = self.run_check([[cut], [cut], [cut]])
        self.assertFalse(v['ok'])
        self.assertEqual(len(calls), 3)

    def test_a_refused_key_stops_at_once(self):
        v, calls = self.run_check([[dict(self.good(), error='HTTP 402: no funds')]])
        self.assertTrue(v['refused'])
        self.assertEqual(len(calls), 1)


if __name__ == '__main__':
    unittest.main()
