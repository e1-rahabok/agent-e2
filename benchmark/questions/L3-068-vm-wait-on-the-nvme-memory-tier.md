# VM wait on the NVMe memory tier

## Prompt
- An ESXi 9.1 host uses memory tiering: 512 GB of DRAM and a 512 GB NVMe tier.
- Tier 1 (NVMe) consumed has been above 0 all week.

Which statements about how a VM on this host waits on the NVMe tier are correct?

- A. A vCPU that touches a page on the NVMe tier waits until ESXi brings the page back to DRAM.
- B. The VM that holds the most memory on the NVMe tier is the VM that waits most on it.
- C. A VM's wait on the tier grows with the pages it reads back from NVMe and the latency of each read.
- D. NVMe write bandwidth is time the VMs spend waiting for their pages to be written to the tier.
- E. While NVMe read latency stays below 200 µs, the tier costs a VM no measurable time.
- F. Host active memory below 50% of DRAM shows that no VM on the host waits on the tier.
- G. Move first the VM that holds the most memory on the NVMe tier, to cut the time VMs wait.
- H. A high read latency on an idle NVMe device is a wake-up delay that no vCPU waits through.
- I. A guest write to a page on the NVMe tier does not wait; only a read fetches the page back.

## Answers
A, C

## Explanation
- A is correct: the CPU cannot read or write NVMe directly; a page on tier 1 is fetched back to DRAM when it becomes active, and the vCPU that touched it waits for the fetch.
- B is wrong: tier 1 consumed holds cold pages. It is saturation (memory spilled beyond DRAM), not a wait: a VM whose pages on NVMe stay cold reads nothing back.
- C is correct: what a VM loses is its NVMe reads times the read latency; the per-VM NVMe read bandwidth shows who pays.
- D is wrong: NVMe write bandwidth is demotion, cold pages moved down in the background, off the vCPU's path. It costs device endurance and can raise read latency, but no vCPU waits on it.
- E is wrong: over-correction. Each fetch costs about 1,000 times a DRAM access (about 100-200 µs against about 100 ns); many fetches at a good latency still slow a VM.
- F is wrong: the host figure is a leading signal for the whole host, not each VM's experience. A VM with high NVMe read bandwidth waits whatever the host average says.
- G is wrong: the wrong action from B. That VM's pages on NVMe are cold; move or protect the VMs that read from NVMe.
- H is wrong: the vCPU that touched the page waited for that read, wake-up included. The wake-up explains the latency; it does not remove the wait. With few reads the total wait is small (reads times latency), but it is not zero.
- I is wrong: the CPU cannot write NVMe directly either; any access to a page on NVMe raises a page fault and the page is fetched to DRAM before the write completes (vSphere 9.1 documentation, pp. 1848, 1872). Only demotion writes are off the vCPU's path.
- Misconception: B: the most memory on the NVMe tier read as the most waiting. Or E: a read latency inside the guideline read as no cost. Or I: "writes do not hurt, only reads come from NVMe."

## Notes
- Paired with 0147 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item B17.
- I added in the 2026-11-15 audit: the write fact is now vendor-sourced in memory-tiering (vSphere 9.1 documentation, pp. 1848, 1872); with 0147 D it is two questions.
- H reworded in the 2026-11-16 re-review: it now asks whether the touching vCPU waits (memory-tiering, Misconceptions: "the VM that touched the page waited 900 µs"), not whether the VM is slowed. Q249 answered 2026-11-16: the touching vCPU waits for the full fetch, so H stays false; the Touching a page on NVMe line now agrees. Key A, C unchanged.
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
misconception: [B, I]
misconception_type: [consumption-as-contention, average-hides-worst]
pair: "0147"
status: draft
```
