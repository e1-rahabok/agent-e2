# Over-allocated memory and overhead

## Prompt
- An application owner asks for 24 VMs with 256 GB of memory each, on a DRS cluster with DPM turned on. The vendor's sizing says the application working set is about 40 GB per VM, and the rest would serve as file system cache in the Guest OS (Linux). The alternative on the table is 64 GB per VM.
- The ESX hosts have enough free memory today. They are not overcommitted and are in the high memory state.
- The VMs would get no memory reservation. The swap file location is the VM directory on a VMFS datastore.
- A colleague says: "Over-allocation costs nothing. The Guest OS uses the extra memory only as cache, and if a host runs short, ESX takes the unused memory back with ballooning."
- The colleague's existing VMs of this application (256 GB each), after three months: Granted about 250 GB per VM; Linux `free -g` buff/cache about 200 GB; VM Active about 40 GB.

Which statements are correct?

- A. Over- and under-allocation are equally harmful, so 256 GB and 64 GB per VM carry the same risk.
- B. DPM puts a host into standby only when granted memory is low, so the 256 GB VMs can keep hosts powered on.
- C. ESX balloons idle guest memory even when the host has free memory, so Granted falls back toward the 40 GB that is active.
- D. At 256 GB per VM with no reservation, each Linux guest needs at least 256 GB of swap space for ballooning.
- E. ESX sets each VM's balloon target with an idle memory tax, which charges idle memory more than active memory.
- F. With vSphere HA on and VMs running, DPM keeps at least two hosts of the cluster powered on.
- G. ESX can reclaim the per-VM overhead of the over-allocated memory through ballooning when hosts run short.
- H. DRS uses granted memory as a VM's memory demand for vMotion recommendations, so the 256 GB VMs constrain migrations.
- I. A swap file larger than 100 GB can make the VM's power-on take significantly longer.
- J. DRS bases its memory decisions on Active memory, so it sees only the 40 GB working set of each VM.
- K. Under-allocating below the 40 GB working set would hurt more than over-allocating, as the guest would thrash.
- L. Over-allocation costs nothing, because the Guest OS uses the extra memory only as file system cache.
- M. A 256 GB VM carries about 11.5 GB of per-VM overhead, a 64 GB VM about 3.5 GB.
- N. Swap files are created only when a host starts to swap, so they take no space while memory is not overcommitted.

## Likely wrong answer
- A: "Over- and under-allocation are equally bad."
- G: "If a host runs short, ballooning gives all of it back."
- L: "Over-allocation is harmless: the guest only uses it as cache."

## Expected key points
- Answer: B, D, E, F, H, I, K, M.
- A is false: Performance Best Practices for vSphere 9.1 calls under-allocation the more damaging error; the impact of over-allocating is far less, though substantial over-allocation is still to avoid.
- B is true: since vSphere 7.0 DPM computes memory demand from granted memory, and memory demand is low only if granted memory is low.
- C is false: no host pressure, no balloon; a VM inside its configured memory on a host with free memory is not ballooned.
- D is true: the Guest OS needs swap space of at least configured memory minus the memory reservation for ballooning, because the balloon can push the guest to page; with no reservation that is 256 GB per VM.
- E is true: the allocation target that sets the balloon follows shares and the working set and taxes idle memory (Mem.IdleTax), so idle memory is charged more than active memory.
- F is true: in a cluster with HA active and at least one VM powered on, DPM keeps at least two hosts powered on, even with HA admission control deactivated.
- G is false: ESX can reclaim over-allocated memory but not the memory overhead associated with it.
- H is true: since vSphere 7.0 DRS uses granted memory for the memory demand in vMotion recommendations; over-provisioned memory constrains migration options more than before.
- I is true: the vendor says a swap file larger than 100 GB can raise the power-on time significantly (reservations shrink it, but they lock host memory).
- J is false: DRS and DPM read granted memory since vSphere 7.0, not Active.
- K is true: under-allocation is the more damaging error; a VM that cannot hold its working set thrashes, with a dramatic effect on performance. 64 GB, above the 40 GB working set, is safe for the VM.
- L is false: the colleague's claim; the overhead, the granted-memory effect on DRS and DPM, and the swap file space remain.
- M is true: per-VM overhead grows with configured memory; about 4.5% of 256 GB (11.5 GB) against 5.5% of 64 GB (3.5 GB), about 8 GB per VM and about 190 GB for 24 VMs that support no application.
- N is false: the swap file is created at power-on with its full size, whether or not the host ever swaps.

## Notes
- Option I (power-on time of a swap file above 100 GB) rests on the VMware vSphere 9.1 PDF (build of 2026-11-02), Resource Management, Using Swap Files with vSphere (p. 1875): "When you create a large swap file (for example, larger than 100GB), the amount of time it takes for the virtual machine to power on can increase significantly." No knowledge file states it.
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "Memory Sizing" (p. 33: under-allocation causes thrashing; over-allocated memory is used for file system caches; ESX cannot reclaim the overhead of over-allocated memory), DRS and DPM sections (pp. 76-79: since vSphere 7.0 DRS considers granted memory for vMotion recommendations, "over-provisioning a virtual machine's memory could even more significantly constrain the DRS migration options"; DPM calculates memory demand from granted memory and puts hosts into standby only if memory demand is low), "Memory Swapping Optimizations" (p. 35). VMware vSphere 9.1 PDF (build of 2026-11-02): "The Reservable Memory is Lower than Expected" (overhead 4.5% for 256 GB, 5.5% for 64 GB, 6% for 16 GB, representative values), "Using Swap Files" (a swap file larger than 100 GB can raise the power-on time significantly).
- Why one answer: each effect is a documented statement; the question asks for the effects and for the comparison, with numbers that follow from them.
- Debatable risk: how much margin above the working set is right is a design choice, so the key does not give one. The overhead percentages are the documentation's representative values, so the figures are "about". The growth of Granted by guest page cache is a general Linux behavior, given in the prompt as values.
- Changed in the 2026-11-15 audit: the stem gives the three-month values without the reason (it stated the page-cache reading); D (swap file size, redundancy #43), E (no balloon without host pressure, #39) and F (ballooning reclaims the guest cache, #41) replaced in place by true facts not tested twice: guest swap space for ballooning (with L3-038 G), the idle memory tax (with L4-911 C), DPM keeping two hosts on with HA; M without the hint "(documented representative values)".

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
source_path: "Synthetic, 2026-11-13, for the coverage gap (project/plan.md)"
misconception_type: [reclamation-as-contention]
status: draft
```
