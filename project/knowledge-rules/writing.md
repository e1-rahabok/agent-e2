# Writing rules

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

## Rules
- One fact per bullet or table row. A mistake should sit on one line.
- One English word per concept. The agent's vocabulary: [`knowledge/glossary.md`](../../knowledge/glossary.md). Words to avoid: [vocabulary.md](vocabulary.md). Repository terms: [`project/terms.md`](../terms.md).
- State mechanism and reason, not only the definition.
- Facts may come from the source, official docs, or Claude's own knowledge; the author chooses what goes in. A fact still to check gets a `review_notes` line with its section and the URL to check against. No generic filler.
- No text aimed at human motivation.
- No AI-speak. Plain words, short sentences, the fact itself:
  - no filler words or stock phrases of generated text;
  - no praise, hedging or summary lines;
  - no adjective where a number or a mechanism can stand; name the thing.
  - The list of flagged phrases, each with its plain replacement: [`project/tools/tags.yaml`](../tools/tags.yaml), `avoid_ai_speak`. The review checks them; lint stopped checking writing style on 2026-11-10 ([`project/plan.md`](../plan.md)). The same rule applies to documents, commit messages and pull request text.
- Titles and headings are noun phrases that name the topic, as in a reference book: "Sub-metric formulas", not "How each sub-metric is calculated".
  - No questions, no openers How, Why, What, When, Where, Which, Who; no commands ("Design the alerts as a set"); no claims ("CPU Ready does not apply to ESXi"); no slogans ("Begin with the end in mind"). A claim is a fact: it goes in a bullet under the heading. Sentence headings are a habit of generated text, so they count as AI-speak.
  - Reason: [`harness/kb.py`](../../harness/kb.py) puts the file title and the heading in front of every chunk. Words such as how, why, is and does name no topic, so they add nothing to search; a claim in a heading sits outside the one-fact-per-bullet rule, where a review misses it.
  - The title names the scope of the whole file. A sub-topic that one section covers goes in that section's heading, not in the title: "Windows CPU scheduling", not "Windows CPU scheduling and thread states". Reason: the title repeats in every chunk, so a sub-topic in the title pulls the other chunks into searches they do not answer and spends the context budget.
  - At most 8 words for a title, 9 for a heading. No list of contents after a colon. Words in parentheses (an alias, a counter name) do not count.
  - Exceptions, because these titles are the words users type: a metric file title is the metric name; a troubleshooting title is the symptom ("VM disk latency is high"); a decision tree title is the question as users ask it ("Can this cluster take more VMs?").
  - Fixed section names (templates in [`project/templates/`](../templates)): `Definition`, `Reason`, `Impact`, `Checks, in order` (read by [`harness/flows.py`](../../harness/flows.py)), `Order rationale`, `Interpretation`, `Not alerted`.
  - Lint checks the word limits, a list after a colon in a title, and the openers How, Why, What, When, Where, Which, Who (decision tree titles exempt). The review checks commands, claims and slogans: no pattern finds them.
- Write full sentences. No slogans ("Three sides, three metrics."), no aphorisms in place of the mechanism, no "X, not Y" where a plain statement says it.
- One vSphere object type per metric file.
- Refer to another knowledge file as a link with its id: [`id`](relative/path.md). GitHub makes it clickable for review; the harness keeps only `id` for the model ([`ARCHITECTURE.md`](../../ARCHITECTURE.md), section Ingest). The same in every Markdown file of the repository, [`knowledge/glossary.md`](../../knowledge/glossary.md) included: its parser keeps only `id` as well. [`project/tools/link_refs.py`](../tools/link_refs.py) adds missing links; lint fails on a bare id.
- Formulas as plain text. Diagrams as Mermaid plus a text explanation.
- Tables: short cells (about 12 words). At most 4 columns when cells hold text; number tables such as colour bands can have more. When rows carry long explanations, use one bullet block per row instead (bold item, one sub-bullet per field). GitHub renders a fixed-width column, so wide tables wrap every cell. Split a wide table in two, or move long explanations to bullets under the table.
- Every metric file ends its body with `## Misconceptions`, written in the misconception format of KNOWLEDGE-ENGINEERING.md, section 4.
- CPU scheduling language: a vCPU is a thread in the scheduler. It demands runtime. The kernel decides how much runtime it gets. Avoid "need", "want", "wish".
- Quotation marks only for verbatim text. Paraphrase without quotes, so the author can search the book for real quotes.

