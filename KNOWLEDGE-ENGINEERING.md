# Knowledge engineering

What the knowledge base holds, in what form, and how to write it. For human reviewers and writers. Not indexed.
Why the system can win: [MISSION.md](MISSION.md). How the parts run, including ingest and indexing: [ARCHITECTURE.md](ARCHITECTURE.md). What the agent is told about the knowledge base: [harness/AGENT.md](harness/AGENT.md). Plan and open gaps: [project/plan.md](project/plan.md).

Part A says what the knowledge is (sections 1-4). Part B gives the rules for writing it (sections 5-13). Part C is the workflow (section 14).

# Part A. The knowledge

## 1. The problem
- Source: the author's books, quizzes, field answers and 20+ years of operating vSphere.
- Most of this knowledge is tacit. It is judgment ("this reading is misleading when…"), not definitions.
- Three readers must use the same knowledge:
  - a small local model, which reads short retrieved passages and follows rules literally;
  - the harness, which needs exact, structured values it can look up and compute with;
  - a human expert, who must be able to review every fact and trace it to its source.
- No single format serves all three. Each kind of knowledge gets its own form. All forms live in one git repository, reviewed and versioned together.

### Principles
1. The AI is the reader; humans review. Content is facts, mechanisms, formulas and reasons; no text aimed at human motivation or narrative.
2. Mechanism before counter. A metric is a byproduct of the architecture; a metric file points back to the concepts it follows from.
3. Technology before object. A technology (CPU, memory, storage, network) works across Guest OS, VM, ESXi and cluster: master how it works, then apply it to each object (author, 2026-11-06).
4. Nuance is explicit. Same name with a different meaning, and the reverse, is stored as links and traps, not buried in prose.
5. Vantage points are never mixed. One object type and one layer per metric file; Guest OS is its own layer and folder.
6. Traceable to source. Every file records its source document and heading path.
7. Depth before breadth. One complete mechanism beats twenty shallow counter definitions.
8. Measured, not assumed. A structure change is kept only when the benchmark or the retrieval check improves.

### Limits
- Turning expert judgment into files is lossy; some tacit knowledge resists codifying.
- The model retrieves and recombines text. Structure improves its answers; it does not create understanding.
- Quality drifts without review. Coverage is partial on purpose: depth first.

## 2. Knowledge forms
| Form | Holds | Where |
|---|---|---|
| Structured prose | Mechanisms, reasons, edge cases | `knowledge/**/*.md` |
| Traps | Misconceptions and their correction | `## Traps` in each file |
| Metadata tags | Technology, pillar, product, object, layer, instance, metric class | `## Metadata` yaml at the end of each file |
| Links | Same name, same meaning, derived from, related | `same_name`, `same_meaning`, `internal_derive`, `related` |
| Folder hierarchy | Raw metrics by technology, derived content by object, VCF Operations as a derived layer, pillars across products | `knowledge/` |
| Catalog | Counter unit, rollup, statistics level; esxtop fields; thresholds; object model | `knowledge/catalog/*.yaml` → SQLite |
| Troubleshooting flows | The expert's order of checks and the branch at each step | `diagnosis/` files |
| Formulas and calculator | Conversions and identities (summation ms ↔ %, KB vs kb, esxtop state sums) | `harness/calc.py`, formulas in files |
| Images with text twins | The author's diagrams and charts | `images/` folders |
| Glossary | Controlled vocabulary, synonyms, confusable pairs, words to avoid | `knowledge/glossary.md` |
| Provenance | Source, review notes, corrections, author answers | metadata, `project/author-questions.md` |
| Rules as code | Architecture and writing rules | `project/tools/lint.py`, `project/tools/tags.yaml` |
| Executable expectations | What an expert answers to a hard question, and the trap a non-expert falls into | `benchmark/questions/` |

Reason for each form, and its readers:

