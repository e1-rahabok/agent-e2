# Knowledge engineering

This document describes what Agent E2 knows, how each kind of knowledge reaches the model, and why it is shaped that way. It is the design overview for reviewers; the detailed rules for writers are modules in [project/knowledge-rules/](project/knowledge-rules/). Not indexed.
Related reading: why the system can win is in [MISSION.md](MISSION.md); how the parts run, including ingest and indexing, in [ARCHITECTURE.md](ARCHITECTURE.md); what the agent is told about the knowledge base, in [harness/AGENT.md](harness/AGENT.md); the plan and open gaps, in [project/plan.md](project/plan.md).

## From expertise to knowledge the model reads

```mermaid
flowchart LR
  subgraph Sources["1. Sources"]
    B[Author's books, spreadsheets, diagrams]
    D[Documentation: manuals, white papers, expert answers]
    E[Environment: screenshots, API, GUI, lab tests]
  end
  SN["2. Source note per topic, claims tied to evidence (project/sources/)"]
  subgraph Codify["3. Codify: one form per kind, one home per fact"]
    P[Markdown: mechanisms, misconceptions, flows]
    Y[Catalog YAML: counters, thresholds, object model]
    L[Tags and links: the expert's map]
  end
  subgraph Check["4. Check"]
    LI[Lint: every merge]
    BM[Retrieval check and benchmark]
    AQ[Author review: status reviewed, gate of release 1.0]
  end
  subgraph Use["5. Used by the AI"]
    R[Agent and harness: five paths to the model]
    A[Model: read, apply, answer with citations]
  end
  B --> SN
  D --> SN
  E --> SN
  SN --> Codify
  Codify --> Check
  Check -->|lint passes, drafts carry their status| R
  R --> A
  A -->|wrong answers traced to knowledge, retrieval or model| SN
```

- Experts hold judgment, not definitions. Each kind of judgment gets its own form: prose for reasons, misconception lines for wrong readings, YAML for exact numbers, and numbered steps for the order of checks.
- Tags and links carry the expert's mental map: which files must be read together.
- Every file passes lint before it is merged. Draft files are served before the author has reviewed them, with their status in the reading set; release 1.0 ships only reviewed files ([project/plan.md](project/plan.md), M6). Section 7 says how review progress is tracked.
- The loop closes: every wrong answer is traced back to a missing fact, a retrieval miss or a model error.

| Read | For |
|---|---|
| This file | The design: the problem, where knowledge lives, forms, Level 400 and misconceptions, why the structure is so, workflow, releases and health |
| [placement.md](project/knowledge-rules/placement.md) | Which folder a file goes in; the `knowledge/` tree |
| [flows.md](project/knowledge-rules/flows.md) | Health checks, troubleshooting flows, decision trees: vocabulary, order, step format |
| [metadata.md](project/knowledge-rules/metadata.md) | `retriever_guide` values, every metadata field, the dimensions not to mix |
| [thresholds.md](project/knowledge-rules/thresholds.md) | What a threshold is, the catalog files, one place per number |
| [writing.md](project/knowledge-rules/writing.md) | Writing rules, the author's editing checklist, format choices, images, versions |
| [vocabulary.md](project/knowledge-rules/vocabulary.md) | Words to avoid, each with its replacement and reason |
| [terminology.md](project/knowledge-rules/terminology.md) | Glossary entries, confusable pairs, up-front misconceptions, product labels, budget |
| [project/sources/README.md](project/sources/README.md) | Source notes and their evidence |

## 1. The problem
- Source: the author's books, spreadsheets and field answers, and 20+ years of operating vSphere.
- Most of this knowledge is tacit. It is judgment ("this reading is misleading when…"), not definitions.
- Three readers must use the same knowledge:
  - a small local model, which reads short retrieved passages and follows rules literally;
  - the harness, which needs exact, structured values it can look up and compute with;
  - a human expert, who must be able to review every fact and trace it to its source.
