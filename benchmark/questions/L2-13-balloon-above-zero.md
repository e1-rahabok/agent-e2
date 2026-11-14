# Balloon above 0: is the VM slow?

## Prompt
- In the vSphere Client, a 16 GB Linux VM shows Ballooned memory at 2 GB, flat for the last hour.
- The application owner asks for more memory because "the host is taking memory away from the VM".

Which statements are correct?

- A. Ballooned at 2 GB shows that the VM waits for memory now.
- B. Ballooned counts memory the balloon took at some time, possibly long before this hour.
- C. A flat line means the balloon neither grew nor shrank during the hour.
- D. VM Memory Latency (Memory Contention in VCF Operations) is the counter that shows whether the VM waits for memory.
- E. VM Memory Latency includes the time Linux spends paging out to fill the balloon.
- F. Linux gives the balloon free and cache pages before pages that its processes are using.
- G. ESXi keeps physical pages behind the ballooned 2 GB, ready to hand back to the VM at once.
- H. Ballooning cannot slow this VM, whatever the guest does next.
- I. Adding the requested memory is the right response to the 2 GB balloon.

## Likely wrong answer
- A: "Balloon above 0 means the VM is starved of memory and slow: give it more RAM."

## Expected key points
- Answer: B, C, D, F.
- A is false: ballooning by itself does not cause a performance problem; a hit comes only when the guest needs those pages again, and the wait shows in Latency, not in Ballooned.
- B is true: Ballooned is past tense; the pages stay ballooned while the guest does not ask for them, and the balloon can date from pressure long gone.
- C is true: a flat value means nothing was reclaimed or returned in the hour; on its own it shows neither current host pressure nor a wait.
- D is true: Memory Latency is the share of time a vCPU waits for a page fault (mostly swap-in, plus decompression); VCF Operations Memory Contention maps to it.
- E is false: Latency excludes balloon activity; the hypervisor cannot see what the guest does to fill the balloon.
- F is true: the guest gives the balloon Free pages first, then Cache, then Modified, then In Use.
- G is false: ballooned pages map to no ESXi page; ESXi gave their physical pages to other VMs.
- H is false: a problem occurs when the guest requests a ballooned page again; the more is ballooned, the higher the chance of a future hit. This is the over-correction of A.
- I is false: the balloon alone shows no wait; check Latency first. With no wait, more memory fixes nothing the owner sees.

## Notes
- Revised 2026-11-12: situation and the owner's claim added; key points aligned with the knowledge files.
- Left out of the options: whether a VM or resource pool limit causes ballooning (open author question Q214), and "adding memory does not stop the balloon", which leans on the same question.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A one fact; B and C no longer negate A; H the over-correction and I the wrong action added. Old option F ("The balloon driver ships in open-vm-tools, so stopping the tools service on this VM stops ballooning") removed: whether stopping the VMware Tools service stops ballooning on Linux is raised as an author question with 0022. Key changed from B, C, D, G to B, C, D, F (relettered; same facts).

## Metadata
```yaml
id: "0052"
title: "Balloon above 0: is the VM slow?"
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 200
answer_type: deterministic
answer: [B, C, D, F]
misconception: [A]
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/ballooned
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [reclamation-as-contention]
pair: "0388"
status: draft
```
