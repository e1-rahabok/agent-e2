"""Planning calculator: how many VMs fit on an ESXi host or a cluster, before any workload runs.

The model only gathers the inputs and explains the result; the arithmetic is here. Method:
knowledge/sp5-framework/capacity/class-of-service-planning.md, section Planning calculator.

Per ESXi host, three models (allocation, reservation, utilization) for each of CPU and memory: six numbers.
The host is full at the first of the six to reach 100%. Mixed classes are compared in the allocation model by
dividing each class's demand by its overcommit ratio. HA hosts are added on top: capacity counts the hosts that
carry load (hosts - ha_hosts).

Class defaults (overcommit, reservation, expected concurrent peak, typical VM size) are rows of
knowledge/catalog/thresholds-capacity.yaml, section rules, ids starting with "planning-". One place per number.
"""
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = ('gold', 'silver', 'bronze')
CLASS_PARAMS = ('cpu-overcommit', 'memory-overcommit', 'cpu-reservation', 'memory-reservation',
                'cpu-concurrent-peak', 'memory-concurrent-peak', 'vcpu')
HOST_PARAMS = ('gb-per-vcpu', 'hypervisor-threads', 'hypervisor-memory-gb', 'system-reservation-ghz')
MODELS = ('allocation', 'reservation', 'utilization')


def defaults(root=ROOT):
    """Planning defaults from the threshold catalog: {'gold': {...}, 'silver': {...}, 'bronze': {...}, 'host': {...}}."""
    rows = yaml.safe_load(open(os.path.join(root, 'knowledge', 'catalog', 'thresholds-capacity.yaml')))['rules']
    vals = {r['id'][len('planning-'):]: r['value'] for r in rows if r['id'].startswith('planning-')}
    out = {c: {p: vals[f'{c}-{p}'] for p in CLASS_PARAMS} for c in CLASSES}
    out['host'] = {p: vals[p] for p in HOST_PARAMS}
    return out


def _classes(overrides, d):
    cls = {c: dict(d[c]) for c in CLASSES}
    for c, v in (overrides or {}).items():
        if c not in cls:
            raise ValueError(f'unknown class {c}: use gold, silver, bronze')
        cls[c].update({k.replace('_', '-'): x for k, x in v.items()})
    for c in cls.values():
        c.setdefault('memory-gb', c['vcpu'] * d['host']['gb-per-vcpu'])  # follows an overridden vCPU count
    return cls


def supply(cores, ghz, ram_gb, ht=True, hypervisor_threads=None, hypervisor_memory_gb=None,
           system_reservation_ghz=None, memory_tiering_gb=0, root=ROOT):
    """Usable capacity of one ESXi host per model. CPU in threads (allocation, utilization) or GHz (reservation)."""
    h = defaults(root)['host']
    hv_t = h['hypervisor-threads'] if hypervisor_threads is None else hypervisor_threads
    hv_m = h['hypervisor-memory-gb'] if hypervisor_memory_gb is None else hypervisor_memory_gb
    sys_r = h['system-reservation-ghz'] if system_reservation_ghz is None else system_reservation_ghz
    threads = cores * (2 if ht else 1)
    dram = ram_gb - hv_m
    return {'threads': threads, 'cpu_threads': threads - hv_t,
            'cpu_reservable_ghz': cores * ghz - sys_r,  # reservation is capped at the base clock, per core
            'memory_dram_gb': dram, 'memory_tiering_gb': memory_tiering_gb,
            'memory_gb': dram + memory_tiering_gb, 'ghz': ghz,
            'note': 'Usable = total - hypervisor overhead. HA is not subtracted per host: HA hosts are added to the cluster.'}


def vms_per_host(vm_class, cores, ghz, ram_gb, ht=True, classes=None, **host):
    """How many VMs of one class fit on one host: the six numbers, the smallest, and the model and resource that bind."""
    root = host.pop('root', ROOT)
    d = defaults(root)
    cls = _classes(classes, d)[vm_class]
    s = supply(cores, ghz, ram_gb, ht, root=root, **host)
    vcpu, mem = cls['vcpu'], cls['memory-gb']
    six = {
        ('allocation', 'cpu'): cls['cpu-overcommit'] * s['cpu_threads'] / vcpu,
        ('allocation', 'memory'): (s['memory_dram_gb'] * cls['memory-overcommit'] + s['memory_tiering_gb']) / mem,
        ('reservation', 'cpu'): s['cpu_reservable_ghz'] / (vcpu * cls['cpu-reservation'] * ghz),
        ('reservation', 'memory'): s['memory_gb'] / (mem * cls['memory-reservation']),
        ('utilization', 'cpu'): s['cpu_threads'] / (vcpu * cls['cpu-concurrent-peak']),
        ('utilization', 'memory'): s['memory_gb'] / (mem * cls['memory-concurrent-peak']),
    }
    (model, res), n = min(six.items(), key=lambda kv: kv[1])
    return {'class': vm_class, 'vm': {'vcpu': vcpu, 'memory_gb': mem}, 'supply': s,
            'vms': {f'{m} {r}': round(v, 2) for (m, r), v in six.items()},
            'fit': int(n), 'exact': round(n, 2), 'binding': f'{model} {res}'}


