# One VM waits for memory while the host latency stays low

## Prompt
See [the vCenter memory latency chart of the host](0403/vcenter-host-memory-latency-past-day.png) and [the vCenter memory latency chart of one of its VMs](0403/vcenter-vm-memory-latency-past-day.png).

- Users of an application report that it was slow for about half an hour yesterday.
- The host team checks the host's memory Latency, sees it low all day, and wants to close the ticket as not a memory problem.

Which statements are correct?

- A. The host value stays low because it averages all the host's running VMs.
- B. The host's low memory Latency shows that no VM on it waited for memory yesterday.
- C. The VM's vCPUs waited on page faults for 5% or more of their time for about half an hour.
- D. The host value would show the wait only if all its VMs waited at the same time.
- E. Close the ticket: the host's low value rules out a memory wait on any of its VMs.
- F. To find the VMs that waited, list the highest VM memory Latency among the host's VMs.
- G. The VM's Latency value is the share of its memory that ESXi holds on disk.

## Input to supply
- Product: vSphere Client 9.1. One ESXi host running 10 VMs or more.
- Lab step: on one VM, make the guest touch more memory than ESXi lets it keep for about 30 minutes (for example a memory limit well below the guest's working set, with a memory load tool in the guest), then remove the cause.
- Screen 1: vSphere Client > the host > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past day; counter Latency (%); target the host. Save as `benchmark/questions/0403/vcenter-host-memory-latency-past-day.png`.
- Screen 2: vSphere Client > that VM > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past day; counter Latency (%); target the VM. Save as `benchmark/questions/0403/vcenter-vm-memory-latency-past-day.png`.
- Condition the key depends on:
  - host Latency at 0.5% or less for the whole day;
  - the VM's Latency at 5% or more for 20-40 minutes in the same day, and near 0 the rest of the day.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: "Host memory latency stayed low, so no VM waited: not a memory problem."

## Expected key points
- Answer: A, C, F.
- A true: host memory Latency is a normalized average of the running VMs' Latency; one VM's wait is diluted by the others.
- B false: the average hides the VM that suffers, as the VM chart shows.
- C true: the VM chart shows Latency at 5% or more for about half an hour: its vCPUs waited for page faults ESXi resolves, mostly swap-in.
- D false: over-correction. Any VM's wait adds to the average; one VM among many moves it only a little.
- E false: the wrong action from B. The VM waited on memory in the window the users report.
- F true: the worst VM decides; read the maximum VM memory Latency (VCF Operations Memory Contention) across the host's VMs.
- G false: Latency is a share of time, not of memory space.

## Notes
- Paired with 0402 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D13.
- The knowledge base does not say how the host value weights its VMs, so no option computes it.
- The lab step only produces the condition; no option rests on why the VM waited (a limit's effects touch open author questions Q205 and Q214).
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
answer: [A, C, F]
misconception: [B]
misconception_type: [average-hides-worst]
pair: "0402"
status: awaiting-input
```
