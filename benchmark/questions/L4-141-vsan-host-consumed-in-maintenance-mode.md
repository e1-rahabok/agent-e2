# vSAN host Consumed with no VMs in maintenance mode

## Prompt
See [the vCenter memory chart of the host](0390/vcenter-host-memory-consumed-maintenance.png) and [its System Resource Reservation page](0390/vcenter-host-system-resource-reservation.png).

- An ESXi 9.1 host in a vSAN cluster sits empty in maintenance mode, waiting for a BIOS update.
- The firmware team sees that it still consumes memory with nothing on it, and asks whether to report a memory leak to the server vendor with the BIOS ticket.

Which statements are correct?

- A. Consumed fell when the VMs left and then stayed about level for the rest of the chart.
- B. Consumed fell to about 0 once the last VM had left the host for maintenance.
- C. With no VMs left, Consumed holds the host's own working memory: kernel modules, vSAN and other services.
- D. An empty host's Consumed should match the memory figure on the System Resource Reservation page.
- E. The System Resource Reservation figure is set aside for the host's own services, not measured use.
- F. The steady Consumed of the empty host is a kernel memory leak to report to the vendor.
- G. Only vSAN keeps an empty host's Consumed above 0; a host without it would show none.
- H. Restart the host before it returns to service, so that it starts again with Consumed at 0.
- I. The VMs took their overhead memory with them when they moved to the other hosts.

## Input to supply
- Product: vSphere Client 9.1; one ESXi host in a vSAN cluster.
- Screen 1: vSphere Client > the host > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past week (or a custom range of 3-4 days) that covers the hours before the host entered maintenance mode and at least one day after; counter Consumed (KB); target the host. Save as `benchmark/questions/0390/vcenter-host-memory-consumed-maintenance.png`.
- Screen 2: vSphere Client > the host > Configure > System > System Resource Reservation, with the memory value visible. Save as `benchmark/questions/0390/vcenter-host-system-resource-reservation.png`.
- Condition the key depends on:
  - Consumed drops when the host enters maintenance mode, then stays flat (within 10%) and above 10 GB at every point of at least one day with 0 VMs, with no upward trend;
  - the memory reservation on screen 2 differs from that flat Consumed by 20% or more, in either direction;
  - neither value within 1 GB of 17, 32, 41, 49 or 57 GB (numbers of the knowledge base and of 0056).
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
D: "With no VMs, Consumed should show what the kernel has reserved." Or F: "An empty host should consume almost nothing: a leak."

## Expected key points
- Answer: A, C, E, I.
- A true: the chart shows the step down at the evacuation and a level line after it.
- B false: with 0 VMs the line stays above 10 GB.
- C true: host Consumed counts every ESXi page in use: VMs, VM overhead and all kernel processes, vSAN included. With 0 VMs it is the kernel and its services.
- D false: Consumed is actual use, not reservation; on an empty host the two can sit far apart.
- E true: the reservation is what the host sets aside for its own services; what they use shows in Consumed.
- F false: vSAN and the kernel modules keep their memory with no VMs; a level Consumed after the evacuation is their steady use, not growth.
- G false: over-correction. Without vSAN the kernel, its processes and NSX still consume memory; an empty host does not read 0.
- H false: the wrong action. Nothing leaks; after a restart the kernel and vSAN take their memory again.
- I true: VM overhead is part of host Consumed while the VMs run and leaves with them; what stays is the host's own use.

## Notes
- Paired with 0056 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C16.
- No option says whether the kernel reservation is above or below kernel use: that is open (author question Q202). No option names the VCF Operations metric ESX System Usage (open author question Q215).
- The System Resource Reservation page is the one the CPU Demand files point to (vsphere/technology/cpu/metrics/host/demand); here only its memory value is read.
- Review fixes 2026-11-15: new situation (firmware wait, vendor leak report); options reworded away from 0056; screen readings added (A true, B false; B is not the negation of A); the condition keeps the knowledge-base and 0056 numbers out. Key A, D, G → A, C, E, I.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0390"
title: "vSAN host Consumed with no VMs in maintenance mode"
product: [vsphere, vsan]
technology: [memory, system]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/metrics/host/consumed
  - vsphere/architecture/overhead
  - vsphere/technology/cpu/metrics/host/demand
knowledge_main: vsphere/technology/memory/metrics/host/consumed
attachments:
  - 0390/vcenter-host-memory-consumed-maintenance.png
  - 0390/vcenter-host-system-resource-reservation.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C16"
answer: [A, C, E, I]
misconception: [D, F]
misconception_type: [provider-vs-consumer]
pair: "0056"
status: awaiting-input
```
