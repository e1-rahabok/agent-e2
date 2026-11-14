# VM wait on the NVMe memory tier

## Prompt
- An ESXi 9.1 host uses memory tiering: 512 GB of DRAM and a 512 GB NVMe tier.
- Tier 1 (NVMe) consumed has been above 0 all week.

Which statements about how a VM on this host waits on the NVMe tier are correct?

- A. A vCPU that touches a page on the NVMe tier waits until ESXi brings the page back to DRAM.
- B. The VM that holds the most memory on the NVMe tier is the VM that waits most on it.
- C. A VM's wait on the tier grows with the pages it reads back from NVMe and the latency of each read.
- D. A guest write to a page on the NVMe tier first waits for that page to come back to DRAM.
- E. NVMe write bandwidth is time the VMs spend waiting for their pages to be written to the tier.
- F. While NVMe read latency stays below 200 µs, the tier costs a VM no measurable time.
- G. Host active memory below 50% of DRAM shows that no VM on the host waits on the tier.
- H. Move first the VM that holds the most memory on the NVMe tier, to cut the time VMs wait.
- I. A high read latency on an idle NVMe device cost the VMs nothing, because the device was only waking up.

## Likely wrong answer
B: the most memory on the NVMe tier read as the most waiting. Or F: a read latency inside the guideline read as no cost.

## Expected key points
- Answer: A, C, D.
- A true: the CPU cannot read or write NVMe directly; a page on tier 1 is fetched back to DRAM when it becomes active, and the vCPU that touched it waits for the fetch.
- B false: tier 1 consumed holds cold pages. It is saturation (memory spilled beyond DRAM), not a wait: a VM whose pages on NVMe stay cold reads nothing back.
- C true: what a VM loses is its NVMe reads times the read latency; the per-VM NVMe read bandwidth shows who pays.
- D true: a write to a cold page waits for the page to come back first, so it shows as NVMe read bandwidth, not write bandwidth.
- E false: NVMe write bandwidth is demotion, cold pages moved down in the background, off the vCPU's path. It costs device endurance and can raise read latency, but no vCPU waits on it.
- F false: over-correction. Each fetch costs about 1,000 times a DRAM access (about 100-200 µs against about 100 ns); many fetches at a good latency still slow a VM.
- G false: the host figure is a leading signal for the whole host, not each VM's experience. A VM with high NVMe read bandwidth waits whatever the host average says.
- H false: the wrong action from B. That VM's pages on NVMe are cold; move or protect the VMs that read from NVMe.
- I false: the VMs that read during the wake-up waited for each read. The wake-up explains the latency; it does not remove the wait (reads times latency).

## Notes
- Paired with 0147 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item B17.
- D rests on a line of memory-tiering that its review notes mark as an inference from the architecture (NVMe is not byte-addressable); no Broadcom page states it. 0147 option D rests on the same line.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0384"
title: "VM wait on the NVMe memory tier"
product: [vsphere]
technology: [memory]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/concepts/memory-tiering
  - vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host
knowledge_main: vsphere/technology/memory/concepts/memory-tiering
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B17"
answer: [A, C, D]
misconception: [B]
misconception_type: [consumption-as-contention, average-hides-worst]
pair: "0147"
status: draft
```
