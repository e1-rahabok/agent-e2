# <Symptom or question>

## Checks, in order
1. Contention metrics first, then consumption, then context.

## How to read the result
- Value pattern → meaning → next check.

## Traps
- Wrong conclusion → correct conclusion.

## Metadata
```yaml
id: vsphere/<technology>/diagnosis/<slug>
retriever_guide: what-to-check
scope: vsphere
technology: [cpu]
pillar: [performance]
product: [vsphere]
object: [VirtualMachine]
internal_derive: []                # ids of concept and metric files the checks rely on
related: []
source:
  document: <document name, version, revision>
  path: <heading path and pages>
corrections: []
review_notes: []
status: draft
```
