# VM health check: a slow night job with four resources to read

## Prompt
- db-erp-02: 8 vCPUs, 48 GB, Windows Server 2022, powered on 41 days. No vMotion and no HA restart in the last 7 days. The host runs its cores at about 2.5 GHz against a nominal 2.0 GHz.
- The owner reports that the nightly job at 02:00 took three times longer last night. Nothing else changed.
- VCF Operations, 02:00 to 03:00, worst 5-minute cycle of the hour. The "peak" values are the highest 20-second value within the 5-minute cycle:
  - CPU: Usage 89%, Net Run 71%, Ready 0.7% (5-minute average), peak vCPU Ready 1.4%, peak vCPU Co-stop 0.3%.
  - Memory: Consumed 48 GB (100% of configured), Ballooned 11 GB, Swapped 3 GB, Compressed 1.5 GB, Swap-in rate 0 KBps, Memory Contention 0% (5-minute average and peak).
  - Disk, all virtual disks: read latency 4 ms and write latency 6 ms (5-minute averages). Peak latency within the collection cycle: 410 ms in the cycles starting 02:10 and 02:15, below 25 ms in every other cycle.
  - Network: peak transmitted packets dropped 0%, received packets dropped 0.
- Inside Windows, 5-minute average: processor queue length 3.5 on 8 vCPUs.

You run the health check on this VM. Which statements are correct?

- A. Memory is the main finding: 11 GB ballooned, 3 GB swapped and Consumed at 100% show the VM is short of memory.
- B. CPU Usage of 89% is consumption that includes the Turbo gain; it does not show that the VM waited.
- C. CPU is not a finding: peak Ready 1.4% and peak Co-stop 0.3% are a small share of the 71% Net Run.
- D. Disk is fine, because the 5-minute read and write latency stay low at 4 ms and 6 ms in that hour.
- E. The 410 ms peak tells which of the VM's virtual disks was slow, so the flow can start there.
- F. Balloon, swap and compression are past reclamation; Memory Contention 0% and no swap-in mean no memory wait.
- G. Storage is the finding: the 5-minute averages hide a 410 ms peak in the 02:10 and 02:15 cycles.
- H. Next, open the storage flow: each virtual disk, read and write apart, outstanding IO, then KAVG, DAVG and QAVG.
- I. The VM's network latency counter in vCenter must be read before the network can be ruled out.
- J. The health check reads consumption first and looks at contention only when consumption is high.
- K. Network is not a finding: dropped packets, the only network contention counter of a VM, are 0.
- L. This data proves that the slow nightly job lines up in time with the 410 ms latency peak.
- M. The data points to adding vCPUs and memory to the VM before the next nightly run.
- N. The Windows processor queue belongs to the Guest OS layer, outside the VM health check.

## Likely wrong answer
- A: "Memory is the problem: ballooned 11 GB, swapped 3 GB and Consumed at 100%."
- M: "CPU Usage is high at 89% and memory is full: add memory and vCPUs."
- D: "All 5-minute averages are low, so the VM is healthy and the cause is the application."

## Expected key points
- Answer: B, C, F, G, H, K, N.
- A is false: the misconception; Ballooned, Swapped and Compressed are amounts reclaimed earlier, and Consumed is consumption. The balloon is a leading warning about host pressure, not proof that this VM is slow.
- B is true: Usage counts the delivered frequency (2.5 GHz against 2.0 GHz nominal) while Run is 71%; consumption sizes the VM, contention shows waiting. Read contention first.
- C is true: 1.4% + 0.3% against 71% Net Run is a loss of about 2% of the time the vCPUs wanted to run.
- D is false: the misconception; the 5-minute averages hide the 20-second peak of 410 ms.
- E is false: the peak is one value for the VM, taken across all virtual disks and both directions; it does not say which disk.
- F is true: the current wait is Memory Contention (vSphere memory latency), 0%, and the swap-in rate is 0.
- G is true: only the disk peak is a wait; 410 ms in two cycles inside the job window is the finding.
- H is true: the storage flow reads per virtual disk, read and write apart, outstanding IO, then the host's KAVG, DAVG and QAVG, and what ran on the datastore in that window.
- I is false: vSphere has no VM network latency counter.
- J is false: contention first, consumption after; consumption sizes the VM and does not show whether it waits. Efficiency (sizing) comes last.
- K is true: received and transmitted drops are 0.
- L is false: the data gives only the job's start (02:00) and that it took three times longer, not when it ran slow; the peak is one value per 5-minute cycle, with no time inside it. Check the job's timeline against the two cycles.
- M is false: CPU waits are about 2% of the run time and memory wait is 0%; adding vCPUs or memory does not address a storage wait.
- N is true: run queue, page-outs and disk queue inside the guest belong to the Guest OS layer, checked as its own object. If the storage flow finds nothing, the wait is inside the Guest OS.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Public source: Broadcom KB 444403, Understanding "Peak" or "Worst" Performance Metrics in VMware VCF / Aria Operations (VCF Operations 9.x and Aria Operations 8.x; the page shows no updated date): VCF Operations polls vCenter every 5 minutes, takes 15 samples of 20 seconds, and the peak metrics show the highest of them; averages hide short spikes. Mechanism of memory counters: Balloon, Swapped and Compressed are amounts, Memory Contention (vSphere mem.latency, "time spent waiting to swap in or decompress guest physical memory") is the wait. Turbo: Usage counts the delivered frequency.
- Why one answer: the numbers decide it. Only the disk peak is a wait; CPU waits are about 2% of the run time and memory wait is 0%. The order contention, then consumption, then sizing is the design logic of the VM check (section Principle and Order rationale of the VM health check file).
- Debatable risk: low. The only judgment is how much to say about the balloon: the key calls it a leading warning, not a finding of a slow VM, which follows from the counter definitions. The 410 ms figure is chosen far above any latency threshold, so no threshold is argued.
- Rests on: the knowledge file's design logic (vm-health-check, Principle, Checks 3 to 6, Order rationale) and the vendor definitions above.

## Metadata
```yaml
id: "0350"
title: "VM health check: a slow night job with four resources to read"
product: [vsphere, vcf-operations, windows]
technology: [cpu, memory, storage, network]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [B, C, F, G, H, K, N]
misconception: [A, M, D]
input: [text]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/vm/vm-health-check
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
  - vsphere/technology/cpu/metrics/comparisons/consumption-metrics
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
knowledge_main: vsphere/object-types/vm/vm-health-check
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [consumption-as-contention, reclamation-as-contention, average-hides-worst]
status: draft
```
