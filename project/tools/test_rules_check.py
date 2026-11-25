"""Unit tests for the flow chart check of rules_check.py. Run: python3 -m unittest project/tools/test_rules_check.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rules_check  # noqa: E402

CHART = """```mermaid
flowchart TD
  S1[1. Ready high?] -->|yes| S2[2. Limit?]
  S1 -->|no| F[Other flow]
  F --> S3[3. Placement]
  S2 --> E2[Cause: limit]
```
"""
STEPS = [('1', 'Ready. High → step 2. Low → the other flow, then → step 3.'), ('2', 'Limit found → cause.'), ('3', 'Placement.')]


class FlowChartCheckTest(unittest.TestCase):
    def test_matching_chart_passes(self):
        self.assertEqual(rules_check.flow_chart_problems(CHART, STEPS), [])

    def test_arrow_through_other_flow_counts(self):
        edges, boxes = rules_check.chart_edges(CHART.split('\n', 1)[1].rsplit('```', 1)[0])
        self.assertIn(('1', '3'), edges)
        self.assertEqual(boxes, {'1', '2', '3'})

    def test_missing_chart(self):
        self.assertIn('without a Mermaid flowchart', rules_check.flow_chart_problems('no chart', STEPS)[0])

    def test_step_without_box(self):
        msgs = rules_check.flow_chart_problems(CHART, STEPS + [('4', 'Log.')])
        self.assertTrue(any('step 4 has no box' in m for m in msgs))

    def test_arrow_missing_from_text(self):
        steps = [('1', 'Ready. High → step 2.'), STEPS[1], STEPS[2]]
        self.assertTrue(any('chart arrow 1 → 3' in m for m in rules_check.flow_chart_problems(CHART, steps)))

    def test_branch_missing_from_chart(self):
        steps = [STEPS[0], ('2', 'Limit found → cause. None → step 3.'), STEPS[2]]
        self.assertTrue(any('no arrow 2 → 3' in m for m in rules_check.flow_chart_problems(CHART, steps)))

    def test_lettered_steps_and_ampersand(self):
        chart = "```mermaid\nflowchart TD\n  Sa[a. Ballooning] --> Sb[b. Consumed] & Sc[c. Swap]\n```"
        steps = [('a', 'Ballooning → step b; swap → step c.'), ('b', 'x'), ('c', 'y')]
        self.assertEqual(rules_check.flow_chart_problems(chart, steps), [])

    def test_hand_off_needs_a_click(self):
        steps = [('1', 'Ready high → `a/other-flow`. → step 2.'), ('2', 'x.')]
        chart = "```mermaid\nflowchart TD\n  S1[1. Ready] --> S2[2. x]\n  S1 --> O[Other]\n```"
        msgs = rules_check.flow_chart_problems(chart, steps, {'a/other-flow'})
        self.assertTrue(any('has no box with a click line' in m for m in msgs))
        linked = chart.replace('\n```', '\n  click O "https://x/blob/main/knowledge/a/other-flow.md" "Other" _blank\n```')
        self.assertEqual(rules_check.flow_chart_problems(linked, steps, {'a/other-flow'}), [])

    def test_click_without_hand_off(self):
        chart = '```mermaid\nflowchart TD\n  S1[1. x]\n  click S1 "https://x/blob/main/knowledge/a/b.md" "B" _blank\n```'
        msgs = rules_check.flow_chart_problems(chart, [('1', 'x.')], {'a/b'})
        self.assertTrue(any('no step hands off' in m for m in msgs))


if __name__ == '__main__':
    unittest.main()
