<p align="center">
  <img src="https://img.shields.io/badge/Isvara-Level%20400%20private%20cloud%20expertise-1f6feb?style=for-the-badge" alt="Isvara: Level 400 private cloud expertise">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/vSphere-9.1-607078?logo=vmware&logoColor=white" alt="vSphere 9.1">
  <img src="https://img.shields.io/badge/VCF-9.1.1-607078?logo=vmware&logoColor=white" alt="VCF 9.1.1">
  <img src="https://img.shields.io/badge/model-27--32B%20open%20weights-6f42c1" alt="Model: 27-32B open weights">
  <img src="https://img.shields.io/badge/runs-offline%20%28dark%20site%29-2da44e" alt="Runs offline">
  <img src="https://img.shields.io/badge/knowledge%20files-205-0969da" alt="Knowledge files: 205">
  <img src="https://img.shields.io/badge/benchmark%20cases-28-bf8700" alt="Benchmark cases: 28">
  <img src="https://img.shields.io/badge/target-99%25%20stable%20correct-d1242f" alt="Target: 99% stable correct">
  <img src="https://img.shields.io/badge/python-3.10%2B-3776ab?logo=python&logoColor=white" alt="Python 3.10+">
</p>

# Isvara: private cloud expertise

**🏛️ [Architecture](ARCHITECTURE.md) · 🧠 [Knowledge engineering](KNOWLEDGE-ENGINEERING.md) · 🧪 [Test design](benchmark/test-design.md) · ⚙️ [Harness](harness/README.md)**

**Business problem:**
- Many private cloud customers cannot send operational data to a cloud AI service: regulated industries, government and defence, and dark sites with no Internet at all.
- Others can use cloud AI but must contain its cost: per-token fees grow with every question, user and automated check.
- Frontier AI models answer vSphere performance questions from public Internet text, which repeats common misconceptions. Their answers sound expert and are often wrong at Level 400.

**Goal:** a 32B-class open-weight model, running offline on one GPU (dark site, no Internet, no per-token cost), answers Level 400 private cloud operations questions better than frontier models.

**How:** model + harness + knowledge.
- **Knowledge** (`knowledge/`): Level 400 mechanisms, metrics, traps and troubleshooting flows, written to be retrieved by a small model. Version 1.0 covers vSphere 9.1 metrics and the Guest OS layer; the end scope is the private cloud stack (vSAN, NSX, VCF Operations, Kubernetes, Linux).
- **Harness** (`harness/`): the software around the model: hybrid retrieval, link expansion, exact tools (metric catalog lookup, calculator, flow executor), and an answer verifier. See `harness/README.md`.
- **How the parts work together** (who drives, one question step by step, how Level 400 is delivered offline): `ARCHITECTURE.md`.
- **How expert knowledge is captured** (the forms of codified knowledge, three slices, thresholds, how knowledge enters and is kept right): `KNOWLEDGE-ENGINEERING.md`.
- **Model**: a 27-32B open-weight model on a local GPU, chosen by benchmark.
- **Proof** (`benchmark/`): a fixed benchmark scored against a frontier model, with luck removed (Unsure option, confident-wrong rate, 5 runs must agree).

**Why it can work, why 32B, which models:** `project/solution-design.md`.
**Status and review:** not achieved yet; best small model 58% vs frontier 75% on the first 17 questions. Findings and decisions: `project/review-2026-11-04.md`.

Readers: the model reads `knowledge/`. The author reviews for QA. Everything below is the contract the files are written to.

## Layout

