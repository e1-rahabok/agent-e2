# PowerCLI memory report of a SQL Server VM

## Prompt
- sql-07 is a Windows Server VM running SQL Server, with 32,768 MB of memory configured, no reservation and no limit. Its host, esx-22, stays at 71% memory Consumed all week, in the esxtop memory state high.
- A capacity script in PowerCLI collects, as Past day averages, the VM's quick statistics (`ExtensionData.Summary.QuickStats`) and vCenter performance counters (`Get-Stat`):

| Field | Value |
|---|---|
| QuickStats GuestMemoryUsage | 1,966 MB |
| QuickStats HostMemoryUsage | 33,840 MB |
| mem.consumed.average | 32,700 MB |
| mem.entitlement.average | 22,118 MB |
| mem.vmmemctl.average (Ballooned) | 0 |
| mem.swapped.average, mem.compressed.average | 0, 0 |
| mem.latency.average | 0% |

- Inside Windows, Task Manager shows 29.4 GB in use, most of it the SQL Server buffer pool.
- The capacity team proposes three things: cut sql-07 to 4 GB because GuestMemoryUsage shows about 2 GB; drop every row with HostMemoryUsage above the configured memory as bad data; and set a 32 GB reservation, because Entitlement shows ESXi holding back about 10 GB.

Which statements are correct?

- A. GuestMemoryUsage is ESXi's Active estimate for the VM, not a counter read from Windows.
- B. GuestMemoryUsage is the memory Windows reports in use, collected through VMware Tools.
- C. HostMemoryUsage adds the VM's overhead to the host memory the VM consumes.
- D. HostMemoryUsage above the 32,768 MB configured is bad data that the report should drop.
- E. Like HostMemoryUsage, the VM's Consumed counter can pass 32,768 MB when SQL Server grows.
- F. The VM's overhead in this sample is about 1,140 MB.
- G. Entitlement of about 21.6 GB shows ESXi holding back about 10 GB of memory the VM asked for.
- H. Entitlement below configured memory, with nothing ballooned, compressed or swapped and Latency at 0, is no sign of a memory shortage.
- I. Entitlement equals Granted plus overhead, so Windows has touched only about 21 GB.
- J. A 32 GB reservation would lift Entitlement to 32 GB and close the gap.
- K. Cut sql-07 to 4 GB of memory, as the guest uses about 2 GB.

## Likely wrong answer
B: "GuestMemoryUsage is what Windows uses." D: "A VM cannot use more than its configured memory, so those rows are bad data." G: "Entitlement below configured means ESXi gives the VM less than it needs."

## Expected key points
- Answer: A, C, F, H.
- A is correct: in the vSphere API quick statistics, Guest memory usage (`guestMemoryUsage`) is active guest memory: the Active estimate, a sampled ESXi estimate, not Consumed and not a Guest OS counter.
- B is wrong: layer confusion. The value comes from ESXi's sampling, not from Windows; Windows shows 29.4 GB in use.
- C is correct: Host memory usage (`hostMemoryUsage`) is consumed host memory including the VM's overhead, so it reads above Consumed, which excludes overhead.
- D is wrong: the overhead sits on top of Consumed, so HostMemoryUsage above configured memory is normal for a VM whose Consumed is near configured.
- E is wrong: over-correction. Consumed is capped by configured memory (and by a limit): it can reach it, not exceed it.
- F is correct: 33,840 - 32,700 = 1,140 MB.
- G is wrong: the misconception of VM Memory Entitlement ("Entitlement below configured memory means the VM is short of memory"). Entitlement is a value of the ESXi memory scheduler, not memory withheld: at rest it can sit below configured memory with nothing reclaimed.
- H is correct: Entitlement below configured is a fault only with reclamation or Latency beside it; here Ballooned, Swapped, Compressed and Latency are 0 and the host is in high.
- I is wrong: the misconception "Entitlement = Granted + Overhead". The API gives no formula; the scheduler computes it from estimated demand and the reservation, limit and shares.
- J is wrong: Entitlement does not follow a reservation; setting and removing a reservation left it where it was.
- K is wrong: the wrong action. GuestMemoryUsage is Active, a kernel estimate that misses the buffer pool SQL Server holds; Windows has 29.4 GB in use.

## Notes
- Sources: the knowledge base, VM Memory Consumed (Formula: the API quick statistics `guestMemoryUsage` and `hostMemoryUsage`; Consumed excludes overhead and cannot exceed configured memory), VM Memory Active (sampled ESXi estimate), VM Memory Entitlement (scheduler value; below configured memory is no fault without reclamation or Latency; does not follow a reservation; no formula).
- Author decision Q230 (2026-11-15): Entitlement is tested here only as the knowledge base now defines it, a scheduler value with one troubleshooting use.
- The overhead of 1,140 MB is about 3.5% of 32 GB, inside the range of documented per-VM overhead.

## Metadata
```yaml
id: "0453"
title: PowerCLI memory report of a SQL Server VM
product: [vsphere, windows]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/entitlement
  - vsphere/technology/memory/metrics/virtual-motherboard/active
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/entitlement
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/memory/metrics/virtual-motherboard/entitlement"
answer: [A, C, F, H]
misconception: [B, D, G]
misconception_type: [layer-confusion, consumption-as-contention]
status: draft
```
