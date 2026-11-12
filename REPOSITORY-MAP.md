# Repository map

Where each thing lives. For people; not indexed. How the parts work together: [ARCHITECTURE.md](ARCHITECTURE.md), section Repository.

## Root
| File | For |
|---|---|
| [README.md](README.md) | What Agent E2 is, in one page |
| [MISSION.md](MISSION.md) | Why a small local model can win; requirements; risks |
| [ARCHITECTURE.md](ARCHITECTURE.md) | The whole system: repository, parts, modes, query flow |
| [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md) | The knowledge design: where knowledge lives, forms, Level 400 and misconceptions. Rules: `project/knowledge-rules/` |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add or change a file |
| [CLAUDE.md](CLAUDE.md) | How Claude works in this repository |
| [SECURITY.md](SECURITY.md) | Security policy |

## Product: deployed to the site
| Folder | Holds |
|---|---|
| `knowledge/` | What Agent E2 reads. The only indexed folder. Placement rules: [project/knowledge-rules/placement.md](project/knowledge-rules/placement.md) |
| `knowledge/catalog/` | Exact data in YAML, read by code: vCenter counters, esxtop fields, object model, thresholds (performance KPI, capacity models and decisions, alerts), user terms |
| `knowledge/sp5-framework/` | The method: how to operate VCF, the SP5 Framework (source: Private Cloud Management by Iwan Rahabok). `concepts/`: across pillars (overview, health check, health-risk-efficiency, class of service, modelling). `observability/`: how to read telemetry. `outputs/`: alerts, dashboards, reports, NOC live screen. `performance/`, `capacity/`: one pillar each |
| `knowledge/vsphere/architecture/` | vSphere design every metric follows from: provider and consumer, VM vs Guest OS realms, overhead, resource controls |
| `knowledge/vsphere/technology/` | One technology at a time (`cpu`, `memory`, `storage`, `network`, `gpu`): how it works, metrics per object, what to set, troubleshooting and decision trees within that technology |
| `knowledge/vsphere/object-types/` | One folder per object type (`vm`, `esxi`, `cluster`, `resource-pool`, `datastore`, `datastore-cluster`, `distributed-switch`, `distributed-port-group`): what combines technologies, KPIs, models, the object's alerts (`<object>-alerts`), its health check (`<object>-health-check`), troubleshooting and decision trees on that object |
| `knowledge/vsphere/tools/` | How esxtop and the vSphere Client show the counters |
| `knowledge/vcf-operations/` | The product VCF Operations: its role, `features/`, `dashboards/` and the report suite as built in it, and how an alert definition works (`alert-definitions`). How to design them is method (`sp5-framework/outputs/`); metrics it computes about vSphere objects live with those objects |
| `knowledge/guest-os/` | Windows and Linux: a separate realm from the VM; the hypervisor neither sees nor controls it. The Guest OS alerts: `guest-os-alerts` |
| `knowledge/glossary.md` | The agent's vocabulary |
| `knowledge/misconceptions.md` | Level 300 wrong beliefs and their corrections, given to the agent up front; not indexed. Where knowledge lives: [KNOWLEDGE-ENGINEERING.md](KNOWLEDGE-ENGINEERING.md), section 2 |
| `harness/` | Retrieval, catalog, calculator, planning calculator, flow executor, agent loop, verifier. [README](harness/README.md), [AGENT.md](harness/AGENT.md) |

## Flows
A flow is an expert's order of checks, run step by step by the `flow` tool. Three kinds, named by `retriever_guide` (health-check, troubleshooting, decision-tree); the harness finds them by that metadata, wherever the file sits, and gives the agent one index, grouped by kind. What each kind is: [Health check](knowledge/sp5-framework/concepts/health-check.md). Lint checks that these tables list every flow.

### Health checks: is this object healthy?
Started by a schedule or a request, never by a problem. Always on one object type, never on a technology or a pillar; every pillar in order: availability, performance, security, capacity. The parent includes its children, except across a realm (the Guest OS is not part of the VM or host check). A failed step opens a troubleshooting flow.

| Object | File |
|---|---|
| VM | [`vsphere/object-types/vm/vm-health-check`](knowledge/vsphere/object-types/vm/vm-health-check.md) |
| ESXi host | [`vsphere/object-types/esxi/esxi-health-check`](knowledge/vsphere/object-types/esxi/esxi-health-check.md) |
| vSphere cluster | [`vsphere/object-types/cluster/cluster-health-check`](knowledge/vsphere/object-types/cluster/cluster-health-check.md) |

### Troubleshooting: why is it down or slow?
Started by a known problem: a complaint, an alert, or a failed health check step. Start a performance complaint at the VM slow flow.