| Form | Why this form | Read by |
|---|---|---|
| Structured prose | Reasons need prose; one fact per bullet keeps a mistake to one line and a chunk to one topic | Model, human |
| Traps | Experts know when a true number is read wrongly; the wrong conclusion, written in the user's words, retrieves its correction | Model, human, benchmark |
| Metadata tags | Lets one file be found from several perspectives and filters retrieval | Harness, website |
| Links | Encodes the expert's mental map: which facts must be read together | Harness, model |
| Folder hierarchy | One browsable tree in the order the author reviews | Human |
| Catalog | Exact values must not depend on retrieval luck or model memory | Harness tools |
| Troubleshooting flows | Small models skip steps; an ordered, executable form keeps them on the path | Harness (flow tool), model |
| Formulas and calculator | Arithmetic is where models slip; code does it exactly | Harness |
| Images with text twins | Diagrams carry expert insight; the text twin makes them usable by a text-only model | Model, human, vision model |
| Glossary | Wrong words produce wrong reasoning (VM vs Guest OS, storage vs disk, vCenter vs VCF Operations) | Model, human, lint |
| Provenance | Every fact must be traceable and challengeable | Human |
| Rules as code | A rule that a script checks cannot drift | Lint |
| Executable expectations | Shows that the knowledge changes answers | Benchmark |

## 3. Slices
The author's books describe metrics from three perspectives: technology, object, and operations management (pillar). A folder tree holds one; tags and links hold the others.
- Example: VM CPU Ready.
  - Technology: `vsphere/technology/cpu/metrics/virtual-motherboard/ready` (folder), `technology: cpu` (tag).
  - Object: `object: VirtualMachine` (tag), listed in `vsphere/object-types/vm/overview-what-to-monitor` (link), part of the VM Performance KPI.
  - Operations management: `pillar: performance` (tag), used by `operations-management/performance/performance-kpi-design` and the cluster KPI (links).
- Retrieval filters on any tag. The model follows any link. A website can show any slice without moving a file.

## 4. Traps and Level 400

### Levels
This is the one definition of the levels; the benchmark uses it (`benchmark/design.md`, section 3.2).

| Level | Can do | Example (VM CPU Ready) |
|---|---|---|
| 100 | Name the metric. | "Ready is a CPU metric." |
| 200 | Define it. | "Ready is time a vCPU waited for a physical thread." |
| 300 | Use it: read the value, apply a common threshold, follow a runbook. | "Ready above 5% is bad; add capacity." |
| 400 | Explain the mechanism, predict where the reading misleads, and say what to check instead. | "2% Ready on 10% Run delayed 20% of the work; 2% on 98% Run is fine. Ready includes limit time and the summation counter grows with vCPU count, so check Run, Max Limited and the per-vCPU %." |

- The knowledge base is written at Level 400. Levels 100-200 are assumed; generic models already reach Level 300 from public text.
- The trap separates 400 from 300. A Level 300 reader acts on the reading at face value. A Level 400 reader knows when the reading misleads.

### Trap definition
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

### Trap use
- Retrieval: a trap line holds the wrong conclusion in the user's own words, so a question that carries the misconception retrieves the file that corrects it.
- `same_name` links bring in the other object's meaning of the same label. They are the main guard against the first trap type.
- Benchmark: every multiple-choice question has a trap option named in `## Likely wrong answer`; the trap rate is reported per model. See `benchmark/design.md`.
- A trap needs a mechanism and a source, like any other fact.

# Part B. Writing rules

## 5. Layout

