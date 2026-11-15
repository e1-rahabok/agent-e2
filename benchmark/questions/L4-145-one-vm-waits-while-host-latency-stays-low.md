# One VM waits for memory while the host latency stays low

## Prompt
See [the vCenter memory latency chart of the host](0403/vcenter-host-memory-latency-past-day.png) and [the vCenter memory latency chart of one of its VMs](0403/vcenter-vm-memory-latency-past-day.png).

- Users of an application report that it was slow for about half an hour yesterday.
- The host team checks the host's memory Latency, sees it low all day, and wants to close the ticket as not a memory problem.

Which statements are correct?

- A. The host line dilutes one VM's wait across all the VMs running on the host.
- B. The flat, low host line shows that every VM on the host got the memory it touched without waiting.
- C. The VM's line shows its vCPUs stalled on page faults 5% or more of the time for about half an hour.
- D. The host line rises above 1% in the same half hour as the VM's line peaks.
- E. The host line would react only if all of the host's VMs waited together.
- F. Mark the ticket as not a memory issue on the strength of the host chart.
- G. To find who waited, rank the host's VMs by their own memory Latency or Memory Contention.
- H. The VM's peak value is the part of its memory that ESXi had put on disk.

## Input to supply
- Product: vSphere Client 9.1. One ESXi host running 20 VMs or more.
- Lab step: on one VM, make the guest touch more memory than ESXi lets it keep for about 30 minutes (for example a memory limit well below the guest's working set, with a memory load tool in the guest), then remove the cause.
- Screen 1: vSphere Client > the host > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past day; counter Latency (%); target the host. Save as `benchmark/questions/0403/vcenter-host-memory-latency-past-day.png`.
- Screen 2: vSphere Client > that VM > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past day; counter Latency (%); target the VM. Save as `benchmark/questions/0403/vcenter-vm-memory-latency-past-day.png`.
- Condition the key depends on:
  - the host runs 20 VMs or more all day;
  - host Latency at 0.5% or less at every point of the day;
  - the VM's Latency between 5% and 10% for 20-40 minutes in the same day, and 0 at every other point.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: "The host's memory latency stayed low, so no VM waited: not a memory problem."

## Expected key points
- Answer: A, C, G.
- A true: host memory Latency is a normalized average of the running VMs' Latency; one VM's wait among 20 or more is diluted, as the host line shows.
- B false: the average hides the VM that suffers, as the VM chart shows.
- C true: the VM chart shows Latency of 5% or more for about half an hour: its vCPUs waited for page faults ESXi resolves, mostly swap-in.
- D false: the host line stays at 0.5% or less at every point of the day.
- E false: over-correction. Any VM's wait adds to the average; one VM among many moves it only a little.
- F false: the wrong action from B. The VM waited on memory in the window the users report.
- G true: the worst VM decides; read the maximum VM memory Latency (VCF Operations Memory Contention) across the host's VMs.
- H false: Latency is a share of time, not of memory space.

## Notes
- Paired with 0402 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D13.
- The knowledge base does not say how the host value weights its VMs, so no option computes it; the condition keeps the VM at 5-10% among 20 or more VMs so that the host line stays low.
- The lab step only produces the condition; no option rests on why the VM waited (a limit's effects touch open author questions Q205 and Q214).
- Review fixes 2026-11-15: options reworded away from 0402; a false screen reading added (D); the condition fixes 20 VMs or more and the VM at 5-10%. Key A, C, F → A, C, G.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0403"
title: "One VM waits for memory while the host latency stays low"
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/host/latency
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - sp5-framework/observability/aggregation
knowledge_main: vsphere/technology/memory/metrics/host/latency
attachments:
  - 0403/vcenter-host-memory-latency-past-day.png
  - 0403/vcenter-vm-memory-latency-past-day.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D13"
answer: [A, C, G]
misconception: [B]
misconception_type: [average-hides-worst]
pair: "0402"
status: awaiting-input
```