| Symptom | File |
|---|---|
| Users say the VM is slow | [`sp5-framework/performance/vm-slow`](knowledge/sp5-framework/performance/vm-slow.md) |
| Windows is slow (step 1 of VM slow) | [`guest-os/system/troubleshooting/ms-windows-slow`](knowledge/guest-os/system/troubleshooting/ms-windows-slow.md) |
| Linux is slow (step 1 of VM slow) | [`guest-os/system/troubleshooting/linux-os-slow`](knowledge/guest-os/system/troubleshooting/linux-os-slow.md) |
| VM CPU Contention or Latency is high | [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](knowledge/vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high.md) |
| VM CPU Other Wait is high | [`vsphere/technology/cpu/troubleshooting/vm-other-wait-high`](knowledge/vsphere/technology/cpu/troubleshooting/vm-other-wait-high.md) |
| VM CPU Run and Used differ | [`vsphere/technology/cpu/troubleshooting/run-vs-used-gap`](knowledge/vsphere/technology/cpu/troubleshooting/run-vs-used-gap.md) |
| VM memory latency (contention) is high | [`vsphere/technology/memory/vm-memory-latency-high`](knowledge/vsphere/technology/memory/vm-memory-latency-high.md) |
| VM storage performance: what to check | [`vsphere/technology/storage/troubleshooting/vm-storage-performance-checks`](knowledge/vsphere/technology/storage/troubleshooting/vm-storage-performance-checks.md) |
| ESXi storage latency is high | [`vsphere/technology/storage/troubleshooting/host-storage-latency`](knowledge/vsphere/technology/storage/troubleshooting/host-storage-latency.md) |
| vNIC receive drops | [`vsphere/technology/network/vnic-rx-drops`](knowledge/vsphere/technology/network/vnic-rx-drops.md) |
| VMs in a cluster face contention | [`vsphere/object-types/cluster/troubleshooting/cluster-vm-contention`](knowledge/vsphere/object-types/cluster/troubleshooting/cluster-vm-contention.md) |
| VM starved of resources in a DRS cluster | [`vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster`](knowledge/vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster.md) |

### Decision trees: can it, should it, how much?
Started by one operational question; ends in a choice to act, with its reason. Not a health check, even when a health check step reads its result.

| Question | File |
|---|---|
| Can this cluster take more VMs? | [`vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms`](knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md) |
| Does this ESXi host have CPU headroom? | [`vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom`](knowledge/vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom.md) |
| Should this large, idle VM be downsized? | [`vsphere/technology/cpu/decision-tree/oversized-vm-downsizing`](knowledge/vsphere/technology/cpu/decision-tree/oversized-vm-downsizing.md) |
| Is memory overcommit affecting this VM? | [`vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm`](knowledge/vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm.md) |

## Proof: not deployed
| Folder | Holds |
|---|---|
| `benchmark/questions/` | Questions with answer keys. Never indexed. Template: `benchmark/_templates/question.md` |
| `benchmark/runner/` | Runner, judge, retrieval check (`retrieval_eval.py`), config |
| `benchmark/results/` | Run results, `results.csv` |
| `benchmark/*.md` | [design](benchmark/design.md), [models](benchmark/models.md), [live test](benchmark/live-test.md), [retrieval check](benchmark/retrieval-check.md) |

## Project: not deployed
| Folder | Holds |
|---|---|
| `project/README.md` | What the project folder holds |
| `project/plan.md` | Milestones, decisions, open work. Read first |
| `project/author-questions.md` | Questions for the author |
| `project/design-thresholds.md` | Threshold catalog design: use cases, files, fields. Proposal |
| `project/alert_close_cycle_design_best_practices.md` | Example of an alert close cycle design, for review (Q155 answer; reviewed in `project/design-thresholds.md`, section 9.5) |
| `project/review-*.md` | Dated reviews of the mission, architecture and benchmark |
| `project/vocabulary.md`, `project/terms.md` | Writing vocabulary; repository terms |
| `project/sources/` | Source documents. Read-only |
| `project/knowledge-rules/` | Rules for knowledge files, one module each: placement, flows, metadata, thresholds, writing, terminology |
| `project/templates/` | Templates for knowledge files: concept, metric, configuration, alerts (one object type), screen, and the three flow kinds (health check, troubleshooting, decision tree) |
| `project/tools/` | `lint.py` and `tags.yaml` (checks and allowed values), `link_refs.py` and `moved.yaml` (old file ids → current ids), `tidy.py`, `kpi_csv.py`, `answered.py`, `renumber_questions.py`, `coverage.py` (question set against the blueprint) |
| `project/archive/` | Retired documents |
