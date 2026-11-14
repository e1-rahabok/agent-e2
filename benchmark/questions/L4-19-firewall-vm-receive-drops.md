# Receive drops on a firewall VM

## Prompt
- A virtual firewall appliance (VMXNET3 vNIC, 8 vCPUs) shows about 2,600 received packets dropped every 5 minutes at peak traffic.
- Its CPU Ready is below 1% and no single vCPU is saturated inside the appliance.
- The host uplinks show no drops and no errors.
- On the host, vsish counters for its port (cumulative), read twice 5 minutes apart at peak:
  - clientStats: droppedRx rose by 2,620.
  - vmxnet3 rxSummary: running out of buffers rose by 2,620; number of times the 1st ring is full rose by 354; 1st ring size 512; 2nd ring size 512; all other reasons unchanged at 0.

What causes the drops, and what do you change? What would you check before changing it?

## Likely wrong answer
"The physical network is congested: ask for a faster uplink, or ask the network team to check the switch."

## Expected key points
- The VM's receive ring is too small for the bursts: the drop count matches "running out of buffers", and the 1st ring is full hundreds of times. All other drop reasons are 0.
- The drop happens inside the host, between the virtual switch and the guest driver, not on the physical network: the uplinks show nothing.
- Fix: raise the receive ring size in the guest's VMXNET3 driver (512 is small; for example 2,048 or more, within the driver's maximum).
- Check first that the guest drains the ring in time: no vCPU waiting on Ready or Co-stop, no vCPU saturated by packet processing. A larger ring absorbs a burst; it does not help a guest that cannot keep up.
- For a network appliance, also check whether the VM uses receive side scaling (RSS), so several vCPUs process its receive queues.
- vSphere charts show that packets are dropped, not why: vsish on the host shows the reason.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12: the ring size advice no longer cites the book; Ready and per-vCPU saturation added to the stem so the ring, not CPU, is the cause. After the independent review: vsish counters read as increases; Broadcom KB 2039495 (VMXNET3 loss in high bursts when buffers run out) moved here from the key.
## Metadata
```yaml
id: "0060"
title: "Receive drops on a firewall VM"
product: [vsphere]
technology: [network]
object: [vm, guest-os]
tool: [vcenter, esxtop]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/network/vnic-rx-drops
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/configuration/rss-and-interrupt-coalescing
  - vsphere/technology/network/concepts/packet-drop-accounting
knowledge_main: vsphere/technology/network/vnic-rx-drops
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [layer-confusion]
status: draft
```
