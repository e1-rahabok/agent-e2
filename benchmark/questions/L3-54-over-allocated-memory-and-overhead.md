# Over-allocated memory and overhead

## Prompt
- An application owner asks for 128 GB of memory for a new VM. The vendor's sizing says the application working set is about 20 GB, and the rest would serve as file system cache in the Guest OS.
- The ESX hosts have enough free memory today. They are not overcommitted.
- A colleague says: "Over-allocation costs nothing. If the host runs short, ESX takes the unused memory back with ballooning."

Is the colleague right? Compare the effect of over-allocating and under-allocating memory on the VM and on the host.

## Likely wrong answer
"Over-allocation is harmless because ballooning gives the unused memory back." Or: "Over- and under-allocation are equally bad."

## Expected key points
- Under-allocation is the more damaging error: if the VM cannot hold its working set, the guest thrashes (paging), with a dramatic effect on performance. Allocate at least the working set.
- Over-allocation has far less effect on the VM itself. Memory beyond the working set is typically used by the Guest OS for file system cache, and ESX can use ballooning to reclaim it when host memory is low.
- But over-allocation raises the VM memory overhead, which grows with the configured memory size. ESX cannot reclaim that overhead, so it takes memory that could run more VMs.
- The colleague is partly right (ballooning reclaims the cache) but wrong that it costs nothing. Avoid substantial over-allocation too.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "Memory Sizing" (page 33). https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices (fetched 2026-11-13).
- Why one answer: the document states the asymmetry and the overhead point in terms. The question asks for the effects, not for the right size.
- Debatable risk: how large a margin is acceptable is a design choice, and the key points do not ask for a number.

## Metadata
```yaml
id: "0298"
title: Over-allocated memory and overhead
product: [vsphere]
technology: [memory]
task: judge-setting
level: 300
answer_type: judged
input: [text]
object: [vm, esxi]
tool: [none]
knowledge:
  - vsphere/technology/memory/configuration/memory-sizing
  - vsphere/technology/memory/concepts/memory-overhead
  - vsphere/technology/memory/concepts/ballooning
knowledge_main: vsphere/technology/memory/configuration/memory-sizing
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [reclamation-as-contention]
status: draft
```
