"""Unit tests for project/tools/sources.py. Run: python3 -m unittest project/tools/test_sources.py"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sources  # noqa: E402

GOOD = """# VM CPU sizing

- Release: vSphere 9.1
- Date: 2026-11-18

## Sizing rule
- Fit the VM in one NUMA node first [E1].

## Evidence
- E1: Performance Best Practices for VMware vSphere 9.1 (revision 20260624), p. 23
- E2: evidence/esxtop-numa.png (ESXi 9.1)
"""


class SourcesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = sources.SOURCES
        sources.SOURCES = self.tmp.name
        os.makedirs(os.path.join(self.tmp.name, 'evidence'))
        open(os.path.join(self.tmp.name, 'evidence', 'esxtop-numa.png'), 'w').close()

    def tearDown(self):
        sources.SOURCES = self.old
        self.tmp.cleanup()

    def write(self, name, text):
        with open(os.path.join(self.tmp.name, name), 'w', encoding='utf-8') as f:
            f.write(text)

    def test_refs(self):
        self.assertEqual(sources.refs('project/sources/a.md > Sizing rule; Performance Best Practices, p. 23'),
                         [('a.md', ['Sizing rule'])])
        self.assertEqual(sources.refs('Reports > Functional Considerations'), [])
        self.assertEqual(sources.refs(None), [])

    def test_good_note(self):
        self.write('a.md', GOOD)
        self.assertEqual(sources.check('a.md', ['Sizing rule']), [])

    def test_problems(self):
        self.write('b.md', GOOD.replace('- Release: vSphere 9.1\n', '').replace('[E1]', '[E3]')
                   .replace('esxtop-numa.png', 'missing.png'))
        msgs = ' | '.join(sources.check('b.md', ['No such heading']))
        for part in ('no such heading', 'Release', '[E3]', 'missing.png'):
            self.assertIn(part, msgs)

    def test_missing_and_future(self):
        self.assertIn('does not exist', sources.check('none.md', [])[0])
        self.assertIn('not yet digested', sources.check('future/x.md', [])[0])

    def test_no_evidence_section(self):
        self.write('c.md', GOOD.split('## Evidence')[0])
        self.assertTrue(any('## Evidence' in m for m in sources.check('c.md', [])))


if __name__ == '__main__':
    unittest.main()
