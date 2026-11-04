# ESXi Memory Compressed

## Meaning
- Two host counters: the amount subjected to compression, and the resulting compressed amount.
- The book takes Compressed to be the result.
- Pages can stay compressed for a long time when nothing requests them. Example: about 5 GB compressed for about 1 year, with balloon at 0 (no current pressure).
![Compressed flat at about 5 GB for a year](../../images/esxi-memory-compressed-flat-for-1-year.png)

## Traps
- "Compressed > 0 means current pressure" → it can be years old. Check balloon and swap-in.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/host/compressed
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- HostSystem
metric_class: context
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/host/swap-used
- vsphere/technology/memory/metrics/virtual-motherboard/compressed
- vsphere/technology/memory/concepts/swap-and-compression
images:
  - path: ../../images/esxi-memory-compressed-flat-for-1-year.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Memory Compressed']
    image_type: timeline
    sample: '1 host, 1 year'
source:
  document: PART 3 - Counters.docx
  path: Memory > ESXi > Overview; Swap + Compress
corrections: []
review_notes:
- 'Section ''Meaning'': the book is unsure whether Compressed is the input or the result.'
status: draft
```