```text
knowledge/                           # what the model reads (indexed)
├── catalog/                         # structured data read by harness tools, not chunked as prose:
│                                    # vCenter counters, esxtop fields, thresholds, object model (YAML)
├── foundations/                     # vendor-neutral: units, sampling, accounting, perspectives, naming
├── glossary.md                      # one glossary: terms, synonyms, confusable pairs, words to avoid (all products)
├── operations-management/           # pillars of operations that cut across products and technologies
│   ├── performance/                 # KPI design; diagnosis/ for cross-technology flows (VM slow triage)
│   └── capacity/                    # capacity model, sizing; diagnosis/ for capacity decisions
├── vsphere/
│   ├── foundations/                 # vSphere-wide: provider/consumer, VM vs Guest OS, overhead,
│   │                                # resource controls (reservation, limit, shares), core rules
│   ├── technology/                  # raw metrics, by technology (book route: contention first, then consumption)
│   │   └── cpu/ gpu/ memory/ storage/ network/
│   │       ├── concepts/            # how it works
│   │       ├── metrics/<object>/    # one metric, one object type per file: virtual-motherboard/, host/,
│   │       │                        # cluster/, datastore/; comparisons/ for side-by-side groups
│   │       ├── configuration/       # what to set
│   │       ├── diagnosis/           # flows within this technology
│   │       └── images/
│   ├── object-types/                # multi-technology content, by object (book route)
│   │   └── vm/ esxi/ cluster/ ...   # concepts/, metrics/, configuration/, diagnosis/, images/
│   └── tools/                       # how each tool shows the counters
│       ├── esxtop/                  # panels, fields, units vs the vSphere Client
│       └── vsphere-client/          # vCenter statistics (levels, rollups, intervals), documentation guidance;
│                                    # screens/ for the screen library (release 1.1)
├── vcf-operations/                  # what VCF Operations computes or adds; links to the source files, never repeats them
│   ├── concepts/
│   ├── kpis/                        # KPIs with sub-metrics and colour bands (VCF Operations, vCommunity management pack)
│   ├── metrics/<object>/            # derived metrics: vm/, esxi/, cluster/
│   └── ui/                          # screen library for VCF Operations (release 1.1)
├── guest-os/                        # Windows, Linux: a separate layer, not Broadcom products, not part of the VM
│   └── <technology>/                # concepts/, metrics/, images/ (scope: guest-os, layer: guest-os)
├── _templates/                      # concept, metric, configuration, diagnosis, screen (not indexed)
└── raw-input/                       # source documents (not indexed)
```

- The author's book sees metrics from 3 perspectives: technology, pillar of operations, product. A folder tree holds one hierarchy; tags (`technology`, `pillar`, `product`, `object`) hold the others, and retrieval and the website browse by any of them.
- The folders follow the book's blend:
  - raw metrics follow the technology route: `vsphere/technology/<tech>/`;
  - multi-technology content follows the object route: `vsphere/object-types/<object>/`;
  - what VCF Operations computes: `vcf-operations/`;
  - pillars that cut across products (vSphere, vSAN, NSX, Guest OS): `operations-management/<pillar>/`.
- Placement rules, so a fact lives in one place:
  - A raw metric about one technology goes in `technology/`, even when it belongs to one object. VM CPU Ready: `vsphere/technology/cpu/metrics/virtual-motherboard/`.
  - `object-types/` holds what combines technologies for one object: vMotion, DRS, admission control, cluster operations. Each object folder gets an overview file that lists what to monitor, in priority order, linking the technology and VCF Operations files.
  - VCF Operations is a thin derived layer. A metric about a source object is documented once, at the source. `vcf-operations/` holds only what VCF Operations computes or adds (KPIs, derived metrics such as CPU Contention, 20-second peaks, disk space metrics), with `internal_derive` links to the source files. See `vcf-operations/concepts/vcf-operations-role`.
  - How a tool shows the counters (esxtop panels and fields, vCenter statistics levels and rollups, units per tool) goes in `vsphere/tools/<ui>/`. The metric's meaning stays in its metric file.
  - `operations-management/` holds only content that applies across products or technologies. Product-specific pillar content stays with the product's object and is linked from there.
  - Flows: one technology → `technology/<tech>/diagnosis/`; one object, several technologies → `object-types/<object>/diagnosis/`; across technologies or products (triage, capacity decisions) → `operations-management/<pillar>/diagnosis/`.
- Storage, not disk. Datastores, adapters, paths and vSAN are storage but not disks; a disk is one layer. vCenter keeps separate counter groups per layer (`virtualDisk`, `disk`, `datastore`, `storageAdapter`, `storagePath`), and the same label means a different scope in each. One word for folder, tag and glossary: `storage`.
- vCenter is the administrative tool (create VMs, configure switches). Capacity planning and performance troubleshooting are done in VCF Operations. The knowledge base never uses the two names interchangeably.
- Three foundations levels, different scope:
  - `knowledge/foundations/`: true across VCF 9 components and Guest OS.
  - `knowledge/operations-management/`: how a pillar uses metrics, across products.
  - `knowledge/vsphere/foundations/`: true only in vSphere.
