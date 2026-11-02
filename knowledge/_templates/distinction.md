---
id: <scope>/<area>/distinctions       # e.g. vsphere/cpu/distinctions
type: distinction
scope: vsphere                        # vendor-neutral | vsphere
resources: [cpu]
objects: [vcpu, vm, esxi, cluster]
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances
corrections: []
review_notes: []
status: draft
---

# <Resource> distinctions

One block per distinction. Keep every block self-contained: it may be retrieved alone.

## <Metric name>: <object A> vs <object B>
- pattern: <same-name-different-formula | same-name-different-meaning | same-name-different-behaviour | same-purpose-different-name | confusing-name | incorrect-name | mixing-terminology>
- <object A>: what it measures, includes, excludes.
- <object B>: what it measures, includes, excludes.
- why: the mechanism or vantage point that causes the difference.
- trap: the wrong conclusion this causes.
- src: <Heading 4> > <Heading 5>
