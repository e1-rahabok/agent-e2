# Receive drops on a firewall VM

## Prompt
- A virtual firewall appliance (VMXNET3 vNIC) shows about 2,600 received packets dropped every 5 minutes at peak traffic.
- On the host, vsish shows for its port:
  - clientStats: droppedRx 2,620.
  - vmxnet3 rxSummary: running out of buffers 2,620; number of times the 1st ring is full 354; 1st ring size 512; 2nd ring size 512; all other reasons 0.

What causes the drops, and what do you change?

## Likely wrong answer
"The physical network is congested: ask for a faster uplink."

## Expected key points
- The VM receive ring is too small: the drops match "running out of buffers" and the 1st ring fills up.
- Increase the receive ring size: the book suggests 2K instead of 512.
- For network VMs such as firewalls and routers, also check whether the VM requests NetQ RSS.
- VMXNET3 can lose packets in very high bursts when buffers run out (Broadcom KB 2039495).
- vSphere charts show that packets are dropped, not why: only vsish shows the reason.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: question-0060
title: "Receive drops on a firewall VM"
product: [vsphere]
technology: [network]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/network/diagnosis/vnic-rx-drops
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/configuration/rss-and-interrupt-coalescing
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: draft
```
