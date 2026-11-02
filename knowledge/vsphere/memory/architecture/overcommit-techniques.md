---
id: vsphere/memory/architecture/overcommit-techniques
type: concept
scope: vsphere
resources: [memory]
objects: [esxi, vm, cluster]
related:
  - vsphere/memory/architecture/page-sharing
  - vsphere/memory/architecture/host-level-swapping
  - vsphere/memory/interpretation/overcommit-indicators
  - vsphere/memory/distinctions
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Memory Considerations > Memory Overcommit Techniques (pp. 33-34)
corrections: []
review_notes:
  - "Checked against 9.1 (revision 20260624). Pages 33-34 unchanged."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices"
  - "Source points to white paper 'Understanding Memory Resource Management in VMware vSphere 5.0'. The source says most concepts still apply. Not read."
status: draft
---

# Memory overcommit techniques

## Purpose
- ESX uses five mechanisms to reduce the machine physical memory required by each VM.
- The five mechanisms are page sharing, ballooning, memory compression, swap to host cache, and regular host-level swapping.
- Page sharing runs continuously. The other four are triggered in order as memory pressure rises. Each trigger is listed under its mechanism below.
- Sharing, ballooning, compression and swap to host cache allow significant overcommitment, usually with little or no impact on performance.
- Regular host-level swapping can significantly affect performance.

## Page sharing
- Shares identical memory pages between VMs.
- Details: see `vsphere/memory/architecture/page-sharing`.

## Ballooning
- Trigger: host memory begins to get low, and VM memory usage approaches its memory target.
- Mechanism: the `vmmemctl` module, installed in the guest OS as part of VMware Tools, makes the guest OS relinquish the memory pages it considers least valuable.
- Performance: closely matches the performance of a native system under similar memory constraints.
- Requirement: the guest OS must have sufficient swap space configured.

## Memory compression
- Trigger: VM memory usage approaches the level at which host-level swapping would be required.
- Mechanism: ESX compresses memory pages, which reduces the number of pages it must swap out.
- Performance: decompression latency is much smaller than swap-in latency. Compression has significantly less impact than swapping out the same pages.

## Swap to host cache
- Trigger: memory compression does not keep VM memory usage low enough.
- Mechanism: ESX reclaims memory by host-level swapping to a host cache, if one is configured.
- Host cache: a special swap cache the administrator configures. In most cases it is on SSD.
- Performance: much faster than regular swap files on hard disk storage. Impact is far lower than regular host-level swapping, even though some swapped pages may be active.

## Regular host-level swapping
- Trigger: the host cache is full, or no host cache is configured.
- Mechanism: ESX swaps pages out to a regular swap file.
- Performance: can cause significant VM performance degradation, because of high access latency.
- This swapping is transparent to the guest OS. It is distinct from swapping inside the guest OS.

## Guidance
- Avoid overcommitting memory to the point where regular host-level swapping swaps out active memory pages.
- Overcommit indicators: see `vsphere/memory/interpretation/overcommit-indicators`.

## Traps
- "Ballooning means memory pressure now" → ballooning can reflect reclamation that happened earlier. See `vsphere/memory/distinctions`.
- "Host-level swapping and guest OS swapping are the same" → they are distinct. Host-level swapping is transparent to the guest.
- "Memory compression is as costly as swapping" → decompression latency is much smaller than swap-in latency.