- No single format serves all three, so each kind of knowledge gets its own form. All the forms live in one git repository and are reviewed and versioned together.

### Principles
1. The AI is the reader; humans review. Content is facts, mechanisms, formulas and reasons, with no text aimed at human motivation and no narrative.
2. Mechanism before counter. A metric is a byproduct of the architecture, so a metric file points back to the concepts it follows from.
3. Technology before object. A technology (CPU, memory, storage, network) works across Guest OS, VM, ESXi and cluster. Master how it works first, then apply it to each object.
4. Nuance is explicit. The same name with a different meaning, and the reverse, is stored as links and misconception lines instead of being buried in prose.
5. Vantage points are never mixed: one object type and one layer per metric file (exceptions in section 5). The Guest OS is its own layer and folder.
6. Traceable to source. Every file records its source and heading path. A file digested from a source note names the note, and the note holds the evidence (section 6).
7. Depth before breadth. One complete mechanism beats twenty shallow counter definitions.
8. Measured, not assumed. A structure change is kept only when the retrieval check improves, or holds while the content becomes more correct; the benchmark proves the release ([`benchmark/retrieval-check.md`](benchmark/retrieval-check.md)).

### Limits
- Turning expert judgment into files is lossy, and some tacit knowledge resists codifying.
- The model retrieves and recombines text. Structure improves its answers; it does not create understanding.
- Quality drifts without review. Coverage is partial on purpose, because depth comes first.

## 2. Where the knowledge lives

- Agent E2 combines two bodies of knowledge in every answer, the same two the author carries as a consultant:
  - the method, the SP5 Framework: how to operate VCF, in VCF terms and examples (`sp5-framework/`);
  - the product, VCF 9.x: what each component is and does (`vsphere/`, `vcf-operations/`), and the Guest OS above the VM (`guest-os/`).
- Sources are stated once, here. The knowledge is written from [`project/sources/`](project/sources) and from https://isvara.io, which holds the latest copy of the author's books, spreadsheets and other material. The knowledge base is a superset of them: it adds vendor documents, mechanisms and corrections. A knowledge file therefore never names the author's books or spreadsheets. Its `source.document` is `Knowledge base`, plus any vendor document with its version, which can go stale. Its `source.path` may name a source note (section 6). `corrections` record differences from vendor documents only.
- Scope is VCF only, with nothing about competitor products. Folder rules: [`project/knowledge-rules/placement.md`](project/knowledge-rules/placement.md).
- Agent E2 is purpose-built, so its domain knowledge is not only in what search returns. Up-front text, code and the agent's instructions carry VMware knowledge too. All of it is deployed to the site, and the author reviews all of it.
- The home of a fact is decided by how it must reach the model, not by its subject. There are five paths, each for a failure the others cannot prevent:

```mermaid
flowchart LR
  Q[Question and screenshots] --> AG[Agent: case and reading plan]
  subgraph KB["knowledge/: one home per fact"]
    MD[Markdown files]
    CAT[Catalog YAML]
    UPL[Misconception lines marked up_front]
    GL[Glossary]
  end
  MD -->|1 retrieved: search and links| RS[Reading set]
  CAT -->|2 looked up exactly: SQLite| EX[Exact values]
  UPL -->|3 given up front: upfront_knowledge.py| UP[Up-front block]
  GL -->|3| UP
  CODE["Code: arithmetic_calculator.py, answer_check.py, user_terms.py"] -->|4 executed| EX
  RULES["Instructions: answer_modes.py, expert_agent.py"] -->|5 every answer| M
  AG --> RS
  AG --> EX
  RS --> M[Model]
  EX --> M
  UP --> M
  M --> ANS[Answer with file citations]
```

