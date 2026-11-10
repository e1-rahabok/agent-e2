# Repository map

Where each thing lives. For people; not indexed. How the parts work together: [ARCHITECTURE.md](ARCHITECTURE.md), section Repository.

## Root
| File | For |
|---|---|
| [README.md](README.md) | What Agent E2 is, in one page |
| [MISSION.md](MISSION.md) | Why a small local model can win; requirements; risks |
| [ARCHITECTURE.md](ARCHITECTURE.md) | The whole system: repository, parts, modes, query flow |
| [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md) | How knowledge is written, placed and tagged |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add or change a file |
| [CLAUDE.md](CLAUDE.md) | How Claude works in this repository |
| [SECURITY.md](SECURITY.md) | Security policy |

## Product: deployed to the site
| Folder | Holds |
|---|---|
| `knowledge/` | What Agent E2 reads. The only indexed folder |
| `knowledge/catalog/` | Exact data in YAML: vCenter counters, esxtop fields, thresholds, object model |
| `knowledge/observability/` | How to read any metric: input types, collection interval, aggregation, units, thresholds |
| `knowledge/sp5-framework/` | Operations management across products (the SP5 Framework). `concepts/`: the framework across pillars (overview, Triple See Method, SLAs, health). `alerts/`: alert architecture. `performance/`, `capacity/`: one pillar each |
| `knowledge/vsphere/` | `architecture/` (provider/consumer, VM vs Guest OS, overhead, resource controls), `technology/<cpu, memory, storage, network, gpu>/` (metrics, including those VCF Operations computes), `object-types/<vm, esxi, cluster>/` (KPIs, models, health checks), `tools/<esxtop, vsphere-client, vcf-operations>/` |
| `knowledge/vcf-operations/` | VCF Operations itself: `concepts/` (role, channels), `features/`, `dashboards/`, `reports/`, `alerts/` (alert definitions). Metrics it computes about vSphere objects live with those objects |
| `knowledge/guest-os/` | Windows and Linux, a separate layer |
| `knowledge/glossary.md` | The agent's vocabulary |
| `knowledge/moved.yaml` | Old file ids → current ids |
| `harness/` | Retrieval, catalog, calculator, flow executor, agent loop, verifier. [README](harness/README.md), [AGENT.md](harness/AGENT.md) |

## Flows
Order of checks, run step by step by the `flow` tool. Each sits next to its technology or object, in a folder named `troubleshooting/` or `health-check/`; the harness finds them by that folder name and gives the agent one index of all flows. Start a performance complaint at the VM slow flow. Lint checks that this table lists every flow.

| Kind | Flow | File |
|---|---|---|
| Health check | Can this cluster take more VMs? | [`sp5-framework/capacity/health-check/can-cluster-take-more-vms`](knowledge/sp5-framework/capacity/health-check/can-cluster-take-more-vms.md) |
| Health check | Does this ESXi host have CPU headroom? | [`vsphere/technology/cpu/health-check/host-cpu-capacity-headroom`](knowledge/vsphere/technology/cpu/health-check/host-cpu-capacity-headroom.md) |
| Health check | Downsizing a large, idle VM | [`vsphere/technology/cpu/health-check/oversized-vm-downsizing`](knowledge/vsphere/technology/cpu/health-check/oversized-vm-downsizing.md) |
| Health check | ESXi: health check | [`vsphere/object-types/esxi/health-check/esxi-health-check`](knowledge/vsphere/object-types/esxi/health-check/esxi-health-check.md) |
| Health check | VM: health check | [`vsphere/object-types/vm/health-check/vm-health-check`](knowledge/vsphere/object-types/vm/health-check/vm-health-check.md) |
| Health check | vSphere cluster: health check | [`vsphere/object-types/cluster/health-check/cluster-health-check`](knowledge/vsphere/object-types/cluster/health-check/cluster-health-check.md) |
| Troubleshooting | ESXi storage latency is high | [`vsphere/technology/storage/troubleshooting/host-storage-latency`](knowledge/vsphere/technology/storage/troubleshooting/host-storage-latency.md) |
| Troubleshooting | Overcommit indicators | [`vsphere/technology/memory/troubleshooting/overcommit-indicators`](knowledge/vsphere/technology/memory/troubleshooting/overcommit-indicators.md) |
| Troubleshooting | Users say the VM is slow | [`sp5-framework/performance/troubleshooting/vm-slow`](knowledge/sp5-framework/performance/troubleshooting/vm-slow.md) |
| Troubleshooting | VM CPU Contention or Latency is high | [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](knowledge/vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high.md) |
| Troubleshooting | VM CPU Other Wait is high | [`vsphere/technology/cpu/troubleshooting/vm-other-wait-high`](knowledge/vsphere/technology/cpu/troubleshooting/vm-other-wait-high.md) |
| Troubleshooting | VM CPU Run and Used differ | [`vsphere/technology/cpu/troubleshooting/run-vs-used-gap`](knowledge/vsphere/technology/cpu/troubleshooting/run-vs-used-gap.md) |
| Troubleshooting | VM memory latency (contention) is high | [`vsphere/technology/memory/troubleshooting/vm-memory-latency-high`](knowledge/vsphere/technology/memory/troubleshooting/vm-memory-latency-high.md) |
| Troubleshooting | VM starved of resources in a DRS cluster | [`vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster`](knowledge/vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster.md) |
| Troubleshooting | VM storage performance: what to check | [`vsphere/technology/storage/troubleshooting/vm-storage-performance-checks`](knowledge/vsphere/technology/storage/troubleshooting/vm-storage-performance-checks.md) |
| Troubleshooting | VMs in a cluster face contention | [`vsphere/object-types/cluster/troubleshooting/cluster-vm-contention`](knowledge/vsphere/object-types/cluster/troubleshooting/cluster-vm-contention.md) |
| Troubleshooting | vNIC receive drops | [`vsphere/technology/network/troubleshooting/vnic-rx-drops`](knowledge/vsphere/technology/network/troubleshooting/vnic-rx-drops.md) |

## Proof: not deployed
| Folder | Holds |
|---|---|
| `benchmark/questions/` | Questions with answer keys. Never indexed |
| `benchmark/runner/` | Runner, judge, retrieval check (`retrieval_eval.py`), config |
| `benchmark/results/` | Run results, `results.csv` |
| `benchmark/*.md` | [design](benchmark/design.md), [models](benchmark/models.md), [live test](benchmark/live-test.md), [retrieval check](benchmark/retrieval-check.md) |

## Project: not deployed
| Folder | Holds |
|---|---|
| `project/plan.md` | Milestones, decisions, open work. Read first |
| `project/author-questions.md` | Questions for the author |
| `project/explainers/` | Worked examples for people (SLA vs KPI). Not for Agent E2; not indexed |
| `project/design-thresholds.md` | Threshold catalog design: use cases, files, fields. Proposal |
| `project/vocabulary.md`, `project/terms.md` | Writing vocabulary; repository terms |
| `project/sources/` | Source documents. Read-only |
| `project/templates/` | Templates for knowledge files |
| `project/tools/` | `lint.py`, `tags.yaml`, `threshold_inventory.py`, `answered.py`, `link_refs.py` |
| `project/archive/` | Retired documents |
