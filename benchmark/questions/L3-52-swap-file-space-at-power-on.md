# Swap file space at power-on

## Prompt
- A new VMFS datastore holds the files of 40 VMs. The swap file location is the default, the VM directory.
- Each VM has 64 GB of configured memory and a 16 GB memory reservation.
- The ESX hosts do not overcommit memory, and no host-level swapping is expected.
- All 40 VMs will be powered on. Ignore the VMX swap file and the VM overhead.

How much datastore space do the regular swap (.vswp) files of the 40 VMs need at power-on?

- A. 2,560 GB
- B. 1,920 GB
- C. 640 GB
- D. 1,280 GB
- E. None, because ESX creates a swap file only when it starts host-level swapping.

## Likely wrong answer
A (swap file equal to configured memory) or E (swap files exist only when swapping happens).

## Expected key points
- Answer: B.
- At first power-on ESX creates a swap file for the VM equal to the configured memory minus the memory reservation: 64 GB - 16 GB = 48 GB. For 40 VMs, 1,920 GB.
- The file is created at power-on, whether or not the host ever swaps. If it cannot be created, the VM does not power on.
- With a reservation equal to the configured memory the swap file is zero bytes, and host-level swapping is eliminated for that VM.
- 640 GB (C) is the reserved memory. 2,560 GB (A) ignores the reservation.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "Memory Swapping Optimizations" (page 35): swap file "equal in size to the difference between the virtual machine's configured memory size and its memory reservation". vSphere 9.1 documentation (VMware vSphere 9.1 PDF, build of 2026-11-02), vSphere Resource Management, "Swap Space and Memory Overcommitment" and "Swap File Location": the host creates the swap file when the VM powers on and the VM does not power on if it cannot.
- Why one answer: the size is a stated formula and the prompt gives all values.
- Debatable risk: option D (1,280 GB) is a distractor with no basis. On vSAN or vVols the swap file is a separate object with its own policy, so the prompt names a VMFS datastore.

## Metadata
```yaml
id: "0296"
title: Swap file space at power-on
product: [vsphere]
technology: [memory, storage]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [datastore, vm]
tool: [none]
knowledge:
  - vsphere/technology/memory/configuration/host-level-swapping
  - vsphere/technology/memory/concepts/memory-overhead
knowledge_main: vsphere/technology/memory/configuration/host-level-swapping
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [B]
misconception: [A, E]
misconception_type: []
status: draft
```