```text
knowledge/                           # what the model reads (indexed)
├── catalog/                         # structured data read by harness tools, not chunked as prose:
│                                    # vCenter counters, esxtop fields, thresholds, object model (YAML)
├── foundations/                     # vendor-neutral: units, sampling, accounting, perspectives, naming
├── glossary.md                      # one glossary: terms, synonyms, distinctions, words to avoid (all products)
├── operations-management/           # pillars of operations that cut across products
│   ├── performance/                 # KPI design, troubleshooting method
│   └── capacity/                    # capacity model, sizing
├── vsphere/
│   ├── foundations/                 # vSphere-wide: provider/consumer, VM vs Guest OS, vCenter statistics, esxtop,
│   │                                # overhead, resource controls (reservation, limit, shares)
│   ├── technology/                  # raw metrics, by technology (book route: contention first, then consumption)
│   │   └── cpu/ gpu/ memory/ storage/ network/
│   │       ├── concepts/            # how it works
│   │       ├── metrics/<object>/    # one metric, one object type per file: virtual-motherboard/, host/,
│   │       │                        # cluster/, datastore/; comparisons/ for side-by-side groups
│   │       ├── configuration/       # what to set
│   │       ├── diagnosis/           # flows within this technology
│   │       └── images/
│   ├── object-types/                # derived metrics and multi-technology content, by object (book route)
│   │   └── vm/ esxi/ cluster/ ...   # concepts/, metrics/, configuration/, diagnosis/, images/
│   └── screens/                     # screen library for screenshot upload (release 1.1): vsphere-client/, esxtop/
├── vcf-operations/                  # what VCF Operations adds: computed metrics, KPIs, capacity engine, policies,
│                                    # alerts, super metrics. Links to the source files; never repeats them.
├── guest-os/                        # Windows, Linux: a separate layer, not Broadcom products, not part of the VM
│   └── <technology>/                # concepts/, metrics/, images/ (scope: guest-os, layer: guest-os)
├── _templates/                      # concept, metric, configuration, diagnosis, screen (not indexed)
└── raw-input/                       # source documents (not indexed)
harness/                             # the software around the model: retrieval, tools, verifier, prompts (not indexed)
benchmark/                           # proof: questions with answer keys, attachments, runner, results (not indexed)
project/                             # design, decisions, author questions, to-do, archive (not indexed)
tools/                               # lint.py (file and tag checks), tags.yaml (allowed tag values) (not indexed)
```

- The author's book sees metrics from 3 perspectives: technology, pillar of operations, product. A folder tree holds one hierarchy; tags (`technology`, `pillar`, `product`, `object`) hold the others, and retrieval and the website browse by any of them.
- The folders follow the book's blend:
  - raw metrics follow the technology route: `vsphere/technology/<tech>/`;
  - derived metrics follow the object route, and within each object the pillars: `vsphere/object-types/<object>/`;
  - pillars that cut across products (vSphere, vSAN, NSX, Guest OS): `operations-management/<pillar>/`.
- Placement rules, so a fact lives in one place:
  - A metric about one technology goes in `technology/`, even when it belongs to one object. VM CPU Ready: `vsphere/technology/cpu/metrics/virtual-motherboard/`.
  - `object-types/` holds what combines technologies for one object: KPIs, vMotion, cluster risk, DRS, admission control. Each object folder gets an overview file that lists what to monitor, in priority order, linking the technology files.
  - `operations-management/` holds only content that applies across products. Product-specific pillar content stays with the product's object (cluster usable capacity with HA: `vsphere/object-types/cluster/`) and is linked from there.
  - Flows: one technology → `technology/<tech>/diagnosis/`; one object, several technologies → `object-types/<object>/diagnosis/`; across products → `operations-management/performance/`.
  - VCF Operations is a thin derived layer. A metric about a source object is documented once, at the source. `vcf-operations/` holds only what VCF Operations computes or adds, with `internal_derive` links to the source files. See `vcf-operations/concepts/vcf-operations-role`.
- Storage, not disk. Datastores, adapters, paths and vSAN are storage but not disks; a disk is one layer. vCenter keeps separate counter groups per layer (`virtualDisk`, `disk`, `datastore`, `storageAdapter`, `storagePath`), and the same label means a different scope in each. One word for folder, tag and glossary: `storage`.
- vCenter is the administrative tool (create VMs, configure switches). Capacity planning and performance troubleshooting are done in VCF Operations. The knowledge base never uses the two names interchangeably.
- Three foundations levels, different scope:
  - `knowledge/foundations/`: true across VCF 9 components and Guest OS.
  - `knowledge/operations-management/`: how a pillar uses metrics, across products.
  - `knowledge/vsphere/foundations/`: true only in vSphere.
