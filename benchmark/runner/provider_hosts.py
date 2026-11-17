"""The provider hosts of a model, and which host each of the five runs prefers.

Why (2026-11-16): the gateway sent every Gemma call to one host (Novita AI, 20 to 27 tokens a second, the slowest of the healthy hosts;
FriendliAI gave 100) and the call time rose from 36 s to 175 s. Hosts differ in speed, in load and in uptime (GMICloud was down for 24
hours). Real deployments differ in host, quantization and sampling too, so the five runs of a question go to different hosts: the score
is pooled over them, and the host of every answer is recorded (answers.csv, column provider).

How:
  - discover_hosts: one tiny call; the gateway names the host that answered and the other hosts it could use
    (message.provider_metadata.gateway.routing: finalProvider, fallbacksAvailable);
  - healthy_hosts: one tiny call pinned to each host (providerOptions.gateway.only); a host that fails is left out of the round;
  - order_for_run: run r prefers host (r - 1) mod n and falls back to the others in a fixed order (providerOptions.gateway.order).
"""
import json


def routing_of(reply_data):
    """The gateway's routing record of a reply, or {}."""
    msg = ((reply_data.get('choices') or [{}])[0].get('message')) or {}
    meta = reply_data.get('providerMetadata') or reply_data.get('provider_metadata') or msg.get('provider_metadata') or {}
    gw = meta.get('gateway') if isinstance(meta, dict) else None
    return (gw or {}).get('routing') or {} if isinstance(gw, dict) else {}


def hosts_in(routing):
    """The host that answered first, then the others the gateway lists, without duplicates."""
    out = []
    for h in [routing.get('finalProvider') or routing.get('resolvedProvider')] + list(routing.get('fallbacksAvailable') or []):
        if h and h not in out:
            out.append(h)
    return out


def order_for_run(hosts, run):
    """Run 1 prefers hosts[0], run 2 hosts[1], ... the others follow in their order. [] when there is nothing to spread over."""
    if len(hosts) < 2:
        return []
    k = (int(run) - 1) % len(hosts)
    return [hosts[k]] + [h for i, h in enumerate(hosts) if i != k]


def _tiny(client, model, params, order=None, only=None):
    """One tiny chat call; the raw reply data (the client returns the parsed message, so the raw post is used)."""
    body = {'model': model, 'messages': [{'role': 'user', 'content': 'Reply OK.'}], 'max_tokens': 20}
    body.update({k: v for k, v in (params or {}).items() if k in ('reasoning',)})
    opts = {}
    if order:
        opts['order'] = order
    if only:
        opts['only'] = only
    if opts:
        body['providerOptions'] = {'gateway': opts}
    data, _, latency = client._post('/chat/completions', body)
    return data, latency


def discover_hosts(client, model, params=None):
    """[] when the gateway names no host (a model with one host, or a reply without routing)."""
    data, _ = _tiny(client, model, params)
    return hosts_in(routing_of(data))


def healthy_hosts(client, model, hosts, params=None, log=print):
    """The hosts that answer a tiny call pinned to them, in the given order."""
    good = []
    for h in hosts:
        try:
            _tiny(client, model, params, only=[h])
            good.append(h)
        except Exception as e:      # noqa: BLE001  any failure leaves the host out of the round
            log(f'{model}: host {h} left out ({str(e)[:120]})')
    return good


def choose_hosts(client, model, params=None, log=print, wanted=None):
    """The hosts to spread the runs of a model over: the discovered hosts that answer. [] means: do not spread."""
    hosts = list(wanted) if wanted else discover_hosts(client, model, params)
    if len(hosts) < 2:
        return []
    good = healthy_hosts(client, model, hosts, params, log)
    return good if len(good) >= 2 else []


def describe(hosts_by_model):
    return json.dumps(hosts_by_model, sort_keys=True)
