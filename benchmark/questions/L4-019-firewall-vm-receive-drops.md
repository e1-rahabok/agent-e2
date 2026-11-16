# Receive drops on a firewall VM

## Prompt
- A virtual firewall appliance (VMXNET3 vNIC, 8 vCPUs) shows about 4,300 received packets dropped every 5 minutes at peak traffic.
- Its CPU Ready is below 1%, Co-stop below 0.1%, and no single vCPU is saturated inside the appliance.
- The host uplinks show no drops and no errors.
- On the host, vsish counters for its port (cumulative), read twice 5 minutes apart at peak:
  - clientStats: droppedRx rose by 4,310.
  - vmxnet3 rxSummary: running out of buffers rose by 4,310; number of times the 1st ring is full rose by 611; 1st ring size 1,024; 2nd ring size 1,024; all other reasons unchanged at 0.

Which statements about the cause, the fix and the checks before the fix are correct?

- A. The drops happen inside the host, between the virtual switch port and the guest driver.
- B. The physical network is congested: ask for faster uplinks, or ask the network team to check the switch.
- C. The guest's VMXNET3 receive ring is too small for the bursts: the drop count matches "running out of buffers".
- D. The fix is a larger receive ring in the guest's VMXNET3 driver, such as 4,096 instead of 1,024.
- E. Before raising the ring, check that no vCPU of the guest waits in Ready or Co-stop or is saturated.
- F. Configuring more receive queues in the guest than the appliance has vCPUs gives it headroom for the next peak.
- G. Only 611 of the 4,310 drops are ring-full events, so most of the drops have another reason.
- H. For a firewall appliance, check whether receive side scaling spreads its receive queues over several vCPUs.
- I. The vSphere performance charts show that packets were dropped, not why; the reason is in the vsish rxSummary.
- J. Receive drops on the vNIC belong to the network team, since the packets arrived over the uplinks.

## Likely wrong answer
- B: "The physical network is congested: ask for a faster uplink, or ask the network team to check the switch."
- J: "Receive drops are a network problem, so the network team owns them."

## Expected key points
- Answer: A, C, D, E, H, I.
- A true: the uplinks show nothing; the drop happens between the virtual switch and the guest driver.
- B false: the uplinks show no drops and no errors, and every drop matches a full guest ring.
- C true: the drop count matches "running out of buffers", the 1st ring is full hundreds of times, and all other drop reasons are 0.
- D true: 1,024 is small for these bursts; raise the receive ring in the guest driver, within the driver's maximum.
- E true: a larger ring absorbs a burst; it does not help a guest that cannot keep up. A ring that the guest does not empty in time fills whatever its size, so the vCPUs' Ready, Co-stop and saturation come first.
- F false: the receive queues a VM can use are capped by its vCPU count, so queues beyond 8 add nothing.
- G false: "running out of buffers" rose by the full 4,310, matching droppedRx, and every other reason stayed at 0; "# of times the 1st ring is full" counts ring-full events, not dropped packets.
- H true: RSS in the guest adapter spreads the receive queues over several vCPUs for network-intensive appliances, at some CPU cost; the VM's request for host-side NetQ RSS (`ethernetX.pNicFeatures`) is a separate setting.
- I true: the charts count drops (droppedRx, %DRPRX) without a reason; the rxSummary counters in vsish tell a full ring from the other causes.
- J false: a full VMXNET3 ring is caused and fixed in the Guest OS driver, so the Guest OS owner fixes it.

## Notes
- Revised 2026-11-12: the ring size advice no longer cites the book; Ready and per-vCPU saturation added to the stem so the ring, not CPU, is the cause. After the independent review: vsish counters read as increases; Broadcom KB 2039495 (VMXNET3 loss in high bursts when buffers run out) moved here from the key.
- 2026-11-16 re-review: F (a larger ring helps a CPU-starved guest) and E were a near-negation pair; F replaced in place with the queue count capped by vCPUs (false; vnic-rx-drops). Co-stop added to the stem, which E names.
- Audit 2026-11-15: G (CPU Ready as the cause, refuted by the stem's Ready below 1%) replaced with a reading of the rxSummary deltas (ring-full events against dropped packets); H's key point names guest RSS and host NetQ RSS apart.
- Review 2026-11-15: new counter values and ring sizes; the earlier ones copied the vnic-rx-drops example. Key unchanged.
- 2026-11-14: option J (a full ring is invisible to the hypervisor) removed; ring-drop visibility is tested in 0039 and 0420 (project/question-pairing-2026-11-14.md). Old K relettered J. Key unchanged: A, C, D, E, H, I.
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
misconception: [B,J]
input: [text]
knowledge:
  - vsphere/technology/network/vnic-rx-drops
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/configuration/rss-and-interrupt-coalescing
  - vsphere/technology/network/concepts/packet-drop-accounting
knowledge_main: vsphere/technology/network/vnic-rx-drops
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception_type: [layer-confusion]
status: draft
```