- `metrics/<object>` folder names: `virtual-motherboard`, `host`, `cluster`, `datastore` under `vsphere/technology/`; `vm`, `esxi`, `cluster` under `vcf-operations/metrics/`. The `object` tag holds the vSphere managed object type name.
- A VM is a virtual motherboard, not a complete machine. Its raw metrics live in `metrics/virtual-motherboard/` (`object: VirtualMachine`, `layer: virtual-motherboard`). The folder name is in every file id, so the model reads it with every VM chunk.
- Guest OS knowledge (Windows, Linux) is a separate layer and not a Broadcom product. It lives in `knowledge/guest-os/<technology>/` with `scope: guest-os`, `layer: guest-os` and no VM object, even though VMware Tools stores some counters on the VM object. Boundary files comparing Guest OS and VM stay in `knowledge/vsphere/`. A VCF Operations KPI over Guest OS counters (Guest OS Performance) stays in `guest-os/` by this rule.
- Screen library (release 1.1): one file per screen type, in `vsphere/tools/<ui>/screens/` or `vcf-operations/ui/screens/`, with a screenshot, a full text twin, the metrics it shows (`metrics_shown`), UI and version (`ui`, `ui_version`). Template: `knowledge/_templates/screen.md`.
- Indexed: `knowledge/**/*.md`, except `_templates/` and `raw-input/`. How files are ingested: `ARCHITECTURE.md`, section Local LLM use.
- `project/tools/lint.py` enforces the folder and tag rules.

## 6. Structure rationale
- A generic AI fails on vSphere metrics in a known way: it knows the general meaning of a label and applies it where vSphere differs.
- Each structural choice blocks one failure:

| Choice | Failure it blocks |
|---|---|
| Concepts separate from metrics | Answering from a definition without the mechanism behind the value. |
| One object type per metric file | Mixing the VM, ESXi and cluster meanings of the same label. |
| `same_name` / `same_meaning` links | Treating two metrics as equal because the labels match, or as different because the labels differ. |
| Book-order folders plus tags | One hierarchy for review in the book's order; tags give the other perspectives (technology, pillar, product, object). |
| VCF Operations as its own folder | Taking a derived VCF Operations metric for a vCenter counter (Contention vs Latency). |
| Tool references in `tools/` | Reading esxtop, vCenter and VCF Operations values as the same thing. |
| `retriever_guide` | Retrieving a definition when the question asks what to check or what to set. |
| Small files, one fact per line | A retrieved chunk carrying unrelated facts; an error spreading beyond one line. |
| Metadata at the end, parsed separately | Audit text (status, corrections) polluting the embedded content. |
| Foundations at three levels | vSphere-only rules applied to other products, or general rules duplicated per product. |
| A `## Traps` section in every metric file | A true observation read to the wrong conclusion. See section 4. |

- Each format choice serves both readers:

| Choice | Machine benefit | Human benefit |
|---|---|---|
| Markdown, not HTML or JSON | Clean chunking by heading | Readable and reviewable on GitHub |
| One fact per bullet | Small, single-topic chunks | A mistake is one line to fix |
| Mechanism before metric name | The model learns why, not only what | Matches how an expert explains |
| Metadata at the end of the file | Parsed separately, never embedded as text | The body reads like a page |
| Wrong conclusion → correct reading | The misconception retrieves its correction | The trap is explicit and reviewable |
| Tables only when simple | Rows survive chunking | Scannable |
| Exact data in YAML, prose in markdown | Lookups are exact; prose stays short | Data is reviewable as a table |
| Mermaid plus text for diagrams | Text-only models read the steps | GitHub renders the chart |

