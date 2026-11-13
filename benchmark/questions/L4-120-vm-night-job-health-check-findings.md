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

You run the health check on this VM. Which findings do you report, in which order, and which readings are not findings? What do you open next, and what can this data not prove?

## Likely wrong answer
"Memory is the problem: ballooned 11 GB, swapped 3 GB and Consumed at 100%. CPU Usage is also high at 89%. Add memory and vCPUs." Or "All 5-minute averages are low, so the VM is healthy and the cause is the application."

## Expected key points
- Read contention first, consumption after. CPU Usage 89% and Consumed 100% are consumption: Usage includes the Turbo gain (2.5 GHz against 2.0 GHz nominal), and Run is 71%. They size the VM; they do not show that it waited.
- CPU is not a finding: peak Ready 1.4% and peak Co-stop 0.3% against Run of 71% is a loss of about 2% of the time the vCPUs wanted to run.
- Memory is not a finding now: Ballooned, Swapped and Compressed are reclamation that happened earlier. The current wait is Memory Contention (latency), 0%, and the swap-in rate is 0. The balloon is a leading warning about host pressure, for the configuration step (limit, reservation, host state), not a slow VM.
- Storage is the finding: the 5-minute averages (4 and 6 ms) hide a 20-second peak of 410 ms in two cycles, 02:10 and 02:15. This opens the storage flow: virtual disk, read and write apart, outstanding IO, then KAVG, DAVG and QAVG on the host, and what ran on the datastore in that window.
- Network is not a finding: dropped packets are the only network contention counter of a VM, and they are 0. vSphere has no network latency counter.
- Limits of the data: the peak is one value for the VM, taken across all virtual disks and both directions, so it does not say which disk, and the peaks of different metrics can come from different 20-second blocks, so it does not prove the slow job lines up with the peak. Check the job's timeline against the two cycles.
- The Windows queue and page-out are the Guest OS layer, outside the VM health check. If the storage flow finds nothing, the wait is inside the Guest OS. Efficiency (sizing) comes last and is not decided from Consumed.

## Notes
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
answer_type: judged
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
