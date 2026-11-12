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

Why are packets dropped? Will 8 more vCPUs help? What do you change?

## Likely wrong answer
"The VM needs more CPU: add vCPUs." Or "the physical network drops the packets: ask the network team."

## Expected key points
- The receive work of the adapter runs on one vCPU: Processor(0) is saturated by deferred procedure calls (network receive processing) while the other seven are almost idle. That vCPU cannot drain the receive ring fast enough, so the ring fills and new packets are dropped.
- The drop is inside the VM, at the VMXNET3 ring: vCenter counts it as receive drops, and Windows counts it too (Packets Received Discarded). It is not the physical network.
- VM CPU Usage of 16% is an average over 8 vCPUs: one vCPU at 100% is 12.5% of the VM. The average hides it.
- Ready at 0.4% rules out ESXi starving the vCPU: the bottleneck is how the guest spreads its receive work.
- More vCPUs do not help: the receive processing stays on the one vCPU. A larger ring only absorbs bursts.
- Fix: spread receive processing over several vCPUs with receive side scaling (RSS): enable RSS in Windows and on the VMXNET3 adapter, with several receive queues (no more than the vCPU count).
- Then check the drops and the per-vCPU load again; the Guest OS owner makes the guest change.

## Notes
- Drafted by Claude 2026-11-12 for the network slots of question set 1.0 (origin: synthetic). Counts only after author approval.
- Differs from 0060 (receive ring too small for bursts): here the ring is already large and one vCPU cannot drain it.
- Broadcom KB 440347, Mitigating VMXNET3 adapter packet drops due to single receive queue (all interrupts on one vCPU; a maximum ring does not fix it; enable RSS, queues capped by the vCPU count): https://knowledge.broadcom.com/external/article/440347
- Host-side RSS on the physical NIC needs the NIC driver's RSS on and `ethernetX.pNicFeatures = "4"` in the VM's configuration (rss-and-interrupt-coalescing).

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
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/network/configuration/rss-and-interrupt-coalescing
  - vsphere/technology/network/vnic-rx-drops
  - vsphere/technology/network/concepts/packet-drop-accounting
knowledge_main: vsphere/technology/network/configuration/rss-and-interrupt-coalescing
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12, network slots (benchmark/design.md, section 3)"
misconception_type: [average-hides-worst, layer-confusion]
status: draft
```