- `metrics/<object>` folder names: `virtual-motherboard`, `host`, `cluster`, `datastore`. The `object` tag holds the vSphere managed object type name.
- A VM is a virtual motherboard, not a complete machine. Its raw metrics live in `metrics/virtual-motherboard/` (`object: VirtualMachine`, `layer: virtual-motherboard`). The folder name is in every file id, so the model reads it with every VM chunk.
- Guest OS knowledge (Windows, Linux) is a separate layer and not a Broadcom product. It lives in `knowledge/guest-os/<technology>/` with `scope: guest-os`, `layer: guest-os` and no VM object, even though VMware Tools stores some counters on the VM object. Boundary files comparing Guest OS and VM stay in `knowledge/vsphere/`.
- Screen library (`screens/`, release 1.1): one file per screen type with a screenshot, a full text twin, the metrics it shows (`metrics_shown`), UI and version (`ui`, `ui_version`). Template: `knowledge/_templates/screen.md`.
- `tools/lint.py` enforces the folder and tag rules.

## Why this structure
- Full reasoning: `project/philosophy-and-structure.md`.
- A generic AI fails on vSphere metrics in a known way: it knows the general meaning of a label and applies it where vSphere differs.
- Each structural choice blocks one failure:

| Choice | Failure it blocks |
|---|---|
| Concepts separate from metrics | Answering from a definition without the mechanism behind the value. |
| One object type per metric file | Mixing the VM, ESXi and cluster meanings of the same label. |
| `same_name` / `same_meaning` links | Treating two metrics as equal because the labels match, or as different because the labels differ. |
| Book-order folders plus tags | One hierarchy for review in the book's order; tags give the other perspectives (technology, pillar, product, object). |
| `retriever_guide` | Retrieving a definition when the question asks what to check or what to set. |
| Small files, one fact per line | A retrieved chunk carrying unrelated facts; an error spreading beyond one line. |
| Metadata at the end, parsed separately | Audit text (status, corrections) polluting the embedded content. |
| Foundations at three levels | vSphere-only rules applied to other products, or general rules duplicated per product. |
| A `## Traps` section in every metric file | A true observation read to the wrong conclusion. See Traps and Level 400. |

## Traps and Level 400

### Levels
| Level | Can do | Example (VM CPU Ready) |
|---|---|---|
| 100 | Name the metric. | "Ready is a CPU metric." |
| 200 | Define it. | "Ready is time a vCPU waited for a physical thread." |
| 300 | Use it: read the value, apply a common threshold, follow a runbook. | "Ready above 5% is bad; add capacity." |
| 400 | Explain the mechanism, predict where the reading misleads, and say what to check instead. | "2% Ready on 10% Run delayed 20% of the work; 2% on 98% Run is fine. Ready includes limit time and the summation counter grows with vCPU count, so check Run, Max Limited and the per-vCPU %." |

- The knowledge base is written at Level 400. Levels 100-200 are assumed; generic models already reach Level 300 from public text.
- What separates 400 from 300 is the trap: a Level 300 reader takes the reading at face value and acts on it; a Level 400 reader knows when the reading lies.

### What a trap is
- A trap is a wrong conclusion drawn from a true observation. The number is right; the reading is wrong.
- It is plausible: an experienced administrator, a generic AI, or even the vendor documentation would draw it.
- It has a mechanism: the knowledge base can say why the conclusion fails and what to check instead.
- Format, one per line, in the `## Traps` section at the end of the file body:

```text
- "<the wrong conclusion, in the words someone would use>" → <the correct reading, the reason, and what to check instead>.
```

- Example: "Swap Consumed = Swap Out - Swap In" → no. Swap Out and Swap In are cumulative totals; Swap Consumed is what sits in swap now, like VM Swapped.

### Trap types
| Type | The reading goes wrong because | Example |
|---|---|---|
| Same name, other object | One label has different meanings on VM, ESXi, cluster | VM CPU Usage vs ESXi CPU Usage |
| Layer confusion | A Guest OS reading is taken as a VM reading, or the reverse | Guest OS run queue called a VM metric |
| Consumption read as contention | Utilization is taken as a performance signal | "Host CPU 90%, so VMs are slow" |
| Average hides the worst | A host or cluster average hides the VM that suffers | "Host Ready is low, so every VM is fine" |
| Rollup and interval | Averaging over 5 minutes or a day removes 20-second peaks | "The 1-week chart shows the peak" |
| Unit and normalization | Summation, per-vCPU vs per-VM, KB vs kb, ms vs % | "Ready of 2,000 ms is high" |
| Frequency and Hyper-Threading | Turbo, power management and HT bend percentages | "Usage above 100% is a data error" |
| Provider vs consumer | A consumer concept is applied to the provider, or the reverse | "Ready applies to ESXi" |
| Cumulative vs current | A running total is read as a current amount | "Swap Consumed = Swap Out - Swap In" |
| Threshold transplanted | A threshold from one layer, product or hardware era is applied elsewhere | "DAVG 10 ms is fine; the docs allow 15 ms" |
| Reclamation read as contention | Balloon, swapped or compressed memory is read as current waiting | "Balloon above 0, so the VM is slow" |
| Tool confusion | vCenter and VCF Operations, or esxtop and vCenter, are treated as the same reading | "Same counter name, so the values match" |

