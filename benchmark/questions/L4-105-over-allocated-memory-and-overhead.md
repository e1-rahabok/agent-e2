# Over-allocated memory and overhead

## Prompt
- An application owner asks for 24 VMs with 256 GB of memory each, on a DRS cluster with DPM turned on. The vendor's sizing says the application working set is about 40 GB per VM, and the rest would serve as file system cache in the Guest OS (Linux). The alternative on the table is 64 GB per VM.
- The ESX hosts have enough free memory today. They are not overcommitted and are in the high memory state.
- The VMs would get no memory reservation. The swap file location is the VM directory on a VMFS datastore.
- A colleague says: "Over-allocation costs nothing. The Guest OS uses the extra memory only as cache, and if a host runs short, ESX takes the unused memory back with ballooning."
- After three months the colleague's VMs would show Granted close to 256 GB, because Linux has filled the extra memory with page cache, while the Active memory of each VM stays near 40 GB.

Which statements are correct?

- A. Over- and under-allocation are equally harmful, so 256 GB and 64 GB per VM carry the same risk.
- B. DPM puts a host into standby only when granted memory is low, so the 256 GB VMs can keep hosts powered on.
- C. ESX balloons idle guest memory even when the host has free memory, so Granted falls back toward the 40 GB that is active.
- D. With no reservation, the swap files take 6,144 GB for 24 VMs at 256 GB, against 1,536 GB at 64 GB.
- E. While the hosts stay in the high memory state, ESX does not balloon the VMs, so Granted stays near 256 GB.
- F. When host memory gets low, ballooning can take back the page cache that Linux holds in the extra memory.
- G. ESX can reclaim the per-VM overhead of the over-allocated memory through ballooning when hosts run short.
- H. DRS uses granted memory as a VM's memory demand for vMotion recommendations, so the 256 GB VMs constrain migrations.
- I. A swap file larger than 100 GB can make the VM's power-on take significantly longer.
- J. DRS bases its memory decisions on Active memory, so it sees only the 40 GB working set of each VM.
- K. Under-allocating below the 40 GB working set would hurt more than over-allocating, as the guest would thrash.
- L. Over-allocation costs nothing, because the Guest OS uses the extra memory only as file system cache.
- M. A 256 GB VM carries about 11.5 GB of per-VM overhead, a 64 GB VM about 3.5 GB (documented representative values).
- N. Swap files are created only when a host starts to swap, so they take no space while memory is not overcommitted.

## Likely wrong answer
- A: "Over- and under-allocation are equally bad."
- G: "If a host runs short, ballooning gives all of it back."
- L: "Over-allocation is harmless: the guest only uses it as cache."

## Expected key points
- Answer: B, D, E, F, H, I, K, M.
- A is false: the source calls under-allocation the more damaging error; the impact of over-allocating is far less, though substantial over-allocation is still to avoid.
- B is true: since vSphere 7.0 DPM computes memory demand from granted memory, and memory demand is low only if granted memory is low.
- C is false: no host pressure, no balloon; a VM inside its configured memory on a host with free memory is not ballooned.
- D is true: with no reservation the swap file equals configured memory: 24 x 256 GB = 6,144 GB, 24 x 64 GB = 1,536 GB.
- E is true: ballooning starts only when host memory gets low (soft state); until then the VM keeps the memory it has touched, here the Linux page cache.
- F is true: memory beyond the working set becomes file system cache, and ESX uses ballooning to reclaim that cache when host memory is low.
- G is false: ESX can reclaim over-allocated memory but not the memory overhead associated with it.
- H is true: since vSphere 7.0 DRS uses granted memory for the memory demand in vMotion recommendations; over-provisioned memory constrains migration options more than before.
- I is true: the vendor says a swap file larger than 100 GB can raise the power-on time significantly (reservations shrink it, but they lock host memory).
- J is false: DRS and DPM read granted memory since vSphere 7.0, not Active.
- K is true: under-allocation is the more damaging error; a VM that cannot hold its working set thrashes, with a dramatic effect on performance. 64 GB, above the 40 GB working set, is safe for the VM.
- L is false: the colleague's claim; the overhead, the granted-memory effect on DRS and DPM, and the swap file space remain.
- M is true: per-VM overhead grows with configured memory; about 4.5% of 256 GB (11.5 GB) against 5.5% of 64 GB (3.5 GB), about 8 GB per VM and about 190 GB for 24 VMs that support no application.
- N is false: the swap file is created at power-on with its full size, whether or not the host ever swaps.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Option I (power-on time of a swap file above 100 GB) rests on the VMware vSphere 9.1 PDF (build of 2026-11-02), Resource Management, Using Swap Files with vSphere (p. 1875): "When you create a large swap file (for example, larger than 100GB), the amount of time it takes for the virtual machine to power on can increase significantly." No knowledge file states it.
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
answer_type: deterministic
answer: [B, D, E, F, H, I, K, M]
misconception: [L, G, A]
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
