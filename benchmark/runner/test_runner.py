"""Tests for the benchmark runner scoring: judge reply parsing and the final score. No model calls.
Run: python3 -m unittest benchmark/runner/test_runner.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import questions as C  # noqa: E402
import judge as J  # noqa: E402
import report  # noqa: E402


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


if __name__ == '__main__':
    unittest.main()