| Path | Holds | Home | Why this path |
|---|---|---|---|
| Retrieved when a question needs it | Mechanisms, metrics, misconceptions, flows | `knowledge/**/*.md` (indexed) | About 320K tokens (November 2026; [`project/tools/knowledge_stats.py`](project/tools/knowledge_stats.py) prints the current figure), too large to send with every question |
| Looked up exactly | Units, rollups, statistics levels, thresholds, user terms | `knowledge/catalog/*.yaml` (loaded into SQLite) | An exact value must not depend on ranking or on the model's memory |
| Given up front, every question | Misconceptions with the widest reach, confusable pairs | Built by [`harness/upfront_knowledge.py`](harness/upfront_knowledge.py) from the `## Misconceptions` lines marked `up_front` in their files and from [`knowledge/glossary.md`](knowledge/glossary.md) | A confident wrong belief is never looked up, so the correction must be in place before the model reasons |
| Executed as code | Arithmetic identities, answer checks, user-word mapping; capacity plans and flow branches (code exists, not yet called by the agent: [`harness/AGENT.md`](harness/AGENT.md), section 4.3) | [`harness/arithmetic_calculator.py`](harness/arithmetic_calculator.py), `answer_check.py`, `user_terms.py`; `capacity_calculator.py`, `flow_executor.py` | Small models slip on arithmetic and skip steps; code does not |
| Agent instructions | Knowledge base first, same-name check, a file for each claim, threshold only with its source, Unsure | [`harness/answer_modes.py`](harness/answer_modes.py) (prompts), [`harness/expert_agent.py`](harness/expert_agent.py) (answer rules) | Conduct for every answer, not a fact about one metric |

- One home per fact. The mechanism lives in `knowledge/`; code and up-front text hold only what they need to act, and point to the file. For example, `arithmetic_calculator.py` converts a summation counter from ms to %, but why Ready is a summation counter is explained in the Ready file. Each up-front misconception ends with `See <id>`.
- Up-front text reaches every answer, while a retrieved file reaches only the answers that find it. A wrong up-front line or prompt rule therefore costs more than a wrong metric file, and it is reviewed first.
- All the domain knowledge the author reviews lives in `knowledge/`, whatever its path to the model. Every knowledge file is indexed, and the up-front block is built from marked lines of those files, so no fact has a second, unindexed copy. `knowledge/` is not the same as chunked prose: the catalog is loaded, not chunked.
- Not deployed: `project/` (lint, allowed tags, moved ids, source notes) and `benchmark/`. They check the knowledge and hold nothing the agent reads.
- Guard: lint rejects hidden text and instruction-like phrases in every knowledge file and benchmark prompt (`injection_patterns` in [`project/tools/rules_check_values.yaml`](project/tools/rules_check_values.yaml)). Knowledge reaches the model as trusted text, so nothing in it may read as an instruction.

### Example: VM CPU Ready on every path
| Path | Where | What it holds |
|---|---|---|
| Retrieved | [`ready`](knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/ready.md) | The mechanism, `internal_derive` to `vcpu-states` and `provider-consumer`, and misconception lines such as "Ready 2% is always low" → read it against Run |
| Looked up | `vcenter-counters.yaml`, row `cpu.ready`; `thresholds-performance.yaml`, row "Peak CPU Ready among any vCPU (%)" | Unit, rollup, statistics level and page; the 20-second colour bands, with `kb` pointing to the file that explains them |
| Up front | The `provider-consumer` line marked `up_front` | "ESXi CPU Ready is high, so the host waits for CPU" → Ready is a consumer metric |
| Glossary and term map | Entries Readiness and Max Limited; the term-map row for "steal time" | The user's words lead to the Ready file |
| Code | `arithmetic_calculator.summation_to_percent(ms, interval_seconds, vcpus)` | The ms to % conversion, done exactly |
| Instructions | Threshold only with its source | The model quotes the catalog row, not a number from memory |
| Proof | Question 0364 ([`L4-121`](benchmark/questions/L4-121-ready-read-against-run.md)), `knowledge_main: ready` | Option E is the misconception (type `threshold-transplanted`): the higher Readiness is not the worse VM |

