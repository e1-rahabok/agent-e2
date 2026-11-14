# vSAN host Consumed with no VMs in maintenance mode

## Prompt
See [the vCenter memory chart of the host](0390/vcenter-host-memory-consumed-maintenance.png) and [its System Resource Reservation page](0390/vcenter-host-system-resource-reservation.png).

- An ESXi 9.1 host in a vSAN cluster entered maintenance mode two days ago; DRS moved all its VMs to other hosts.
- The capacity team expected its Consumed memory to fall to about 0. They ask whether the host leaks memory, and want it rebooted before it returns to service.

Which statements are correct?

- A. Consumed counts the kernel's own memory, vSAN included, so it stays above 0 with no VMs.
- B. With no VMs, Consumed should equal the memory reservation on the System Resource Reservation page.
- C. Consumed above 0 with no VMs shows a memory leak in the kernel.
- D. The memory reservation on that page is memory set aside for the kernel, not a reading of what it uses.
- E. On a host without vSAN, Consumed would fall to 0 once the last VM left.
- F. Reboot the host before it returns to service, to bring Consumed back to 0.
- G. The VMs' overhead memory left the host together with the VMs.

## Input to supply
- Product: vSphere Client 9.1; one ESXi host in a vSAN cluster.
- Screen 1: vSphere Client > the host > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past week (or a custom range of 3-4 days) that covers the hours before the host entered maintenance mode and at least one day after; counter Consumed (KB); target the host. Save as `benchmark/questions/0390/vcenter-host-memory-consumed-maintenance.png`.
- Screen 2: vSphere Client > the host > Configure > System > System Resource Reservation, with the memory value visible. Save as `benchmark/questions/0390/vcenter-host-system-resource-reservation.png`.
- Condition the key depends on:
  - Consumed drops when the host enters maintenance mode and then stays flat (within 10%) and above 10 GB for at least one day with 0 VMs;
  - the memory reservation on screen 2 differs from that flat Consumed by 20% or more, in either direction.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: "With no VMs, Consumed should show the kernel reservation." Or C: "An empty host should consume almost nothing: a leak."

## Expected key points
- Answer: A, D, G.
- A true: host Consumed counts every ESXi page in use: VMs, VM overhead and all kernel processes, vSAN included. With 0 VMs it is the kernel and vSAN.
- B false: Consumed is actual use, not reservation; the two can sit far apart on an empty host.
- C false: vSAN and the kernel modules keep their memory with no VMs; a flat Consumed after the evacuation is their steady use.
- D true: the reservation is what the host sets aside for its own services; what they use shows in Consumed.
- E false: over-correction. Without vSAN the kernel, its processes and NSX still consume memory; an empty host does not read 0.
- F false: the wrong action. Nothing leaks; after a reboot the kernel and vSAN take their memory again.
- G true: VM overhead is part of host Consumed while the VMs run and leaves with them; what stays is the kernel's own use.

## Notes
- Paired with 0056 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C16.
- No option says whether the kernel reservation is above or below kernel use: that is open (author question Q202). No option names the VCF Operations metric ESX System Usage (open author question Q215).
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
knowledge_main: vsphere/technology/memory/metrics/host/consumed
attachments:
  - 0390/vcenter-host-memory-consumed-maintenance.png
  - 0390/vcenter-host-system-resource-reservation.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C16"
answer: [A, D, G]
misconception: [B, C]
misconception_type: [provider-vs-consumer]
pair: "0056"
status: awaiting-input
```