## Editing a knowledge file (author's checklist)
How the model reads a file: the harness cuts it at every `##` heading, and each piece reaches the model alone, with only the file title and that heading in front. So:
1. Each bullet stands alone. No "it", "this" or "the above" pointing to another bullet or section; name the thing again.
2. One fact per bullet, with its reason: "X, because Y". The reason lets the model apply the fact to a new case.
3. Exact names: metric and term names as in the metric files and the glossary, with the object ("VM CPU Ready", not "Ready"). A typo in a name breaks search; a typo in prose costs little.
4. One name per concept. A new name needs the glossary first; another name users say goes into the Also called line of its entry, not into the text.
5. Misconceptions go in `## Misconceptions`, in the user's words: "wrong belief" → correct reading. Search finds a misconception through those words.
6. A number comes with unit, object, interval and source. A threshold in prose also needs a row in the threshold catalog.
7. Plain sentences; grammar and elegance do not matter. Drop stories and personal asides; keep a one-line analogy only when it explains a mechanism a user may ask about.
8. Leave `## Metadata` to Claude: review notes, corrections and links are kept consistent there.
9. Titles and headings are noun phrases: no question, command or claim. Headings at most 9 words, titles at most 8 (lint).
10. After editing: commit, or tell Claude which files changed. Claude runs lint, updates the glossary, term map, threshold catalog and links, notes the source in the metadata, runs the retrieval check (paused by the author since 2026-11-12) and merges.

## Format choices
- Each format choice serves both readers:

| Choice | Machine benefit | Human benefit |
|---|---|---|
| Markdown, not HTML or JSON | Clean chunking by heading | Readable and reviewable on GitHub |
| One fact per bullet | Small, single-topic chunks | A mistake is one line to fix |
| Mechanism before metric name | The model learns why, not only what | Matches how an expert explains |
| Metadata at the end of the file | Parsed separately, never embedded as text | The body reads like a page |
| Wrong conclusion → correct reading | The misconception retrieves its correction | The misconception is explicit and reviewable |
| Tables only when simple | Rows survive chunking | Scannable |
| Exact data in YAML, prose in markdown | Lookups are exact; prose stays short | Data is reviewable as a table |
| Mermaid plus text for diagrams | The model reads the steps; the chart is left out of its text | GitHub renders the chart |

## Images
- `knowledge/` is for Agent E2 only. An image earns its place only if it helps the agent; proof screenshots for human reviewers stay in the book.
- The agent reads the text twin and the alt text, not the pixels: `get_images` returns image records, never the image itself.
- Keep the author's own diagrams and tables from the book. One image per concept, placed under the section it explains. The facts an image proves go in the text.
- Images live in the `images/` folder of the folder that uses them (for example `vsphere/technology/<tech>/images/`, `vsphere/object-types/cluster/images/`, `guest-os/<technology>/images/`).
- Alt text describes what the image shows. The text around it repeats the facts, so retrieval does not depend on the image.
- Every image has its own tags in the file's metadata `images` list ([metadata.md](metadata.md)). The validator fails on a missing or invalid entry.
- Every image file is linked from a knowledge file. The validator fails on an unlinked image: an unlinked image has no context for the AI.
- File names describe what the image shows. No length limit applies (GitHub, git and Markdown accept long names).
  - Pattern: `<object>-<metric or topic>-<what it shows>.png`, lowercase, hyphens. Example: `esxi-storage-adapter-read-write-latency-worst-vs-average-across-hosts.png`.
  - Chart type at the end when it helps: `-distribution`, `-scatter`, `-timeline`, `-table`, `-diagram`.
  - No bare numbers. Sample sizes (192 hosts, 3,385 VMs) go in the alt text and body, not the file name. A number stays only when it is the point, e.g. `62-5-percent`.
- Third-party images (vendor diagrams, documentation screenshots) are not copied. Link the source in `review_notes`.

## Versions and sources
- Write from the current release: vSphere 9.1, VCF 9.1.1 (the Versions section of [`CLAUDE.md`](../../CLAUDE.md) holds the current list).
- Before writing from a vendor document, check that it is the current version and read its revision date; record version and revision in `source.document`.
- A file written from an older version gets a `review_notes` line naming the newer version, and is re-checked before `status: reviewed`.
- The author's book is cited as "Private Cloud Management by Iwan Rahabok (https://isvara.io/download)" in `source.document`, with the heading path in `source.path`. The working files in [`project/sources/`](../sources) (Part 1, 2, 3) are not named in `knowledge/`, and their page numbers are not used: Agent E2 knows the book, not its parts.
- Theory and practice: theoretical advice covers the technology itself (Windows, Linux, Kubernetes), not only what VMware Tools or VCF Operations collects; practical advice states what each product can and cannot do (for example, which Guest OS counters VMware Tools collects).
- Oldest release covered: no knowledge about outdated releases; Linux starts at 5.0. Keep the knowledge base compact.
- [`project/sources/`](../sources) is read-only.