## 3. Knowledge forms
| Form | Holds | Home | Why this form |
|---|---|---|---|
| Structured prose | Mechanisms, reasons, edge cases | `knowledge/**/*.md` | Reasons need prose, and one fact per bullet keeps a mistake to one line |
| Misconceptions | Wrong readings and their correction | `## Misconceptions` in each file | The wrong conclusion, in the user's words, retrieves its correction |
| Metadata tags | Kind of file (`retriever_guide`), scope, technology, pillar, product, object, layer, instance, metric class | `## Metadata` yaml ([metadata.md](project/knowledge-rules/metadata.md)) | One file is found from several perspectives; tags filter retrieval |
| Links | Same name, same meaning, derived from, related | `same_name`, `same_meaning`, `internal_derive`, `related` | The expert's mental map: which facts are read together |
| Folder hierarchy | The method (SP5 Framework) and the product (VCF 9.x) kept apart; inside the product, metrics by technology and KPIs by object | `knowledge/` | One tree, in the order the author reviews; links and tags give the other views |
| Catalog | Units, rollups, statistics levels, esxtop fields, thresholds, object model | `knowledge/catalog/*.yaml` → SQLite | Exact values must not depend on retrieval luck |
| Flows | Order of checks: health check, troubleshooting, decision tree | Files with `retriever_guide` health-check, troubleshooting or decision-tree | Small models skip steps. Today the reading plan puts the flow first and the model follows its steps; executable steps, where code takes the branch, are still to build (Q166) |
| Formulas and calculator | Conversions and identities (summation ms ↔ %, KB vs kb) | [`harness/arithmetic_calculator.py`](harness/arithmetic_calculator.py), formulas in files | Arithmetic is where models slip |
| Images with text twins | The author's diagrams and charts | `images/` folders | Search reads words, not pixels: the text twin lets the image be found, and it costs fewer tokens than the image |
| Terminology | Vocabulary, confusable pairs | [`knowledge/glossary.md`](knowledge/glossary.md) | Wrong words produce wrong reasoning (Usage vs Utilization, KPI vs SLA) |
| Provenance | Source and version, what is still to check, status | metadata; evidence in the source note | Every fact can be traced and challenged |
| Rules as code | Architecture and writing rules (project, not deployed) | [`project/tools/rules_check.py`](project/tools/rules_check.py), `rules_check_values.yaml` | A rule that a script checks cannot drift |
| Executable expectations | Expert answers and the misconception a non-expert holds | [`benchmark/questions/`](benchmark/questions) | Shows that the knowledge changes answers |

### What the model sees of a file

```mermaid
flowchart LR
  subgraph F["One knowledge file"]
    T["# Title"]
    S["## Sections: Meaning, Formula, Reason ..."]
    MC["## Misconceptions"]
    MM[Mermaid chart]
    MD["## Metadata (yaml, last)"]
  end
  T --> CH["Chunks: one per ## section, each prefixed with Title (id) > Heading"]
  S --> CH
  MC --> CH
  CH --> SE[Search]
  MM -.->|removed: the numbered steps carry it| X[Not indexed]
  MD -->|tags: filters| SE
  MD -->|links| PL[Reading plan]
  MD -->|up_front| PR[Up-front block]
  MD -.->|status, source, review_notes, corrections| RV[Review only, never embedded]
```

- A `##` section is the unit of retrieval. A heading names its topic in words a question uses, because the title and heading go in front of every chunk ([`harness/knowledge_loader.py`](harness/knowledge_loader.py)).
- A file link `` [`id`](path.md) `` reaches the model as the id alone; the path is for reviewers on GitHub.
- Section names come from the templates in [`project/templates/`](project/templates) (metric: Meaning, Formula, Includes / excludes, Reason), so the same question finds the same kind of section in every file.

## 4. Misconceptions and Level 400

### Levels
This is the one definition of the levels, and the benchmark uses it ([`benchmark/design.md`](benchmark/design.md), section 3.2).

