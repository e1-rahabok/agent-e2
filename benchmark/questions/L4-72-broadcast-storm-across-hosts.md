# Receive drops across an application tier

## Prompt
- At 10:35 users across one application tier report timeouts. No change was planned.
- [The attached export](0216/vms-network-one-sample-1035.csv) is a VCF Operations view of one 5-minute sample at 10:35 for the 28 VMs of two port groups: pg-app10 (VLAN 10) and pg-db20 (VLAN 20), on hosts esx-01 to esx-04. Counts are per sample.
- The hosts' uplinks are 25 GbE and show low throughput.

Which statements are correct?

- A. app-17 is the source: about 135 million broadcasts in the sample, about 450,000 per second.
- B. The drops hit pg-app10 VMs on all four hosts: not a fault of one host or one uplink.
- C. pg-db20 VMs receive no flood and drop nothing: a broadcast stays inside its VLAN.
- D. The 1-vCPU VMs drop most: every VM takes in each broadcast, and one vCPU cannot keep up.
- E. The VMs with the most receive drops, the 1-vCPU VMs, are where the broadcast flood comes from.
- F. Moving the 1-vCPU VMs to a less busy host stops their drops, as their own host is overloaded.

## Likely wrong answer
E: blaming the VMs that show the most drops. Or F: treating it as a host problem and moving VMs.

## Expected key points
- Answer: A, B, C, D.
- A: app-17 transmits about 134.8 million broadcast packets in 300 seconds, about 450,000 per second; every other VM sends fewer than 1,000. It is a broadcast storm from one VM (a loop or a misbehaving service on it).
- B: the drops span all four hosts in the same port group, so look at what the VMs share: the VLAN and its broadcast domain, not one host's uplink.
- C: pg-db20 VMs receive only about 600-1,700 broadcasts in the sample and drop nothing: VLAN 20 is a separate broadcast domain.
- D: each VM in VLAN 10 must receive and process every broadcast. The 1-vCPU VMs run at about 95% CPU and drop about 40% of what arrives; the 8-vCPU VMs drop under 1%.
- E is wrong: the victims show the drops; the source shows the transmitted broadcasts.
- F is wrong: the storm floods the whole VLAN on every host. A VM moved to another host still receives every broadcast. The usage rate stays low (about 235 Mb/s for the source) because broadcasts are small; the load is the packet rate.
- Next: isolate app-17 (disconnect its adapter or move it to a quarantine port group), then find the cause on it.

## Notes
- Drafted by Claude 2026-11-12 (origin: synthetic). Counts only after author approval.
- The CSV is synthetic, generated with a fixed seed: the drop share falls with the vCPU count of the receiver.

## Metadata
```yaml
id: "0216"
title: "Receive drops across an application tier"
product: [vsphere, vcf-operations]
technology: [network, cpu]
object: [vm, network]
tool: [vcf-operations]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
knowledge:
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/technology/network/metrics/virtual-motherboard/packets
  - vsphere/technology/network/metrics/distributed-switch/packets
  - vsphere/technology/network/concepts/packet-drop-accounting
knowledge_main: vsphere/technology/network/metrics/distributed-switch/packets
attachments:
  - 0216/vms-network-one-sample-1035.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, B, C, D]
misconception: [E, F]
misconception_type: []
pair: "0411"
status: draft
```
