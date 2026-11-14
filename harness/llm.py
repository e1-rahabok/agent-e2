"""OpenAI-compatible client for Vercel AI Gateway, plus a mock for offline runs."""
import json
import os
import random
import re
import time

import requests

GATEWAY = 'https://ai-gateway.vercel.sh/v1'


class LLMError(Exception):
    pass


class GatewayClient:
    def __init__(self, base_url=GATEWAY, api_key=None, timeout=180, max_retries=5):
        self.base = base_url.rstrip('/')
        self.key = api_key or os.environ.get('AI_GATEWAY_API_KEY') or os.environ.get('VERCEL_OIDC_TOKEN')
        self.timeout, self.max_retries = timeout, max_retries

    def _post(self, path, body):
        if not self.key:
            raise LLMError('AI_GATEWAY_API_KEY is not set')
        delay = 2.0
        for attempt in range(self.max_retries + 1):
            t0 = time.time()
            try:
                r = requests.post(self.base + path, json=body, timeout=self.timeout,
                                  headers={'Authorization': f'Bearer {self.key}'})
            except requests.RequestException as e:
                err = str(e)
            else:
                if r.status_code == 200:
                    return r.json(), r.headers, time.time() - t0
                err = f'HTTP {r.status_code}: {r.text[:300]}'
                if r.status_code not in (408, 429, 500, 502, 503, 504):
                    raise LLMError(err)
            if attempt == self.max_retries:
                raise LLMError(err)
            time.sleep(delay + random.random())
            delay *= 2

    def chat(self, model, messages, tools=None, temperature=0.2, max_tokens=4000, provider_order=None, reasoning=None,
             top_p=None, top_k=None, deterministic=False):
        if deterministic:   # a reading step (agent.py, stage 1): the same input reads the same way every time
            temperature, top_p, top_k = 0, None, None
        body = {'model': model, 'messages': messages, 'max_tokens': max_tokens}
        for k, v in (('temperature', temperature), ('top_p', top_p), ('top_k', top_k)):
            if v is not None:   # None: the provider's default
                body[k] = v
        if reasoning:
            body['reasoning'] = reasoning       # gateway field, e.g. {'effort': 'none'} or {'enabled': False}; per model: models.md, section 5
        if tools:
            body['tools'] = tools
            body['tool_choice'] = 'auto'
        if provider_order:
            body['providerOptions'] = {'gateway': {'order': provider_order}}
        data, headers, latency = self._post('/chat/completions', body)
        msg = data['choices'][0]['message']
        usage = data.get('usage') or {}
        return {
            'content': msg.get('content') or '',
            'finish_reason': data['choices'][0].get('finish_reason') or '',     # 'length': the answer was cut at max_tokens
            'tool_calls': msg.get('tool_calls') or [],
            'prompt_tokens': usage.get('prompt_tokens', 0),
            'completion_tokens': usage.get('completion_tokens', 0),
            'latency': round(latency, 2),
            'served_model': data.get('model', model),
            'provider': _provider(data, headers),
        }

    def embed(self, model, inputs):
        data, _, _ = self._post('/embeddings', {'model': model, 'input': inputs})
        return [d['embedding'] for d in sorted(data['data'], key=lambda d: d['index'])]

    def models(self):
        r = requests.get(self.base + '/models', timeout=60)
        r.raise_for_status()
        return {m['id']: m for m in r.json()['data']}

    def credits(self):
        """Account credit balance in US$ (the key's own budget is a separate limit and is not readable)."""
        if not self.key:
            raise LLMError('AI_GATEWAY_API_KEY is not set')
        r = requests.get(self.base + '/credits', timeout=60, headers={'Authorization': f'Bearer {self.key}'})
        if r.status_code != 200:
            raise LLMError(f'HTTP {r.status_code}: {r.text[:200]}')
        return float(r.json()['balance'])