- A file that is not tagged, linked and placed in the right folder is found only by its words. Lint checks tags and links for that reason. How the agent uses this structure: `harness/AGENT.md`, section 3.

## 7. retriever_guide
| Value | Question it answers | Folder | Template |
|---|---|---|---|
| how-it-works | How does it work? Why does the metric behave this way? | `concepts/`, `foundations/` | `concept.md` |
| metric-meaning | What does this number mean on this object? | `metrics/`, `kpis/`, `tools/` | `metric.md` |
| term-meaning | What does this term mean? | `knowledge/glossary.md` | - |
| what-to-set | What should be configured, and why? | `configuration/` | `configuration.md` |
| what-to-check | Something is wrong. What do I check, in what order? | `diagnosis/` | `diagnosis.md` |

## 8. Metadata (end of file)
Every knowledge file and every benchmark question ends with a `## Metadata` section holding one yaml block. No front matter at the top.

| Field | Meaning |
|---|---|
| `id` | Path without `knowledge/` and `.md`. |
| `retriever_guide` | See section 7. |
| `scope` | vendor-neutral (applies across VCF 9 components), operations-management, vsphere, vcf-operations or guest-os; matches the top folder. |
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

## 9. Thresholds
- A threshold has more parts than a number:

```text
threshold = (metric, object, instance reading, sample interval, time window) -> band values and source
```

- Sample interval: the same workload reads higher at 2 seconds (esxtop) than at 20 seconds, and higher at 20 seconds than at 5 minutes. A band set on 20-second peaks cannot be applied to a 5-minute chart. Example: VM Compressed + Swapped (5-minute samples) has a lower band than VM Memory Contention (20-second peaks) although it is the less serious signal.
- Instance reading: for a metric with instances (per vCPU, per disk), the worst instance is always at least the object value. The worst vCPU of a 64-vCPU VM can be far above the VM's normalized Ready. A band must say which reading it applies to, as "Peak CPU Ready among any vCPU" does.
- Where thresholds live:
  - colour bands (green, yellow, orange, red) in the tables of the KPI files (`vcf-operations/kpis/`, `guest-os/system/metrics/guest-os-performance`); the harness catalog reads them at start-up;
  - single thresholds (above X means Y) in `knowledge/catalog/thresholds.yaml`, each quoting its knowledge file so the two cannot drift (lint checks the quote).
- No invented thresholds: a threshold goes in only with a source (book, author, official documentation), quoted.
- The rule for the model is in `foundations/thresholds` (Interval rule, Instance rule). The catalog has `interval` and `instance` fields, filled only where a source states them.

## 10. Troubleshooting flows
- Location: section 5, Placement rules.
- One flow per file. Order: symptom, Mermaid flowchart, numbered steps (`## Checks, in order`), why this order, how to read the result, traps, metadata.
- The numbered steps are what the LLM follows. The Mermaid chart is a second, text-readable view; GitHub renders it for review.
- Each step states: the metric (exact name, matching the metric file title), the object, the threshold with its source, and the next step for each outcome.
  - Example: 1. Check VM CPU Ready (VirtualMachine). Above <threshold> (<source>) → step 2. Otherwise → step 4.
- Every metric or flow named in a step is linked in `internal_derive`, so retrieval brings in the files with the flow.
- Mermaid node text repeats the step number: `S1[1. VM CPU Ready above threshold?]`. Step numbers tie the chart to the text.
- Keep each flowchart to about 15 nodes. Split a larger flow into linked diagnosis files.
- draw.io files are not read by the LLM: the XML is mostly layout and style, and compressed files are unreadable.
  - Keep the `.drawio` file and an exported `.png` in the `images/` folder next to the flow as the editable source.
  - Link the `.png` under the flowchart and tag it in `images` (`image_type: diagram`).
  - The Mermaid chart and numbered steps are the content the LLM uses.

