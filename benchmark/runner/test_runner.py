"""Tests for the benchmark runner scoring: judge reply parsing and the final score. No model calls.
Run: python3 -m unittest benchmark/runner/test_runner.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import cases as C  # noqa: E402
import judge as J  # noqa: E402
import report  # noqa: E402


def row(case, kind, credit, run, track='text', fmt='multiple-choice', exact=None, unsure=0, cw=''):
    return {'model': 'm', 'mode': 'classic', 'case_id': case, 'kind': kind, 'format': fmt, 'track': track, 'run': str(run),
            'credit': str(credit), 'exact': str(int(credit == 1) if exact is None else exact), 'unsure': str(unsure),
            'confident_wrong': cw}


class JudgeParseTest(unittest.TestCase):
    def test_json_with_text_around(self):
        v = J.parse('Here: {"score": 2, "trap": false, "unsure": false, "missed": "", "reason": "ok"} done')
        self.assertEqual(v['score'], 2)

    def test_rejects_bad_score(self):
        self.assertIsNone(J.parse('{"score": 5}'))
        self.assertIsNone(J.parse('no json'))
        self.assertIsNone(J.parse('{"score": "high"}'))


class FinalScoreTest(unittest.TestCase):
    def test_worst_run_counts_and_kinds_average(self):
        rows = [row('a', 'multiple-choice', 1, 1), row('a', 'multiple-choice', 1, 2),       # stable: 1
                row('b', 'multiple-choice', 1, 1), row('b', 'multiple-choice', 0, 2),       # luck: 0
                row('c', 'conversation', 1, 1, fmt='free-text'), row('c', 'conversation', 0.667, 2, fmt='free-text'),
                row('d', 'screenshot', 1, 1, track='vision'), row('d', 'screenshot', 1, 2, track='vision')]
        s = report.final(rows)[('m', 'classic')]
        self.assertAlmostEqual(s['final'], (1 + 0 + 0.667 + 1) / 4, places=3)
        self.assertEqual(s['multiple-choice'], 0.5)
        self.assertAlmostEqual(s['conversation'], 0.667, places=3)
        self.assertEqual(s['screenshot'], 1)
        self.assertEqual(s['luck'], 0.5)

    def test_old_text_track_ignored_when_vision_exists(self):
        rows = [row('d', 'screenshot', 0, 1, track='text'), row('d', 'screenshot', 1, 1, track='vision')]
        self.assertEqual(report.final(rows)[('m', 'classic')]['final'], 1)


class OverrideTest(unittest.TestCase):
    def test_trap_with_full_recall_counts(self):
        rows = [{'mode': 'classic', 'retrieval_recall': '1.0', 'trap': '1'},
                {'mode': 'classic', 'retrieval_recall': '1.0', 'trap': '0'},
                {'mode': 'classic', 'retrieval_recall': '0.5', 'trap': '1'},   # file missing: not an override
                {'mode': 'baseline', 'retrieval_recall': '', 'trap': '1'}]     # no knowledge base: not an override
        self.assertEqual(report.override(rows), 0.5)


class CaseKindTest(unittest.TestCase):
    def test_every_case_has_a_kind_and_free_text_has_a_key(self):
        for c in C.load():
            self.assertIn(c.kind, report.KINDS)
            if not c.choice:
                self.assertTrue(c.key_points, c.id)


if __name__ == '__main__':
    unittest.main()
