# Metadata and retriever_guide

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

## retriever_guide
| Value | Question it answers | Folder | Template |
|---|---|---|---|
| how-it-works | How does it work? Why does the metric behave this way? | `concepts/`, `sp5-framework/observability/`, `sp5-framework/outputs/`, `vsphere/architecture/`, `vcf-operations/` (role, features, dashboards, reports, alert definitions) | `concept.md` |
| metric-meaning | What does this number mean on this object? | `metrics/`, `models/`, `tools/`; `<object>-performance` (KPI) | `metric.md` |
| term-meaning | What does this term mean? | [`knowledge/glossary.md`](../../knowledge/glossary.md) | - |
| what-to-set | What should be configured, and why? Which alerts does this object type get, and why? | `configuration/`; `<object>-alerts` | `configuration.md`, `alerts.md` |
| health-check | Is this object healthy? What do I check, in what order (the what)? | `<object>-health-check` | `health-check.md` |
| troubleshooting | It is down or slow (complaint, alert, failed health check step). Why? What do I check, in what order? | `troubleshooting/`, or the parent folder for a single flow | `troubleshooting.md` |
| decision-tree | Can it, should it, how much? One operational question, ending in a choice to act | `decision-tree/`, or the parent folder for a single tree | `decision-tree.md` |

- `retriever_guide` is the kind of the file: the harness (reading plan, flow executor, catalog, search filter) and lint read it, not the folder. A kind folder exists only with 2 or more files ([placement.md](placement.md)).

## Metadata fields (end of file)
Every knowledge file and every benchmark question ends with a `## Metadata` section holding one yaml block. No front matter at the top.

| Field | Meaning |
|---|---|
| `id` | Path without `knowledge/` and `.md`. A file that moves gets a line in [`project/tools/moved.yaml`](../tools/moved.yaml) (old id → new id): lint names the current id when an old one is still used, and `link_refs.py` rewrites links in the author documents. Not deployed: the harness reads only current ids. |
| `retriever_guide` | See retriever_guide above. |
| `scope` | sp5-framework, vsphere, vcf-operations or guest-os; matches the top folder. Root files (glossary, misconceptions): sp5-framework. |
| `technology` | cpu, memory, storage, network, system. System = the box as a whole: OS, BIOS, or a whole device. |
| `pillar` | availability, performance, security, capacity, value: the five pillars of the SP5 framework. Value covers the cost IT spends, the price it charges tenants, and the business value of the investment. Security is part of the platform; inventory and configuration sit under all five pillars. |
| `product` | vsphere, vsan, nsx, vcf-operations, windows, linux, kubernetes. On a method file: the products its terms and examples use. |
| `object` | vSphere managed object types: VirtualMachine, HostSystem, ClusterComputeResource, ResourcePool, Datastore, Datacenter, Folder, VmwareDistributedVirtualSwitch, DistributedVirtualPortgroup, ... |
| `layer` | Required in `metrics/virtual-motherboard/` and in every file under [`knowledge/guest-os/`](../../knowledge/guest-os). The stack layer that produces the metric: guest-os, virtual-motherboard, hypervisor, physical. |
| `instance` | Metric files only, optional. The instance level when the formula differs by instance: aggregate, per-vcpu, per-vmnic, ... |
| `metric_class` | Metric files only. contention, consumption, or context. Context metrics account for inventory or configuration and answer "it depends" questions. |
| `internal_derive` | Ids of other knowledge-base files that this file is derived from. Internal links only. Not book chapters, not URLs. |
| `same_name` | Metric files only. Ids of metrics with the same label but a different meaning. |
| `same_meaning` | Metric files only. Ids of metrics with a different label but the same meaning. |
| `related` | Ids to retrieve together. |
| `images` | One entry per image linked in the body. Fields: `path` (as linked), `product`, `object`, `metric` (list of metric names shown) and/or `topic` (concept shown), `image_type` (diagram, table, timeline, distribution, scatter, screenshot), `sample` (optional: fleet size and period). The image's own tags: they can differ from the file's, e.g. an ESXi chart inside a cluster concept. |
| `source.document` / `source.path` | Source document (with version and revision) and heading path or pages. |
| `corrections` | Facts that differ from the source document named in `source.document`. Each entry names the section it affects. |
| `review_notes` | Only what is still to check: section, what, and the URL or document to check against. No who-said-it tags. A settled item is deleted. |
| `status` | draft (not reviewed) or reviewed. Agent E2 says so when an answer depends on a draft file. |

- Audit information (corrections, what is still to check, review state) lives only in the metadata block. Body text and headings carry no audit markers and no who-said-it tags: no "", no "the author states".

## Dimensions not to mix
The concepts behind the tags; the allowed values are in [`project/tools/tags.yaml`](../tools/tags.yaml).
- Object type: a kind of managed object (VirtualMachine, HostSystem). Not a component inside an object (vCPU, vmnic).
- Object: one named instance of an object type ("db01"). Not a metric or a layer.
- Instance (metric): a sub-component a metric is reported for (vCPU 0, vmnic1, vmhba0). Tag `instance`. Not an object type.
- Layer: a level of the stack: guest-os, virtual-motherboard, hypervisor, physical. Guest OS is a layer, not an object type.
- Vantage point: the layer or object a metric is observed from (consumer VM vs provider ESXi). Expressed through `object` and `layer`.
- Perspective (book): technology, pillar of operations, product. Not a layer.
- Technology: cpu, gpu, memory, storage, network, system (the box as a whole). Not a product.
- Pillar: availability, performance, security, capacity, value. Not a technology.
- Metric class: contention, consumption, context. Not a pillar.
- Metric: a measured value with name, unit and formula, for one object type. Counter: the raw source counter (`cpu.ready.summation`); a metric may use several. Property: an attribute set by configuration or capability (configured hosts, maximum VMs), not produced at an interval. A count of inventory (VMs in a cluster) and a state (power state) are metrics: `knowledge/foundations/input-types`.
- Misconception: a wrong conclusion from a true observation or a public rule of thumb, held with confidence at Level 300, with the mechanism that corrects it. One concept, two homes: `## Misconceptions` in the file, and the widest-reaching ones up front in [`knowledge/misconceptions.md`](../../knowledge/misconceptions.md). [`KNOWLEDGE-ENGINEERING.md`](../KNOWLEDGE-ENGINEERING.md), section 4.
- Level 400: mechanism, where the reading misleads, what to check instead. Level 300: a metric and a common threshold at face value.
- Thread (physical): a hardware thread, a provider. Thread (software): an OS thread, a consumer.
