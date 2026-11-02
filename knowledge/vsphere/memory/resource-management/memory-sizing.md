---
id: vsphere/memory/resource-management/memory-sizing
type: concept
scope: vsphere
resources: [memory]
objects: [vm, esxi]
related:
  - vsphere/memory/architecture/memory-overhead
  - vsphere/memory/architecture/overcommit-techniques
  - vsphere/cpu/resource-management/resource-settings-guidance
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX Memory Considerations > Memory Sizing (p. 31)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
status: draft
---

# Memory sizing

## Under-allocation
- Allocate enough memory to hold the working set of the applications that run in the VM.
- Under-allocation causes thrashing.
- Thrashing can dramatically impact performance.
- The source says it is very important not to under-allocate memory.

## Over-allocation
- The performance impact of over-allocating memory is far less than the impact of under-allocating it.
- Avoid substantial over-allocation nevertheless.
- Memory allocated beyond the working set is typically used by the guest OS for file system caches.
- When host memory is low, ESX uses ballooning to reclaim that cache memory. See `vsphere/memory/architecture/overcommit-techniques`.
- ESX can reclaim over-allocated memory. It cannot reclaim the memory overhead associated with over-allocated memory.
- Result: over-allocation consumes memory that could otherwise support more VMs.

## Traps
- "Over-allocation is harmless because ballooning reclaims it" → ballooning reclaims the cache memory the guest uses. The overhead of the over-allocated memory stays. See `vsphere/memory/architecture/memory-overhead`.
- "Under-allocation is as safe as over-allocation" → the source calls under-allocation the more damaging error, because of thrashing.
