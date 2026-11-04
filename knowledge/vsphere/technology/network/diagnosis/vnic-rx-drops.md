# vNIC receive drops: find the reason with vsish

## Checks, in order
1. Port statistics for the vNIC port:
```text
vsish -e get /net/portsets/DvsPortset-0/ports/<port>/clientStats
```
   - droppedRx above 0 confirms receive drops (example: 2,620).
2. Reason, from the vmxnet3 receive queue summary:
```text
vsish -e get /net/portsets/DvsPortset-0/ports/<port>/vmxnet3/rxSummary
```
   - running out of buffers: matches the drop count (example: 2,620).
   - # of times the 1st ring is full: example 354.
   - 1st ring size and 2nd ring size: example 512 each.
   - Other reasons (fail to map, rx queue stopped, copy failures, large headers, MTU exceeded) at 0 rule them out.

## How to read the result
- Drops = running out of buffers and ring full: the receive ring is too small. The book suggests 2K instead of 512.
- Network VMs (firewalls, routers) or VMs expecting high packet rates: check whether the VM requests NetQ RSS.
- VMXNET3 can lose packets in very high bursts when buffers run out (KB 2039495).

## Traps
- "vSphere shows the drop reason" → only vsish shows it.

## Metadata
```yaml
id: vsphere/technology/network/diagnosis/vnic-rx-drops
retriever_guide: what-to-check
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive:
- vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
related:
- vsphere/technology/network/metrics/host/packets-dropped
- vsphere/technology/network/configuration/rss-and-interrupt-coalescing
source:
  document: PART 3 - Counters.docx
  path: Network > ESXi > Contention Metrics > Dropped Packet > vsish
corrections: []
review_notes:
- 'Section ''How to read the result'': the 2K ring size is the author''s suggestion.'
status: draft
```
