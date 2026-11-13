# Where is the network latency counter?

## Prompt
- An application owner reports that calls from web-03 to db-05 took twice as long between 14:00 and 14:30 yesterday.
- Both VMs are on the same cluster, different hosts, same distributed port group. Neither VM shows dropped packets in vCenter for that window.
- The owner asks you to open the VM network latency chart in vCenter for both VMs and the hosts in between.

Can you? Where can network latency be measured, and which vSphere conditions can add latency without showing any dropped packet?

## Likely wrong answer
"Open the VM's network latency counter in the vSphere Client" — or "no dropped packets, so the network added no delay."

## Expected key points
- No: vCenter has no network latency, jitter or retransmit counter for a VM or its virtual NIC. For a VM, dropped packets are the only sign of network trouble.
- No drops does not mean no delay. Latency is measured where the traffic ends: in the application (response times), in the guest (round-trip times, TCP statistics), or with the network team's tools (flow records, packet capture).
- CPU contention on either VM (Ready, Co-stop) adds delay without a drop: a packet waits until the vCPU runs to process it.
- Virtual interrupt coalescing on the adapter adds delay without a drop: packets are batched, from a few hundred microseconds to a few milliseconds.
- A VM in the path (a firewall, an NSX Edge, a security agent VM) adds delay without a drop on the two VMs: its own CPU or memory contention slows every flow through it.
- Next: compare Ready and Co-stop of web-03, db-05 and any VM in the path for 14:00-14:30.

## Notes
- Drafted by Claude 2026-11-12 for the network slots of question set 1.0 (origin: synthetic). Counts only after author approval.
- TCP retransmits seen inside the guest belong to a Guest OS question of the set; this one tests what vSphere measures and what it can add.

## Metadata
```yaml
id: "0214"
title: "Where is the network latency counter?"
product: [vsphere]
technology: [network, cpu]
object: [vm, network]
tool: [vcenter]
task: explain-mechanism
level: 300
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/technology/network/configuration/rss-and-interrupt-coalescing
  - vsphere/technology/network/concepts/network-observability
knowledge_main: vsphere/technology/network/metrics/vm-network-metrics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12, network slots (benchmark/design.md, section 3)"
misconception_type: [tool-confusion]
status: draft
```
