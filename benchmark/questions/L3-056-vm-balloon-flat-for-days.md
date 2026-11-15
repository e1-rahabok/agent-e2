# VM balloon flat for days

## Prompt
See [the vCenter chart of the VM's balloon and memory latency](0388/vcenter-vm-balloon-latency-past-week.png) and [the vCenter chart of its swap rates](0388/vcenter-vm-swap-rates-past-week.png).

- A Linux VM runs a message queue broker.
- Its owner has seen the balloon in the vSphere Client and blames it for slow message delivery this week: "ESXi keeps squeezing my VM. Give it a third more memory."

Which statements are correct?

- A. The ballooned amount has not changed for at least the last three days.
- B. Balloon above 0 shows that ESXi is reclaiming more memory from the VM right now.
- C. ESXi did not make the VM wait on memory for any measurable time this week.
- D. Swap in rate rose above 0 at least once during the week.
- E. A balloon can hold any share of a VM's memory without ever slowing the VM.
- F. Set a full memory reservation on the VM to end its wait for the ballooned memory.
- G. While the balloon holds memory, no ESXi page stands behind it: ESXi uses that memory elsewhere.

## Input to supply
- Product: vSphere Client 9.1; a Linux VM with the `vmw_balloon` driver loaded and a configured memory other than 16 GB.
- Screen 1: vSphere Client > the VM > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past week; counters Balloon (KB) and Latency (%); target the VM. Save as `benchmark/questions/0388/vcenter-vm-balloon-latency-past-week.png`.
- Screen 2: the same chart with counters Swap in rate and Swap out rate (KBps). Save as `benchmark/questions/0388/vcenter-vm-swap-rates-past-week.png`.
- Condition the key depends on:
  - Balloon rises once and then stays flat (within 2%) for at least the last 3 days, at between 15% and 50% of the configured memory;
  - Latency 0.00 at every point of the week;
  - Swap in rate 0 at every point of the week.
- How to produce it: a field VM that matches, or in a lab, host memory pressure that inflates the balloon while the guest keeps its working set inside the memory left to it (an idle or lightly loaded guest).
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: "The balloon is there, so ESXi is taking memory from the VM right now and slowing it."

## Expected key points
- Answer: A, C, G.
- A true: the balloon line is flat for the last three days or more: nothing was reclaimed or given back, and the guest did not ask for those pages again.
- B false: Ballooned is a held amount; a flat line means no more is being reclaimed. A balloon above 0 says ESXi reclaimed memory at some point.
- C true: Memory Latency is the share of time a vCPU waits for a page fault ESXi resolves (mostly swap-in, plus decompression); it reads 0.00 at every point, and swap-in is 0.
- D false: the swap in rate line is 0 at every point of the week.
- E false: over-correction. A hit comes when the guest needs a ballooned page again; the more is ballooned, the higher the chance, and the same amount hurts a small VM more than a large one.
- F false: the wrong action. The VM shows no wait to end: Latency and swap-in are 0 all week.
- G true: ballooned pages map to no ESXi page; ESXi gave their physical pages to other uses.

## Notes
- Paired with 0052 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C12.
- Left out: Balloon target (no option needs it); whether a memory limit causes ballooning (open author question Q214); whether Linux pages to fill the balloon, which VM counters cannot see. F is false for a reason that stands without them: the VM did not wait.
- The configured memory and the balloon share keep away from the knowledge-base example (16 GB, 10,430 MB ballooned).
- Review fixes 2026-11-15: new situation and owner quote (0052 has the same request); options reworded away from 0052; screen readings added (A, C true; D false); Latency and swap-in now 0 at every point; the option that more memory cures the slowness replaced by F (guest paging could not be ruled out). Key A, C, E → A, C, G.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0388"
title: "VM balloon flat for days"
product: [vsphere, linux]
technology: [memory]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/ballooned
attachments:
  - 0388/vcenter-vm-balloon-latency-past-week.png
  - 0388/vcenter-vm-swap-rates-past-week.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C12"
answer: [A, C, G]
misconception: [B]
misconception_type: [reclamation-as-contention]
pair: "0052"
status: awaiting-input
```
