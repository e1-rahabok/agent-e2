"""Tests for diagram_text.py: the text of a small SVG, and that the root documents hold current text for every diagram."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagram_text  # noqa: E402

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
<rect width="400" height="200" fill="#ffffff"/>
<text x="10" y="20" font-size="20" font-weight="bold">Title of it</text>
<text x="10" y="40" font-size="12.5">Subtitle of it</text>
<rect x="10" y="60" width="14" height="14" fill="#e6f4e4"/><text x="30" y="72" font-size="11.5">Knowledge</text>
<rect x="10" y="100" width="120" height="60" fill="#e6f4e4"/>
<text x="20" y="120" font-size="13" font-weight="bold">Box A</text><text x="20" y="140" font-size="11.5">about a</text>
<rect x="250" y="100" width="120" height="60" fill="#f2f2f2"/>
<text x="260" y="120" font-size="13" font-weight="bold">Box B</text>
<path d="M 132 130 L 248 130" fill="none" marker-end="url(#ah)"/>
<text x="190" y="122" font-size="10.5" text-anchor="middle">sends</text>
</svg>'''


class DiagramText(unittest.TestCase):
    def test_small_svg(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'a.svg')
            open(p, 'w').write(SVG)
            text = diagram_text.svg_to_text(p)
        self.assertIn('**Title of it.** Subtitle of it', text)
        self.assertIn('green = Knowledge', text)
        self.assertIn('- n1 **Box A** (Knowledge): about a', text)
        self.assertIn('- n1 Box A --> n2 Box B: sends', text)

    def test_documents_are_current(self):
        problems = []
        diagram_text.check(lambda path, msg: problems.append((path, msg)))
        self.assertEqual(problems, [])


if __name__ == '__main__':
    unittest.main()
