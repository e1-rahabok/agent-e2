# VM health check: a slow night job with four resources to read

## Prompt
- db-erp-02: 8 vCPUs, 48 GB, Windows Server 2022, powered on 41 days. No vMotion and no HA restart in the last 7 days. The host runs its cores at about 2.5 GHz against a nominal 2.0 GHz.
- The owner reports that the nightly job at 02:00 took three times longer last night. Nothing else changed.
- VCF Operations, 02:00 to 03:00, worst 5-minute cycle of the hour. The "peak" values are the highest 20-second value within the 5-minute cycle:
  - CPU: Usage 89%, Net Run 71%, Ready 0.7% (5-minute average), peak vCPU Ready 1.4%, peak vCPU Co-stop 0.3%.
  - Memory: Consumed 28 GB (58% of configured), Ballooned 11 GB, Swapped 3 GB, Compressed 1.5 GB, Swap-in rate 0 KBps, Memory Contention 0% (5-minute average and peak).
  - Disk, all virtual disks: read latency 4 ms and write latency 6 ms (5-minute averages). Peak latency within the collection cycle: 410 ms in the cycles starting 02:10 and 02:15, below 25 ms in every other cycle.
  - Network: peak transmitted packets dropped 0%, received packets dropped 0.
- Inside Windows, 5-minute average: processor queue length 3.5 on 8 vCPUs.

You run the health check on this VM. Which statements are correct?

- A. CPU is not a finding: peak vCPU Ready is 1.4% and peak vCPU Co-stop 0.3%.
- B. The 410 ms peak tells which of the VM's virtual disks was slow, so the flow can start there.
- C. Storage is the finding: the peak disk latency reached 410 ms in the 02:10 and 02:15 cycles.
- D. Next, open the storage flow: each virtual disk, outstanding IO, then KAVG, DAVG and QAVG.
- E. The VM's network latency counter in vCenter must be read before the network can be ruled out.
- F. The health check reads consumption first and looks at contention only when consumption is high.
- G. Network is not a finding: dropped packets, the only network contention counter of a VM, are 0.
- H. This data proves that the slow nightly job lines up in time with the 410 ms latency peak.
- I. The data points to adding vCPUs and memory to the VM before the next nightly run.
- J. The Windows processor queue belongs to the Guest OS layer, outside the VM health check.

## Likely wrong answer
- I: "CPU Usage is high at 89% and 11 GB is ballooned and 3 GB swapped: add memory and vCPUs."
- F: "Start with what the VM uses; contention only matters when usage is high."

## Expected key points
- Answer: A, C, D, G, J.
- A is true: peak Ready 1.4% and peak Co-stop 0.3% per vCPU are low; the vCPUs got the physical CPU they asked for.
- B is false: the peak is one value for the VM, taken across all virtual disks and both directions; it does not say which disk.
- C is true: only the disk peak is a wait; 410 ms in two cycles inside the job window is the finding, and the 5-minute averages of 4 and 6 ms hide it.
- D is true: the storage flow reads latency per virtual disk, outstanding IO, then the host's KAVG, DAVG and QAVG, and what ran on the datastore in that window.
- E is false: vSphere has no VM network latency counter.
- F is false: contention first, consumption after; consumption sizes the VM and does not show whether it waits. Efficiency (sizing) comes last.
- G is true: received and transmitted drops are 0.
- H is false: the data gives only the job's start (02:00) and that it took three times longer, not when it ran slow; the peak is one value per 5-minute cycle, with no time inside it. Check the job's timeline against the two cycles.
- I is false: CPU waits are small and Memory Contention is 0% with no swap-in, so the balloon, swap and compression amounts are past reclamation, not a wait; adding vCPUs or memory does not address a storage wait.
- J is true: run queue, page-outs and disk queue inside the guest belong to the Guest OS layer, checked as its own object. If the storage flow finds nothing, the wait is inside the Guest OS.

## Notes
- Public source: Broadcom KB 444403, Understanding "Peak" or "Worst" Performance Metrics in VMware VCF / Aria Operations (VCF Operations 9.x and Aria Operations 8.x; the page shows no updated date): VCF Operations polls vCenter every 5 minutes, takes 15 samples of 20 seconds, and the peak metrics show the highest of them; averages hide short spikes. Memory Contention (vSphere mem.latency, "time spent waiting to swap in or decompress guest physical memory") is the wait; Balloon, Swapped and Compressed are amounts.
- The 410 ms figure is chosen far above any latency threshold, so no threshold is argued.
- Rests on: vm-health-check, Principle, Checks 3 to 6, Order rationale.
- Changed in the 2026-11-15 audit: Consumed 48 GB (100%) beside 11 GB ballooned, 3 GB swapped and 1.5 GB compressed was impossible; now 28 GB (58%), under the breaker's bound of 29.5-32.5 GB. Redundancy: old A (balloon read as a wait, #40), B (Turbo puts Usage above Run, #19), D (5-minute average hides the peak, #13) and F (reclaimed amounts are not a wait, #38) dropped, each over the two-question cap with no untested fact of the same truth in the cited files; C reworded without the Run comparison (#15), G without "the averages hide" (#13), H without "read and write apart" (#51). Letters: C->A, E->B, G->C, H->D, I->E, J->F, K->G, L->H, M->I, N->J.

## Metadata
```yaml
id: "0350"
title: "VM health check: a slow night job with four resources to read"
product: [vsphere, vcf-operations, windows]
technology: [cpu, memory, storage, network]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A, C, D, G, J]
misconception: [I]
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
misconception_type: [consumption-as-contention, reclamation-as-contention]
status: draft
```