| Level | Can do | Example (VM CPU Ready) |
|---|---|---|
| 100 | Name the metric. | "Ready is a CPU metric." |
| 200 | Define it. | "Ready is time a vCPU waited for a physical thread." |
| 300 | Use it: read the value, apply a common threshold, follow a runbook. | "Ready above 5% is bad; add capacity." |
| 400 | Explain the mechanism, predict where the reading misleads, and say what to check instead. | "2% Ready on 10% Run delayed 20% of the work; 2% on 98% Run is fine. Ready includes limit time and the summation counter grows with vCPU count, so check Run, Max Limited and the per-vCPU %." |

- The knowledge base is written at Level 400. Levels 100-200 are assumed, and generic models already reach Level 300 from public text.
- What separates 400 from 300 is knowing where a correct number is read wrongly. A Level 300 reader acts on the reading at face value. A Level 400 reader knows the mechanism, and so knows when the reading misleads.

### What a misconception is
- A misconception is a wrong conclusion drawn from a true observation or from a public rule of thumb. The number is right; the reading is wrong.
- It is held with confidence at Level 300: an experienced administrator, a frontier model trained on public text, or the vendor documentation states it.
- It has a mechanism: the knowledge base says why the conclusion fails and what to check instead. A misconception without a mechanism is an opinion, and it does not go in.
- Agent E2 does not set misconceptions for other models to fall into. It beats them by knowing the mechanism behind the number. A misconception is only where that depth becomes visible, because a model that has only Level 300 text repeats it.
- The word is misconception, as in the author's books, and not "trap". In IT infrastructure a trap is an event notification (SNMP trap, a log message an alert traps), and in CPU virtualization it is a hand-over to the hypervisor (trap-and-emulate). The knowledge base uses both meanings, so a third would collide in search.
- Format: one per line, in the `## Misconceptions` section at the end of the file body:

```text
- "<the wrong conclusion, in the words someone would use>" → <the correct reading, the reason, and what to check instead>.
```

- Example: "Swap Consumed = Swap Out - Swap In" → no. Swap Out and Swap In are cumulative totals; Swap Consumed is what sits in swap now, like VM Swapped.

### One home, two paths to the model
- Home: `## Misconceptions` in the file, in the user's own words, next to the mechanism. A question that carries the belief brings in its correction through the reading set.
- Up front: the dozen with the widest reach are marked in their file (metadata `up_front`: the wrong belief, as quoted in the line). [`harness/upfront_knowledge.py`](harness/upfront_knowledge.py) collects the marked lines into the up-front block, so the correction is in place before the model reasons, even when the question does not name the file. There is one copy: the author edits the line in its file.
- Not a confusable pair: two real terms swapped (Core vs Thread Utilization) is a vocabulary error, and it is kept in the glossary. A misconception is a wrong belief about how something works.

### Misconception types
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
| Label read as model | The label names a different model than the one the product computes | "Total Capacity (GHz) is the host's CPU capacity" |

### Product label and better model (Q208)
- The product shows a label and computes it with a simple model. The label is reality: the operator reads it on the screen, types it into a question, and acts on what it seems to say. The product is not wrong; it is simpler, because its designer had to fit one number on a summary screen with no one there to explain it. Agent E2 is the one who explains, so it holds both the label and the better model, and never trades one for the other.

| Layer | Example: Total Capacity (CPU) | Example: CPU Usage (MHz) |
|---|---|---|
| Product label, as the UI shows it | Total Capacity, GHz | Usage (MHz) |
| What the product computes | cores × base frequency | productive cycles, scaled by frequency |
| The decision the label invites (Level 300) | "this is how much the host can hold" | "this is how busy the CPU is" |
| The better model and its name | Total Base Capacity (GHz): GHz at base clock; space for vCPUs is counted in physical threads | CPU Throughput: completed work, not busy time |

