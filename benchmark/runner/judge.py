"""Judge: scores free-text and compound answers 0-3 against the question's answer key.

The judge is a frontier model that is never a candidate. It sees the question (and its images),
`## Expected key points`, `## Likely wrong answer` and the answer under test. The model under test never
sees the key. Rubric and reasons: benchmark/design.md, section 14.
"""
import json
import random
import re

from llm import LLMError

RUBRIC = """Score the answer on this scale:
0 = wrong, or falls into the likely wrong answer, or contradicts a key point.
1 = avoids the likely wrong answer, but the reason is missing or wrong.
2 = correct conclusion, with the right reason (the mechanism or vantage point in the key points).
3 = as 2, and it also states what to check next, or covers every key point.

Rules:
- Judge facts, not style or length. Extra correct detail neither adds nor costs points.
- A statement that contradicts a key point caps the score at 0, even when other parts are right.
- An answer that says the question cannot be settled from the information available scores 0 and is marked unsure.
- The key points are the truth for this question, even where general IT practice says otherwise.
- Use only the key points and the question. Do not reward knowledge the key points do not contain."""

SYSTEM = ('You grade answers to VMware vSphere and VCF operations questions against an expert answer key.\n'
          + RUBRIC + '\n'
          'Reply with one JSON object and nothing else:\n'
          '{"score": 0-3, "trap": true|false, "unsure": true|false, "missed": "<key point missed, or empty>", '
          '"reason": "<one sentence>"}\n'
          'trap = the answer states the likely wrong answer.')


def _user(question, answer, images):
    text = (f'Question:\n{question.prompt}\n\nExpected key points (the answer key):\n{question.key_points}\n\n'
            f'Likely wrong answer:\n{question.likely_wrong or "(none given)"}\n\nAnswer to grade:\n{answer or "(empty)"}')
    if not images:
        return {'role': 'user', 'content': text}
    return {'role': 'user', 'content': [{'type': 'text', 'text': text}] + images}


def parse(text):
    """Return the judge's verdict dict, or None when it cannot be read."""
    m = re.search(r'\{.*\}', text or '', re.S)
    if not m:
        return None
    try:
        v = json.loads(m.group(0))
        score = int(v['score'])
    except (ValueError, KeyError, TypeError):
        return None
    if score not in (0, 1, 2, 3):
        return None
    return {'score': score, 'trap': bool(v.get('trap')), 'unsure': bool(v.get('unsure')),
            'missed': str(v.get('missed') or '')[:200], 'reason': str(v.get('reason') or '')[:300]}


class Judge:
    def __init__(self, client, model, cfg):
        self.client, self.model = client, model
        self.temperature = cfg.get('judge_temperature', 0)
        self.max_tokens = cfg.get('judge_max_tokens', 1500)
        self.provider_order = cfg.get('provider_order', {}).get(model)

    def grade(self, question, answer, images=None):
        """Returns (verdict, result). One retry when the reply is not valid JSON; then LLMError."""
        msgs = [{'role': 'system', 'content': SYSTEM}, _user(question, answer, images or [])]
        for _ in range(2):
            res = self.client.chat(self.model, msgs, temperature=self.temperature, max_tokens=self.max_tokens,
                                   provider_order=self.provider_order)
            v = parse(res['content'])
            if v:
                return v, res
            msgs = msgs + [{'role': 'assistant', 'content': res['content'] or ''},
                           {'role': 'user', 'content': 'Reply with the JSON object only.'}]
        raise LLMError(f'judge reply not parseable: {(res["content"] or "")[:200]}')


class MockJudge:
    """Offline stand-in: random scores, seeded. Proves the pipeline only."""
    model = 'mock-judge'

    def __init__(self, seed=0):
        self.rng = random.Random(seed)

    def grade(self, question, answer, images=None):
        s = self.rng.randint(0, 3)
        return ({'score': s, 'trap': s == 0, 'unsure': False, 'missed': '', 'reason': 'mock'},
                {'prompt_tokens': 0, 'completion_tokens': 0, 'latency': 0})
