# Uplink load against the sum of VM traffic

## Prompt
- Host esx-05 has two 10 GbE uplinks, vmnic0 and vmnic1, on one distributed switch. vmk1 is vSAN.
- It runs a three-tier application: web-01 to web-04, app-01 to app-03 and db-01, plus a backup proxy util-01. All VMs are on one port group, one VLAN.
- [The attached export](0217/esx-05-esxtop-network-busy-hour.csv) is the esxtop network panel of esx-05, averaged over the busy hour, one row per port.
- The capacity planner adds up MbTX/s and MbRX/s of the nine VMs: about 14,000 Mb/s. Against 20 Gb/s of uplinks, the planner wants two more 10 GbE ports.

Which statements are correct?

- A. Traffic between VMs on the same host and port group never leaves the virtual switch.
- B. In each direction the two uplinks carry about 2 Gb/s of the 20 Gb/s they offer.
- C. The sum of the VMs' throughput is the uplink load, so the host needs two more ports.
- D. If DRS moves db-01 to another host, esx-05's uplink load rises: its flows cross the wire.
- E. The vmnic totals include VMkernel traffic such as vSAN, which no VM counter shows.
- F. The vmnics count each VM-to-VM packet only once, which is why the VM sum is higher.

## Likely wrong answer
C: adding up VM throughput and reading it as the load on the uplinks.

## Expected key points
- Answer: A, B, D, E.
- The VM ports add up to about 14,000 Mb/s, but vmnic0 and vmnic1 together carry about 2,160 Mb/s transmit and 1,870 Mb/s receive.
- A: web, app and db talk to each other inside the host. That traffic is switched in the distributed switch's host data plane and never touches a vmnic. Only the clients' traffic to the web VMs and util-01's backup traffic leave the host.
- B: full duplex gives each 10 GbE port 10 Gb/s in each direction: 20 Gb/s transmit and 20 Gb/s receive for the two. About 2 Gb/s is used each way.
- C is wrong: the VM counters measure what each VM sends and receives, not what crosses the uplinks. Two more ports would add nothing.
- D: placement changes the uplink load. db-01 exchanges about 2,700 Mb/s with the app VMs; on another host that traffic would leave both hosts through their uplinks.
- E: vmk1 (vSAN) carries about 860 Mb/s transmit and 1,040 Mb/s receive through vmnic1; no VM counter includes it.
- F is wrong: in-host VM-to-VM traffic is not on the vmnics at all; each VM's port counts its own side, so a flow appears on two VM ports and on no vmnic.
- Plan uplink capacity from the vmnic counters per direction, and keep VMs that talk a lot on the same host where DRS rules allow.

## Notes
- Drafted by Claude 2026-11-12 (origin: synthetic). Counts only after author approval.
- The CSV is synthetic, generated with a fixed seed and ±6% noise per VM: the vmnic totals (bytes and packets) are the external VM traffic plus the VMkernel ports, by construction.

## Metadata
```yaml
id: "0217"
title: "Uplink load against the sum of VM traffic"
product: [vsphere, vsan]
technology: [network, system]
object: [esxi, vm, network]
tool: [esxtop]
task: decide-capacity
level: 400
answer_type: deterministic
input: [table]
knowledge:
  - vsphere/technology/network/concepts/network-observability
  - vsphere/technology/network/metrics/host/throughput
  - vsphere/technology/network/metrics/distributed-switch/packets
  - vsphere/technology/network/concepts/network-characteristics
knowledge_main: vsphere/technology/network/concepts/network-observability
attachments:
  - 0217/esx-05-esxtop-network-busy-hour.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, B, D, E]
misconception: [C]
misconception_type: [provider-vs-consumer, same-name-other-object]
pair: "0407"
status: draft
```
