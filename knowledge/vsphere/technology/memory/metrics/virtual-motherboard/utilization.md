# VM Memory Utilization (VCF Operations)

## Formula
```text
Utilization (KB) = Guest Needed Memory (KB)
                 + Guest Page In Rate per second × Guest Page Size (KB)
                 + Memory Total Capacity (KB) - Guest Physically Usable Memory (KB)
```
- Can exceed 100%.

## Why it can be high when the guest looks low
- Guest metrics from VMware Tools not collected: falls back to Consumed (KB). A mixed source makes the value fluctuate.
- Guest Physically Usable Memory below configured memory. Example: 58 GB usable on an 80 GB VM.
- Low utilization: 5% of total memory is added, not 5% of used. A 128 GB VM shows 6.4 GB extra.
- The 5% is a hardcoded buffer inside Guest Needed Memory, the first term of the formula: Needed = physical - max(0, Unneeded - 5% of physical). See `guest-os/memory/concepts/windows-memory`, section Needed Memory.
- Excessive paging is added. Excessive is relative.
- Linux Available and Windows Cache are included, to be conservative.

## Traps
- "Utilization above 100% is an error" → the formula adds paging and unusable memory.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/utilization
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vcf-operations
- windows
- linux
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: consumption
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- guest-os/memory/concepts/windows-memory
- vsphere/technology/memory/concepts/guest-os-vs-vm-memory
source:
  document: PART 3 - Counters.docx
  path: Memory > VM > Consumption Metrics > Utilization
corrections: []
review_notes:
- "Section 'Why it can be high': author (2026-11-03), Q018: the 5% is a hardcoded buffer in the formula, through Guest Needed Memory (book, Windows chapter, Needed Memory)."
status: draft
```