- The test for a label: the label invites a decision that its computed model does not support, and the knowledge base holds the better model. A label that names what it computes stays a plain metric.
- Never reword a label: quote it as the product shows it, then correct the model behind it. Tone: "the product uses a simpler model", never "the product is wrong".
- Homes: the glossary entry named by the label (Product label, Invites, Better name, File); the metric file keeps the mechanism and a misconception line; a term-map row matches the user's words and carries no note. The list of labels is the set of glossary entries with a `Product label:` line.
- Rules for better names, the five-step teaching order and where each part lives: [`terminology.md`](project/knowledge-rules/terminology.md), Product label entry.

### Use
- Retrieval: a misconception line holds the wrong conclusion in the user's own words, so a question that carries it retrieves the file that corrects it.
- `same_name` links bring in the other object's meaning of the same label. They are the main guard against the first type.
- Benchmark: every multiple-choice question names its misconception option in metadata `misconception`, and its wording in `## Explanation`. The misconception rate, the share of answers that pick it, shows whether a model holds the Level 300 belief.
- A misconception needs a mechanism and a source, like any other fact.

## 5. Structure rationale
- A generic AI fails on vSphere metrics in a known way: it knows the general meaning of a label and applies it where vSphere differs.
- Each structural choice blocks one failure:

| Choice | Failure it blocks |
|---|---|
| Concepts separate from metrics | Answering from a definition without the mechanism behind the value. |
| One object type per metric file | Mixing the VM, ESXi and cluster meanings of the same label. |
| `same_name` / `same_meaning` links | Treating two metrics as equal because the labels match, or as different because the labels differ. |
| One slice in folders, the others in tags and links | A file found from one perspective only. The folder holds technology or object; tags hold pillar, product and object; links hold the rest ([placement.md](project/knowledge-rules/placement.md), Slices). |
| Derived metrics beside their source metrics | Taking a derived VCF Operations metric for a vCenter counter (Contention vs Latency): both sit in the same folder, linked by `same_name` or `internal_derive`. |
| Tool references in `tools/` | Reading esxtop, vCenter and VCF Operations values as the same thing. |
| `retriever_guide` | Retrieving a definition when the question asks what to check or what to set. |
| One topic per file, one fact per bullet, one chunk per `##` section | A retrieved chunk carrying unrelated facts; an error spreading beyond one line. |
| Metadata at the end, parsed separately | Audit text (status, corrections) polluting the embedded content. |
| Method apart from product (SP5 Framework vs vSphere and VCF Operations) | A design rule mistaken for product behaviour, or a product limit mistaken for a rule of the method. |
| A `## Misconceptions` section in every metric file | A true observation read to the wrong conclusion. See section 4. |

- Files are a topic, not a page count: the median is about 600 words, and a concept with many parts (memory tiering, overhead) runs to about 2,800. Size is held by the section, the unit of retrieval, not by the file.
- Two kinds of file carry two object types, on purpose: `comparisons/` files, which set objects side by side, and [`cluster/metrics/availability`](knowledge/vsphere/object-types/cluster/metrics/availability.md), which keeps its ESXi part until the availability model after 1.0 ([project/plan.md](project/plan.md), M1).
- A file that is not tagged, linked and placed in the right folder is found only by its words, which is why lint checks tags and links. How the agent plans with this structure: [`harness/AGENT.md`](harness/AGENT.md), sections 4.2 and 6.

## 6. Workflow: from source to reviewed file

```mermaid
flowchart LR
  subgraph In["Sources"]
    BK[Author's books, spreadsheets, diagrams]
    DOC[Documentation]
    ENV[Environment]
  end
  ENV --> EV["evidence/ files: screenshots, API output, lab results"]
  BK --> SN
  DOC --> SN
  EV --> SN
  SN["Source note: one topic, a few pages, vendor and measured claims tagged E1, E2"] --> DG["Digest: each fact gets one home file"]
  DG --> HOME["Home file: the fact, source.path names the note"]
  DG --> LINK[Other files: a link to the home, no copy]
  HOME --> CK[Lint, retrieval check, author review]
  LINK --> CK
```

