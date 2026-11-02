# Isvara-2 — vSphere metrics knowledge base for AI

Level 400 knowledge of vSphere metrics, for retrieval by an AI assistant.
Primary reader: AI. Secondary reader: the author, for QA.

Metrics are a byproduct of how the system works. Concepts explain the mechanism; metric files explain the meaning from one vantage point.

## Layout

```text
knowledge/
├── foundations/                     # vendor-neutral: naming, terminology, units, sampling, thresholds, perspectives
├── vsphere/
│   ├── foundations/                 # cross-technology vSphere concepts: provider/consumer, VM vs Guest OS,
│   │                                # visibility layers, kernel worlds, resource management, overhead
│   ├── cpu/
│   │   ├── concepts/                # how it works
│   │   ├── metrics/<object-folder>/ # one metric, one vSphere object type per file
│   │   │   └── comparisons/         # groups of metrics compared side by side
│   │   ├── configuration/           # what to set, for any pillar
│   │   └── diagnosis/               # symptom → checks → meaning
│   ├── memory/  storage/  network/  system/     # same four subfolders
│   ├── cluster-resource-management/ # DRS, DPM, shares, vCLS: concepts/ and configuration/
│   └── glossary/                    # term definitions
├── _templates/                      # concept, metric, configuration, diagnosis
└── raw-input/                       # source documents (not indexed)
evaluation/                          # golden cases with answer keys (not indexed)
docs/                                # design decisions, To Do, legacy files (not indexed)
```

- Folders follow technology first. Tags give the other angles (pillar, product, object).
- `object-folder` names: `virtual-machine`, `host`, `cluster`, `datastore`, ... The `object` tag holds the vSphere managed object type name.

## Indexing rules
- Index: `knowledge/**/*.md`.
- Do not index: `knowledge/_templates/`, `knowledge/raw-input/`, `evaluation/`, `docs/`, this README, `CLAUDE.md`.
  - `evaluation/` holds answer keys. Indexing it invalidates the evaluation.
- Parse YAML front matter as metadata, not as text to embed.
- When a file is retrieved, also consider retrieving the ids in `related`, `internal_derive`, `same_name` and `same_meaning`.

## retriever_guide: which question a file answers
| Value | Question it answers | Folder | Template |
|---|---|---|---|
| how-it-works | How does it work? Why does the metric behave this way? | `concepts/`, `foundations/` | `concept.md` |
| metric-meaning | What does this number mean on this object? | `metrics/` | `metric.md` |
| term-meaning | What does this term mean? | `glossary/` | `concept.md` |
| what-to-set | What should be configured, and why? | `configuration/` | `configuration.md` |
| what-to-check | Something is wrong. What do I check, in what order? | `diagnosis/` | `diagnosis.md` |

## Front matter
| Field | Meaning |
|---|---|
| `id` | Path without `knowledge/` and `.md`. |
| `retriever_guide` | See the table above. |
| `scope` | vendor-neutral or vsphere. |
| `technology` | cpu, memory, storage, network, system. System = the box as a whole: OS, BIOS, or a whole device. |
| `pillar` | availability, performance, security, capacity, value. |
| `product` | vsphere, vsan, nsx, vcf-operations, windows, linux, kubernetes. Empty for vendor-neutral files. |
| `object` | vSphere managed object types: VirtualMachine, HostSystem, ClusterComputeResource, ResourcePool, Datastore, Datacenter, Folder, VmwareDistributedVirtualSwitch, DistributedVirtualPortgroup, ... |
| `instance` | Metric files only, optional. The instance level when the formula differs by instance: aggregate, per-vcpu, per-vmnic, ... |
| `metric_class` | Metric files only. contention, consumption, or context. Context metrics account for inventory or configuration and answer "it depends" questions. |
| `internal_derive` | Ids of other knowledge-base files that this file is derived from. Internal links only. Not book chapters, not URLs. |
| `same_name` | Metric files only. Ids of metrics with the same label but a different meaning. |
| `same_meaning` | Metric files only. Ids of metrics with a different label but the same meaning. |
| `related` | Ids to retrieve together. |
| `source.document` / `source.path` | Source document (with version and revision) and heading path or pages. |
| `corrections` | Author facts not yet in the uploaded source document. Each entry names the section it affects. |
| `review_notes` | Open questions, source URLs, and facts from Claude's own knowledge (with section names). |
| `status` | draft (AI-extracted, not reviewed) or reviewed (author approved). |

- Audit information (corrections, Claude's own knowledge, review state) lives only in front matter. Body text and headings carry no audit markers.

## Writing rules
- One fact per bullet or table row. A mistake should sit on one line.
- State mechanism and reason, not only the definition.
- Facts may come from the source, the author, official docs, or Claude's own knowledge. Record any fact not in the source document in `review_notes` with its section. No generic filler. No invented thresholds.
- No text aimed at human motivation.
- One vSphere object type per metric file.
- Formulas as plain text. Diagrams as Mermaid plus a text explanation.
- CPU scheduling language: a vCPU is a thread in the scheduler. It demands runtime. The kernel decides how much runtime it gets. Avoid "need", "want", "wish".

## QA workflow
1. AI extracts a section into files with `status: draft`.
   - Run `python3 scripts/validate.py`. It must pass before merge.
2. Author reviews, answers `review_notes`, fixes errors.
3. Author sets `status: reviewed`.
4. When the source document is updated, move `corrections` into the normal text and clear them.
5. Run `evaluation/` golden cases with and without the knowledge base; record results in `evaluation/results/results.csv`.
