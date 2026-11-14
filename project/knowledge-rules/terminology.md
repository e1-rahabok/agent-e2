# Terminology

Part of the knowledge rules; overview and why: [KNOWLEDGE-ENGINEERING.md](../../KNOWLEDGE-ENGINEERING.md). For writers and reviewers. Not indexed.

Agent E2 has four jobs with words. Each has one home, so a fact is written once.

| Job | Failure it prevents | Home | Reaches the model |
|---|---|---|---|
| Recognize the user's word | Search misses the file ("steal time", "%RDY", "uptime KPI") | Glossary, Also called; the term map ([`knowledge/catalog/user-terms.yaml`](../../knowledge/catalog/user-terms.yaml)) for phrases | Query terms, files and notes before search |
| Know what a term means here | The public meaning wins (ESXi CPU Demand read where capacity Demand is meant) | Glossary entry; the file for a metric | Search: the reading set |
| Keep two terms apart | The answer uses the wrong one of two real terms | Glossary, Not to confuse with | Up-front block `terms` |
| Drop a wrong belief | A confident rule of thumb, never looked up | The `## Misconceptions` line of its file, marked `up_front` | Up-front block `rules` |

Glossary entry ([`knowledge/glossary.md`](../../knowledge/glossary.md), read by [`harness/kb.py`](../../harness/kb.py), checked by lint):
- `- **Term**: meaning`, then optional lines `  - Also called: a, b`, `  - Not to confuse with Other term: difference.`, ``  - File: `id` ``. Grouped by area under `###` headings, alphabetical within each. Not `##`: the glossary must stay one chunk, so search never ranks this summary above the files that hold the mechanism (retrieval check 2026-11-11: with `##` areas the glossary entered 18 of 95 retrieved contexts instead of 3, and 2 questions lost a needed file).
- Meaning only where Agent E2's meaning differs from public text, or a 32B model lacks it (SP5 and VCF Operations terms, redefined words). No Level 100 or 200 definitions.
- A metric with its own file is an entry only when it has another name or a confusable partner.
- Same name, two things (Demand for capacity, Demand on ESXi): two entries with a qualifier, each pointing at the other.

A confusable pair passes all four tests:
1. Two (or three) terms of the same kind, each a real term: two metrics, two processes, two scores. "Reservation vs usage" is a rule, not a pair.
2. Swapped in practice by public text, vendor documents or frontier models. Not a difference every VMware administrator knows (Ballooned vs Swapped, allocation vs reservation).
3. The swap changes the answer: another verdict, metric, number or action.
4. Not already a misconception. One home per fact.
- Written once, under the term users misuse; the difference names both terms, so the line reads alone.

Up-front misconception (metadata `up_front`, [metadata.md](metadata.md)):
- One home: a line of the `## Misconceptions` section of the file that holds the mechanism, marked by `up_front` with its wrong belief; [`harness/primer.py`](../../harness/primer.py) collects the marked lines (Q211).
- Chosen by reach: a belief a frontier model applies without being asked, that changes the verdict on many questions: what is a problem, which metric decides, what to add or size by.
- Level 300: a VMware administrator with hands-on vSphere knowledge still holds it. Not a definition, not a swap of two terms (those are glossary entries).
- One line, in the misconception format: the wrong belief in quotes, →, the correct reading. The block adds `See` and the file id.

Up-front budget: the up-front blocks together stay within 3,000 tokens ([`harness/primer.py`](../../harness/primer.py), lint). A new pair or misconception needs room; drop a weaker one first.
