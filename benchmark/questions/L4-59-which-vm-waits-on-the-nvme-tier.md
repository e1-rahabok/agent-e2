# Which VM waits on the NVMe memory tier?

## Prompt
- ESXi 9.1 host with memory tiering: 1 TB of DRAM and a 1 TB NVMe tier (ratio 1:1). No memory overcommit beyond the two tiers.
- Host, last hour: active memory about 380 GB; tier 1 consumed about 600 GB; NVMe tier read bandwidth about 310 MBps; NVMe read latency 180-260 µs.
- Two application teams report slowness: the owners of `oltp-02` and of `cache-04`. `cache-04` runs a session cache that mostly writes.
- [The attached per-VM table](0147/tiered-host-per-vm-1-hour.csv) was built from the vSphere Client per-VM tier charts and `memstats` (tier1Consumed), averaged over the last hour.

Which statements are correct?

- A. `arch-01` waits most on NVMe: it holds the most memory on the tier, so most of its page touches land on NVMe.
- B. `oltp-02` waits on NVMe: it reads about 140 MBps of pages back, and each fetch stalls the vCPU that touched it.
- C. `etl-03` waits on NVMe writes: it has the highest write bandwidth, and each write holds its vCPU until done.
- D. `cache-04` mostly writes, yet shows NVMe reads: a write to a page on NVMe waits for the page to come back to DRAM.
- E. No VM here is slowed by tiering: host active memory is below 50% of DRAM, the line Broadcom gives for good tiering.
- F. If tiering is turned off for `oltp-02`, it also needs a full reservation, or its pages can end up in the host swap file.

## Likely wrong answer
A: the most memory on NVMe read as the most waiting. Or E: the host average read as every VM's experience.

## Expected key points
- Answer: B, D, F.
- A is wrong: tier 1 consumed is cold pages. It is saturation, not a wait. `arch-01` reads almost nothing back (0.2 MBps), so its pages stay cold.
- B: NVMe read bandwidth is the performance signal. A fetch costs about 100-200 µs against about 100 ns from DRAM; at 140 MBps that is tens of thousands of fetches each second for one VM.
- C is wrong: NVMe write bandwidth is demotion, cold pages moved down in the background, off the vCPU's path. It costs device wear and can raise read latency, but the VM does not wait on it.
- D: the CPU cannot write to NVMe directly. A guest write to a cold page first fetches it, so it shows as read bandwidth.
- E is wrong: the host figure is an average. Per-VM read bandwidth shows who pays: two VMs account for most of the 310 MBps.
- F: a VM with tiering turned off needs a full memory reservation (vSphere 9.1 documentation, Deactivate Memory Tiering for a VM): it competes for DRAM with the tiered VMs, and without the reservation its pages can go to the host swap file, slower than NVMe. A tiered VM's reservation, by contrast, can be served partly from NVMe.

## Notes
- Sources: vSphere 9.1 documentation, vSphere Resource Management > Memory Tiering over NVMe (per-VM and per-tier counters, VMs kept in DRAM, full reservation); Memory Tiering Performance, VCF 9.0 performance study (https://www.vmware.com/docs/memtier-vcf9-perf), Using and monitoring Memory Tiering; the knowledge base, memory tiering and the decision tree "Is memory tiering slowing this host?".
- The plan's slot was "memory latency on a tiered host". Whether VM memory contention counts tier-1 fetches is not stated by any source read (knowledge base review note), so the question asks for the per-VM tier counters instead.

## Metadata
```yaml
id: "0147"
title: "Which VM waits on the NVMe memory tier?"
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host
  - vsphere/technology/memory/concepts/memory-tiering
knowledge_main: vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host
attachments:
  - 0147/tiered-host-per-vm-1-hour.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the memory slots (project/plan.md, M2)"
answer: [B, D, F]
misconception: [A, E]
misconception_type: [consumption-as-contention, average-hides-worst]
status: draft
```
