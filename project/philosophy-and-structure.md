# Philosophy and structure

Not indexed. Explains design decisions for whoever (AI or human) maintains the repository.
Conventions (layout, metadata, writing rules) are in the root `README.md`.

## Purpose
- Give an AI assistant Level 400 understanding of vSphere metrics.
- Target: the cases where a generic AI answers confidently and wrongly, because the general meaning of a metric does not hold in vSphere.
- Most documentation-based AI systems become metric dictionaries. They retrieve a definition but cannot explain why a value behaves as it does.

## Principles
1. **AI is the reader. Humans only review.**
   - Content is facts, mechanisms, formulas and reasons.
   - No text aimed at human motivation, narrative or the author's voice.
   - Format still supports human QA: one fact per line, source path per file, flagged corrections, review status.
2. **Mechanism before counter.**
   - Metrics are a byproduct of the architecture. A metric file points back to the concepts it follows from.
3. **Nuance is captured explicitly.**
   - Same name, different meaning (and the reverse) is stored as distinction blocks, not buried in prose.
4. **Vantage points are never mixed.**
   - A metric file covers one object type (VM, ESXi, cluster, datastore, ...) and one layer. vCPU is an instance, not an object. Guest OS is a layer with its own folder.
5. **General vs vSphere-specific.**
   - `knowledge/foundations/`: applies across VCF 9 components (naming, units, sampling, thresholds).
   - `knowledge/vsphere/foundations/`: true only in vSphere (virtualization mechanisms). Different scope; never merged.
6. **Traceable to source.**
   - Every file records the source document and heading path. Needed for QA and for updating when the source changes.
7. **Measured, not assumed.**
   - Golden cases in `benchmark/` test answers with and without the knowledge base.

## Structure decisions
| Decision | Reason |
|---|---|
| `knowledge/foundations/` at top level | Vendor-neutral content also applies to NSX, vSAN and other products. |
| `knowledge/vsphere/foundations/` | Cross-resource vSphere mechanisms (provider/consumer, visibility, resource management) do not belong to one resource. |
| Technology first, then concepts / metrics / configuration / diagnosis | Book raw metrics follow technology. The four subfolders match the four question types in `retriever_guide`. |
| `metrics/<object-folder>/` | One vSphere object type per file. Same label on another object is a different file, linked via `same_name`. Different labels with the same meaning are linked via `same_meaning`. |
| No `distinctions.md` | Same-name traps live in the metric files they belong to. Groups of metrics live in `metrics/comparisons/`. |
| Tags for pillar, product, object | Folders give one hierarchy. Tags let the AI slice by the other two angles of the book. |
| `knowledge/glossary.md` at top level | One glossary for all products. Allowed tag values are machine settings and live in `tools/tags.yaml`. |
| `vsphere/object-types/` (was `resource-management/`, split 2026-11-04) | Reservation, limit and shares in `vsphere/foundations/`; DRS, admission control, DPM, vCLS in `object-types/cluster/`. |
| Metadata block at the end of each file | Retrievers filter on it. Reviewers see source, corrections and status in one place. At the end, so the content reads first on GitHub. |
| `raw-input/` not indexed | Source documents are binary and unstructured. Derived files are what the AI reads. |
| `benchmark/` one file per case | Scales to hundreds of cases. Never indexed: holds answer keys. |

## Reader model
- Reader: a local LLM using retrieval. Small context window; retrieves a few chunks per question.
- Consequences:
  - Small files and one fact per line keep each chunk on topic.
  - Links in metadata let the retriever expand from one hit to its traps and mechanisms.
  - Diagrams carry text equivalents, because the model may not read images.
- Ingest, query and answer steps: root `README.md`, section How a local LLM uses it.

## Limitations
- Converting expert knowledge into files is lossy. Some tacit knowledge is hard to codify.
- The AI retrieves and recombines text. Structure and golden cases improve answer quality; they do not create understanding.
- Quality drifts without regular review. `status: draft` files are unreviewed.
- Screenshots and diagrams must be converted to text (formulas, Mermaid, descriptions) to be retrievable.
- Coverage is intentionally partial: depth first, breadth later.

## How to improve
1. Depth before breadth: one complete mechanism beats twenty shallow counter definitions.
2. Extract a source section in full. Keep every distinction.
3. Add golden cases for each new section, especially traps a generic AI falls into.
4. Run evaluation before and after a change. Keep changes that raise scores.
5. Remove files that are generic, unsourced or contradicted by the source.
