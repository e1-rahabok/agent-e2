# <Object> <Metric name>

## Meaning
- What it measures, from this object's vantage point.

## Formula
```text
<plain-text formula>
```

## Includes / excludes
- includes:
- excludes:

## Why
- The mechanism behind the value.

## Traps
- Wrong conclusion → correct conclusion.

## Metadata
```yaml
id: vsphere/<technology>/metrics/<object-folder>/<metric-slug>   # object-folder: virtual-machine | host | cluster | datastore | ...
retriever_guide: metric-meaning
scope: vsphere
technology: [cpu]
pillar: [performance]
product: [vsphere]
object: [VirtualMachine]           # exactly one vSphere managed object type per file (comparisons may list several)
instance: [aggregate]              # optional: aggregate | per-vcpu | per-vmnic | ... when the formula differs by instance
metric_class: contention           # contention | consumption | context
internal_derive: []                # ids of concept files this metric's meaning is derived from (internal links only)
same_name: []                      # ids of metrics with the same label but a different meaning
same_meaning: []                   # ids of metrics with a different label but the same meaning
related: []
source:
  document: <document name, version, revision>
  path: <heading path and pages>
corrections: []
review_notes: []
status: draft
```
