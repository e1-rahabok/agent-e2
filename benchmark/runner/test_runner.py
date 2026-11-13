"""Tests for the benchmark runner scoring: judge reply parsing and the final score. No model calls.
Run: python3 -m unittest benchmark/runner/test_runner.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import questions as C  # noqa: E402
import governor as G  # noqa: E402
import judge as J  # noqa: E402
import report  # noqa: E402
import exitcodes as X  # noqa: E402
import health as H  # noqa: E402
import naming as N  # noqa: E402
import preflight as P  # noqa: E402
import run_all as RA  # noqa: E402
import summarize as S  # noqa: E402
from llm import MockClient, ParamClient  # noqa: E402


def row(question, answer_type, inp, level, credit, run, track='text', exact=None, unsure=0, cw=''):
    return {'model': 'm', 'mode': 'classic', 'question_id': question, 'answer_type': answer_type, 'input': inp,
            'level': str(level), 'track': track, 'run': str(run),
            'credit': str(credit), 'exact': str(int(credit == 1) if exact is None else exact), 'unsure': str(unsure),
            'confident_wrong': cw}


class JudgeParseTest(unittest.TestCase):
    def test_json_with_text_around(self):
        v = J.parse('Here: {"score": 2, "misconception": false, "unsure": false, "missed": "", "reason": "ok"} done')
        self.assertEqual(v['score'], 2)

    def test_rejects_bad_score(self):
        self.assertIsNone(J.parse('{"score": 5}'))
        self.assertIsNone(J.parse('no json'))
        self.assertIsNone(J.parse('{"score": "high"}'))


class AttachmentTest(unittest.TestCase):
    """A CSV attachment reaches the model as text; a link to an attachment reaches it as its words only."""
    def _question(self):
        import tempfile
        body = ('# T\n\n## Prompt\n- [The attached table](0046/datastore-ds01-vm-disk-space.csv) lists the VMs.\n\n'
                'Which is right?\n\n- A. One\n- B. Two\n\n## Expected key points\n- Answer: A.\n\n## Metadata\n```yaml\n'
                'id: "9999"\nanswer_type: deterministic\nanswer: [A]\nattachments: [0046/datastore-ds01-vm-disk-space.csv]\n```\n')
        d = tempfile.mkdtemp()
        path = os.path.join(d, 'L2-99-t.md')
        open(path, 'w').write(body)
        return C.Question(path)

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
    def test_worst_run_counts_and_groups_average(self):
        rows = [row('a', 'deterministic', 'text', 100, 1, 1), row('a', 'deterministic', 'text', 100, 1, 2),        # stable: 1
                row('b', 'deterministic', 'text', 400, 1, 1), row('b', 'deterministic', 'text', 400, 0, 2),        # luck: 0
                row('c', 'judged', 'text', 400, 1, 1), row('c', 'judged', 'text', 400, 0.667, 2),
                row('d', 'deterministic', 'table screenshot', 400, 1, 1, track='vision'),
                row('d', 'deterministic', 'table screenshot', 400, 1, 2, track='vision')]
        s = report.final(rows)[('m', 'classic')]
        self.assertAlmostEqual(s['final'], (1 + 0 + 0.667 + 1) / 4, places=3)
        self.assertAlmostEqual(s['answer:deterministic'], 2 / 3, places=3)
        self.assertAlmostEqual(s['answer:judged'], 0.667, places=3)
        self.assertEqual(s['input:table'], 1)
        self.assertEqual(s['input:screenshot'], 1)
        self.assertEqual(s['input:table_n'], 1)
        self.assertEqual(s['level:100'], 1)
        self.assertAlmostEqual(s['level:400'], (0 + 0.667 + 1) / 3, places=3)
        self.assertEqual(s['luck'], 0.5)

    def test_old_text_track_ignored_when_vision_exists(self):
        rows = [row('d', 'deterministic', 'screenshot', 400, 0, 1, track='text'),
                row('d', 'deterministic', 'screenshot', 400, 1, 1, track='vision')]
        self.assertEqual(report.final(rows)[('m', 'classic')]['final'], 1)


class ReleaseGateTest(unittest.TestCase):
    def test_gap_and_paired_test_against_reference(self):
        rows = []
        for i in range(10):  # the model right on all 10, the reference on 2
            q = f'q{i}'
            rows.append(dict(row(q, 'deterministic', 'text', 400, 1, 1), model='e2', mode='agentic'))
            rows.append(dict(row(q, 'deterministic', 'text', 400, int(i < 2), 1), model=report.REFERENCE[0], mode=report.REFERENCE[1]))
        fin = report.final(rows)
        b, c, p = report.mcnemar(rows, 'e2', 'agentic')
        self.assertEqual((b, c), (8, 0))
        self.assertAlmostEqual(p, 1 / 256)
        g = {name.split(' (')[0]: ok for name, _, _, ok in report.gate(fin, rows, 'e2')}
        self.assertTrue(all(g.values()), g)

    def test_fails_below_final_score(self):
        rows = [dict(row(f'q{i}', 'deterministic', 'text', 400, int(i < 8), 1), model='e2', mode='agentic') for i in range(10)]
        g = {name: ok for name, _, _, ok in report.gate(report.final(rows), rows, 'e2')}
        self.assertFalse(g['Final score'])
        self.assertNotIn('Gap to the frontier model', g)


class RetrievalSummaryTest(unittest.TestCase):
    def test_main_file_misses_are_counted(self):
        import retrieval_eval as R
        rows = [('0001', ['a', 'b'], ['a'], ['a', 'b'], 'a'),
                ('0002', ['c', 'd'], ['c'], ['c'], 'd'),
                ('0003', ['e'], [], [], '')]
        s = R.summary(rows)
        self.assertEqual(s['complete'], 1)
        self.assertEqual((s['main_keyed'], s['main_missed']), (2, ['0002']))
        self.assertAlmostEqual(s['context'], 3 / 5)


class PromptSplitTest(unittest.TestCase):
    def test_bullet_options_and_blank_lines(self):
        stem, opts, footer = C.Question._split_prompt('- Fact one.\n- Fact two.\n\nChoose:\n\n- A. one\n- B. two\n\n- C. three\n\nHint: x')
        self.assertEqual([o[0] for o in opts], ['A', 'B', 'C'])
        self.assertTrue(stem.startswith('- Fact one.'))
        self.assertEqual(footer, 'Hint: x')

    def test_plain_options_still_parse(self):
        stem, opts, footer = C.Question._split_prompt('Stem\n\nA. one\nB. two')
        self.assertEqual([o[1] for o in opts], ['one', 'two'])


class OverrideTest(unittest.TestCase):
    def test_misconception_with_full_recall_counts(self):
        rows = [{'mode': 'classic', 'retrieval_recall': '1.0', 'misconception': '1'},
                {'mode': 'classic', 'retrieval_recall': '1.0', 'misconception': '0'},
                {'mode': 'classic', 'retrieval_recall': '0.5', 'misconception': '1'},   # file missing: not an override
                {'mode': 'baseline', 'retrieval_recall': '', 'misconception': '1'}]     # no knowledge base: not an override
        self.assertEqual(report.override(rows), 0.5)


class QuestionFieldsTest(unittest.TestCase):
    def test_every_question_has_groups_and_judged_has_a_key(self):
        for c in C.load():
            self.assertIn(c.answer_type, report.ANSWER_TYPES)
            self.assertTrue(set(c.input_types) <= set(report.INPUT_TYPES), c.id)
            self.assertIn(str(c.level), report.LEVELS, c.id)
            if not c.choice:
                self.assertTrue(c.key_points, c.id)


class _Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


class GovernorTest(unittest.TestCase):
    """Concurrency per model: probe above the proven value, never below it. A fake clock stands in for time."""

    def make(self, proven=None, **kw):
        self.clock, self.lines = _Clock(), []
        return G.Governor(proven or {'m': 12}, window=10, clock=self.clock, log=self.lines.append, **kw)

    def drive(self, gov, n, rate_of, model='m', tag='classic', error=lambda i: ''):
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
        g.record('m', 'classic', 'HTTP 429: rate limited')
        self.assertEqual(g.limit_of('m'), 12)
        self.drive(g, 200, lambda c: 3.0 * c)
        self.assertEqual(g.limit_of('m'), 12)

    def test_429_after_the_probe_ended_returns_to_proven(self):
        g = self.make()
        self.drive(g, 200, lambda c: 3.0 * c)
        self.assertEqual(g.limit_of('m'), 16)
        g.record('m', 'classic', 'HTTP 429: x')
        self.assertEqual(g.limit_of('m'), 12)

    def test_429_at_the_proven_value_never_lowers_it(self):
        g = self.make({'opus': 3})
        g.record('opus', 'classic', 'HTTP 429: no access')
        g.record('opus', 'classic', 'HTTP 429: no access')
        self.assertEqual(g.limit_of('opus'), 3)
        self.assertEqual(sum('proven value' in s for s in self.lines), 1)    # warned once

    def test_other_error_in_the_window_rejects_the_step(self):
        g = self.make()
        self.drive(g, 200, lambda c: 3.0 * c, error=lambda i: 'HTTP 502: bad gateway' if 14 <= i <= 40 else '')
        self.assertEqual(g.limit_of('m'), 12)

    def test_window_across_two_modes_is_measured_again(self):
        g = self.make()
        self.drive(g, 25, lambda c: 10.0 * c, tag='baseline')       # fast mode
        self.drive(g, 200, lambda c: 2.0 * c, tag='agentic')        # slow mode, same shape
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

    RUN = os.path.join(os.path.dirname(__file__), 'run.py')

    def run_py(self, *args):
        import subprocess
        return subprocess.run([sys.executable, self.RUN, '--mock', *args], capture_output=True, text=True, timeout=300)

    def test_stop_at_the_limit_then_resume_without_flags(self):
        import csv
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as out:
            r = self.run_py('--models', 'x/one,x/two', '--modes', 'classic', '--runs', '1', '--questions', 'L1-01',
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
            self.assertEqual({x['mode'] for x in rows}, {'classic'})
            self.assertTrue(os.path.exists(os.path.join(folder, 'report.md')))
            cfg = json.load(open(os.path.join(folder, 'config.json')))
            self.assertEqual(cfg['started'], started)                                   # the original start is kept
            self.assertEqual(len(cfg['resumed']), 1)
            self.assertEqual(list(cfg['models']), ['x/one', 'x/two'])


class NamingTest(unittest.TestCase):
    def test_slug_keeps_the_model_name(self):
        self.assertEqual(N.slug('google/gemma-4-31b-it'), 'gemma-4-31b-it')
        self.assertEqual(N.slug('alibaba/qwen3.8-27b'), 'qwen3.8-27b')
        self.assertEqual(N.slug('anthropic/claude-opus-5.5'), 'claude-opus-5.5')

    def test_folder_is_date_then_model_and_never_overwrites(self):
        import datetime
        import tempfile
        day = datetime.date(2026, 11, 14)
        with tempfile.TemporaryDirectory() as out:
            self.assertEqual(N.run_name(['google/gemma-4-31b-it'], out, today=day), '20261114-gemma-4-31b-it')
            os.makedirs(os.path.join(out, '20261114-gemma-4-31b-it'))
            self.assertEqual(N.run_name(['google/gemma-4-31b-it'], out, today=day), '20261114-gemma-4-31b-it-2')
            self.assertEqual(N.run_name(['a/x', 'b/y'], out, mock=True, today=day), '20261114-x+y-mock')


class HealthTest(unittest.TestCase):
    def row(self, **kw):
        r = {'model': 'm', 'answer_type': 'deterministic', 'parse_ok': 1, 'error': '', 'truncated': 0}
        r.update(kw)
        return r

    def test_healthy_run_never_trips(self):
        h = H.Health()
        self.assertTrue(all(h.record(self.row()) is None for _ in range(100)))

    def test_cut_off_answers_trip_the_check_after_enough_answers(self):
        h = H.Health(window=40, max_bad=0.25, min_answers=20)
        for _ in range(15):
            self.assertIsNone(h.record(self.row(truncated=1, parse_ok=0)))         # too few answers to judge
        reason = None
        for _ in range(10):
            reason = h.record(self.row(truncated=1, parse_ok=0))
        self.assertIn('invalid', reason)
        self.assertEqual(h.code, X.UNHEALTHY)

    def test_a_few_wrong_or_unparsed_answers_are_not_a_problem(self):
        h = H.Health()
        for i in range(60):
            self.assertIsNone(h.record(self.row(parse_ok=0 if i % 10 == 0 else 1)))     # 10% unparsed

    def test_unparsable_free_text_is_not_counted_but_an_error_is(self):
        self.assertFalse(H.Health.is_bad(self.row(answer_type='judged', parse_ok=0)))
        self.assertTrue(H.Health.is_bad(self.row(error='HTTP 500')))

    def test_budget_refusal_trips_at_once(self):
        h = H.Health()
        reason = h.record(self.row(error='HTTP 402: Insufficient funds'))
        self.assertIn('402', reason)
        self.assertEqual(h.code, X.BUDGET)

    def test_each_model_has_its_own_window(self):
        h = H.Health(min_answers=20)
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


class _Q:
    def __init__(self, id, choice=True, images=False, scorable=True):
        self.id, self.choice, self.has_images, self.scorable = id, choice, images, scorable


class PreflightTest(unittest.TestCase):
    def srow(self, mode='classic', **kw):
        r = {'mode': mode, 'answer_type': 'deterministic', 'parse_ok': '1', 'error': '', 'truncated': '0', 'latency': '10',
             'completion_tokens': '100', 'prompt_tokens': '8000', 'cost_usd': '0.01', 'steps': '1'}
        r.update(kw)
        return r

    def test_sample_is_spread_and_has_each_kind(self):
        qs = [_Q(f'c{i}') for i in range(40)] + [_Q(f'j{i}', choice=False) for i in range(20)] + [_Q('v1', images=True), _Q('skip', scorable=False)]
        ids = [q.id for q in P.pick_sample(qs, 7)]
        self.assertEqual(len(ids), 7)
        self.assertEqual(sum(i.startswith('c') for i in ids), 4)
        self.assertEqual(sum(i.startswith('j') for i in ids), 2)
        self.assertIn('v1', ids)
        self.assertNotIn('skip', ids)
        self.assertEqual(ids, [q.id for q in P.pick_sample(qs, 7)])          # the same sample every time

    def test_good_sample_has_no_problem(self):
        rows = [self.srow('classic'), self.srow('agentic', steps='4')]
        problems, stats = P.evaluate(rows, 4000, ['classic', 'agentic'])
        self.assertEqual(problems, [])
        self.assertEqual(stats['agentic']['steps'], 4)

    def test_cut_off_answers_are_a_problem(self):
        rows = [self.srow(truncated='1', completion_tokens='4000'), self.srow()]
        problems, _ = P.evaluate(rows, 4000, ['classic'])
        self.assertTrue(any('cut off' in p for p in problems))

    def test_unreadable_letters_and_errors_are_problems(self):
        rows = [self.srow(parse_ok='0'), self.srow(parse_ok='0'), self.srow(), self.srow(error='HTTP 400: reasoning not supported')]
        problems = P.evaluate(rows, 4000, ['classic'])[0]
        self.assertTrue(any('readable letter' in p for p in problems))
        self.assertTrue(any('HTTP 400' in p for p in problems))

    def test_thinking_tokens_close_to_the_cap_are_a_problem_even_when_the_answer_is_not_cut(self):
        problems = P.evaluate([self.srow(completion_tokens='3000')], 4000, ['classic'])[0]
        self.assertTrue(any('max_tokens' in p for p in problems))

    def test_a_mode_without_a_valid_answer_is_a_problem(self):
        problems = P.evaluate([self.srow('classic')], 4000, ['classic', 'web'])[0]
        self.assertTrue(any('web' in p for p in problems))

    def test_projection_scales_with_answers_and_concurrency(self):
        stats = {'classic': {'latency': 12.0, 'cost': 0.01}}
        minutes, cost = P.project(stats, n_questions=150, runs=5, judged_share=0.4, concurrency=12, judge_cost=0.0035)
        self.assertAlmostEqual(minutes, 750 * (12 + 0.4 * P.JUDGE_SECONDS) / 12 / 60, places=6)
        self.assertAlmostEqual(cost, 750 * (0.01 + 0.4 * 0.0035), places=6)


class RoundHelpersTest(unittest.TestCase):
    def test_exit_codes_map_to_actions(self):
        self.assertEqual([RA.classify(c) for c in (0, 3, 5, 6, 1, 137)], ['complete', 'stopped', 'invalid', 'refused', 'crashed', 'crashed'])

    def test_unresolved_counts_only_failures_never_answered_later(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, 'answers.csv'), 'w').write(
                'model,mode,question_id,track,run,error\n'
                'm,classic,Q1,text,1,HTTP 500\n'
                'm,classic,Q1,text,1,\n'              # retried and answered
                'm,classic,Q2,text,1,HTTP 500\n')     # still failing
            self.assertEqual(RA.unresolved(d), {('m', 'classic', 'Q2', 'text', '1')})

    def test_earlier_run_folders_move_to_the_archive_and_the_round_stays(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            for n in ('old-a', 'new-a'):
                os.makedirs(os.path.join(d, 'results', n))
                open(os.path.join(d, 'results', n, 'config.json'), 'w').write('{}')
            open(os.path.join(d, 'results', 'README.md'), 'w').write('x')
            moved = RA.archive_old(os.path.join(d, 'results'), {'new-a'}, os.path.join(d, 'arch'))
            self.assertEqual(moved, ['old-a'])
            self.assertTrue(os.path.isdir(os.path.join(d, 'arch', 'old-a')))
            self.assertTrue(os.path.isdir(os.path.join(d, 'results', 'new-a')))
            self.assertTrue(os.path.exists(os.path.join(d, 'results', 'README.md')))

    def test_first_launch_names_the_folder_and_a_resume_names_only_the_folder(self):
        e = {'model': 'a/m', 'modes': ['baseline', 'web'], 'folder': '20261114-m', 'params': {'reasoning': {'effort': 'none'}}}
        first = RA.child_cmd(e, '/out', 50, resume=False)
        self.assertIn('--name', first)
        self.assertEqual(first[first.index('--modes') + 1], 'baseline,web')
        self.assertIn('"effort": "none"', first[first.index('--params') + 1])
        again = RA.child_cmd(e, '/out', 50, resume=True)
        self.assertEqual(again[again.index('--resume') + 1], '/out/20261114-m')
        self.assertNotIn('--models', again)


class RoundRecoveryTest(unittest.TestCase):
    """run_all.py with a fake run.py that exits with scripted codes: recovery without any model call."""

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
        env = dict(os.environ, AI_GATEWAY_API_KEY='x', RUN_ALL_CHILD=os.path.join(d, 'child.py'),
                   FAKE_SEQ=os.path.join(d, 'seq.json'), FAKE_LOG=os.path.join(d, 'log.txt'))
        out = os.path.join(d, 'out')
        os.makedirs(out)
        p = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'run_all.py'), '--out', out, '--skip-preflight',
                            '--only', model, *extra], capture_output=True, text=True, env=env, timeout=120)
        calls = [json.loads(x) for x in open(os.path.join(d, 'log.txt')).read().splitlines()] if os.path.exists(os.path.join(d, 'log.txt')) else []
        return p, calls, out

    def test_a_crashed_run_is_relaunched_with_resume_then_given_up(self):
        p, calls, _ = self.round_('google/gemma-4-31b-it', [1, 1, 1, 1])
        self.assertEqual(len(calls), 3)                                   # the first launch and 2 retries (release.retries)
        self.assertNotIn('--resume', calls[0])
        self.assertIn('--resume', calls[1])
        self.assertEqual(p.returncode, X.UNHEALTHY, p.stdout + p.stderr)
        self.assertIn('NOT complete', p.stdout)

    def test_invalid_answers_restart_the_run_with_the_next_settings_and_keep_the_folder_as_evidence(self):
        p, calls, out = self.round_('alibaba/qwen3.8-27b', [X.UNHEALTHY, X.STOPPED])
        self.assertEqual(len(calls), 2, p.stdout + p.stderr)
        self.assertIn('"none"', calls[0][calls[0].index('--params') + 1])
        self.assertIn('"low"', calls[1][calls[1].index('--params') + 1])
        self.assertNotIn('--resume', calls[1])                            # from the beginning: mixed settings would measure nothing
        self.assertTrue([n for n in os.listdir(out) if '-invalid-0' in n])
        self.assertEqual(p.returncode, X.STOPPED)

    def test_invalid_answers_on_the_last_settings_fail_the_run(self):
        p, calls, _ = self.round_('google/gemma-4-31b-it', [X.UNHEALTHY])
        self.assertEqual(len(calls), 1)                                   # gemma has one entry: nothing to try
        self.assertEqual(p.returncode, X.UNHEALTHY)

    def test_a_refused_key_stops_the_round_with_the_budget_code(self):
        p, calls, _ = self.round_('google/gemma-4-31b-it', [X.BUDGET])
        self.assertEqual(p.returncode, X.BUDGET)
        self.assertIn('raise the key budget', p.stdout)

    def test_a_limit_stop_asks_for_a_relaunch_and_a_second_start_needs_resume(self):
        p, calls, out = self.round_('google/gemma-4-31b-it', [X.STOPPED])
        self.assertEqual(p.returncode, X.STOPPED)
        self.assertIn('--resume', p.stdout)
        self.assertTrue(os.path.exists(os.path.join(out, '.round.json')))


class RoundMockTest(unittest.TestCase):
    """The whole round offline: runs in parallel, one folder per model, README, earlier folders archived."""

    def test_round_end_to_end(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            out, arch = os.path.join(d, 'out'), os.path.join(d, 'arch')
            os.makedirs(os.path.join(out, '20261101-old'))
            open(os.path.join(out, '20261101-old', 'config.json'), 'w').write('{}')
            p = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'run_all.py'), '--out', out, '--archive-dir', arch,
                                '--skip-preflight', '--child-args', '--mock --runs 1 --questions L1-01,L1-02'],
                               capture_output=True, text=True, env=dict(os.environ, AI_GATEWAY_API_KEY='x'), timeout=300)
            self.assertEqual(p.returncode, X.OK, p.stdout + p.stderr)
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


class SummarizeTest(unittest.TestCase):
    def test_summary_reads_the_numbers_from_the_folders(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as out:
            run = os.path.join(os.path.dirname(__file__), 'run.py')
            for m in ('x/one', 'x/two'):
                subprocess.run([sys.executable, run, '--mock', '--models', m, '--modes', 'baseline,classic,agentic', '--runs', '1',
                                '--questions', 'L1-01,L1-02,L2-01', '--out', out], capture_output=True, text=True, timeout=300, check=True)
            folders = [os.path.join(out, n) for n in sorted(os.listdir(out))]
            text = S.build(folders)
            self.assertIn('## Final score', text)
            self.assertIn('## Lift', text)
            self.assertIn('x/one', text)
            self.assertIn('Agentic is', text)
            self.assertEqual(len(folders), 2)


class PreflightLadderTest(unittest.TestCase):
    """check_model tries the settings of a model in order and keeps the first that answers cleanly (run_sample replaced: no model call)."""

    def good(self, mode='classic'):
        return {'mode': mode, 'answer_type': 'deterministic', 'parse_ok': '1', 'error': '', 'truncated': '0', 'latency': '5',
                'completion_tokens': '120', 'prompt_tokens': '9000', 'cost_usd': '0.002', 'steps': '1'}

    def run_check(self, results):
        calls = []

        def fake(model, modes, ids, params, cfg_path, log):
            calls.append(params)
            return results[len(calls) - 1], ''
        real = P.run_sample
        P.run_sample = fake
        try:
            pf = {'min_parse_rate': 0.95, 'max_token_share': 0.5}
            ladder = [{'reasoning': {'effort': 'none'}}, {'reasoning': {'effort': 'low'}}, {'reasoning': {'effort': 'low'}, 'max_tokens': 8000}]
            v = P.check_model('x/m', ['classic'], ladder, {'max_tokens': 4000}, 'cfg', [_Q('a')], {}, pf, lambda s: None)
        finally:
            P.run_sample = real
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
