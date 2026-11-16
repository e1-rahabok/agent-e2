# Receive drops while seven vCPUs idle

## Prompt
- rp-02 is a Windows Server 2022 reverse proxy VM: 8 vCPUs, one VMXNET3 adapter.
- The vCenter statistics level of the 1-day interval was raised to 3 last quarter. At the daily peak, vCenter shows for rp-02:
  - Receive packets dropped: about 180,000 per 5-minute sample. Transmit packets dropped: 0.
  - CPU Usage: 16%. CPU Ready: 0.4%.
- Inside Windows, Performance Monitor at the same peak:
  - Processor(0) % Processor Time: 100%, of which % DPC Time 72%.
  - Processor(1) to Processor(7) % Processor Time: 4-7% each.
- On the host, `vsish` rxSummary for the adapter's port: "running out of buffers" and "# of times the 1st ring is full" rising.
- The receive ring of the adapter was already raised to 4,096 last month. The drops came back as traffic grew.
- The owner asks for 8 more vCPUs.

Which statements are correct?

- A. Processor(0) is saturated by deferred procedure calls from network receive work, while the other seven vCPUs are nearly idle.
- B. Eight more vCPUs will stop the drops, because Windows will spread the receive work over the added vCPUs.
- C. The packets are dropped upstream by the physical switch, so the network team should check its port counters.
- D. One vCPU at 100% is about 12.5% of an 8-vCPU VM; a VM CPU Usage of 16% hides a saturated vCPU.
- E. CPU Ready of 0.4% shows ESXi is not holding the vCPUs back; the bottleneck is how Windows places its receive work.
- F. The drop happens when the VMXNET3 receive ring has no free buffer for the next frame.
- G. Raising the receive ring again is the lasting fix: with a ring large enough, how fast one vCPU drains it stops mattering.
- H. Enable receive side scaling in Windows and on the VMXNET3 adapter, with several receive queues spread over the vCPUs.
- I. Configure more RSS receive queues than vCPUs, for example 16 queues on 8 vCPUs, to leave headroom for traffic growth.
- J. Moving rp-02 to a less busy host leaves its receive drops as they are, as long as the adapter keeps one receive queue.

## Likely wrong answer
- B: "The VM is short of CPU: give it 8 more vCPUs."
- C: "The physical network drops the packets: ask the network team."

## Expected key points
- Answer: A, D, E, F, H, J.
- A true: % DPC Time is deferred procedure call time, kernel and driver work; here the VMXNET3 receive processing lands on one vCPU (Processor(0) at 100%, 72% DPC) while Processor(1) to (7) sit at 4-7%. That vCPU cannot drain the ring fast enough, so the ring fills.
- B false: with a single receive queue, the receive processing stays on one vCPU whatever the vCPU count (Broadcom KB 440347). More vCPUs add nothing to that one queue.
- C false: a full guest receive ring drops the frame inside the host, not in the physical network; the guest's CPU, the vCPU's Ready and the ring decide it.
- D true: VM CPU Usage (%) is the sum over the vCPUs against the VM's capacity, so one busy vCPU of eight is about 12.5%; the average hides the saturated vCPU (usage disparity).
- E true: Ready near 0 rules out ESXi starving the vCPU; the bottleneck is the guest's spread of receive work.
- F true: with no free descriptor in the ring, the hypervisor cannot copy the frame into guest memory and discards it (tail drop).
- G false: a larger ring absorbs bursts; it cannot fix a vCPU that drains too slowly. KB 440347: raising the rings to their maximum did not stop the drops.
- H true: RSS in the guest with several receive queues spreads receive processing over several vCPUs (vnic-rx-drops, section Single receive queue; KB 440347).
- I false: the number of receive queues a VM can use is capped by its vCPU count (vnic-rx-drops; KB 440347).
- J true: with a single receive queue the ring fills because one vCPU inside the guest drains it; another host changes nothing in the guest, so the drops stay (vnic-rx-drops, Single receive queue; KB 440347).

## Notes
- Differs from 0060 (receive ring too small for bursts): here the ring is already large and one vCPU cannot drain it.
- Broadcom KB 440347, Mitigating VMXNET3 adapter packet drops due to single receive queue (all interrupts on one vCPU; a maximum ring does not fix it; enable RSS, queues capped by the vCPU count): https://knowledge.broadcom.com/external/article/440347
- Host-side RSS on the physical NIC needs the NIC driver's RSS on and `ethernetX.pNicFeatures = "4"` in the VM's configuration (rss-and-interrupt-coalescing).
- 2026-11-14: option G (the ring-full drop invisible to ESXi) removed: it was the negation of F. Options relettered; key changed from A, D, E, F, I, K to A, D, E, F, H, J (same facts).
- Review 2026-11-15: F no longer says that vCenter counts the drop (ring-drop visibility is tested in 0039 and 0420). Options H and I rested on Broadcom KB 440347 alone; its facts (single receive queue, maximum ring does not fix it, RSS in the guest, queues capped by the vCPU count) were added to vnic-rx-drops. Key unchanged.
- Audit 2026-11-15: the stem states the raised statistics level (at the default level a VM keeps no network drop history, vcenter-statistics); the Windows counter Packets Received Discarded (not confirmed to carry the ring-full count, packet-drop-accounting) replaced with the host's vsish rxSummary; J (the Guest OS owner fixes a full ring) was over the two-question cap (0345, 0060 keep it) and was replaced with the single-queue symptom "moving the VM to another host does not help"; the hedge "can hide" in D made plain.

## Metadata
```yaml
id: "0212"
title: "Receive drops while seven vCPUs idle"
product: [vsphere, windows]
technology: [network, cpu]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A, D, E, F, H, J]
misconception: [B, C]
input: [text]
knowledge:
  - vsphere/technology/network/configuration/rss-and-interrupt-coalescing
  - vsphere/technology/network/vnic-rx-drops
  - vsphere/technology/network/concepts/packet-drop-accounting
  - guest-os/cpu/metrics/processor-time
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
knowledge_main: vsphere/technology/network/configuration/rss-and-interrupt-coalescing
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception_type: [average-hides-worst, layer-confusion]
status: draft
```
