# ESXi Memory Swap Used

## Meaning
- The host-level counterpart of VM Swapped. Different names for different vantage points.

## Swap counters at host level
| Counter | Meaning |
|---|---|
| Swap Consumed | Memory swapped by all powered-on VMs and vSphere services. Falls when pages are swapped back in. Not Swap Out minus Swap In, the same as VM Swapped. |
| Swap In, Swap Out | Cumulative amounts swapped in or out to date. |
| Swap In Rate, Swap Out Rate | Rates. |

- 5 swap counters at host level, not 6: Swap Target is missing.
- Swap Out is cumulative: it does not fall when pages are swapped in.
- Small swap-in rates matter little: 1-2 KB/s averaged over 20 s = 20-40 KB.
![Cumulative swap in and swap out](../../images/esxi-memory-swap-in-vs-swap-out-cumulative.png)

## Misconceptions
- "Swap Consumed = Swap Out - Swap In" → no. Swap Out and Swap In are cumulative totals. Swap Consumed is what sits in swap now, like VM Swapped.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/host/swap-used
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- performance
product:
- vsphere
object:
- HostSystem
metric_class: contention
internal_derive:
- vsphere/technology/memory/concepts/host-memory-states
same_name: []
same_meaning:
- vsphere/technology/memory/metrics/virtual-motherboard/swapped
related:
- vsphere/technology/memory/metrics/host/compressed
- vsphere/technology/memory/concepts/swap-and-compression
images:
  - path: ../../images/esxi-memory-swap-in-vs-swap-out-cumulative.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Memory Swap In', 'ESXi Memory Swap Out']
    image_type: timeline
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > ESXi > Swap + Compress
corrections: []
review_notes:
- 'To check: metric_class: set to contention.'
- 'Section ''Swap counters at host level'': from Memory > ESXi.'
- 'To check: whether host Swap In Rate and Swap Out Rate include compression.'
status: draft
```
