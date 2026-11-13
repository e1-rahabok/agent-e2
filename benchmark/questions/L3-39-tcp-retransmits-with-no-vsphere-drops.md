# TCP retransmits with no drops in vSphere

## Prompt
- A Linux VM exports data to a partner every night. Between 01:00 and 02:00 the transfers slow down.
- Inside Linux, `nstat` in that hour: TcpRetransSegs rises from almost 0 to about 3% of TcpOutSegs.
- vCenter, same hour: the VM's transmit and receive dropped packets are 0. The host's vmnics show no drops and no errors.
- The host's 10 GbE uplink transmits about 9.4 Gbps in that hour; the backup also runs then.
- The vSphere team says: "vSphere shows no drops, so the network is clean. It must be the application."

Are they right? Where can the packets be lost, and how do you confirm it?

## Likely wrong answer
"vSphere and the Guest OS show no dropped packets, so the network is clean; the problem is in the application."

## Expected key points
- No: zero drops in vSphere do not prove the network is clean.
- Ethernet does not acknowledge frames: ESXi counts a frame as sent once the physical NIC puts it on the wire. A frame dropped later, by a congested top-of-rack switch, is counted only in that switch.
- The TCP retransmissions in Linux are the evidence: no acknowledgement came back, so Linux sent the data again; each loss also slows TCP down.
- Confirm with the network team: discard and queue-drop counters on the physical switches in the path (the top-of-rack ports facing the host first, then upstream, the firewall and the WAN link) in 01:00-02:00, or a packet capture at both ends.
- The uplink near line rate while the backup runs points at congestion in that hour.
- vSphere has no retransmit or network latency counter; the retransmits must be read inside the guest.

## Metadata
```yaml
id: "0268"
title: "TCP retransmits with no drops in vSphere"
product: [linux, vsphere]
technology: [network]
task: troubleshoot
level: 300
answer_type: judged
input: [text]
object: [guest-os, vm, network]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
knowledge_main: vsphere/technology/network/concepts/packet-drop-accounting
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the Guest OS slots (project/plan.md, M2)"
misconception_type: [layer-confusion]
status: draft
```
