# Network I/O Control for a patch window

## Prompt
- A cluster of 12 hosts, each with 2 × 25 GbE uplinks on one distributed switch with Network I/O Control version 3.
- Shares per traffic type today: virtual machine traffic 50; vMotion 100 (raised last year to shorten evacuations); vSAN 100; management 50; vSphere Replication 50; backup (NFC) 50. No limits, no reservations. Replication and backup run only at night.
- In the monthly patch window, by day, hosts enter maintenance mode one by one and evacuate their VMs. During each evacuation the VMs that stay on the source host respond slowly; their transmit throughput drops by more than half.
- The platform team proposes:
  1. a limit of 5 Gb/s on vMotion traffic;
  2. a reservation of 2 Gb/s on the network adapter of each of the 40 production VMs per host.

Will the proposal protect the VMs? What causes the slowdown, and what would you set instead?

## Likely wrong answer
"Yes: a limit costs nothing because it acts only when the uplink is busy, and the reservations guarantee each VM 2 Gb/s."

## Expected key points
- The cause is the shares: on a saturated uplink, shares divide the bandwidth only among the traffic types active on that adapter. Idle Replication and backup count for nothing.
- During an evacuation, VM traffic (50) competes with vMotion (100): the VMs get about one third of the uplink, less when vSAN (100) is busy too. That matches a drop of more than half.
- Fix: raise virtual machine traffic above vMotion (for example VM traffic 100, vMotion 50). Shares act only under contention, so vMotion still uses all idle bandwidth.
- The limit stops vMotion from taking the uplink, but it applies even when the uplinks are idle: every evacuation is held to 5 Gb/s and takes longer.
- Network I/O Control acts on traffic the host transmits: it shapes the vMotion the source host sends, which is where the VMs suffer here.
- The reservations cannot be granted: total reservations are capped at 75% of each uplink, 2 × 18.75 = 37.5 Gb/s per host, against 40 × 2 = 80 Gb/s. Per-VM reservations also need a reservation for virtual machine traffic at the switch, which is 0 today, and they enter DRS placement.

## Notes
- Drafted by Claude 2026-11-12 for the network slots of question set 1.0 (origin: synthetic). Counts only after author approval.
- Revised after the independent review (2026-11-12): the shares now cause the symptom; shares divide only among active traffic types (vSphere Networking, Bandwidth Allocation for System Traffic; netioc, section Shares and its misconceptions).

## Metadata
```yaml
id: "0215"
title: "Network I/O Control for a patch window"
product: [vsphere, vsan]
technology: [network, system]
object: [network, esxi, vm]
tool: [vcenter]
task: judge-setting
level: 400
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/network/concepts/netioc
  - sp5-framework/performance/noisy-neighbour
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/network/concepts/netioc
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12, network slots (benchmark/design.md, section 3)"
misconception_type: []
status: draft
```
