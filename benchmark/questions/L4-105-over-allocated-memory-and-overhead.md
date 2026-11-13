# Over-allocated memory and overhead

## Prompt
- An application owner asks for 24 VMs with 256 GB of memory each, on a DRS cluster with DPM turned on. The vendor's sizing says the application working set is about 40 GB per VM, and the rest would serve as file system cache in the Guest OS (Linux). The alternative on the table is 64 GB per VM.
- The ESX hosts have enough free memory today. They are not overcommitted and are in the high memory state.
- The VMs would get no memory reservation. The swap file location is the VM directory on a VMFS datastore.
- A colleague says: "Over-allocation costs nothing. The Guest OS uses the extra memory only as cache, and if a host runs short, ESX takes the unused memory back with ballooning."
- After three months the colleague's VMs would show Granted close to 256 GB, because Linux has filled the extra memory with page cache, while the Active memory of each VM stays near 40 GB.

Is the colleague right? Compare 256 GB with 64 GB per VM: what does each choice cost the VMs, the hosts, the DRS and DPM decisions and the datastore, and what does ballooning change?

## Likely wrong answer
"Over-allocation is harmless because ballooning gives the unused memory back." Or: "Over- and under-allocation are equally bad." Or: only the host memory is counted, and the DRS, DPM and datastore effects are missed.

## Expected key points
- Under-allocation is the more damaging error: if the VM cannot hold its working set the guest thrashes, with a dramatic effect on performance. So 64 GB, above the 40 GB working set, is safe for the VM, and 256 GB gains the VM little.
- The colleague is partly right. The memory beyond the working set becomes file system cache in the Guest OS, and ESX can use ballooning to reclaim that cache. But ballooning starts only when host memory gets low (soft state). Until then the VM keeps the memory, and Granted stays near 256 GB.
- Host cost: VM memory overhead grows with the configured memory and ESX cannot reclaim it. Representative documented values are about 4.5% of the VM size for a 256 GB VM (about 11.5 GB) and 5.5% for a 64 GB VM (about 3.5 GB). Per VM the difference is about 8 GB, and for 24 VMs about 190 GB of host memory that supports no application.
- DRS and DPM: since vSphere 7.0 DRS uses granted memory as the memory demand of a VM when it computes vMotion recommendations, and DPM uses granted memory too. Granted near 256 GB makes the VMs look large and constrains DRS migration options, and it keeps DPM from putting hosts into standby, although the Active memory is small.
- Datastore and power-on: with no reservation the swap file is the configured memory: 24 x 256 GB = 6,144 GB against 24 x 64 GB = 1,536 GB. It is created at power-on whether or not the host ever swaps. The vendor adds that a swap file larger than 100 GB can lengthen power-on significantly (reservations shrink it, but they lock host memory).
- Conclusion: the colleague is wrong that it costs nothing. Ballooning returns the cache but not the overhead, the granted-memory inflation for DRS and DPM, or the swap file space. Size to the working set with a margin and avoid substantial over-allocation.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "Memory Sizing" (p. 33: under-allocation causes thrashing; over-allocated memory is used for file system caches; ESX cannot reclaim the overhead of over-allocated memory), DRS and DPM sections (pp. 76-79: since vSphere 7.0 DRS considers granted memory for vMotion recommendations, "over-provisioning a virtual machine's memory could even more significantly constrain the DRS migration options"; DPM calculates memory demand from granted memory and puts hosts into standby only if memory demand is low), "Memory Swapping Optimizations" (p. 35). VMware vSphere 9.1 PDF (build of 2026-11-02): "The Reservable Memory is Lower than Expected" (overhead 4.5% for 256 GB, 5.5% for 64 GB, 6% for 16 GB, representative values), "Using Swap Files" (a swap file larger than 100 GB can raise the power-on time significantly).
- Why one answer: each effect is a documented statement; the question asks for the effects and for the comparison, with numbers that follow from them.
- Debatable risk: how much margin above the working set is right is a design choice, so the key does not give one. The overhead percentages are the documentation's representative values, so the figures are "about". The growth of Granted by guest page cache is a general Linux behavior, stated in the prompt as an observation.
- Rewritten 2026-11-13 to raise difficulty: adds the granted-memory effect on DRS and DPM, the unreserved swap file space and the power-on delay of large swap files, and the overhead calculation from the documented percentages; the colleague's claim stays half true.

## Metadata
```yaml
id: "0298"
title: Over-allocated memory and overhead
product: [vsphere]
technology: [memory]
task: judge-setting
level: 400
answer_type: judged
input: [text]
object: [vm, esxi, cluster]
tool: [none]
knowledge:
  - vsphere/technology/memory/configuration/memory-sizing
  - vsphere/technology/memory/concepts/memory-overhead
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/object-types/cluster/concepts/drs-overview
  - vsphere/object-types/cluster/concepts/dpm
  - vsphere/technology/memory/configuration/host-level-swapping
knowledge_main: vsphere/technology/memory/configuration/memory-sizing
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [reclamation-as-contention]
status: draft
```
