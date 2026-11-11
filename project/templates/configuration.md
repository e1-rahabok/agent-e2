# <Setting or practice>

## What to set
- Setting, value, scope (host, VM, cluster).

## Why
- Mechanism and trade-off.

## When not to
- Conditions where the setting hurts.

## Misconceptions
- Wrong conclusion → correct conclusion.

## Metadata
```yaml
id: vsphere/technology/<technology>/configuration/<slug>
retriever_guide: what-to-set
scope: vsphere
technology: [cpu]
pillar: [performance]
product: [vsphere]
object: [HostSystem]
internal_derive: []                # ids of concept files explaining why the setting matters
related: []
images:  # one entry per image linked in the body; omit when none
  - path: ../../images/<name>.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['<metric name>']   # and/or topic: '<concept>'
    image_type: timeline         # diagram, table, timeline, distribution, scatter, screenshot
    sample: '<optional: fleet size and period>'
source:
  document: <document name, version, revision>
  path: <heading path and pages>
corrections: []
review_notes: []
status: draft
```
