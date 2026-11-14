# Receive drops while seven vCPUs idle

## Prompt
- rp-02 is a Windows Server 2022 reverse proxy VM: 8 vCPUs, one VMXNET3 adapter.
- At the daily peak, vCenter shows for rp-02:
  - Receive packets dropped: about 180,000 per 5-minute sample. Transmit packets dropped: 0.
  - CPU Usage: 16%. CPU Ready: 0.4%.
- Inside Windows, Performance Monitor at the same peak:
  - Processor(0) % Processor Time: 100%, of which % DPC Time 72%.
  - Processor(1) to Processor(7) % Processor Time: 4-7% each.
  - Network Interface, Packets Received Discarded: rising.
- The receive ring of the adapter was already raised to 4,096 last month. The drops came back as traffic grew.
- The owner asks for 8 more vCPUs.

Which statements are correct?

- A. Processor(0) is saturated by deferred procedure calls from network receive work, while the other seven vCPUs are nearly idle.
- B. Eight more vCPUs will stop the drops, because Windows will spread the receive work over the added vCPUs.
- C. The packets are dropped upstream by the physical switch, so the network team should check its port counters.
- D. One vCPU at 100% is about 12.5% of an 8-vCPU VM, so a VM CPU Usage of 16% can hide a saturated vCPU.
- E. CPU Ready of 0.4% shows ESXi is not holding the vCPUs back; the bottleneck is how Windows places its receive work.
- F. The drop happens when the VMXNET3 receive ring has no free buffer, and vCenter counts it as a receive drop on the VM.
- G. A drop in the guest's receive ring is invisible to ESXi, so only the Windows counters inside the guest can show it.
- H. Raising the receive ring again is the lasting fix: with a ring large enough, how fast one vCPU drains it stops mattering.
- I. Enable receive side scaling in Windows and on the VMXNET3 adapter, with several receive queues spread over the vCPUs.
- J. Configure more RSS receive queues than vCPUs, for example 16 queues on 8 vCPUs, to leave headroom for traffic growth.
- K. The change is made inside Windows by the Guest OS owner; afterwards the drops and the per-vCPU load are read again.

## Likely wrong answer
- B: "The VM is short of CPU: give it 8 more vCPUs."
- C: "The physical network drops the packets: ask the network team."

## Expected key points
- Answer: A, D, E, F, I, K.
- A true: % DPC Time is deferred procedure call time, kernel and driver work; here the VMXNET3 receive processing lands on one vCPU (Processor(0) at 100%, 72% DPC) while Processor(1) to (7) sit at 4-7%. That vCPU cannot drain the ring fast enough, so the ring fills.
- B false: with a single receive queue, the receive processing stays on one vCPU whatever the vCPU count (Broadcom KB 440347). More vCPUs add nothing to that one queue.
- C false: a full guest receive ring drops the frame inside the host, not in the physical network; the guest's CPU, the vCPU's Ready and the ring decide it.
- D true: VM CPU Usage (%) is the sum over the vCPUs against the VM's capacity, so one busy vCPU of eight is about 12.5%; the average hides the saturated vCPU (usage disparity).
- E true: Ready near 0 rules out ESXi starving the vCPU; the bottleneck is the guest's spread of receive work.
- F true: a full VMXNET3 ring is counted at the port, by the VM (droppedRx, %DRPRX) and by the guest.
- G false: ESXi counts the ring-full drop at the port and on the VM; the guest sees it too.
- H false: a larger ring absorbs bursts; it cannot fix a vCPU that drains too slowly. KB 440347: raising the rings to their maximum did not stop the drops.
- I true: RSS with several receive queues spreads receive processing over several vCPUs (KB 440347).
- J false: the number of receive queues cannot exceed the VM's vCPU count (KB 440347).
- K true: receive drops on a VMXNET3 ring are caused and fixed in the Guest OS driver, so the Guest OS owner makes the change; then check the drops and per-vCPU load.

## Notes
- Drafted by Claude 2026-11-12 (origin: synthetic). Counts only after author approval.
- Differs from 0060 (receive ring too small for bursts): here the ring is already large and one vCPU cannot drain it.
- Broadcom KB 440347, Mitigating VMXNET3 adapter packet drops due to single receive queue (all interrupts on one vCPU; a maximum ring does not fix it; enable RSS, queues capped by the vCPU count): https://knowledge.broadcom.com/external/article/440347
- Host-side RSS on the physical NIC needs the NIC driver's RSS on and `ethernetX.pNicFeatures = "4"` in the VM's configuration (rss-and-interrupt-coalescing).
- No option relies on which Windows counter carries the ring-full count: that is an open review note in packet-drop-accounting.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

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
answer: [A, D, E, F, I, K]
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
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [average-hides-worst, layer-confusion]
status: draft
```
