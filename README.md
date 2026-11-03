# Isvara-2 — vSphere metrics knowledge base for AI

Level 400 knowledge of vSphere metrics, for retrieval by an AI assistant.
Primary reader: AI. Secondary reader: the author, for QA.

Metrics are a byproduct of how the system works. Concepts explain the mechanism; metric files explain the meaning from one vantage point.

## Layout

```text
knowledge/
├── foundations/                     # general: applies across VCF 9 components (vSphere, vSAN, NSX, VCF Operations, Guest OS)
│                                    # naming, units, sampling, thresholds, perspectives
├── glossary/                        # terminology.md: terms, allowed tag values, words to avoid (all products)
├── vsphere/
│   ├── foundations/                 # vSphere-specific only: provider/consumer, VM vs Guest OS,
│   │                                # visibility layers, kernel worlds, resource management, overhead
│   ├── cpu/
│   │   ├── concepts/                # how it works
│   │   ├── metrics/<object-folder>/ # one metric, one vSphere object type per file
│   │   │   └── comparisons/         # groups of metrics compared side by side
│   │   ├── configuration/           # what to set, for any pillar
│   │   └── diagnosis/               # symptom → checks → meaning
│   ├── memory/  storage/  network/  system/     # same four subfolders
│   ├── cluster-resource-management/ # DRS, DPM, shares, vCLS: concepts/ and configuration/
│   ├── <technology>/images/         # the author's diagrams, linked from the files they explain
│   └── glossary/                    # vSphere-specific term definitions
├── _templates/                      # concept, metric, configuration, diagnosis
└── raw-input/                       # source documents (not indexed)
evaluation/                          # golden cases with answer keys (not indexed)
docs/                                # design decisions, To Do, legacy files (not indexed)
```

- Folders follow technology first. Tags give the other angles (pillar, product, object).
- Two foundations levels. They have different scope; do not merge them.
  - `knowledge/foundations/`: holds only what applies across VCF 9 components.
  - `knowledge/vsphere/foundations/`: holds what is true only in vSphere.
  - Test: if the fact is still true for vSAN, NSX or a Guest OS, it goes in `knowledge/foundations/`.
- `object-folder` names: `virtual-machine`, `host`, `cluster`, `datastore`, ... The `object` tag holds the vSphere managed object type name.

## Why this structure
- Full reasoning: `docs/philosophy-and-structure.md`.
- A generic AI fails on vSphere metrics in a known way: it knows the general meaning of a label and applies it where vSphere differs.
- Each structural choice blocks one failure:

| Choice | Failure it blocks |
|---|---|
| Concepts separate from metrics | Answering from a definition without the mechanism behind the value. |
| One object type per metric file | Mixing the VM, ESXi and cluster meanings of the same label. |
| `same_name` / `same_meaning` links | Treating two metrics as equal because the labels match, or as different because the labels differ. |
| Technology-first folders plus tags | One hierarchy for browsing; tags give the other angles (pillar, product, object) for filtering. |
| `retriever_guide` | Retrieving a definition when the question asks what to check or what to set. |
| Small files, one fact per line | A retrieved chunk carrying unrelated facts; an error spreading beyond one line. |
| Metadata at the end, parsed separately | Audit text (status, corrections) polluting the embedded content. |
| Two foundations levels | vSphere-only rules applied to other products, or general rules duplicated per product. |

## How a local LLM uses it
- Design target: a local LLM with a small context window and retrieval-augmented generation (RAG). The knowledge base is the retrieval corpus. No fine-tuning is assumed.
- No ingest or query code is in this repository. The steps below are the contract the files are written for.

### Ingest
1. Index `knowledge/**/*.md` except the folders listed in Indexing rules.
2. Split each file at `## Metadata`. Parse the yaml block into filter fields. Do not embed it.
3. Chunk the body by `##` heading. Files are short, so one file is often one chunk.
4. Prefix each chunk with the file title and `id`, so a chunk is understood without its neighbours.
5. Keep image links in the chunk. The text next to each image states the same facts, so a text-only model loses nothing.

### Query
1. Classify the question into one `retriever_guide` value: how-it-works, metric-meaning, term-meaning, what-to-set, what-to-check.
2. Extract filters from the question: `product`, `object`, `technology`, `pillar`.
3. Retrieve by similarity within those filters.
4. Expand: add files named in `related`, `internal_derive`, `same_name`, `same_meaning`.
   - `same_name` is the main trap guard: it brings in the other object's meaning of the same label.