1. Gather. Most of the knowledge (over 80%) comes from the author's books, spreadsheets and diagrams. The rest comes from documentation (manuals, white papers, blogs, expert answers) and from the environment (screenshots, live instances through the API or GUI, lab tests). For a vendor document, use the current version and read its revision date.
2. Write the source note. The author and Claude write one Markdown note per topic, a few pages long, in [`project/sources/`](project/sources). It carries its release and date and an `## Evidence` section. Each claim about vendor behaviour, and each measured number, is tagged with its evidence (`[E1]`). The author's own judgment needs no tag: it is the knowledge base's own source. Format: [project/sources/README.md](project/sources/README.md).
   - Evidence is primary: a vendor document with version, revision and page; a screenshot or API output kept in [`project/sources/evidence/`](project/sources/evidence) with its build; a lab test with its setup. A summary written by a model is not evidence, the note included.
3. Digest. Claude reads the note and proposes which knowledge files and folders to change. Before writing, each fact in the note gets one home file; every other file that needs it gets a link, not a copy. This is where contradictions start: the 2026-11-15 review found 27, mostly answers applied to one file and not to its neighbours ([project/review-2026-11-15.md](project/review-2026-11-15.md)).
   - Write each fact in the form that fits it (section 3), and add tags, links and misconceptions.
   - The home file's `source.path` names the note and heading: `project/sources/<note>.md > <heading>`. Lint checks that the note and heading exist and that the note's evidence tags resolve. [`project/tools/source_trace.py`](project/tools/source_trace.py) lists which files each note feeds, from the metadata, so the trace is never kept by hand. When a note changes, those files are rechecked.
   - Files start as `status: draft`.
4. Ask. Every conflict or gap becomes an author question in [`project/author-questions.md`](project/author-questions.md), with a verbatim search string. The answer is applied to the file and the review note is deleted. Extraction continues meanwhile; it does not wait for answers.
5. Check. `python3 project/tools/rules_check.py` must pass before merge (folders, tags, layers, links, images, quotes, tables, phrases, source notes). Unit tests check the tools.
6. Prove. The retrieval check confirms that the right files are found, the benchmark runs the questions against the whole system, and every wrong answer is traced to knowledge, retrieval or model.
7. Review. The author reviews each file, answers `review_notes`, fixes errors and sets `status: reviewed`. Release content is final and curated: every file is reviewed.

## 7. Releases and health

### Releases
- Coverage is vSphere 9.x and VCF 9.x; knowledge of older releases is after 1.0 ([project/plan.md](project/plan.md), After 1.0). The current releases are listed in [`CLAUDE.md`](CLAUDE.md), section Versions.
- A fact that holds only from a release says so in its text ("since VCF Operations 9.1.1"), because the model reads text and metadata is not embedded.
- When Broadcom ships a release:
  1. Read the release notes and the new revision of each vendor document named in `source.document`.
  2. Rewrite each changed fact in its home file and update the version in `source.document`; the files that link to it follow without edits.
  3. When the vendor fixes a document, move the matching `corrections` into the text and clear them.
  4. When a source note is about the changed behaviour, update its release line and evidence first; [`source_trace.py`](project/tools/source_trace.py) lists the files to recheck.
  5. Run the retrieval check; the benchmark questions that cite a changed file are rechecked.

### Health
[`project/tools/knowledge_stats.py`](project/tools/knowledge_stats.py) prints the numbers; [project/plan.md](project/plan.md) records them at each review, so this file holds no figure that goes stale.

| Number | Why it matters |
|---|---|
| Reviewed files | Release 1.0 needs all of them (M6) |
| Open review notes | Each is a fact still to check |
| Corrections to vendor documents | Each waits for a vendor fix |
| Up-front lines | Each reaches every answer, so it is reviewed first |
| Files no question names | Knowledge the benchmark does not prove |
| Files no other file links to | Found only by their words |
| Source notes cited by no knowledge file | Evidence with no trace to the knowledge |

- Contradictions are found by review, not by a script: the question bank audit and the knowledge review list them ([project/plan.md](project/plan.md), M1). The digest step (section 6, step 3) prevents new ones.
