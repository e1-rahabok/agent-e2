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

    def chat(self, model, messages, tools=None, temperature=0.2, max_tokens=4000, provider_order=None):
        body = {'model': model, 'messages': messages, 'temperature': temperature, 'max_tokens': max_tokens}
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
    """Offline stand-in. Picks answers at random (seeded) and exercises the tool loop once."""

    def __init__(self, seed=0):
        self.rng = random.Random(seed)

    def chat(self, model, messages, tools=None, temperature=0.2, max_tokens=4000, provider_order=None):
        last = messages[-1]
        tool_turns = sum(1 for m in messages if m['role'] == 'tool')
        if tools and tool_turns == 0:
            q = next(m['content'] for m in messages if m['role'] == 'user')
            q = q if isinstance(q, str) else q[0]['text']
            return self._tool('search', {'query': q[:200]})
        if tools and tool_turns == 1:
            hit = re.search(r'"id": "([^"]+)"', messages[-1]['content'])
            if hit:
                return self._tool('read_file', {'id': hit.group(1)})
        text = json.dumps([m['content'] if isinstance(m['content'], str) else m['content'][0]['text'] for m in messages if m['role'] == 'user'])
        letters = sorted(set(re.findall(r'\\n([A-H])\. ', text)))
        pick = sorted(self.rng.sample(letters, k=1 if letters else 0)) or ['A']
        return {'content': f'ANSWER: {", ".join(pick)}\nREASON: mock', 'tool_calls': [],
                'prompt_tokens': 500, 'completion_tokens': 20, 'latency': 0.01,
                'served_model': model, 'provider': 'mock'}

    def _tool(self, name, args):
        return {'content': '', 'tool_calls': [{'id': f'call_{self.rng.randint(0, 10**9)}', 'type': 'function',
                                               'function': {'name': name, 'arguments': json.dumps(args)}}],
                'prompt_tokens': 400, 'completion_tokens': 30, 'latency': 0.01, 'served_model': 'mock', 'provider': 'mock'}

    def embed(self, model, inputs):
        raise LLMError('mock client has no embeddings')