5. Add the matching foundations files when the answer depends on units, sampling, thresholds or the provider/consumer view.
6. Fit to the context window. Priority: matching metric or diagnosis file, then its concepts, then foundations, then the rest of the links.

### Answer
- Answer from the retrieved text. Prefer mechanism and reason over a definition.
- Cite each file `id` used.
- Treat `status: draft` content as unreviewed. Say so when the answer depends on it.
- Use terms from `knowledge/glossary/terminology.md`. Avoid the words in its Words to avoid table.
- Quote a threshold only when a file states it with its source.

### Measurement
- `evaluation/` runs the same golden cases with and without the knowledge base. A structure change is kept only when scores improve.

## Indexing rules
- Index: `knowledge/**/*.md`.
- Do not index: `knowledge/_templates/`, `knowledge/raw-input/`, `evaluation/`, `docs/`, this README, `CLAUDE.md`.
  - `evaluation/` holds answer keys. Indexing it invalidates the evaluation.
- Metadata is the last section of each file: `## Metadata` followed by one yaml block. Parse it as metadata, not as text to embed.
- Images live in `knowledge/vsphere/<technology>/images/`. Each image link carries alt text; the body text states the same facts. Return the image link when a diagram answers the question.
- When a file is retrieved, also consider retrieving the ids in `related`, `internal_derive`, `same_name` and `same_meaning`.

## retriever_guide: which question a file answers
| Value | Question it answers | Folder | Template |
|---|---|---|---|
| how-it-works | How does it work? Why does the metric behave this way? | `concepts/`, `foundations/` | `concept.md` |
| metric-meaning | What does this number mean on this object? | `metrics/` | `metric.md` |
| term-meaning | What does this term mean? | `glossary/` | `concept.md` |
| what-to-set | What should be configured, and why? | `configuration/` | `configuration.md` |
| what-to-check | Something is wrong. What do I check, in what order? | `diagnosis/` | `diagnosis.md` |

## Metadata (end of file)
| Field | Meaning |
|---|---|
| `id` | Path without `knowledge/` and `.md`. |
| `retriever_guide` | See the table above. |
| `scope` | vendor-neutral (applies across VCF 9 components) or vsphere. |
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

- Audit information (corrections, Claude's own knowledge, review state) lives only in the metadata block. Body text and headings carry no audit markers.

## Writing rules
- One fact per bullet or table row. A mistake should sit on one line.
- State mechanism and reason, not only the definition.
- Facts may come from the source, the author, official docs, or Claude's own knowledge. Record any fact not in the source document in `review_notes` with its section. No generic filler. No invented thresholds.
- No text aimed at human motivation.
- One vSphere object type per metric file.
- Formulas as plain text. Diagrams as Mermaid plus a text explanation.
- CPU scheduling language: a vCPU is a thread in the scheduler. It demands runtime. The kernel decides how much runtime it gets. Avoid "need", "want", "wish".

## Images
- Keep the author's own diagrams and tables from the book. One image per concept, placed under the section it explains.
- Alt text describes what the image shows. The text around it repeats the facts, so retrieval does not depend on the image.
- File names describe what the image shows. No length limit applies (GitHub, git and Markdown accept long names); clarity wins.
  - Pattern: `<object>-<metric or topic>-<what it shows>.png`, lowercase, hyphens. Example: `esxi-storage-adapter-read-write-latency-worst-vs-average-across-hosts.png`.
  - Chart type at the end when it helps: `-distribution`, `-scatter`, `-timeline`, `-table`, `-diagram`.
  - No bare numbers. Sample sizes (192 hosts, 3,385 VMs) go in the alt text and body, not the file name. A number stays only when it is the point, e.g. `62-5-percent`.
- Third-party images (vendor diagrams, documentation screenshots) are not copied. Link the source in `review_notes`.

## QA workflow
1. AI extracts a section into files with `status: draft`.
   - Run `python3 scripts/validate.py`. It must pass before merge.
2. Author reviews, answers `review_notes`, fixes errors.
3. Author sets `status: reviewed`.
4. When the source document is updated, move `corrections` into the normal text and clear them.
5. Run `evaluation/` golden cases with and without the knowledge base; record results in `evaluation/results/results.csv`.
