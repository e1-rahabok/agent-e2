# Network I/O Control for a patch window

## Prompt
- A cluster of 12 hosts, each with 2 × 25 GbE uplinks on one distributed switch with Network I/O Control version 3.
- Shares per traffic type today: virtual machine traffic 50; vMotion 100 (raised last year to shorten evacuations); vSAN 100; management 50; vSphere Replication 50; backup (NFC) 50. No limits, no reservations. Replication and backup run only at night.
- In the monthly patch window, by day, hosts enter maintenance mode one by one and evacuate their VMs. During each evacuation the VMs that stay on the source host respond slowly; their transmit throughput drops by more than half.
- The platform team proposes:
  1. a limit of 5 Gb/s on vMotion traffic;
  2. a reservation of 2 Gb/s on the network adapter of each of the 40 production VMs per host.

Which statements are correct?

- A. The vMotion limit costs nothing outside an evacuation peak, because a limit only acts when the uplink is saturated.
- B. Each of the 40 production VMs per host can be granted its 2 Gb/s adapter reservation on these 2 × 25 GbE hosts.
- C. Shares split a saturated uplink only among the traffic types active on it, so idle Replication and backup count for nothing.
- D. In an evacuation, VM traffic (50) against vMotion (100) gets about a third of the uplink, less when vSAN is busy too.
- E. With 400 shares in total, VM traffic at 50 is held to an eighth of each uplink whenever the host is busy.
- F. Raising VM traffic above vMotion, for example VM traffic 100 and vMotion 50, protects the VMs during evacuations.
- G. After that share change, vMotion still uses all the bandwidth the VMs leave idle, so evacuations stay fast on quiet uplinks.
- H. Network I/O Control shapes transmit traffic, so it acts on the vMotion stream leaving the source host, next to the VMs.
- I. The fix belongs on the destination host, because Network I/O Control limits the vMotion traffic a host receives.
- J. Per-VM adapter reservations draw on the bandwidth reserved for virtual machine traffic on the host, which is 0 here.
- K. Per-VM adapter reservations are only a scheduling hint to the host; DRS and HA ignore them when they place or restart VMs.

## Likely wrong answer
- A: "A limit costs nothing; it only acts when the uplink is busy."
- B: "The reservations guarantee each VM 2 Gb/s."

## Expected key points
- Answer: C, D, F, G, H, J.
- A false: a Network I/O Control limit is enforced even when the switch is not saturated, so every evacuation is held to 5 Gb/s and takes longer.
- B false: total reservations are capped at 75% of each physical adapter: 2 × 18.75 = 37.5 Gb/s per host, against 40 × 2 = 80 Gb/s.
- C true: shares divide the link only among consumers that want bandwidth; unused bandwidth goes to the others.
- D true: 50 / (50 + 100) is a third; with vSAN (100) busy as well, 50 / 250 is a fifth. That fits a drop of more than half.
- E false: shares count only the traffic types active on the adapter, and only under contention; idle types do not dilute VM traffic.
- F true: the shares cause the symptom, so the shares fix it: VM traffic above vMotion under contention.
- G true: shares act only under contention; on an idle uplink vMotion still takes all free bandwidth.
- H true: Network I/O Control controls transmit traffic only; the source host transmits the vMotion stream next to the VMs' traffic.
- I false: Network I/O Control does not limit receive traffic.
- J true: with DRS, the total of VM reservations on a host must stay within the bandwidth reserved for virtual machine system traffic on its physical adapters (vSphere 9.1 Networking); that reservation is 0 today.
- K false: DRS includes Network I/O Control bandwidth reservations in its calculations, and admission control and HA placement use them.

## Notes
- Drafted by Claude 2026-11-12 (origin: synthetic). Counts only after author approval.
- Revised after the independent review (2026-11-12): the shares now cause the symptom; shares divide only among active traffic types (vSphere Networking, Bandwidth Allocation for System Traffic; netioc, section Shares and its misconceptions).
- Option J and K: Broadcom TechDocs, vSphere 9.1 Networking, Configure Bandwidth Allocation for a Virtual Machine (with DRS, the total of VM reservations on a host does not exceed the bandwidth reserved for virtual machine system traffic on the host physical adapters; DRS and HA place VMs where their reservations can be met): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-networking/network-io-control/bandwidth-allocation-for-virtual-machine-traffic/configure-bandwidth-allocation-for-a-virtual-machine.html
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

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
answer_type: deterministic
answer: [C, D, F, G, H, J]
misconception: [A, B]
input: [text]
knowledge:
  - vsphere/technology/network/concepts/netioc
  - sp5-framework/performance/noisy-neighbour
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/network/concepts/netioc
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: []
status: draft
```
