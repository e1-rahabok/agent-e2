"""Unit tests for flow_map_diagram.py. Run: python3 -m unittest project/tools/test_flow_map_diagram.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flow_map_diagram  # noqa: E402
import knowledge_loader  # noqa: E402

DOCS, _ = knowledge_loader.load()
VM_SLOW = 'vsphere/object-types/vm/troubleshooting/vm-slow'


class FlowMapTest(unittest.TestCase):
    def test_hand_off_needs_the_arrow(self):
        self.assertTrue(flow_map_diagram.HAND_OFF.search('Windows → `a/b-c`'))
        self.assertTrue(flow_map_diagram.HAND_OFF.search('→ the VM: `a/b-c`'))
        self.assertFalse(flow_map_diagram.HAND_OFF.search('events in the window (`a/b-c`, its checks)'))
        self.assertFalse(flow_map_diagram.HAND_OFF.search('→ step 3. See `a/b-c`'))

    def test_vm_slow_hands_off_to_guest_os(self):
        offs = flow_map_diagram.hand_offs(DOCS)[VM_SLOW]
        self.assertIn('guest-os/system/troubleshooting/ms-windows-slow', offs)
        self.assertIn('guest-os/system/troubleshooting/linux-os-slow', offs)

    def test_update_is_stable(self):
        text = '# Map\n\n## Flows\nTables.\n\n## Next\nMore.\n'
        once = flow_map_diagram.updated(text, DOCS)
        self.assertIn(flow_map_diagram.HEADING, once)
        self.assertEqual(flow_map_diagram.updated(once, DOCS), once)
        self.assertTrue(once.rstrip().endswith('More.'))


if __name__ == '__main__':
    unittest.main()
