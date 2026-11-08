"""Tests for the harness tools. Run: python3 -m unittest harness/test_tools.py (from the repository root)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import calc  # noqa: E402
import catalog  # noqa: E402
import flows  # noqa: E402
import kb  # noqa: E402
import modes  # noqa: E402
import verify  # noqa: E402
from llm import MockClient  # noqa: E402
from retrieval import Retriever  # noqa: E402

DOCS, CHUNKS = kb.load()
CAT = catalog.get(DOCS)


class MovedTest(unittest.TestCase):
    def test_old_id_resolves_to_current_file(self):
        import kb
        self.assertTrue(kb.MOVED, 'knowledge/moved.yaml is empty')
        for old, new in kb.MOVED.items():
            self.assertEqual(kb.resolve(old), new)
            self.assertIn(new, DOCS)
        self.assertEqual(kb.resolve('vsphere/foundations/resource-controls'), 'vsphere/foundations/resource-controls')


class CatalogTest(unittest.TestCase):
    def test_counter_by_full_name(self):
        r = CAT.lookup('cpu.ready.summation')
        top = r['counters'][0]
        self.assertEqual((top['counter'], top['object'], top['rollup'], top['level']), ('cpu.ready', 'VirtualMachine', 'Summation', 1))
        self.assertEqual(top['kb'], 'vsphere/technology/cpu/metrics/virtual-motherboard/ready')

    def test_gpu_is_level_4(self):
        r = CAT.lookup('GPU utilization')
        self.assertTrue(r['counters'])
        self.assertTrue(all(c['level'] == 4 for c in r['counters']))

    def test_api_units(self):
        r = CAT.lookup('mem.vmmemctl', object='vm')
        self.assertEqual((r['api'][0]['unit'], r['api'][0]['level']), ('kiloBytes', 1))
        self.assertEqual(r['counters'][0]['unit'], 'Megabytes (MB)')

    def test_esxtop_field(self):
        self.assertEqual(CAT.lookup('%RDY')['esxtop'][0]['field'], '%RDY')
        self.assertTrue(CAT.lookup('DAVG')['esxtop'][0]['field'].startswith('DAVG'))

    def test_object_filter(self):
        r = CAT.lookup('balloon', object='vm')
        self.assertTrue(r['counters'])
        self.assertTrue(all(c['object'] == 'VirtualMachine' for c in r['counters']))

    def test_thresholds_have_source(self):
        r = CAT.lookup('KAVG')
        self.assertTrue(any(t['value'] == 0.5 and t['source'] == 'book' for t in r['thresholds']))

    def test_bands_parsed_from_knowledge(self):
        bands = CAT.thresholds(name='Peak CPU Ready among any vCPU')['bands']
        self.assertEqual((bands[0]['green'], bands[0]['red']), ('0-2', '8-16'))

    def test_object_path(self):
        p = CAT.path('vm', 'cluster')['path']
        self.assertIsNotNone(p)
        self.assertLessEqual(len(p), 3)
        self.assertIn('many-to-many', ' '.join(CAT.path('VirtualMachine', 'Datastore')['path']))

    def test_facts_for_context(self):
        f = CAT.facts_for(['vsphere/technology/cpu/metrics/virtual-motherboard/ready'])
        self.assertIn('cpu.ready', f)
        self.assertIn('statistics level 1', f)
        self.assertIn('Threshold', f)


class KpiLookupTest(unittest.TestCase):
    def test_model_found_by_title_with_bands(self):
        r = CAT.lookup('Cluster Risk')
        self.assertTrue(r['metric_files'])
        self.assertTrue(r['bands'])


class CalcTest(unittest.TestCase):
    def r(self, e):
        return calc.evaluate(e)['result']

    def test_summation(self):
        self.assertEqual(self.r('summation_to_percent(2000, 20, 1)'), 10)
        self.assertAlmostEqual(self.r('summation_to_percent(2000, 300)'), 0.666667)
        self.assertEqual(self.r('percent_to_summation(100, 20, 4)'), 80000)

    def test_units(self):
        self.assertEqual(self.r('convert(1, "GB", "MB")'), 1024)
        self.assertEqual(self.r('convert(1, "Gbps", "Mbps")'), 1000)
        self.assertEqual(self.r('convert(8, "Mb", "MBd")'), 1)
        self.assertEqual(self.r('convert(3, "GHz", "MHz")'), 3000)
        self.assertIn('ambiguous', ' '.join(calc.evaluate('convert(1, "Kbps", "KBps")')['notes']))

    def test_rejects_unsafe_and_bad_input(self):
        self.assertIn('error', calc.evaluate('__import__("os")'))
        self.assertIn('error', calc.evaluate('2 ** 1000'))
        self.assertIn('thousands', calc.evaluate('13,856 * 300')['error'])
        self.assertIn('error', calc.evaluate('convert(1, "GB", "ms")'))


class FlowTest(unittest.TestCase):
    def test_every_flow_parses(self):
        self.assertEqual(flows.check(DOCS), [])
        self.assertGreaterEqual(len(flows.flow_ids(DOCS)), 12)

    def test_step_and_reference(self):
        out = flows.run(DOCS, 'vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high', '4')
        self.assertEqual((out['of'], out['next'], out['refers_to']), (6, '5', ['2']))

    def test_lettered_steps(self):
        out = flows.run(DOCS, 'vsphere/technology/memory/troubleshooting/overcommit-indicators')
        self.assertEqual(len(out['steps']), 4)
        self.assertTrue(out['steps'][0].startswith('a. '))

    def test_unknown(self):
        self.assertIn('flows', flows.run(DOCS, 'vsphere/technology/cpu/metrics/virtual-motherboard/ready'))


class VerifyTest(unittest.TestCase):
    Q = 'Stem\n\nA. one\nB. two\nC. Not covered by the knowledge base.\nD. Unsure: the information available does not settle this question.'

    def types(self, reply, context=''):
        return [(i['type'], i['hard']) for i in verify.check(reply, self.Q, context, set(DOCS))]

    def test_clean(self):
        self.assertEqual(self.types('ANSWER: A, B\nREASON: fine.'), [])

    def test_hard(self):
        self.assertIn(('format', True), self.types('I think A'))
        self.assertIn(('format', True), self.types('ANSWER: F\nREASON: x'))
        self.assertIn(('hedge', True), self.types('ANSWER: A, D\nREASON: x'))

    def test_soft(self):
        self.assertIn(('ungrounded', False), self.types('ANSWER: A\nREASON: Ready above 25% is bad.', context='Ready above 50%'))
        self.assertEqual(self.types('ANSWER: A\nREASON: Ready above 50% is bad.', context='Ready above 50%'), [])
        self.assertIn(('citation', False), self.types('ANSWER: A\nREASON: see vsphere/cpu/metrics/nope.'))


class ModesTest(unittest.TestCase):
    CFG = {'temperature': 0.2, 'max_tokens': 100, 'classic_k': 4, 'context_tokens': 6000,
           'agent_max_calls': 8, 'agent_tool_tokens': 20000}

    def test_agentic_uses_new_tools(self):
        ret = Retriever(DOCS, CHUNKS)
        res, used, trace, fb = modes.answer('agentic', MockClient(), 'mock', VerifyTest.Q, [], self.CFG, ret)
        actions = [s['action'] for s in trace]
        self.assertIn('catalog', actions)
        self.assertIn('calculate', actions)
        self.assertFalse(fb)

    def test_classic_context_has_catalog_facts(self):
        # The mechanism, not the ranking: when the Ready file is retrieved, its catalog facts lead the context.
        ret = Retriever(DOCS, CHUNKS)
        ready = 'vsphere/technology/cpu/metrics/virtual-motherboard/ready'
        ret.search = lambda q, k=8, filters=None: [{'id': ready, 'title': DOCS[ready].title, 'score': 1.0}]
        ctx, used, _ = modes.classic_context(ret, 'What is the rollup and statistics level of VM CPU Ready?', self.CFG)
        self.assertIn(ready, used)
        self.assertTrue(ctx.startswith('Catalog facts'))

    def test_repair_turn_on_hedge(self):
        class Hedger(MockClient):
            calls = 0

            def chat(self, model, messages, tools=None, **kw):
                Hedger.calls += 1
                text = 'ANSWER: A, D\nREASON: x' if Hedger.calls == 1 else 'ANSWER: D\nREASON: x'
                return {'content': text, 'tool_calls': [], 'prompt_tokens': 1, 'completion_tokens': 1, 'latency': 0}
        ret = Retriever(DOCS, CHUNKS)
        res, used, trace, fb = modes.answer('classic', Hedger(), 'mock', VerifyTest.Q, [], self.CFG, ret)
        self.assertEqual(res['content'], 'ANSWER: D\nREASON: x')
        self.assertIn('repair', [s['action'] for s in trace])

    def test_open_answer_has_no_options_and_no_letter_repair(self):
        class Recorder(MockClient):
            systems = []

            def chat(self, model, messages, tools=None, **kw):
                Recorder.systems.append(messages[0]['content'])
                return {'content': 'Ready includes limit time, so check Max Limited.', 'tool_calls': [],
                        'prompt_tokens': 1, 'completion_tokens': 1, 'latency': 0}
        ret = Retriever(DOCS, CHUNKS)
        res, used, trace, fb = modes.answer('classic', Recorder(), 'mock', 'Why is Ready high?', [], self.CFG, ret, 'open')
        self.assertNotIn('repair', [s['action'] for s in trace])
        self.assertNotIn('ANSWER:', Recorder.systems[0])
        self.assertNotIn('Unsure option', Recorder.systems[0])
        for p in modes.PROMPTS['open'].values():
            self.assertNotIn('option', p.lower())


if __name__ == '__main__':
    unittest.main()


class PrimerTest(unittest.TestCase):
    import primer as P  # noqa: E402

    def test_all_blocks_present_and_within_budget(self):
        t = self.P.build(DOCS, {b: True for b in self.P.BLOCKS})
        for head in ('## Map of the knowledge base', '## Level 300 misreadings', '## Confusable terms',
                     '## Troubleshooting flows', '## Procedure'):
            self.assertIn(head, t)
        self.assertLessEqual(self.P.tokens(t), self.P.BUDGET_TOKENS)

    def test_off_by_default(self):
        self.assertEqual(self.P.build(DOCS, {}), '')

    def test_flow_index_lists_every_flow_file(self):
        t = self.P.flows_block(DOCS)
        for i in DOCS:
            if '/troubleshooting/' in i or '/health-check/' in i:
                self.assertIn(i, t)

    def test_agentic_adds_primer_to_system_prompt(self):
        class Recorder(MockClient):
            def chat(self, model, msgs, **kw):
                self.system = msgs[0]['content']
                return super().chat(model, msgs, **kw)
        cfg = dict(ModesTest.CFG, agent_primer={'rules': True})
        rec = Recorder()
        res, used, trace, fb = modes.answer('agentic', rec, 'mock', VerifyTest.Q, [], cfg, Retriever(DOCS, CHUNKS))
        self.assertIn('## Level 300 misreadings', rec.system)
        self.assertIn('primer', [s['action'] for s in trace])


class WindowTest(unittest.TestCase):
    def test_estimate_counts_text_and_images(self):
        msgs = [{'role': 'user', 'content': [{'type': 'text', 'text': 'x' * 400}, {'type': 'image_url'}]}]
        self.assertEqual(modes.msgs_tokens(msgs, {'image_tokens': 1500}), 100 + 1500)

    def test_agent_stops_tools_when_window_is_full(self):
        cfg = dict(ModesTest.CFG, context_window=2000, max_tokens=100)
        res, used, trace, fb = modes.answer('agentic', MockClient(), 'mock', VerifyTest.Q, [], cfg, Retriever(DOCS, CHUNKS))
        self.assertIn('context_full', [s['action'] for s in trace])


class RetrievalFixTest(unittest.TestCase):
    def test_query_expansion_adds_preferred_term(self):
        import retrieval
        terms = retrieval.glossary_terms(DOCS)
        self.assertIn('ESXi', retrieval.expand_query('Is this ESX host overloaded?', terms))

    def test_route_puts_a_troubleshooting_file_first(self):
        cfg = dict(ModesTest.CFG, route_troubleshooting=True)
        ctx, used, _ = modes.classic_context(Retriever(DOCS, CHUNKS), 'Users say the VM is slow. What do you check first?', cfg)
        self.assertIn('/troubleshooting/', used[0])

    def test_expand_derive_adds_linked_files(self):
        ret = Retriever(DOCS, CHUNKS)
        ready = 'vsphere/technology/cpu/metrics/virtual-motherboard/ready'
        ret.search = lambda q, k=8, filters=None, min_hits=3: [{'id': ready, 'title': DOCS[ready].title, 'score': 1.0}]
        derive = [l['id'] for l in ret.links(ready, 'internal_derive')][:3]
        cfg = dict(ModesTest.CFG, expand_derive=True, context_tokens=50000)
        ctx, used, _ = modes.classic_context(ret, 'Ready', cfg)
        for d in derive:
            if d in DOCS:
                self.assertIn(d, used)
