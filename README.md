# Isvara-2 — vSphere metrics knowledge base for AI

Level 400 knowledge of vSphere metrics, for retrieval by an AI assistant.
Primary reader: AI. Secondary reader: the author, for QA.

Counters are a byproduct of the architecture. Mechanisms and distinctions come first; counter files come last.

## Layout

```text
knowledge/
├── foundations/              # vendor-neutral: naming, terminology, units, sampling, thresholds
├── vsphere/
│   ├── foundations/          # provider/consumer, VM vs Guest OS, visibility layers,
│   │                         # kernel worlds, resource management, overhead, sources
│   ├── cpu/
│   │   ├── distinctions.md   # same-name traps for this resource
│   │   ├── architecture/
│   │   ├── resource-management/
│   │   ├── counters/<object>/  # one object per file: vcpu, vm, esxi, cluster, ...
│   │   └── interpretation/
│   ├── memory/  storage/  network/   # same pattern
│   ├── glossary/
│   └── troubleshooting/
├── _templates/               # concept, distinction, counter
└── raw-input/                # source documents (not indexed)
evaluation/                   # golden questions with answer keys (not indexed)
```

## Indexing rules
- Index: `knowledge/**/*.md`.
- Do not index: `knowledge/_templates/`, `knowledge/raw-input/`, `evaluation/`.
  - `evaluation/` holds answer keys. Indexing it invalidates the evaluation.
- Parse YAML front matter as metadata, not as text to embed.
- When a file is retrieved, also consider retrieving the ids in its `related` list.

## File types
| type | Purpose | Template |
|---|---|---|
| concept | A mechanism or mental model. Explains why metrics behave as they do. | `_templates/concept.md` |
| distinction | Same name, different meaning (or the reverse). One block per distinction. | `_templates/distinction.md` |
| counter | One counter, one object, one data source. | `_templates/counter.md` |

## Front matter
| Field | Meaning |
|---|---|
| `id` | Path without `knowledge/` and `.md`. Used in `related`. |
| `type` | concept, distinction, counter. |
| `scope` | vendor-neutral or vsphere. |
| `resources` | cpu, memory, storage, network. |
| `objects` | Vantage points covered: guest-os, vcpu, vm, esxi, cluster, datastore, ... |
| `related` | Ids to retrieve together. |
| `source.document` / `source.path` | Source document and heading path. For QA and future updates. |
| `corrections` | Facts from the author not yet in the uploaded source document. Remove once the document is updated. |
| `review_notes` | Open questions for the author. |
| `status` | draft (AI-extracted, not reviewed) or reviewed (author approved). |

- Inside a file, `src:` on a block gives the heading path relative to `source.path`.
- `[author-correction YYYY-MM-DD]` marks a fact that differs from the uploaded source document.

## Writing rules
- One fact per bullet or table row. A mistake should sit on one line.
- State mechanism and reason, not only the definition.
- Only facts from the source or the author. No generic filler. No invented thresholds.
- No text aimed at human motivation.
- Never mix vantage points in one counter file.
- Formulas as plain text. Diagrams as Mermaid plus a text explanation.
- CPU scheduling language: a vCPU is a thread in the scheduler. It demands runtime. The kernel decides how much runtime it gets. Avoid "need", "want", "wish".

## QA workflow
1. AI extracts a section into files with `status: draft`.
2. Author reviews, answers `review_notes`, fixes errors.
3. Author sets `status: reviewed`.
4. When the source document is updated, move `corrections` into the normal text and clear them.
5. Run `evaluation/` golden questions with and without the knowledge base; record results.