class ParamClient:
    """Adds per-model request settings to every chat call: `reasoning` (the gateway's reasoning field), `max_tokens`,
    and the sampling settings of the model's own card (`temperature`, `top_p`, `top_k`: what a local server applies by default).

    One wrapper instead of a parameter threaded through every mode: the same settings reach Agent E2, baseline, web and the
    answer repair. A model without an entry passes through unchanged (the judge, an embedding call). A call marked
    deterministic (the agent's reading of the question) keeps temperature 0 instead of the card's sampling.
    """

    def __init__(self, inner, params, sampling=None):
        self.inner, self.params, self.sampling = inner, params or {}, sampling or {}

    def chat(self, model, messages, **kw):
        if model in self.sampling and not kw.get('deterministic'):
            kw.update({k: self.sampling[model].get(k) for k in ('temperature', 'top_p', 'top_k')})
        p = self.params.get(model) or {}
        if 'max_tokens' in p:
            kw['max_tokens'] = p['max_tokens']
        if p.get('reasoning'):
            kw['reasoning'] = p['reasoning']
        return self.inner.chat(model, messages, **kw)

    def __getattr__(self, name):
        return getattr(self.inner, name)


def _provider(data, headers):
    """Record whichever provider hint the gateway returns; the field name is not fixed."""
    for k in ('provider', 'x-vercel-ai-provider', 'x-provider'):
        if isinstance(data.get(k), str):
            return data[k]
        if headers.get(k):
            return headers[k]
    meta = data.get('providerMetadata') or data.get('provider_metadata') or {}
    gw = meta.get('gateway') if isinstance(meta, dict) else None
    if isinstance(gw, dict):
        routing = gw.get('routing') or {}
        return routing.get('finalProvider') or routing.get('resolvedProvider') or json.dumps(gw)[:80]
    return ''


class MockClient:
    """Offline stand-in. Picks answers at random (seeded); reads a question into a minimal case; serves the web
    reference's tool calls (web_search, then an answer)."""

    def __init__(self, seed=0):
        self.rng = random.Random(seed)

    def chat(self, model, messages, tools=None, temperature=0.2, max_tokens=4000, provider_order=None, reasoning=None, top_p=None, top_k=None,
             deterministic=False):
        tool_turns = sum(1 for m in messages if m['role'] == 'tool')
        if deterministic:   # the agent's reading of the question (agent.py, stage 1)
            return {'content': json.dumps({'kind': 'metric-meaning', 'objects': ['VM'], 'claims': [],
                                           'metrics': [{'name': 'CPU Ready', 'object': 'VM', 'value': None, 'unit': None}]}),
                    'tool_calls': [], 'finish_reason': 'stop', 'prompt_tokens': 300, 'completion_tokens': 60, 'latency': 0.01,
                    'served_model': model, 'provider': 'mock'}
        if tools and tool_turns == 0:
            q = next(m['content'] for m in messages if m['role'] == 'user')
            q = q if isinstance(q, str) else q[0]['text']
            return self._tool(tools[0]['function']['name'], {'query': q[:200]})
        text = json.dumps([m['content'] if isinstance(m['content'], str) else m['content'][0]['text'] for m in messages if m['role'] == 'user'])
        letters = sorted(set(re.findall(r'\\n([A-H])\. ', text)))
        pick = sorted(self.rng.sample(letters, k=1 if letters else 0)) or ['A']
        return {'content': f'ANSWER: {", ".join(pick)}\nREASON: mock', 'tool_calls': [], 'finish_reason': 'stop',
                'prompt_tokens': 500, 'completion_tokens': 20, 'latency': 0.01,
                'served_model': model, 'provider': 'mock'}

    def _tool(self, name, args):
        return {'content': '', 'finish_reason': 'tool_calls', 'tool_calls': [{'id': f'call_{self.rng.randint(0, 10**9)}', 'type': 'function',
                                               'function': {'name': name, 'arguments': json.dumps(args)}}],
                'prompt_tokens': 400, 'completion_tokens': 30, 'latency': 0.01, 'served_model': 'mock', 'provider': 'mock'}

    def embed(self, model, inputs):
        raise LLMError('mock client has no embeddings')
