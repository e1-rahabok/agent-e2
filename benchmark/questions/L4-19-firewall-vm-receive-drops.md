# Receive drops on a firewall VM

## Prompt
- A virtual firewall appliance (VMXNET3 vNIC, 8 vCPUs) shows about 2,600 received packets dropped every 5 minutes at peak traffic.
- Its CPU Ready is below 1% and no single vCPU is saturated inside the appliance.
- The host uplinks show no drops and no errors.
- On the host, vsish counters for its port (cumulative), read twice 5 minutes apart at peak:
  - clientStats: droppedRx rose by 2,620.
  - vmxnet3 rxSummary: running out of buffers rose by 2,620; number of times the 1st ring is full rose by 354; 1st ring size 512; 2nd ring size 512; all other reasons unchanged at 0.

Which statements about the cause, the fix and the checks before the fix are correct?

- A. The drops happen inside the host, between the virtual switch port and the guest driver.
- B. The physical network is congested: ask for faster uplinks, or ask the network team to check the switch.
- C. The guest's VMXNET3 receive ring is too small for the bursts: the drop count matches "running out of buffers".
- D. The fix is a larger receive ring in the guest's VMXNET3 driver, such as 2,048 instead of 512.
- E. Before raising the ring, check that no vCPU of the guest waits in Ready or Co-stop or is saturated.
- F. A larger receive ring stops the drops even when the guest's vCPUs cannot keep up with the packet rate.
- G. The drops come from CPU Ready on the appliance, which keeps its vCPUs from emptying the ring in time.
- H. For a firewall appliance, check whether receive side scaling spreads its receive queues over several vCPUs.
- I. The vSphere performance charts show that packets were dropped, not why; the reason is in the vsish rxSummary.
- J. A full VMXNET3 receive ring is invisible to the hypervisor: only the guest counts the drop.
- K. Receive drops on the vNIC belong to the network team, since the packets arrived over the uplinks.

## Likely wrong answer
- B: "The physical network is congested: ask for a faster uplink, or ask the network team to check the switch."
- K: "Receive drops are a network problem, so the network team owns them."

## Expected key points
- Answer: A, C, D, E, H, I.
- A true: the uplinks show nothing; the drop happens between the virtual switch and the guest driver.
- B false: the uplinks show no drops and no errors, and every drop matches a full guest ring.
- C true: the drop count matches "running out of buffers", the 1st ring is full hundreds of times, and all other drop reasons are 0.
- D true: 512 is small for the bursts; raise the receive ring in the guest driver, within the driver's maximum.
- E true: a larger ring absorbs a burst; it does not help a guest that cannot keep up.
- F false: a ring that the guest does not empty in time fills whatever its size; check the guest's CPU and the vCPUs' Ready and Co-stop first.
- G false: CPU Ready is below 1% and no vCPU is saturated, so the ring size, not CPU, is the cause.
- H true: RSS spreads the receive queues over several vCPUs for network-intensive appliances, at some CPU cost.
- I true: the charts count drops (droppedRx, %DRPRX) without a reason; the rxSummary counters in vsish tell a full ring from the other causes.
- J false: the drop is counted at the port (droppedRx), at the VM (esxtop %DRPRX, vCenter droppedRx) and by the guest.
- K false: a full VMXNET3 ring is caused and fixed in the Guest OS driver, so the Guest OS owner fixes it.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12: the ring size advice no longer cites the book; Ready and per-vCPU saturation added to the stem so the ring, not CPU, is the cause. After the independent review: vsish counters read as increases; Broadcom KB 2039495 (VMXNET3 loss in high bursts when buffers run out) moved here from the key.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
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
answer_type: deterministic
answer: [A,C,D,E,H,I]
misconception: [B,K]
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
