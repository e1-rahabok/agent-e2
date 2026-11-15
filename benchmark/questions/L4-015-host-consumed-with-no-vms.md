# Host Consumed with no VMs

## Prompt
- An ESXi 9.1 host with 512 GB of memory in a vSAN cluster enters maintenance mode; all its VMs move to other hosts.
- In the vSphere Client, host Memory Consumed falls from about 470 GB to about 41 GB and stays there.
- Configure > System > System Resource Reservation on the host shows a memory reservation of about 49 GB, before and after.

Which statements are correct?

- A. Host Consumed counts the memory that the kernel, vSAN and the other host services actually use.
- B. With no VMs, host Consumed should read the kernel memory reservation, about 49 GB.
- C. The kernel's memory reservation can be larger than the memory the kernel uses.
- D. 41 GB on a host with no VMs shows a memory leak in the kernel.
- E. With the VMs gone, Consumed equals the VM overhead memory that was reserved before the move.
- F. On a host without vSAN, Consumed would fall to 0 once the VMs leave.
- G. Reboot the host before it leaves maintenance mode, so that it gives back the 41 GB.

## Likely wrong answer
B: expecting Consumed to equal the kernel reservation. Or F, the over-correction: all that remains is vSAN.

## Expected key points
- Answer: A, C.
- A is true: host Consumed counts pages in physical DIMM: VMs, VM overhead and all kernel processes (user and kernel space), including vSAN and NSX. With 0 VMs it is the kernel and its services.
- B is false: Consumed includes actual kernel use, not the kernel reservation.
- C is true: reservation and use are different metric types; the reservation is a minimum held for the kernel, and its use can stay below it (here about 41 against 49 GB).
- D is false: the kernel, vSAN and NSX keep memory with no VMs; it is normal use, not a leak.
- E is false: VM overhead leaves with the VMs; what stays is the kernel's own use.
- F is false: the kernel and its other services consume memory too; a host with no VMs does not show 0 Consumed, with or without vSAN.
- G is false: the 41 GB is the normal use of the kernel and its services, not a leak, so there is nothing for a reboot to recover.

## Notes
- Revised 2026-11-12: option E added; tags added.
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Rewritten 2026-11-14 (design.md 3.9; project/question-pairing-2026-11-14.md): the stem no longer copies the knowledge example (new numbers: 512 GB host, 470 to 41 GB, 49 GB reservation); A one fact; F the over-correction and G the wrong action added. Key unchanged: A, C.
- No option rests on what ESX System Usage measures (open author question Q215): the reservation is read from the host's System Resource Reservation page.

## Metadata
```yaml
id: "0056"
title: "Host Consumed with no VMs"
product: [vsphere, vsan]
technology: [memory, system]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/memory/metrics/host/consumed
  - vsphere/architecture/overhead
object: [esxi]
tool: [vcenter]
knowledge_main: vsphere/technology/memory/metrics/host/consumed
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, C]
misconception: [B]
misconception_type: [provider-vs-consumer]
pair: "0390"
status: draft
```
