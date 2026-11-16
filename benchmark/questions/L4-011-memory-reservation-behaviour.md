# Memory reservation behaviour

## Prompt
- Host esx-05 runs ESXi, vSAN and NSX and has 512 GB of memory.
- Its powered-on VMs reserve 420 GB of memory in total.

Choose the correct statements:

- A. A memory page touched within a reservation stays held for the VM through days of idling.
- B. Use VM-level reservations sparingly: they lower how far the host can be overcommitted and constrain DRS.
- C. Memory | VMkernel consumed on esx-05 shows all the memory its hypervisor uses, vSAN and NSX included.
- D. The kernel reservation is set aside as physical pages at boot: VMs cannot consume that memory, even the part the kernel has not touched.
- E. With vSAN, NSX and ESXi, the kernel memory reservation is a cap: kernel memory use stays under it, even when ESXi is highly utilized.
- F. Admission control withholds the whole kernel memory reservation from VM reservations, whether the kernel uses it or not.

## Likely wrong answer
D (the kernel reservation assumed to block memory before use) or C (VMkernel consumed read as all hypervisor memory).

## Expected key points
- Answer: A, B, F.
- A is correct: memory is a form of storage; once the VM asks for memory and is served, the page stays held for it, even if the VM idles for days. CPU reservation, by contrast, holds nothing back.
- B is correct: VM reservations are guarantees that admission control counts in full, so they lower how far the host can be overcommitted and can leave DRS no host to move a VM to.
- C is wrong: VMkernel consumed is the VMkernel's own use for core functions; it leaves out the management agents and the NSX agents (host/vim) and the vSAN services (host/opt), so it is well below all hypervisor memory.
- D is wrong: in the page sense the kernel reservation is granted on demand, not set aside at boot; the part the kernel has not consumed is free memory that VMs can consume.
- E is wrong: utilization can exceed reservation. A reservation is a minimum, not a cap, and the kernel reservation covers host/system only; the NSX agents and vSAN services run in host/vim and host/opt, outside it.
- F is correct: in the admission sense the full kernel reservation counts, used or not, so it is not available for VM reservations (vCenter `mem.unreserved` leaves it out).

## Notes
- The kernel reservation has two senses (overhead, section Memory metrics): admission (F, true) and pages (D, false). Only the mechanism separates them.
- Changed in the 2026-11-15 audit: the stem's definition line replaced by host facts that decide no option; A shortened (it was the longest option and correct); B one fact; C replaced in place (a throwaway: resource pools have no reservation) by the VMkernel-consumed misconception (false, overhead Misconceptions); F added, the admission sense of the kernel reservation (true). Answer A, B -> A, B, F.

## Metadata
```yaml
id: "0024"
title: "Memory reservation behaviour"
product: [vsphere]
technology: [memory]
input: [text]
task: judge-setting
knowledge:
  - vsphere/architecture/resource-controls
  - vsphere/technology/memory/metrics/host/reservation
  - vsphere/technology/memory/concepts/memory-as-storage
  - vsphere/architecture/overhead
object: [vm, esxi, resource-pool]
tool: [none]
knowledge_main: vsphere/architecture/resource-controls
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q4 Memory Reservation"
answer_type: deterministic
level: 400                      # author 2026-11-05
answer: [A, B, F]
misconception: [C, D]
misconception_type: [provider-vs-consumer]
status: draft
```
