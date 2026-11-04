# Isvara: private cloud expertise for a local 32B LLM

**Goal:** a 32B-class open-weight model, running offline on one GPU (dark site, no Internet, no per-token cost), answers Level 400 private cloud operations questions better than frontier models.

**How:** model + harness + knowledge.
- **Knowledge** (`knowledge/`): Level 400 mechanisms, metrics, traps and troubleshooting flows, written to be retrieved by a small model. Version 1.0 covers vSphere 9.1 metrics and the Guest OS layer; the end scope is the private cloud stack (vSAN, NSX, VCF Operations, Kubernetes, Linux).
- **Harness** (`harness/`): the software around the model: hybrid retrieval, link expansion, exact tools (metric lookup, calculator, flow executor), grounding and answer checks. Today: retrieval and the tool loop.
- **Model**: a 27-32B open-weight model on a local GPU, chosen by benchmark.
- **Proof** (`benchmark/`): a fixed benchmark scored against a frontier model, with luck removed (Unsure option, guessing penalty, 5 runs must agree).

**Why it can work, why 32B, which models:** `project/solution-design.md`.
**Status and review:** not achieved yet; best small model 58% vs frontier 75% on the first 17 questions. Findings and decisions: `project/review-2026-11-04.md`.

Readers: the model reads `knowledge/`. The author reviews for QA. Everything below is the contract the files are written to.

## Layout

```text
knowledge/                           # what the model reads (indexed)
├── foundations/                     # cross-product concepts: units, sampling, thresholds, naming, perspectives
├── glossary.md                      # one glossary: terms, synonyms, distinctions, words to avoid (all products)
├── guest-os/                        # Windows, Linux: a separate layer, not Broadcom products, not part of the VM
│   └── <technology>/                # concepts/, metrics/, images/ (scope: guest-os, layer: guest-os)
├── vsphere/
│   ├── foundations/                 # vSphere-specific only: provider/consumer, VM vs Guest OS, kernel worlds,
│   │                                # overhead, metric sources, vCenter statistics
│   ├── cpu/
│   │   ├── concepts/                # how it works
│   │   ├── metrics/<object-folder>/ # one metric, one vSphere object type per file
│   │   │   ├── virtual-motherboard/ # VM metrics (a VM is a virtual motherboard)
│   │   │   └── comparisons/         # groups of metrics compared side by side, esxtop references
│   │   ├── configuration/           # what to set, for any pillar
│   │   ├── diagnosis/               # symptom → checks → meaning
│   │   └── images/                  # the author's diagrams, linked from the files they explain
│   ├── memory/  storage/  network/  system/     # same subfolders
│   └── resource-management/         # reservation, limit, shares, admission control, DRS, DPM, vCLS
├── _templates/                      # concept, metric, configuration, diagnosis (not indexed)
└── raw-input/                       # source documents (not indexed)
harness/                             # the software around the model: retrieval, tool loop, prompts (not indexed)
benchmark/                           # proof: questions with answer keys, attachments, runner, results (not indexed)
project/                             # design, decisions, author questions, to-do, archive (not indexed)
tools/                               # lint.py (file and tag checks), tags.yaml (allowed tag values) (not indexed)
```

- Folders follow technology first. Tags give the other angles (pillar, product, object).
- Two foundations levels. They have different scope; do not merge them.
  - `knowledge/foundations/`: holds only what applies across VCF 9 components.
  - `knowledge/vsphere/foundations/`: holds what is true only in vSphere.
  - Test: if the fact is still true for vSAN, NSX or a Guest OS, it goes in `knowledge/foundations/`.
- `object-folder` names: `virtual-motherboard`, `guest-os`, `host`, `cluster`, `datastore`, ... The `object` tag holds the vSphere managed object type name.
- A VM is a virtual motherboard, not a complete machine. Its metrics live in `virtual-motherboard/` (`object: VirtualMachine`, `layer: virtual-motherboard`). The folder name is in every file id, so the model reads it with every VM chunk.
- Guest OS knowledge (Windows, Linux) is a separate layer and not a Broadcom product. It lives in `knowledge/guest-os/<technology>/` with `scope: guest-os`, `layer: guest-os` and no VM object, even though VMware Tools stores some counters on the VM object. Boundary files comparing Guest OS and VM stay in `knowledge/vsphere/`. `tools/lint.py` enforces these rules.

## Why this structure
- Full reasoning: `project/philosophy-and-structure.md`.
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
6. Index each `images` entry as its own record (path, alt text, tags), so an image can be retrieved by product, object, metric or type, and returned with what it shows.

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
- Use terms from `knowledge/glossary.md`. Avoid the words in its Words to avoid table.
- Quote a threshold only when a file states it with its source.

### Troubleshooting questions (`what-to-check`)
- Retrieve the matching `diagnosis/` file first. Retrieve its `internal_derive` metric files with it.
- Follow the numbered steps in `## Checks, in order`, from step 1. Do not skip to a later step.
- At each step: name the metric and object, compare with the stated threshold, then take the branch the step gives.
- Use the Mermaid flow only to confirm the branch. The numbered steps win if they differ.
- When the user has given a value, apply it to the step. When not, ask for that metric's value, or state both branches.
- Stop at the step that gives a conclusion. State the path taken: step numbers, values, thresholds and their sources.
- No diagnosis file matches: say so, then answer from metric and concept files. Do not invent a flow or a threshold.
- Contention before consumption before context, unless the file states another order.

