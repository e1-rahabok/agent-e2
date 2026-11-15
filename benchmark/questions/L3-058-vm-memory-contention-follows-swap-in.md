# VM memory contention follows swap-in, not the balloon

## Prompt
See [the VCF Operations memory charts of the VM](0392/vcf-operations-vm-contention-balloon-swap-in-24h.png).

- A Windows VM runs a reporting service. Its owner reports slow reports at several times yesterday.
- The vSphere team points at the balloon on the VM and proposes to remove the balloon driver from it.

Which statements are correct?

- A. Each rise in Memory Contention falls in an interval in which Swap In Rate is above 0.
- B. A vCPU that touches a page in the swap file stops until ESXi has read the page back.
- C. Memory Contention stays above 0 for most of the day.
- D. Memory Contention climbs and falls with the balloon line.
- E. The larger the balloon, the larger the share of time the VM spends waiting on memory.
- F. Read as a percentage, Memory Contention gives the part of the VM's memory that has left DRAM.
- G. Decompression never adds to Memory Contention; only reads from the swap file do.
- H. Remove the balloon driver so that the VM stops waiting for memory.

## Input to supply
- Product: VCF Operations 9.1; a Windows VM with VMware Tools, on a host under memory pressure for part of the day.
- Screen: VCF Operations > the VM > Metrics, last 24 hours, three charts stacked, with the names of the VCF Operations 9.1 VM metric list: Mem|Contention (%), Mem|Balloon (%), Mem|Swap In Rate (KBps) (all three enabled by default). Save as `benchmark/questions/0392/vcf-operations-vm-contention-balloon-swap-in-24h.png`.
- Condition the key depends on:
  - Mem|Balloon (%) at 10 or more for most of the 24 hours, including hours in which Mem|Contention (%) is 0;
  - Mem|Contention (%) above 0.5 in at least two separate intervals, each one an interval in which Mem|Swap In Rate is above 0;
  - Mem|Contention (%) 0 at every point at which Mem|Swap In Rate is 0;
  - Mem|Swap In Rate above 0 for less than a quarter of the 24 hours.
- How to produce it: a field VM matches more often than a lab; in a lab, overcommit a small host so this VM is ballooned, then let its guest touch more memory than is left to it for short periods, so that ESXi swaps and the guest reads pages back.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
E: "The balloon is memory the VM is waiting for, so it drives contention." Or F: the percentage read as a share of memory.

## Expected key points
- Answer: A, B.
- A true: on the charts, Contention is above 0 only in intervals where Swap In Rate is above 0.
- B true: Memory Contention is the share of time a vCPU waits for a page fault ESXi resolves; a swap-in is such a fault, so the counter tracks swap-in closely.
- C false: Contention is above 0 only in the short intervals with swap-in, and 0 for most of the day.
- D false: the balloon stays high through hours in which Contention is 0.
- E false: the balloon is reclamation inside the guest; ESXi sees no fault on those pages, and the counter excludes balloon activity.
- F false: the counter is a share of time, not of memory space, and not a latency in nanoseconds.
- G false: over-correction. The counter covers decompression of a compressed page too (and copy-on-write breaks); swap-in is most of it.
- H false: the wrong action. The balloon is not what the VM waits on, and without the balloon driver ESXi can only compress or swap, blind to which pages the guest uses: it can take pages the guest needs, and the VM waits when it touches them.

## Notes
- Paired with 0149 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C27.
- Metric names from the VCF Operations 9.1 Virtual Machine metric list (TechDocs, updated 2026-11-12): https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/virtual-machine-metrics.html. Memory|Balloon (KB) is disabled by default there; Mem|Balloon (%) is enabled.
- Review fixes 2026-11-15: options reworded away from 0149; screen readings added (A true; C and D false); the balloon metric named. Key A, B → A, B.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0392"
title: "VM memory contention follows swap-in, not the balloon"
product: [vsphere, vcf-operations, windows]
technology: [memory]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/latency
attachments:
  - 0392/vcf-operations-vm-contention-balloon-swap-in-24h.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C27"
answer: [A, B]
misconception: [E, F]
misconception_type: [reclamation-as-contention, unit-and-normalization]
pair: "0149"
status: awaiting-input
```
