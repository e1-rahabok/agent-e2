# Metadata and retriever_guide

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

## retriever_guide
| Value | Question it answers | Folder | Template |
|---|---|---|---|
| how-it-works | How does it work? Why does the metric behave this way? | `concepts/`, `observability/`, `vsphere/architecture/`, `sp5-framework/alerts/`, `vcf-operations/` features, dashboards, reports, alerts | `concept.md` |
| metric-meaning | What does this number mean on this object? | `metrics/`, `kpis/`, `models/`, `tools/` | `metric.md` |
| term-meaning | What does this term mean? | `knowledge/glossary.md` | - |
| what-to-set | What should be configured, and why? | `configuration/` | `configuration.md` |
| health-check | Is this object healthy? What do I check, in what order (the what)? | `health-check/` | `health-check.md` |
| troubleshooting | It is down or slow (complaint, alert, failed health check step). Why? What do I check, in what order? | `troubleshooting/` | `troubleshooting.md` |
| decision-tree | Can it, should it, how much? One operational question, ending in a choice to act | `decision-tree/` | `decision-tree.md` |

## Metadata fields (end of file)
Every knowledge file and every benchmark question ends with a `## Metadata` section holding one yaml block. No front matter at the top.

| Field | Meaning |
|---|---|
| `id` | Path without `knowledge/` and `.md`. A file that moves gets a line in `project/tools/moved.yaml` (old id → new id): lint names the current id when an old one is still used, and `link_refs.py` rewrites links in the author documents. Not deployed: the harness reads only current ids. |
| `retriever_guide` | See retriever_guide above. |
| `scope` | vendor-neutral (applies across VCF 9 components), sp5-framework, vsphere, vcf-operations or guest-os; matches the top folder. |
| `technology` | cpu, memory, storage, network, system. System = the box as a whole: OS, BIOS, or a whole device. |
| `pillar` | availability, performance, compliance, capacity, value: the five pillars of the SP5 framework. Value covers the cost IT spends, the price it charges tenants, and the business value of the investment. Security is part of the platform; inventory and configuration sit under all five pillars. |
| `product` | vsphere, vsan, nsx, vcf-operations, windows, linux, kubernetes. Empty for vendor-neutral files. |
| `object` | vSphere managed object types: VirtualMachine, HostSystem, ClusterComputeResource, ResourcePool, Datastore, Datacenter, Folder, VmwareDistributedVirtualSwitch, DistributedVirtualPortgroup, ... |
| `layer` | Required in `metrics/virtual-motherboard/` and in every file under `knowledge/guest-os/`. The stack layer that produces the metric: guest-os, virtual-motherboard, hypervisor, physical. |
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
