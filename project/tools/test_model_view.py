"""Unit tests for model_view.py: the review view must match what the harness sends. Run: python3 -m unittest project/tools/test_model_view.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_view  # noqa: E402
import knowledge_loader  # noqa: E402  (model_view puts harness/ on the path)

DOCS, CHUNKS = knowledge_loader.load()
VCPU = 'vsphere/technology/cpu/concepts/vcpu-states'


class ModelViewTest(unittest.TestCase):
    def test_find_by_id_and_path(self):
        self.assertIs(model_view.find(DOCS, VCPU), DOCS[VCPU])
        self.assertIs(model_view.find(DOCS, f'knowledge/{VCPU}.md'), DOCS[VCPU])
        self.assertIsNone(model_view.find(DOCS, 'no/such/file'))

    def test_chunks_are_the_indexed_text(self):
        text = model_view.view(DOCS, CHUNKS, DOCS[VCPU])
        for c in CHUNKS:
            if c.doc is DOCS[VCPU]:
                self.assertIn(c.text, text)
        self.assertNotIn('stateDiagram-v2', text)   # the chart never reaches the model
        self.assertIn('Mermaid charts: 1.', text)

    def test_up_front_line_shown(self):
        doc = next(d for d in DOCS.values() if d.meta.get('up_front'))
        text = model_view.view(DOCS, CHUNKS, doc)
        self.assertIn(f'"{doc.meta["up_front"]}"', text.split('## 3.')[0].split('## 2.')[1])

    def test_unknown_file_fails(self):
        self.assertEqual(model_view.main(['no/such/file']), 1)


if __name__ == '__main__':
    unittest.main()
