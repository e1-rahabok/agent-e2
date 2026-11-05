# Knowledge engineering

How much expert knowledge this repository holds, and in what form. For human reviewers. Not indexed.
How the parts run together: `ARCHITECTURE.md`. Folder and writing rules: sections 8 to 17 below. Test design: `benchmark/test-design.md`.

## 1. The problem
- Source: the author's books, quizzes, field answers and 20+ years of operating vSphere.
- Most of this knowledge is tacit. It is judgment ("this reading is misleading when…"), not definitions.
- Three readers must use the same knowledge:
  - a small local model, which reads short retrieved passages and follows rules literally;
  - the harness, which needs exact, structured values it can look up and compute with;
  - a human expert, who must be able to review every fact and trace it to its source.
- No single format serves all three. Each kind of knowledge gets its own form. All forms live in one git repository, reviewed and versioned together.

## 2. Knowledge forms
| Form | Holds | Where | Size (2026-11-04) |
|---|---|---|---|
| Structured prose | Mechanisms, reasons, edge cases | `knowledge/**/*.md` | 203 files, 1,332 chunks |
| Traps | Misconceptions and their correction | `## Traps` in each file | 411 trap lines |
| Metadata tags | Technology, pillar, product, object, layer, instance, metric class | `## Metadata` yaml at the end of each file | every file |
| Links | Same name, same meaning, derived from, related | `same_name`, `same_meaning`, `internal_derive`, `related` | 32 / 4 / 162 / 725 |
| Folder hierarchy | Book order: raw metrics by technology, derived metrics by object, pillars across products | `knowledge/` | 4 top areas |
| Catalog | Counter unit, rollup, statistics level; esxtop fields; thresholds; object model | `knowledge/catalog/*.yaml` → SQLite | 131 chart counters, 133 API counters, 178 esxtop fields, 31 thresholds, 38 bands, 12 object types |
| Troubleshooting flows | The expert's order of checks and the branch at each step | `diagnosis/` files | 12 flows |
| Formulas and calculator | Conversions and identities (summation ms ↔ %, KB vs kb, esxtop state sums) | `harness/calc.py`, formulas in files | 7 functions |
| Images with text twins | The author's diagrams and charts | `images/` folders | 180 images |
| Glossary | Controlled vocabulary, synonyms, words to avoid | `knowledge/glossary.md` | 76 entries |
| Provenance | Source, review notes, corrections, author answers | metadata, `project/author-questions.md` | 48 author questions |
| Rules as code | Architecture and writing rules | `project/tools/lint.py`, `project/tools/tags.yaml` | runs before every merge |
| Executable expectations | What an expert answers to a hard question, and the trap a non-expert falls into | `benchmark/questions/` | 28 questions |

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

## 4. Machine and human readers
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

## 5. Thresholds
- Two sources today:
  - colour bands (green, yellow, orange, red) in the KPI files: `vsphere/object-types/vm/metrics/vm-performance`, `vsphere/object-types/cluster/metrics/cluster-performance`, `cluster-consumption`, `cluster-risk`, `cluster-sla-sli`, `guest-os/system/metrics/guest-os-performance`. The harness catalog reads these tables at start-up (38 bands);
  - single thresholds (above X means Y) in `knowledge/catalog/thresholds.yaml` (31 rows), each quoting its knowledge file so the two cannot drift (lint checks the quote).
- A threshold has more parts than a number:

```text
threshold = (metric, object, instance reading, sample interval, time window) -> band values and source
```

- Sample interval: the same workload reads higher at 2 seconds (esxtop) than at 20 seconds, and higher at 20 seconds than at 5 minutes. A band set on 20-second peaks cannot be applied to a 5-minute chart. Example: VM Compressed + Swapped (5-minute samples) has a lower band than VM Memory Contention (20-second peaks) although it is the less serious signal.
- Instance reading: for a metric with instances (per vCPU, per disk), the worst instance is always at least the object value. The worst vCPU of a 64-vCPU VM can be far above the VM's normalized Ready. A band must say which reading it applies to, as "Peak CPU Ready among any vCPU" does.
- The rule is written for the model in `foundations/thresholds` (Interval rule, Instance rule). The catalog has `interval` and `instance` fields; they are filled only where a source states them. The values for each band row are an open author question (Q048).

## 6. Intake and quality
1. Extract: the book one Heading 3 at a time, then official documentation for the current release (vSphere 9.1, VCF 9.1.1), checking the document revision each time.
2. Structure: write each fact in the form that fits it (section 2); add tags, links and traps.
3. Ask: every conflict or gap becomes an author question with a verbatim search string. The author's answer is applied, marked in the file's review notes, and kept as a correction until the book is updated.
4. Check: lint enforces the rules (folders, tags, layers, links, images, quotes, tables). Unit tests check the tools.
5. Prove: the benchmark runs the questions against the whole system, the harness-only retrieval test checks that the right files are found, and every wrong answer is traced to knowledge, retrieval or model.
6. Review: the author reviews every file before release; release content is final and curated.

