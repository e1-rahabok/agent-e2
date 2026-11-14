# Balloon above 0: is the VM slow?

## Prompt
- In the vSphere Client, a 16 GB Linux VM shows Ballooned memory at 2 GB, flat for the last hour.
- The application owner asks for more memory because "the host is taking memory away from the VM".

Which statements are correct?

- A. Ballooned at 2 GB proves the VM is short of memory and slow now; adding memory is the fix.
- B. Ballooned counts memory reclaimed at some point; a value above 0 does not mean the balloon is inflating now.
- C. A flat 2 GB shows that the reclaimed amount did not change in the hour, not that the VM is waiting.
- D. VM Memory Latency (Memory Contention in VCF Operations) is the counter that shows whether the VM waits for memory.
- E. VM Memory Latency includes the time Linux spends paging out to make room for the balloon.
- F. The balloon driver ships in open-vm-tools, so stopping the tools service on this VM stops ballooning.
- G. Linux hands the balloon free and cache pages before pages that its processes are using.
- H. ESXi keeps physical pages behind the ballooned 2 GB, ready to give back to the VM at once.

## Likely wrong answer
- A: "Balloon above 0 means the VM is starved of memory and slow: give it more RAM."

## Expected key points
- Answer: B, C, D, G.
- A is false: ballooning by itself does not cause a performance problem; a hit comes only when the guest needs those pages again, and the wait shows in Latency, not in Ballooned.
- B is true: Ballooned is past tense; the pages stay ballooned while the guest does not ask for them, and the balloon can date from pressure long gone.
- C is true: a flat value means nothing was reclaimed or returned in the hour; on its own it shows neither current host pressure nor a wait.
- D is true: Memory Latency is the share of time a vCPU waits for a page fault (mostly swap-in, plus decompression); VCF Operations Memory Contention maps to it.
- E is false: Latency excludes balloon activity; the hypervisor cannot see what the guest does to fill the balloon.
- F is false: on Linux the balloon driver is the `vmw_balloon` kernel module, not part of open-vm-tools; the VM keeps ballooning while vmtoolsd is stopped (Broadcom KB 313773).
- G is true: the guest gives the balloon Free pages first, then Cache, then Modified, then In Use.
- H is false: ballooned pages map to no ESXi page; ESXi gave their physical pages to other VMs.

## Notes
- Revised 2026-11-12: situation and the owner's claim added; key points aligned with the knowledge files.
- Left out of the options: whether a VM or resource pool limit causes ballooning (open author question Q214), and "adding memory does not stop the balloon", which leans on the same question.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0052"
title: "Balloon above 0: is the VM slow?"
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 200
answer_type: deterministic
answer: [B, C, D, G]
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
status: draft
```
