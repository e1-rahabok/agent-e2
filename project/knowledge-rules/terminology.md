# Terminology

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

Agent E2 has five jobs with words. Each has one home, so a fact is written once.

| Job | Failure it prevents | Home | Reaches the model |
|---|---|---|---|
| Recognize the user's word | Search misses the file ("steal time", "%RDY", "uptime KPI") | Glossary, Also called; the term map ([`knowledge/catalog/user-terms.yaml`](../../knowledge/catalog/user-terms.yaml)) for phrases | Query terms, files and notes before search |
| Know what a term means here | The public meaning wins (ESXi CPU Demand read where capacity Demand is meant) | Glossary entry; the file for a metric | Search: the reading set |
| Keep two terms apart | The answer uses the wrong one of two real terms | Glossary, Not to confuse with | Up-front block `terms` |
| Drop a wrong belief | A confident rule of thumb, never looked up | The `## Misconceptions` line of its file, marked `up_front` | Up-front block `rules` |
| Read a product label | The label's name wins over what it computes (Total Capacity (GHz) read as capacity) | Glossary entry named by the label: Product label, Invites, Better name | Term-map note when the question or the case names the label; the teaching order in an open answer |

Glossary entry ([`knowledge/glossary.md`](../../knowledge/glossary.md), read by [`harness/knowledge_loader.py`](../../harness/knowledge_loader.py), checked by lint):
- `- **Term**: meaning`, then optional lines `  - Also called: a, b`, `  - Not to confuse with Other term: difference.`, ``  - File: `id` ``. Grouped by area under `###` headings, alphabetical within each. Not `##`: the glossary must stay one chunk, so search never ranks this summary above the files that hold the mechanism (retrieval check 2026-11-11: with `##` areas the glossary entered 18 of 95 retrieved contexts instead of 3, and 2 questions lost a needed file).
- Meaning only where Agent E2's meaning differs from public text, or a 32B model lacks it (SP5 and VCF Operations terms, redefined words). No Level 100 or 200 definitions.
- A metric with its own file is an entry only when it has another name or a confusable partner.
- Same name, two things (Demand for capacity, Demand on ESXi): two entries with a qualifier, each pointing at the other.

Product label entry (design: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md), section Product label and better model):
- For a label that invites a decision its computed model does not support, when the knowledge base holds the better model.
- Named by the label as a question names it, with its object: ESXi CPU Usage (%), not Usage (%).
- The meaning line says what the product computes. Then `  - Product label: the label verbatim (where it shows)`, `  - Invites: the decision the label invites`, `  - Better name: Name: the better model`, and a `File:` line for the file that owns the metric. Lint requires all four.
- Short: the term map sends meaning, Invites and Better name to the model as one note, inside the reading set, so every word costs a file section at the budget's edge.
- One term-map row names the entry (`label:`) and carries the match patterns; it has no note. A pattern must match the entry term. A new row goes at the end of the term map, so it adds its note without taking the two term-map file slots from older rows; its search words name only what the question's words lack. The mechanism and the misconception line stay in the File.
- No generator: the match patterns are the user's words, which the term map already owns, and [`harness/user_terms.py`](../../harness/user_terms.py) reads the note from the glossary entry at start and puts the entry's File first. A generated copy and its sync check would add machinery and remove no second home.
- Better name:
  - Never reword the label itself. Quote it as the product shows it, then correct the model behind it. Wrong: "vSphere's GHz total". Right: "Total Capacity (GHz) is the capacity at base clock; space for vCPUs is threads" ([vocabulary.md](vocabulary.md), Words to avoid).
  - Reuse Agent E2's existing words where one fits (CPU Throughput, Active, Guest OS Needed Memory), so the names form one family: Usage (MHz) is CPU Throughput, and Total Capacity (GHz) is Total Base Capacity (GHz).
  - A label that already names its model well stays as the better name (Q236): VM CPU Latency, ESXi Memory Usage (%), VM Memory Consumed.
  - Throughput is activity, not capability, so no capacity figure is named a throughput.
  - The better name belongs to Agent E2's vocabulary. A benchmark prompt uses only the label (fairness F1). A key point grades the model, never the better name, which a frontier model cannot know.
- Teaching order, the order the author uses in consulting: (1) name the label as the operator sees it; (2) say what it computes; (3) name the decision it invites and why that decision fails; (4) give the better model and its name; (5) say what to read instead.
  - Applied only when the question or the case names a listed label (a term-map row with `label` matches), and inside the answer's length and shape, never on top of them: 250 words with the conclusion first leave no room for five extra steps.
  - The conclusion carries steps 1, 3 and 4; the mechanism carries step 2; what to check next carries step 5. The text is `LABEL_ORDER` in [`harness/user_terms.py`](../../harness/user_terms.py), added to the rules of an open answer ([`harness/AGENT.md`](../../harness/AGENT.md), section 4.5). A multiple-choice answer gets the note, not the order.
- Not a label entry: Contention (VCF Operations). It is Overlap + Co-stop + Ready + Other Wait (below 1%), time the vCPU did not get, which is what the label says ([`contention`](../../knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/contention.md)). Its wrong reading, that the cluster is overloaded when a limit causes it, is about cause, so it stays a misconception of its file.

A confusable pair passes all four tests:
1. Two (or three) terms of the same kind, each a real term: two metrics, two processes, two scores. "Reservation vs usage" is a rule, not a pair.
2. Swapped in practice by public text, vendor documents or frontier models. Not a difference every VMware administrator knows (Ballooned vs Swapped, allocation vs reservation).
3. The swap changes the answer: another verdict, metric, number or action.
4. Not already a misconception. One home per fact.
- Written once, under the term users misuse; the difference names both terms, so the line reads alone.

Up-front misconception (metadata `up_front`, [metadata.md](metadata.md)):
- One home: a line of the `## Misconceptions` section of the file that holds the mechanism, marked by `up_front` with its wrong belief; [`harness/upfront_knowledge.py`](../../harness/upfront_knowledge.py) collects the marked lines (Q211).
- Chosen by reach: a belief a frontier model applies without being asked, that changes the verdict on many questions: what is a problem, which metric decides, what to add or size by.
- Level 300: a VMware administrator with hands-on vSphere knowledge still holds it. Not a definition, not a swap of two terms (those are glossary entries).
- One line, in the misconception format: the wrong belief in quotes, →, the correct reading. The block adds `See` and the file id.

Up-front budget: the up-front blocks together stay within 3,000 tokens ([`harness/upfront_knowledge.py`](../../harness/upfront_knowledge.py), lint). A new pair or misconception needs room; drop a weaker one first.