## 7. Gaps
| Gap | Plan |
|---|---|
| Interval and instance reading of each threshold band | Author question Q048; catalog fields ready |
| Field heuristics not written in the books | Author questions; real tickets as benchmark questions |
| VCF Operations mechanisms (capacity engine, policies, alerts, super metrics) | Author's VCF Operations chapters; VCF Operations 9.1 metric reference |
| Screenshot library (what each screen shows and how to read it) | Release 1.1; template `knowledge/_templates/screen.md` |
| Export formats and their traps | Release 1.2 |

## 8. Layout

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
- `project/tools/lint.py` enforces the folder and tag rules.

## 9. Structure rationale
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

## 10. Traps and Level 400

### Levels
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
- The model is told to watch for same-name metrics and to answer with the mechanism, not the definition.
- Benchmark: every multiple-choice question has a trap option named in `## Likely wrong answer`; the trap rate is reported per model. See `benchmark/test-design.md`.
- A trap needs a mechanism and a source, like any other fact.

## 11. Troubleshooting flow diagrams
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

## 12. Indexing rules
- Index: `knowledge/**/*.md`.
- Do not index: `knowledge/_templates/`, `knowledge/raw-input/`, `benchmark/`, `project/`, `harness/`, `README.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `KNOWLEDGE-ENGINEERING.md`, `CONTRIBUTING.md`, `SECURITY.md`.
  - `benchmark/` holds answer keys. Indexing it invalidates the evaluation.
- Metadata is the last section of each file: `## Metadata` followed by one yaml block. Parse it as metadata, not as text to embed.
- Images live in the `images/` folder of the folder that uses them: `vsphere/technology/<tech>/images/`, `vsphere/object-types/<object>/images/`, `vsphere/foundations/images/`, `operations-management/<pillar>/images/`, `guest-os/<technology>/images/`. Each image link carries alt text; the body text states the same facts. Return the image link when a diagram answers the question.
- When a file is retrieved, also consider retrieving the ids in `related`, `internal_derive`, `same_name` and `same_meaning`.

## 13. retriever_guide
| Value | Question it answers | Folder | Template |
|---|---|---|---|
| how-it-works | How does it work? Why does the metric behave this way? | `concepts/`, `foundations/` | `concept.md` |
| metric-meaning | What does this number mean on this object? | `metrics/` | `metric.md` |
| term-meaning | What does this term mean? | `knowledge/glossary.md` | - |
| what-to-set | What should be configured, and why? | `configuration/` | `configuration.md` |
| what-to-check | Something is wrong. What do I check, in what order? | `diagnosis/` | `diagnosis.md` |

## 14. Metadata (end of file)
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

## 15. Writing rules
- One fact per bullet or table row. A mistake should sit on one line.
- One English word per concept. Knowledge terms: `knowledge/glossary.md`. Repository terms: `project/terms.md`.
- State mechanism and reason, not only the definition.
- Facts may come from the source, the author, official docs, or Claude's own knowledge. Record any fact not in the source document in `review_notes` with its section. No generic filler. No invented thresholds.
- No text aimed at human motivation.
- One vSphere object type per metric file.
- Formulas as plain text. Diagrams as Mermaid plus a text explanation.
- Tables: short cells (about 12 words). At most 4 columns when cells hold text; number tables such as colour bands can have more. When rows carry long explanations, use one bullet block per row instead (bold item, one sub-bullet per field). GitHub renders a fixed-width column, so wide tables wrap every cell. Split a wide table in two, or move long explanations to bullets under the table.
- Every metric file ends its body with `## Traps`, written in the format of section Traps and Level 400 above.
- CPU scheduling language: a vCPU is a thread in the scheduler. It demands runtime. The kernel decides how much runtime it gets. Avoid "need", "want", "wish".

## 16. Images
- Keep the author's own diagrams and tables from the book. One image per concept, placed under the section it explains.
- Alt text describes what the image shows. The text around it repeats the facts, so retrieval does not depend on the image.
- Every image has its own tags in the file's metadata `images` list (see Metadata). The validator fails on a missing or invalid entry.
- Every image file is linked from a knowledge file. The validator fails on an unlinked image: an unlinked image has no context for the AI.
- File names describe what the image shows. No length limit applies (GitHub, git and Markdown accept long names).
  - Pattern: `<object>-<metric or topic>-<what it shows>.png`, lowercase, hyphens. Example: `esxi-storage-adapter-read-write-latency-worst-vs-average-across-hosts.png`.
  - Chart type at the end when it helps: `-distribution`, `-scatter`, `-timeline`, `-table`, `-diagram`.
  - No bare numbers. Sample sizes (192 hosts, 3,385 VMs) go in the alt text and body, not the file name. A number stays only when it is the point, e.g. `62-5-percent`.
- Third-party images (vendor diagrams, documentation screenshots) are not copied. Link the source in `review_notes`.

## 17. QA workflow
1. AI extracts a section into files with `status: draft`.
   - Run `python3 project/tools/lint.py`. It must pass before merge.
2. Author reviews, answers `review_notes`, fixes errors.
3. Author sets `status: reviewed`.
4. When the source document is updated, move `corrections` into the normal text and clear them.
5. Run `benchmark/` questions with and without the knowledge base; record results in `benchmark/results/results.csv`.