def consumption(vms, cores, ghz, ram_gb, ht=True, hosts=1, ha_hosts=0, classes=None, **host):
    """Planned consumption of a host or cluster for a VM mix {'gold': n, 'silver': n, 'bronze': n}: six percentages.

    Aim for about 90-110% of the binding number at planning: the plan is an estimate, reality will vary.
    """
    root = host.pop('root', ROOT)
    d = defaults(root)
    cls = _classes(classes, d)
    for c in vms:
        if c not in cls:
            raise ValueError(f'unknown class {c}: use gold, silver, bronze')
    carrying = hosts - ha_hosts
    if carrying < 1:
        raise ValueError('hosts - ha_hosts must be at least 1')
    s = supply(cores, ghz, ram_gb, ht, root=root, **host)
    b = cls['bronze']
    n = {c: vms.get(c, 0) for c in CLASSES}
    tot = lambda f: sum(n[c] * f(cls[c]) for c in CLASSES)  # noqa: E731
    pct = {
        ('allocation', 'cpu'): tot(lambda k: k['vcpu'] * b['cpu-overcommit'] / k['cpu-overcommit'])
        / (b['cpu-overcommit'] * s['cpu_threads'] * carrying),
        ('allocation', 'memory'): tot(lambda k: k['memory-gb'] * b['memory-overcommit'] / k['memory-overcommit'])
        / ((s['memory_dram_gb'] * b['memory-overcommit'] + s['memory_tiering_gb']) * carrying),
        ('reservation', 'cpu'): tot(lambda k: k['vcpu'] * k['cpu-reservation'] * ghz) / (s['cpu_reservable_ghz'] * carrying),
        ('reservation', 'memory'): tot(lambda k: k['memory-gb'] * k['memory-reservation']) / (s['memory_gb'] * carrying),
        ('utilization', 'cpu'): tot(lambda k: k['vcpu'] * k['cpu-concurrent-peak']) / (s['cpu_threads'] * carrying),
        ('utilization', 'memory'): tot(lambda k: k['memory-gb'] * k['memory-concurrent-peak']) / (s['memory_gb'] * carrying),
    }
    (model, res), top = max(pct.items(), key=lambda kv: kv[1])
    verdict = 'over' if top > 1.10 else 'fits' if top >= 0.90 else 'room left'
    return {'vms': n, 'hosts': hosts, 'ha_hosts': ha_hosts, 'supply_per_host': s,
            'consumption_pct': {f'{m} {r}': round(v * 100, 1) for (m, r), v in pct.items()},
            'binding': f'{model} {res}', 'binding_pct': round(top * 100, 1), 'verdict': verdict,
            'note': 'Planning only: contention cannot be modelled; in a running cluster read Cluster Performance (%).'}


def plan(args):
    """Tool entry point. args: cores, ghz, ram_gb, optional ht, hosts, ha_hosts, hypervisor_threads,
    hypervisor_memory_gb, system_reservation_ghz, memory_tiering_gb, classes (overrides per class);
    then either vm_class (how many fit per host) or vms (a mix {'gold': n, 'silver': n, 'bronze': n})."""
    a = dict(args)
    try:
        base = {k: a.pop(k) for k in ('cores', 'ghz', 'ram_gb')}
    except KeyError as e:
        return {'error': f'missing {e.args[0]}: give the host cores, base GHz and RAM in GB'}
    extra = {k: a.pop(k) for k in ('ht', 'classes', 'hypervisor_threads', 'hypervisor_memory_gb',
                                    'system_reservation_ghz', 'memory_tiering_gb') if k in a}
    try:
        if 'vm_class' in a:
            return vms_per_host(a['vm_class'], **base, **extra)
        if 'vms' in a:
            return consumption(a['vms'], **base, hosts=a.get('hosts', 1), ha_hosts=a.get('ha_hosts', 0), **extra)
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as e:
        return {'error': str(e)}
    return {'error': 'give vm_class (how many fit per host) or vms (a mix per class)'}