### Measurement
- `benchmark/` runs the same golden cases with and without the knowledge base. A structure change is kept only when scores improve.

## Troubleshooting flow diagrams
- Location: the `diagnosis/` folder of the technology. A flow across technologies goes in `knowledge/vsphere/system/diagnosis/`.
- One flow per file. Order: symptom, Mermaid flowchart, numbered steps, why this order, traps, metadata.
- The numbered steps are what the LLM follows. The Mermaid chart is a second, text-readable view; GitHub renders it for review.
- Each step states: the metric (exact name, matching the metric file title), the object, the threshold with its source, and the next step for each outcome.
  - Example: 1. Check VM CPU Ready (VirtualMachine). Above <threshold> (<source>) → step 2. Otherwise → step 4.
- Every metric named in a step is linked in `internal_derive`, so retrieval brings in the metric files with the flow.
- Mermaid node text repeats the step number: `S1[1. VM CPU Ready above threshold?]`. Step numbers tie the chart to the text.
- Keep each flowchart to about 15 nodes. Split a larger flow into linked diagnosis files.
- draw.io files are not read by the LLM: the XML is mostly layout and style, and compressed files are unreadable.
  - Keep the `.drawio` file and an exported `.png` in the `images/` folder of the technology as the editable source.
  - Link the `.png` under the flowchart and tag it in `images` (`image_type: diagram`).
  - The Mermaid chart and numbered steps are the content the LLM uses.

## Indexing rules
- Index: `knowledge/**/*.md`.
- Do not index: `knowledge/_templates/`, `knowledge/raw-input/`, `benchmark/`, `project/`, `harness/`, `tools/`, this README, `CLAUDE.md`.
  - `benchmark/` holds answer keys. Indexing it invalidates the evaluation.
- Metadata is the last section of each file: `## Metadata` followed by one yaml block. Parse it as metadata, not as text to embed.
- Images live in the `images/` folder of the technology folder that uses them: `knowledge/vsphere/<technology>/images/`, `knowledge/guest-os/<technology>/images/`. Each image link carries alt text; the body text states the same facts. Return the image link when a diagram answers the question.
- When a file is retrieved, also consider retrieving the ids in `related`, `internal_derive`, `same_name` and `same_meaning`.

## retriever_guide: which question a file answers
| Value | Question it answers | Folder | Template |
|---|---|---|---|
| how-it-works | How does it work? Why does the metric behave this way? | `concepts/`, `foundations/` | `concept.md` |
| metric-meaning | What does this number mean on this object? | `metrics/` | `metric.md` |
| term-meaning | What does this term mean? | `knowledge/glossary.md` | - |
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
| `layer` | Required in `metrics/virtual-motherboard/` and in every file under `knowledge/guest-os/`. The stack layer that produces the metric: guest-os, virtual-motherboard, hypervisor, physical. |
| `instance` | Metric files only, optional. The instance level when the formula differs by instance: aggregate, per-vcpu, per-vmnic, ... |
| `metric_class` | Metric files only. contention, consumption, or context. Context metrics account for inventory or configuration and answer "it depends" questions. |
| `internal_derive` | Ids of other knowledge-base files that this file is derived from. Internal links only. Not book chapters, not URLs. |
| `same_name` | Metric files only. Ids of metrics with the same label but a different meaning. |
| `same_meaning` | Metric files only. Ids of metrics with a different label but the same meaning. |
| `related` | Ids to retrieve together. |
| `images` | One entry per image linked in the body. Fields: `path` (as linked), `product`, `object`, `metric` (list of metric names shown) and/or `topic` (concept shown), `image_type` (diagram, table, timeline, distribution, scatter, screenshot), `sample` (optional: fleet size and period). The image's own tags: they can differ from the file's, e.g. an ESXi chart inside a cluster concept. |
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
- Every image has its own tags in the file's metadata `images` list (see Metadata). The validator fails on a missing or invalid entry.
- Every image file is linked from a knowledge file. The validator fails on an unlinked image: an unlinked image has no context for the AI.
- File names describe what the image shows. No length limit applies (GitHub, git and Markdown accept long names); clarity wins.
  - Pattern: `<object>-<metric or topic>-<what it shows>.png`, lowercase, hyphens. Example: `esxi-storage-adapter-read-write-latency-worst-vs-average-across-hosts.png`.
  - Chart type at the end when it helps: `-distribution`, `-scatter`, `-timeline`, `-table`, `-diagram`.
  - No bare numbers. Sample sizes (192 hosts, 3,385 VMs) go in the alt text and body, not the file name. A number stays only when it is the point, e.g. `62-5-percent`.
- Third-party images (vendor diagrams, documentation screenshots) are not copied. Link the source in `review_notes`.

## QA workflow
1. AI extracts a section into files with `status: draft`.
   - Run `python3 tools/lint.py`. It must pass before merge.
2. Author reviews, answers `review_notes`, fixes errors.
3. Author sets `status: reviewed`.
4. When the source document is updated, move `corrections` into the normal text and clear them.
5. Run `benchmark/` golden cases with and without the knowledge base; record results in `benchmark/results/results.csv`.
