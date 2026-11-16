# Balloon above 0: is the VM slow?

## Prompt
- In the vSphere Client, a 16 GB Linux VM shows Ballooned memory at 2 GB, flat for the last hour.
- The application owner asks for more memory because "the host is taking memory away from the VM".

Which statements are correct?

- A. Ballooned at 2 GB shows that ESXi is reclaiming memory from the VM now.
- B. Ballooned counts the pages the balloon still holds, whenever it took them.
- C. Inside Linux, the 2 GB held by the balloon driver counts as used memory, not as free.
- D. VM Memory Latency (Memory Contention in VCF Operations) shows whether the VM waits for memory.
- E. VM Memory Latency includes the time Linux spends paging out to fill the balloon.
- F. Linux gives the balloon free and cache pages before pages that its processes are using.
- G. ESXi keeps physical pages behind the ballooned 2 GB, ready to hand back to the VM at once.
- H. Ballooning cannot slow this VM, whatever the guest does next.
- I. Adding the requested memory is the right response to the 2 GB balloon.
- J. Stopping the VMware Tools service (vmtoolsd) on this VM would stop the balloon.

## Answers
B, C, D, F

## Explanation
- A is false: Ballooned is an amount the balloon holds, not a rate of reclamation; flat for the hour, it shows nothing taken in that hour. The balloon can date from earlier host pressure or from a limit.
- B is true: Ballooned is past tense: the pages reclaimed earlier, possibly days ago, that the balloon still holds; it deflates only when ESXi lowers the VM's Balloon Target.
- C is true: the driver's pinned pages are neither free nor cache to the guest, so the guest's used memory includes the balloon.
- D is true: Memory Latency is the share of time a vCPU waits for a page fault (mostly swap-in, plus decompression); VCF Operations Memory Contention maps to it.
- E is false: Latency excludes balloon activity; the hypervisor cannot see what the guest does to fill the balloon.
- F is true: the guest gives the balloon Free pages first, then Cache, then Modified, then In Use.
- G is false: ballooned pages map to no ESXi page; ESXi gave their physical pages to other VMs.
- H is false: a problem comes when the guest must read back data it gave up for the balloon (from disk or guest swap); the bigger the balloon, the higher that chance. This is the over-correction of the balloon-means-slow reading.
- I is false: the balloon alone shows no wait; check Latency first. The balloon is a provider event (host pressure, or a limit, which balloons a VM on a host with free memory too), so its fix is on the provider side; with no wait, more memory fixes nothing the owner sees.
- J is false: the Linux balloon driver is the kernel module `vmw_balloon`, not part of open-vm-tools; ballooning goes on while vmtoolsd is stopped.
- Misconception: A: "Ballooned at 2 GB means the host is taking memory from the VM right now: give it more RAM."

## Notes
- Changed in the 2026-11-16 re-review: B lost its hedge ("possibly long before"): it now states that Ballooned is an amount held, whenever taken; same truth value.
- Revised 2026-11-12: situation and the owner's claim added; key points aligned with the knowledge files.
- Changed in the 2026-11-15 audit: A reworded to the held-amount reading of its pair 0388 B (the balloon-is-a-wait fact stays in 0149 and 0392); C replaced (the flat line was a near-tautology from the stem) by the balloon counted as used inside the guest (also in 0141 D: two questions). Key points B and H follow the target-driven deflate. A new option on the deflate ("stays until Linux asks for it back") was left out: the knowledge base still says the VM initiates the reallocation (balloon-target), so it is not decidable yet.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A one fact; B and C no longer negate A; H the over-correction and I the wrong action added.

## Metadata
```yaml
id: "0052"
title: "Balloon above 0: is the VM slow?"
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 200
answer_type: deterministic
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
source_path: "Synthetic, 2026-11-05"
misconception_type: [reclamation-as-contention, cumulative-vs-current]
pair: "0388"
status: draft
```