### How traps are used
- Retrieval: a trap line holds the wrong conclusion in the user's own words, so a question that carries the misconception retrieves the file that corrects it.
- `same_name` links bring in the other object's meaning of the same label: the main guard against the first trap type.
- The model is told to watch for same-name metrics and to answer with the mechanism, not the definition.
- Benchmark: every multiple-choice question has a trap option named in `## Likely wrong answer`; the trap rate is reported per model. See `benchmark/test-design.md`.
- A trap without a mechanism is an opinion, not a trap: it needs a source like any other fact.

## How a local LLM uses it
- Design target: a local LLM with a small context window and retrieval-augmented generation (RAG). The knowledge base is the retrieval corpus. No fine-tuning is assumed.
- `harness/` implements the steps below. They are also the contract for any other RAG stack.

### Ingest
1. Index `knowledge/**/*.md` except the folders listed in Indexing rules.
2. Split each file at `## Metadata`. Parse the yaml block into filter fields. Do not embed it.
3. Chunk the body by `##` heading. Files are short, so one file is often one chunk.
4. Prefix each chunk with the file title and `id`, so a chunk is understood without its neighbours.
5. Keep image links in the chunk. The text next to each image states the same facts, so a text-only model loses nothing.
6. Index each `images` entry as its own record (path, alt text, tags), so an image can be retrieved by product, object, metric or type, and returned with what it shows.
7. Load `knowledge/catalog/*.yaml` into a database for exact lookups (unit, rollup, statistics level, thresholds, object relations). Do not chunk it as prose.

### Query
1. Classify the question into one `retriever_guide` value: how-it-works, metric-meaning, term-meaning, what-to-set, what-to-check.
2. Extract filters from the question: `product`, `object`, `technology`, `pillar`.
3. Retrieve by similarity within those filters.
4. Expand: add files named in `related`, `internal_derive`, `same_name`, `same_meaning`.
   - `same_name` is the main trap guard: it brings in the other object's meaning of the same label.
5. Add the matching foundations files when the answer depends on units, sampling, thresholds or the provider/consumer view.
6. Fit to the context window. Priority: matching metric or diagnosis file, then its concepts, then foundations, then the rest of the links.
7. Take exact values (units, rollups, statistics levels, thresholds) from the catalog, and arithmetic from the calculator, not from the model.

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
- Location: one technology → `vsphere/technology/<tech>/diagnosis/`; one object, several technologies → `vsphere/object-types/<object>/diagnosis/`; across products → `operations-management/performance/`.
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
- Do not index: `knowledge/_templates/`, `knowledge/raw-input/`, `benchmark/`, `project/`, `harness/`, `tools/`, this README, `CLAUDE.md`, `ARCHITECTURE.md`, `KNOWLEDGE-ENGINEERING.md`, `CONTRIBUTING.md`, `SECURITY.md`.
  - `benchmark/` holds answer keys. Indexing it invalidates the evaluation.
- Metadata is the last section of each file: `## Metadata` followed by one yaml block. Parse it as metadata, not as text to embed.
- Images live in the `images/` folder of the folder that uses them: `vsphere/technology/<tech>/images/`, `vsphere/object-types/<object>/images/`, `vsphere/foundations/images/`, `operations-management/<pillar>/images/`, `guest-os/<technology>/images/`. Each image link carries alt text; the body text states the same facts. Return the image link when a diagram answers the question.
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
- Tables: short cells (about 12 words). At most 4 columns when cells hold text; number tables such as colour bands can have more. When rows carry long explanations, use one bullet block per row instead (bold item, one sub-bullet per field). GitHub renders a fixed-width column, so wide tables wrap every cell. Split a wide table in two, or move long explanations to bullets under the table.
- Every metric file ends its body with `## Traps`, written in the format of section Traps and Level 400.
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
