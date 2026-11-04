# Knowledge engineering

How much expert knowledge this repository holds, and in what form. For human reviewers. Not indexed.
How the parts run together: `ARCHITECTURE.md`. Folder and writing rules: `README.md`. Test design: `benchmark/test-design.md`.

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
| Rules as code | Architecture and writing rules | `tools/lint.py`, `tools/tags.yaml` | runs before every merge |
| Executable expectations | What an expert answers to a hard question, and the trap a non-expert falls into | `benchmark/cases/` | 28 cases |

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
5. Prove: the benchmark runs the golden cases against the whole system, the harness-only retrieval test checks that the right files are found, and every wrong answer is traced to knowledge, retrieval or model.
6. Review: the author reviews every file before release; release content is final and curated.

## 7. Gaps
| Gap | Plan |
|---|---|
| Interval and instance reading of each threshold band | Author question Q048; catalog fields ready |
| Field heuristics not written in the books | Author questions; real tickets as benchmark cases |
| VCF Operations mechanisms (capacity engine, policies, alerts, super metrics) | Author's VCF Operations chapters; VCF Operations 9.1 metric reference |
| Screenshot library (what each screen shows and how to read it) | Release 1.1; template `knowledge/_templates/screen.md` |
| Export formats and their traps | Release 1.2 |
