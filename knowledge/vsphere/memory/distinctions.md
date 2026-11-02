---
id: vsphere/memory/distinctions
type: distinction
scope: vsphere
resources: [memory]
objects: [vm, esxi, cluster]
related:
  - foundations/naming-patterns
  - foundations/resource-nature
  - vsphere/foundations/resource-management
  - vsphere/foundations/overhead
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity
corrections: []
review_notes: []
status: draft
---

# Memory distinctions

## Memory Usage: VM vs ESXi vs Cluster
- pattern: same-name-same-purpose-different-formula
- VM: Usage maps to Active.
- ESXi: Usage maps to Consumed.
- Cluster: Usage maps to Consumed + Overhead.
- VCF Operations (VM): Usage uses Guest OS data. Falls back to Active if Guest OS data is not available.
- why: two-level memory hierarchy in virtualization.
  - VM level uses Active: what the VM is physically using. Related to performance.
  - ESXi and cluster levels use Consumed: what the VM has claimed. Related to capacity management.
- trap: comparing VM Usage with ESXi Usage as if they measure the same thing. This confusion has led customers to buy more RAM than required.
- src: Naming Complexity

## Memory Consumed: ESXi vs Cluster vs VM
- pattern: same-name-same-purpose-different-formula
- ESXi: includes memory consumed by ESXi itself.
- Cluster: includes only memory consumed by VMs. Includes VM overhead.
- VM: excludes overhead.
- trap: summing VM Consumed and expecting ESXi Consumed or Cluster Consumed.
- src: Naming Complexity

## Swapped (VM) vs Swap Used (ESXi)
- pattern: same-purpose-different-name
- VM calls it Swapped. ESXi calls it Swap Used.
- why: different vantage points.
- src: Naming Complexity

## Memory Ballooned
- pattern: confusing-name (past tense)
- A non-zero Ballooned value does not mean ballooning is happening now.
- Ballooning may have happened days ago. The page stays ballooned while idle, because the Guest OS has not asked for it.
- trap: "Ballooned > 0, so the host is under memory pressure now" → not necessarily.
- src: Other Nuances

## Memory Latency
- Memory Latency indicates a performance problem. It is a primary counter for how well the VM is served.
- Contrast: CPU Latency does not always indicate a performance problem. See `vsphere/cpu/distinctions`.
- src: Naming Complexity

## Memory reservation in Consumed
- Memory Consumed includes reserved memory, even if not yet used by the Guest OS.
- See `vsphere/foundations/resource-management`.

## No VM Memory Demand
- There is VM CPU Demand, but no VM Memory Demand. Memory is space, not time.
- See `foundations/resource-nature`.

## Utilization near 100%
- Memory works as a cache. Near 100% is expected.
- 95% memory utilization can be low; 85% CPU utilization can already be high.
- See `foundations/resource-nature`.

## vMotion effect on Consumed
- After vMotion, VM Memory Consumed on the destination can increase (swapped or compressed pages become regular pages).
- See `vsphere/foundations/overhead`.

## Metric count
- vCenter has 28 memory metrics per VM.
- See `foundations/metric-volume`.