## 11. Writing rules
- One fact per bullet or table row. A mistake should sit on one line.
- One English word per concept. Knowledge terms: `knowledge/glossary.md`. Repository terms: `project/terms.md`.
- State mechanism and reason, not only the definition.
- Facts may come from the source, the author, official docs, or Claude's own knowledge. Record any fact not in the source document in `review_notes` with its section. No generic filler.
- No text aimed at human motivation.
- No AI-speak. Plain words, short sentences, the fact itself:
  - no filler words or stock phrases of generated text;
  - no praise, hedging or summary lines;
  - no adjective where a number or a mechanism can stand; name the thing.
  - The list of flagged phrases, each with its plain replacement: `project/tools/tags.yaml`, `avoid_ai_speak`. Lint flags them. The same rule applies to documents, commit messages and pull request text.
- One vSphere object type per metric file.
- Formulas as plain text. Diagrams as Mermaid plus a text explanation.
- Tables: short cells (about 12 words). At most 4 columns when cells hold text; number tables such as colour bands can have more. When rows carry long explanations, use one bullet block per row instead (bold item, one sub-bullet per field). GitHub renders a fixed-width column, so wide tables wrap every cell. Split a wide table in two, or move long explanations to bullets under the table.
- Every metric file ends its body with `## Traps`, written in the format of section 4.
- CPU scheduling language: a vCPU is a thread in the scheduler. It demands runtime. The kernel decides how much runtime it gets. Avoid "need", "want", "wish".
- Quotation marks only for verbatim text. Paraphrase without quotes, so the author can search the book for real quotes.

## 12. Images
- Keep the author's own diagrams and tables from the book. One image per concept, placed under the section it explains.
- Images live in the `images/` folder of the folder that uses them (for example `vsphere/technology/<tech>/images/`, `vcf-operations/kpis/images/`, `guest-os/<technology>/images/`).
- Alt text describes what the image shows. The text around it repeats the facts, so retrieval does not depend on the image.
- Every image has its own tags in the file's metadata `images` list (section 8). The validator fails on a missing or invalid entry.
- Every image file is linked from a knowledge file. The validator fails on an unlinked image: an unlinked image has no context for the AI.
- File names describe what the image shows. No length limit applies (GitHub, git and Markdown accept long names).
  - Pattern: `<object>-<metric or topic>-<what it shows>.png`, lowercase, hyphens. Example: `esxi-storage-adapter-read-write-latency-worst-vs-average-across-hosts.png`.
  - Chart type at the end when it helps: `-distribution`, `-scatter`, `-timeline`, `-table`, `-diagram`.
  - No bare numbers. Sample sizes (192 hosts, 3,385 VMs) go in the alt text and body, not the file name. A number stays only when it is the point, e.g. `62-5-percent`.
- Third-party images (vendor diagrams, documentation screenshots) are not copied. Link the source in `review_notes`.

## 13. Versions and sources
- Write from the current release: vSphere 9.1, VCF 9.1.1 (the Versions section of `CLAUDE.md` holds the current list).
- Before writing from a vendor document, check that it is the current version and read its revision date; record version and revision in `source.document`.
- A file written from an older version gets a `review_notes` line naming the newer version, and is re-checked before `status: reviewed`.
- `knowledge/raw-input/` is read-only.

# Part C. Workflow

## 14. From source to reviewed file
1. Extract: the book one Heading 3 at a time, then official documentation for the current release, checking the document revision each time. Files start as `status: draft`.
2. Structure: write each fact in the form that fits it (section 2); add tags, links and traps.
3. Ask: every conflict or gap becomes an author question in `project/author-questions.md`, with a verbatim search string. The author's answer is applied, marked in the file's review notes, and kept as a correction until the book is updated. Extraction continues; it does not wait for answers.
4. Check: `python3 project/tools/lint.py` must pass before merge (folders, tags, layers, links, images, quotes, tables, phrases). Unit tests check the tools.
5. Prove: the retrieval check confirms that the right files are found; the benchmark runs the questions against the whole system; every wrong answer is traced to knowledge, retrieval or model.
6. Review: the author reviews each file, answers `review_notes`, fixes errors and sets `status: reviewed`. Release content is final and curated: every file reviewed.
7. Update: when the source document is updated, move `corrections` into the normal text and clear them.
